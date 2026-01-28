#!/usr/bin/env python3
"""
ARM2 Grey-Box Queueing Model
=============================

First production ARM processor (1986)
- 3-stage pipeline
- Hardware multiplier
- Powered Acorn Archimedes
- Target CPI: 1.5
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


class Arm2Model(BaseProcessorModel):
    """
    ARM2 - First Production ARM
    Target CPI: 1.5
    """

    name = "ARM2"
    manufacturer = "Acorn"
    year = 1986
    clock_mhz = 8.0
    transistor_count = 30000
    data_width = 32
    address_width = 26

    def __init__(self):
        # ARM2: Faster than ARM1, calibrated for CPI 1.5
        # 0.52*1.0 + 0.20*2.2 + 0.12*1.7 + 0.16*2.2 = 0.52 + 0.44 + 0.204 + 0.352 = 1.516
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "Data processing"),
            'load': InstructionCategory('load', 2.2, 0, "LDR"),
            'store': InstructionCategory('store', 1.7, 0, "STR"),
            'branch': InstructionCategory('branch', 2.2, 0, "Branch"),
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
