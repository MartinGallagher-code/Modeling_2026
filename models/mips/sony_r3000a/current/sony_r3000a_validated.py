#!/usr/bin/env python3
"""
Sony CXD8530BQ Grey-Box Queueing Model
======================================

Architecture: PlayStation CPU, MIPS R3000A with GTE coprocessor
Year: 1994, Clock: 33.8688 MHz

Target CPI: 1.4
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


class SonyR3000aModel(BaseProcessorModel):
    """
    Sony CXD8530BQ Grey-Box Queueing Model

    PlayStation CPU, MIPS R3000A with GTE coprocessor (1994)
    - MIPS R3000A core
    - GTE coprocessor
    - 4KB I+D cache
    """

    name = "Sony CXD8530BQ"
    manufacturer = "Sony/LSI Logic"
    year = 1994
    clock_mhz = 33.8688
    transistor_count = 300000
    data_width = 32
    address_width = 32

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "ALU/logic ops"),
            'load': InstructionCategory('load', 2.0, 0, "Load from memory"),
            'store': InstructionCategory('store', 2.0, 0, "Store to memory"),
            'branch': InstructionCategory('branch', 2.0, 0, "Branch/jump"),
            'multiply': InstructionCategory('multiply', 4.0, 0, "Multiply"),
            'divide': InstructionCategory('divide', 12.0, 0, "Divide"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.35,
                'load': 0.25,
                'store': 0.15,
                'branch': 0.2,
                'multiply': 0.03,
                'divide': 0.02,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'load': 0.15,
                'store': 0.1,
                'branch': 0.15,
                'multiply': 0.1,
                'divide': 0.05,
            }, "Compute workload"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.2,
                'load': 0.35,
                'store': 0.25,
                'branch': 0.15,
                'multiply': 0.03,
                'divide': 0.02,
            }, "Memory workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.25,
                'load': 0.15,
                'store': 0.1,
                'branch': 0.45,
                'multiply': 0.03,
                'divide': 0.02,
            }, "Control workload"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.3,
                'load': 0.25,
                'store': 0.15,
                'branch': 0.2,
                'multiply': 0.05,
                'divide': 0.05,
            }, "Mixed workload"),
        }

        self.corrections = {
            'alu': 0.7801912477956161,
            'branch': -0.6799043592151801,
            'divide': -8.295401183361065,
            'load': -2.4082272510620926,
            'multiply': -4.999944052672218,
            'store': 1.7674647862084898,
        }

        # Cache configuration for memory hierarchy modeling
        self.cache_config = CacheConfig(
            has_cache=True,
            l1_latency=1.0,
            l1_hit_rate=0.9990,
            dram_latency=8.0,
        )
        self.memory_categories = ['load', 'store']

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Apply cache miss penalty to memory-accessing categories
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
            bottleneck="pipeline_stall",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
