#!/usr/bin/env python3
"""
ARM1 Grey-Box Queueing Model
=============================

First ARM processor (1985)
- 3-stage pipeline
- No cache
- Target CPI: 1.8
"""

from dataclasses import dataclass
from typing import Dict, Any

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


class Arm1Model(BaseProcessorModel):
    """
    ARM1 - First ARM Processor
    Target CPI: 1.8
    """

    name = "ARM1"
    manufacturer = "Acorn"
    year = 1985
    clock_mhz = 8.0
    transistor_count = 25000
    data_width = 32
    address_width = 26

    def __init__(self):
        # ARM1: 3-stage pipeline, calibrated for CPI 1.8
        # 0.52*1.0 + 0.20*2.8 + 0.12*2.2 + 0.16*3.3 = 0.52 + 0.56 + 0.264 + 0.528 = 1.87
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "Data processing"),
            'load': InstructionCategory('load', 2.8, 0, "LDR"),
            'store': InstructionCategory('store', 2.2, 0, "STR"),
            'branch': InstructionCategory('branch', 3.2, 0, "Branch"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.52, 'load': 0.20, 'store': 0.12, 'branch': 0.16,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.62, 'load': 0.14, 'store': 0.10, 'branch': 0.14,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.32, 'load': 0.32, 'store': 0.22, 'branch': 0.14,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.42, 'load': 0.15, 'store': 0.10, 'branch': 0.33,
            }, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.50, 'load': 0.22, 'store': 0.13, 'branch': 0.15,
            }, "Mixed workload"),
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        total_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            total_cpi += contrib
            contributions[cat_name] = contrib

        bottleneck = max(contributions, key=contributions.get)

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=total_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=contributions
        )

    def validate(self) -> Dict[str, Any]:
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles
