#!/usr/bin/env python3
"""
MIPS R2000 Grey-Box Queueing Model
===================================

Target CPI: 1.5 (RISC processor, 1985)
Architecture: Classic 5-stage RISC pipeline

The R2000 was one of the first commercial MIPS RISC processors,
designed for high throughput with simple instructions.
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


class R2000Model(BaseProcessorModel):
    """
    MIPS R2000 Grey-Box Queueing Model

    Target CPI: 1.5
    Calibration: Weighted sum of instruction cycles
    """

    name = "R2000"
    manufacturer = "MIPS"
    year = 1985
    clock_mhz = 8.0

    def __init__(self):
        # Calibrated cycles to achieve CPI = 2.0
        # RISC: most instructions single-cycle, but early MIPS had stalls
        # Calculation: 0.40*1.5 + 0.20*2.5 + 0.10*1.5 + 0.15*2.5 + 0.08*2.5 + 0.04*4.0 + 0.02*1.5 + 0.01*5.0 = 2.0
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.5, 0, "ALU operations"),
            'load': InstructionCategory('load', 2.5, 0, "Load with delay slot"),
            'store': InstructionCategory('store', 1.5, 0, "Store"),
            'branch': InstructionCategory('branch', 2.5, 0, "Branch with delay slot"),
            'jump': InstructionCategory('jump', 2.5, 0, "Jump instructions"),
            'multiply': InstructionCategory('multiply', 4.0, 0, "Multiply"),
            'shift': InstructionCategory('shift', 1.5, 0, "Shift operations"),
            'divide': InstructionCategory('divide', 5.0, 0, "Divide (multi-cycle)"),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.40,
                'load': 0.20,
                'store': 0.10,
                'branch': 0.15,
                'jump': 0.08,
                'multiply': 0.04,
                'shift': 0.02,
                'divide': 0.01,
            }, "Typical RISC workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.50,
                'load': 0.12,
                'store': 0.08,
                'branch': 0.12,
                'jump': 0.05,
                'multiply': 0.08,
                'shift': 0.03,
                'divide': 0.02,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.25,
                'load': 0.35,
                'store': 0.20,
                'branch': 0.10,
                'jump': 0.05,
                'multiply': 0.02,
                'shift': 0.02,
                'divide': 0.01,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.30,
                'load': 0.15,
                'store': 0.08,
                'branch': 0.28,
                'jump': 0.12,
                'multiply': 0.03,
                'shift': 0.02,
                'divide': 0.02,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.38,
                'load': 0.22,
                'store': 0.12,
                'branch': 0.15,
                'jump': 0.06,
                'multiply': 0.04,
                'shift': 0.02,
                'divide': 0.01,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.385535,
            'branch': -0.430264,
            'divide': -1.004471,
            'jump': -0.892888,
            'load': 0.364216,
            'multiply': -1.102745,
            'shift': -0.738764,
            'store': -0.871568
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        base_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            base_cpi += contrib
            contributions[cat_name] = contrib
        bottleneck = max(contributions, key=contributions.get)
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta
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
