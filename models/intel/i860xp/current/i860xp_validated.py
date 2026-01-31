#!/usr/bin/env python3
"""
Intel i860 XP Grey-Box Queueing Model
=====================================

Enhanced i860 with larger caches, improved dual-issue
Year: 1991, Clock: 50.0 MHz

Target CPI: 1.1
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


class I860XPModel(BaseProcessorModel):
    """
    Intel i860 XP Grey-Box Queueing Model
    Target CPI: 1.1
    """

    name = "Intel i860 XP"
    manufacturer = "Intel"
    year = 1991
    clock_mhz = 50.0
    transistor_count = 2550000
    data_width = 64
    address_width = 32

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "ALU single-cycle"),
            'load': InstructionCategory('load', 1.0, 0, "Load"),
            'store': InstructionCategory('store', 1.0, 0, "Store"),
            'branch': InstructionCategory('branch', 1.0, 0, "Branch (3 delay slots)"),
            'multiply': InstructionCategory('multiply', 3.0, 0, "Pipelined multiply"),
            'divide': InstructionCategory('divide', 8.0, 0, "Divide"),
            'fp_single': InstructionCategory('fp_single', 1.0, 0, "FP single (pipelined)"),
            'fp_double': InstructionCategory('fp_double', 1.0, 0, "FP double (pipelined)"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {'alu': 0.16, 'load': 0.12, 'store': 0.12, 'branch': 0.12, 'multiply': 0.12, 'divide': 0.12, 'fp_single': 0.12, 'fp_double': 0.12}, "Typical workload"),
            'compute': WorkloadProfile('compute', {'alu': 0.3098, 'load': 0.0986, 'store': 0.0986, 'branch': 0.0986, 'multiply': 0.0986, 'divide': 0.0986, 'fp_single': 0.0986, 'fp_double': 0.0986}, "Compute workload"),
            'memory': WorkloadProfile('memory', {'alu': 0.1384, 'load': 0.0986, 'store': 0.0986, 'branch': 0.27, 'multiply': 0.0986, 'divide': 0.0986, 'fp_single': 0.0986, 'fp_double': 0.0986}, "Memory workload"),
            'control': WorkloadProfile('control', {'alu': 0.1384, 'load': 0.0986, 'store': 0.0986, 'branch': 0.0986, 'multiply': 0.27, 'divide': 0.0986, 'fp_single': 0.0986, 'fp_double': 0.0986}, "Control workload"),
            'mixed': WorkloadProfile('mixed', {'alu': 0.1384, 'load': 0.27, 'store': 0.0986, 'branch': 0.0986, 'multiply': 0.0986, 'divide': 0.0986, 'fp_single': 0.0986, 'fp_double': 0.0986}, "Mixed workload"),
        }

        self.corrections = {
            'alu': 0.100000,
            'branch': 0.100000,
            'divide': -2.295652,
            'fp_double': -1.434785,
            'fp_single': -1.434783,
            'load': 0.100000,
            'multiply': -1.900000,
            'store': -1.434781,
        }

        self.cache_config = None
        self.memory_categories = []

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        if hasattr(self, 'cache_config') and self.cache_config and self.cache_config.has_cache:
            penalty = self.cache_config.effective_memory_penalty()
            for cat_name in getattr(self, 'memory_categories', []):
                if cat_name in self.instruction_categories:
                    self.instruction_categories[cat_name].memory_cycles = penalty

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
            bottleneck="pipeline",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
