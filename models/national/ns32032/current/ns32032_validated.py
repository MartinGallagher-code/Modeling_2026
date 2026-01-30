#!/usr/bin/env python3
"""
National Semiconductor NS32032 Grey-Box Queueing Model
=======================================================

Target CPI: 10.0 (32-bit CISC, 1984)
Architecture: Complex instruction set, improved NS32016

The NS32032 was an improved version of the NS32016 with
full 32-bit data bus, but still heavily microcoded.
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
    base_cpi: float = 0.0
    correction_delta: float = 0.0

    @classmethod
    def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations, base_cpi=None, correction_delta=0.0):
        ipc = 1.0 / cpi
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi if base_cpi is not None else cpi, correction_delta)

class BaseProcessorModel:
    pass


class Ns32032Model(BaseProcessorModel):
    """
    National Semiconductor NS32032 Grey-Box Queueing Model

    Target CPI: 10.0
    Calibration: Weighted sum of instruction cycles
    """

    name = "NS32032"
    manufacturer = "National Semiconductor"
    year = 1984
    clock_mhz = 10.0

    def __init__(self):
        # Calibrated cycles to achieve CPI = 10.0
        # CISC with complex microcoded instructions
        # Calculation: 0.25*6 + 0.15*8 + 0.20*12 + 0.15*14 + 0.12*10 + 0.08*12 + 0.05*16 = 10.0
        self.instruction_categories = {
            'register_ops': InstructionCategory('register_ops', 6.0, 0, "Register-to-register"),
            'immediate': InstructionCategory('immediate', 8.0, 0, "Immediate operand"),
            'memory_read': InstructionCategory('memory_read', 6.0, 6.0, "Load from memory"),
            'memory_write': InstructionCategory('memory_write', 6.0, 8.0, "Store to memory"),
            'branch': InstructionCategory('branch', 10.0, 0, "Branch/jump"),
            'call_return': InstructionCategory('call_return', 12.0, 0, "Subroutine call/return"),
            'complex': InstructionCategory('complex', 16.0, 0, "Complex addressing/string ops"),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'register_ops': 0.25,
                'immediate': 0.15,
                'memory_read': 0.20,
                'memory_write': 0.15,
                'branch': 0.12,
                'call_return': 0.08,
                'complex': 0.05,
            }, "Typical CISC workload"),
            'compute': WorkloadProfile('compute', {
                'register_ops': 0.40,
                'immediate': 0.25,
                'memory_read': 0.12,
                'memory_write': 0.08,
                'branch': 0.08,
                'call_return': 0.04,
                'complex': 0.03,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'register_ops': 0.15,
                'immediate': 0.10,
                'memory_read': 0.35,
                'memory_write': 0.25,
                'branch': 0.05,
                'call_return': 0.05,
                'complex': 0.05,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'register_ops': 0.18,
                'immediate': 0.10,
                'memory_read': 0.12,
                'memory_write': 0.08,
                'branch': 0.30,
                'call_return': 0.17,
                'complex': 0.05,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'register_ops': 0.25,
                'immediate': 0.15,
                'memory_read': 0.22,
                'memory_write': 0.15,
                'branch': 0.12,
                'call_return': 0.06,
                'complex': 0.05,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        base_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            base_cpi += contrib
            contributions[cat_name] = contrib
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta
        bottleneck = max(contributions, key=contributions.get)
        return AnalysisResult.from_cpi(
            processor=self.name, workload=workload, cpi=corrected_cpi,
            clock_mhz=self.clock_mhz, bottleneck=bottleneck, utilizations=contributions,
            base_cpi=base_cpi, correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles
