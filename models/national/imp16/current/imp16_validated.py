#!/usr/bin/env python3
"""
National IMP-16 Grey-Box Queueing Model
========================================

Target CPI: 8.0 (early bit-slice 16-bit, 1973)
Architecture: Bit-slice based 16-bit microprocessor

The IMP-16 was one of the first 16-bit microprocessors,
built using bit-slice technology for flexibility.
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


class Imp16Model(BaseProcessorModel):
    """
    National IMP-16 Grey-Box Queueing Model

    Target CPI: 8.0
    Calibration: Weighted sum of instruction cycles
    """

    name = "IMP16"
    manufacturer = "National Semiconductor"
    year = 1973
    clock_mhz = 0.5

    def __init__(self):
        # Calibrated cycles to achieve CPI = 8.0
        # Early bit-slice architecture with limited performance
        # Calculation: 0.25*6 + 0.15*8 + 0.20*10 + 0.12*8 + 0.10*9 + 0.08*9 + 0.05*12 + 0.05*10 = 8.16
        self.instruction_categories = {
            'register_ops': InstructionCategory('register_ops', 6.0, 0, "Register-to-register"),
            'immediate': InstructionCategory('immediate', 8.0, 0, "Immediate operand"),
            'memory_read': InstructionCategory('memory_read', 10.0, 0, "Load from memory"),
            'memory_write': InstructionCategory('memory_write', 8.0, 0, "Store to memory"),
            'branch': InstructionCategory('branch', 9.0, 0, "Branch/conditional"),
            'call_return': InstructionCategory('call_return', 9.0, 0, "Subroutine call/return"),
            'shift': InstructionCategory('shift', 12.0, 0, "Shift operations"),
            'io': InstructionCategory('io', 10.0, 0, "I/O operations"),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'register_ops': 0.25,
                'immediate': 0.15,
                'memory_read': 0.20,
                'memory_write': 0.12,
                'branch': 0.10,
                'call_return': 0.08,
                'shift': 0.05,
                'io': 0.05,
            }, "Typical embedded workload"),
            'compute': WorkloadProfile('compute', {
                'register_ops': 0.40,
                'immediate': 0.25,
                'memory_read': 0.12,
                'memory_write': 0.08,
                'branch': 0.08,
                'call_return': 0.04,
                'shift': 0.02,
                'io': 0.01,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'register_ops': 0.15,
                'immediate': 0.10,
                'memory_read': 0.35,
                'memory_write': 0.25,
                'branch': 0.05,
                'call_return': 0.05,
                'shift': 0.03,
                'io': 0.02,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'register_ops': 0.20,
                'immediate': 0.10,
                'memory_read': 0.15,
                'memory_write': 0.08,
                'branch': 0.25,
                'call_return': 0.15,
                'shift': 0.04,
                'io': 0.03,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'register_ops': 0.28,
                'immediate': 0.16,
                'memory_read': 0.20,
                'memory_write': 0.12,
                'branch': 0.10,
                'call_return': 0.07,
                'shift': 0.04,
                'io': 0.03,
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
            processor=self.name, workload=workload, cpi=total_cpi,
            clock_mhz=self.clock_mhz, bottleneck=bottleneck, utilizations=contributions
        )

    def validate(self) -> Dict[str, Any]:
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles
