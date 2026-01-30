#!/usr/bin/env python3
"""
National NS32381 Grey-Box Queueing Model
===========================================

Architecture: 32-bit (1985)
Queueing Model: Sequential execution

Features:
  - NS32000 FPU
  - Pipelined
  - IEEE 754

Date: 2026-01-29
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional

try:
    from common.base_model import BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult
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

        @classmethod
        def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations):
            ipc = 1.0 / cpi
            ips = clock_mhz * 1e6 * ipc
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations)

    class BaseProcessorModel:
        pass


class Ns32381Model(BaseProcessorModel):
    """National NS32381 - NS32000 FPU, higher performance than NS32081"""

    name = "National NS32381"
    manufacturer = "National Semiconductor"
    year = 1985
    clock_mhz = 15.0
    transistor_count = 60000
    data_width = 32
    address_width = 32

    def __init__(self):
        self.instruction_categories = {
            'fp_add': InstructionCategory('fp_add', 6.0, 0, "FP add @5-7c"),
            'fp_mul': InstructionCategory('fp_mul', 8.0, 0, "FP mul @7-9c"),
            'fp_div': InstructionCategory('fp_div', 16.0, 0, "FP div @12-20c"),
            'data_transfer': InstructionCategory('data_transfer', 4.0, 0, "Reg/mem @3-5c"),
        }
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'fp_add': 0.236,
                'fp_mul': 0.471,
                'fp_div': 0.136,
                'data_transfer': 0.157,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'fp_add': 0.336,
                'fp_mul': 0.438,
                'fp_div': 0.103,
                'data_transfer': 0.123,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'fp_add': 0.203,
                'fp_mul': 0.438,
                'fp_div': 0.103,
                'data_transfer': 0.256,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'fp_add': 0.203,
                'fp_mul': 0.438,
                'fp_div': 0.103,
                'data_transfer': 0.256,
            }, "Control-flow intensive"),
        }

    def analyze(self, workload='typical'):
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        total_cpi = sum(
            profile.category_weights[c] * self.instruction_categories[c].total_cycles
            for c in profile.category_weights
        )
        contributions = {c: profile.category_weights[c] * self.instruction_categories[c].total_cycles
                         for c in profile.category_weights}
        bottleneck = max(contributions, key=contributions.get)
        return AnalysisResult.from_cpi(
            self.name, workload, total_cpi, self.clock_mhz, bottleneck, contributions
        )

    def validate(self):
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles
