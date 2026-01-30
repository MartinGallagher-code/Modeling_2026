#!/usr/bin/env python3
"""
Inmos T424 Grey-Box Queueing Model
=====================================

Architecture: 32-bit (1985)
Queueing Model: Sequential execution

Features:
  - T414 variant
  - 4KB SRAM
  - Occam/CSP

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


class T424Model(BaseProcessorModel):
    """Inmos T424 - 32-bit transputer with 4KB on-chip RAM"""

    name = "Inmos T424"
    manufacturer = "Inmos"
    year = 1985
    clock_mhz = 15.0
    transistor_count = 150000
    data_width = 32
    address_width = 32

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.5, 0, "Single-cycle ALU @1-2c"),
            'data_transfer': InstructionCategory('data_transfer', 1.5, 0, "Reg moves @1-2c"),
            'memory': InstructionCategory('memory', 2.5, 0, "On-chip mem @2-3c"),
            'control': InstructionCategory('control', 3.0, 0, "Branch/process @2-4c"),
            'channel': InstructionCategory('channel', 3.5, 0, "Channel comm @3-5c"),
        }
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.329,
                'data_transfer': 0.328,
                'memory': 0.135,
                'control': 0.112,
                'channel': 0.096,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.429,
                'data_transfer': 0.303,
                'memory': 0.11,
                'control': 0.087,
                'channel': 0.071,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.304,
                'data_transfer': 0.428,
                'memory': 0.11,
                'control': 0.087,
                'channel': 0.071,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.304,
                'data_transfer': 0.303,
                'memory': 0.11,
                'control': 0.212,
                'channel': 0.071,
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
