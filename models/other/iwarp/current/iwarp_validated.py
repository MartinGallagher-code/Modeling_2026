#!/usr/bin/env python3
"""
iWarp Grey-Box Queueing Model
================================

Architecture: 32-bit (1985)
Queueing Model: Sequential execution

Features:
  - VLIW dual-issue
  - Systolic comm

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


class IwarpModel(BaseProcessorModel):
    """iWarp - VLIW/systolic array processor, GPU precursor"""

    name = "iWarp"
    manufacturer = "Intel/CMU"
    year = 1985
    clock_mhz = 20.0
    transistor_count = 200000
    data_width = 32
    address_width = 32

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "VLIW ALU @1c"),
            'fp': InstructionCategory('fp', 2.0, 0, "Pipelined FP @2c"),
            'memory': InstructionCategory('memory', 2.0, 0, "On-chip mem @2c"),
            'communication': InstructionCategory('communication', 2.0, 0, "Systolic link @2c"),
            'control': InstructionCategory('control', 2.0, 0, "VLIW seq @2c"),
        }
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.488,
                'fp': 0.128,
                'memory': 0.128,
                'communication': 0.128,
                'control': 0.128,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.588,
                'fp': 0.103,
                'memory': 0.103,
                'communication': 0.103,
                'control': 0.103,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.463,
                'fp': 0.103,
                'memory': 0.228,
                'communication': 0.103,
                'control': 0.103,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.463,
                'fp': 0.103,
                'memory': 0.103,
                'communication': 0.103,
                'control': 0.228,
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
