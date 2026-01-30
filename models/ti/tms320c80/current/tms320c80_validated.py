#!/usr/bin/env python3
"""
TI TMS320C80 MVP Grey-Box Queueing Model
========================================

Architecture: RISC master + 4 DSP cores, early media processor
Year: 1994, Clock: 50.0 MHz

Target CPI: 0.8
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


class Tms320c80Model(BaseProcessorModel):
    """
    TI TMS320C80 MVP Grey-Box Queueing Model

    RISC master + 4 DSP cores, early media processor (1994)
    - 5 processors on chip
    - RISC master + 4 DSPs
    - 2 Gops peak
    """

    name = "TI TMS320C80 MVP"
    manufacturer = "TI"
    year = 1994
    clock_mhz = 50.0
    transistor_count = 4000000
    data_width = 32
    address_width = 32

    def __init__(self):
        self.instruction_categories = {
            'mac': InstructionCategory('mac', 1.0, 0, "Multiply-accumulate"),
            'alu': InstructionCategory('alu', 1.0, 0, "ALU/logic"),
            'load': InstructionCategory('load', 1.0, 0, "Data load"),
            'store': InstructionCategory('store', 1.0, 0, "Data store"),
            'branch': InstructionCategory('branch', 1.0, 0, "Branch/loop"),
            'special': InstructionCategory('special', 1.0, 0, "Special function"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'mac': 0.4,
                'alu': 0.2,
                'load': 0.15,
                'store': 0.1,
                'branch': 0.1,
                'special': 0.05,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'mac': 0.55,
                'alu': 0.2,
                'load': 0.1,
                'store': 0.05,
                'branch': 0.05,
                'special': 0.05,
            }, "Compute workload"),
            'memory': WorkloadProfile('memory', {
                'mac': 0.25,
                'alu': 0.15,
                'load': 0.25,
                'store': 0.2,
                'branch': 0.1,
                'special': 0.05,
            }, "Memory workload"),
            'control': WorkloadProfile('control', {
                'mac': 0.25,
                'alu': 0.15,
                'load': 0.15,
                'store': 0.1,
                'branch': 0.25,
                'special': 0.1,
            }, "Control workload"),
            'mixed': WorkloadProfile('mixed', {
                'mac': 0.35,
                'alu': 0.2,
                'load': 0.15,
                'store': 0.1,
                'branch': 0.1,
                'special': 0.1,
            }, "Mixed workload"),
        }

        self.corrections = {
            'mac': -0.200000,
            'alu': -0.200000,
            'load': -0.200000,
            'store': -0.200000,
            'branch': -0.200000,
            'special': -0.200000,
        }

        # No cache on this processor
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
            bottleneck="parallel_dsp",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
