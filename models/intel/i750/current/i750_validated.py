#!/usr/bin/env python3
"""
Intel i750 Video Processor Grey-Box Queueing Model
==================================================

DVI video processor for motion video decompression
Year: 1989, Clock: 30.0 MHz

Target CPI: 3.0
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional

try:
    from common.base_model import BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult, CacheConfig
except ImportError:
    from dataclasses import dataclass

    @dataclass
    class InstructionCategory:
        name: str
        base_cycles: float
        memory_cycles: float = 0
        description: str = ""
        @property
        def total_cycles(self): return self.base_cycles + self.memory_cycles


    @dataclass
    class CacheConfig:
        has_cache: bool = False
        l1_latency: float = 1.0
        l1_hit_rate: float = 0.95
        l2_latency: float = 10.0
        l2_hit_rate: float = 0.90
        has_l2: bool = False
        dram_latency: float = 50.0
        def effective_memory_penalty(self):
            if not self.has_cache: return 0.0
            l1_miss = 1.0 - self.l1_hit_rate
            if self.has_l2:
                l2_miss = 1.0 - self.l2_hit_rate
                return l1_miss * (self.l2_hit_rate * (self.l2_latency - self.l1_latency) + l2_miss * (self.dram_latency - self.l1_latency))
            return l1_miss * (self.dram_latency - self.l1_latency)


    @dataclass
    class WorkloadProfile:
        name: str
        category_weights: Dict[str, float]
        description: str = ""

    @dataclass
    class AnalysisResult:
        processor: str
        workload: str
        ipc: float
        cpi: float
        ips: float
        bottleneck: str
        utilizations: Dict[str, float]
        base_cpi: float = 0.0
        correction_delta: float = 0.0

        @classmethod
        def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations, base_cpi=None, correction_delta=0.0):
            ipc = 1.0 / cpi if cpi > 0 else 0.0
            ips = clock_mhz * 1e6 * ipc
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                       base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)

    class BaseProcessorModel:
        def get_corrections(self):
            return getattr(self, 'corrections', {})
        def set_corrections(self, corrections):
            self.corrections = corrections
        def compute_correction_delta(self, workload='typical'):
            profile = self.workload_profiles.get(workload, list(self.workload_profiles.values())[0])
            return sum(self.corrections.get(c, 0) * profile.category_weights.get(c, 0) for c in self.corrections)
        def compute_residuals(self, measured_cpi_dict):
            return {w: self.analyze(w).cpi - m for w, m in measured_cpi_dict.items()}
        def compute_loss(self, measured_cpi_dict):
            residuals = self.compute_residuals(measured_cpi_dict)
            return sum(r**2 for r in residuals.values()) / len(residuals) if residuals else 0
        def get_parameters(self):
            params = {}
            for c, cat in self.instruction_categories.items():
                params[f'cat.{c}.base_cycles'] = cat.base_cycles
            for c, v in self.corrections.items():
                params[f'cor.{c}'] = v
            return params
        def set_parameters(self, params):
            for k, v in params.items():
                if k.startswith('cat.') and k.endswith('.base_cycles'):
                    c = k[4:-12]
                    if c in self.instruction_categories:
                        self.instruction_categories[c].base_cycles = v
                elif k.startswith('cor.'):
                    c = k[4:]
                    self.corrections[c] = v
        def get_parameter_bounds(self):
            bounds = {}
            for c, cat in self.instruction_categories.items():
                bounds[f'cat.{c}.base_cycles'] = (0.1, cat.base_cycles * 5)
            for c in self.corrections:
                bounds[f'cor.{c}'] = (-50, 50)
            return bounds
        def get_parameter_metadata(self):
            return {k: {'type': 'category' if k.startswith('cat.') else 'correction'} for k in self.get_parameters()}
        def get_instruction_categories(self):
            return self.instruction_categories
        def get_workload_profiles(self):
            return self.workload_profiles
        def validate(self):
            return {'tests': [], 'passed': 0, 'total': 0, 'accuracy_percent': None}


class I750Model(BaseProcessorModel):
    """
    Intel i750 Video Processor Grey-Box Queueing Model
    Target CPI: 3.0
    """

    name = "Intel i750 Video Processor"
    manufacturer = "Intel"
    year = 1989
    clock_mhz = 30.0
    transistor_count = 750000
    data_width = 16
    address_width = 24

    def __init__(self):
        self.instruction_categories = {
            'pixel': InstructionCategory('pixel', 2.0, 0, "Pixel processing"),
            'dct': InstructionCategory('dct', 4.0, 0, "DCT/IDCT transform"),
            'quantize': InstructionCategory('quantize', 3.0, 0, "Quantization"),
            'motion': InstructionCategory('motion', 5.0, 0, "Motion compensation"),
            'memory': InstructionCategory('memory', 3.0, 0, "Video memory access"),
            'control': InstructionCategory('control', 2.0, 0, "Sequencing"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {'pixel': 0.15, 'dct': 0.17, 'quantize': 0.17, 'motion': 0.17, 'memory': 0.17, 'control': 0.17}, "Typical workload"),
            'compute': WorkloadProfile('compute', {'pixel': 0.3, 'dct': 0.14, 'quantize': 0.14, 'motion': 0.14, 'memory': 0.14, 'control': 0.14}, "Compute workload"),
            'memory': WorkloadProfile('memory', {'pixel': 0.12, 'dct': 0.14, 'quantize': 0.14, 'motion': 0.32, 'memory': 0.14, 'control': 0.14}, "Memory workload"),
            'control': WorkloadProfile('control', {'pixel': 0.12, 'dct': 0.14, 'quantize': 0.14, 'motion': 0.14, 'memory': 0.32, 'control': 0.14}, "Control workload"),
            'mixed': WorkloadProfile('mixed', {'pixel': 0.12, 'dct': 0.32, 'quantize': 0.14, 'motion': 0.14, 'memory': 0.14, 'control': 0.14}, "Mixed workload"),
        }

        self.corrections = {
            'control': 0.500000,
            'dct': -1.000000,
            'memory': 0.000000,
            'motion': -2.000000,
            'pixel': 1.000000,
            'quantize': 0.500000,
        }

        self.cache_config = None
        self.memory_categories = []

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        base_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=corrected_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck="video_pipeline",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
