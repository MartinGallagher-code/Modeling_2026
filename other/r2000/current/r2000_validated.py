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

    @classmethod
    def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations):
        ipc = 1.0 / cpi
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations)

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
        # Calibrated cycles to achieve CPI = 1.5
        # RISC: most instructions single-cycle, loads have latency
        # Calculation: 0.40*1 + 0.20*2 + 0.10*1 + 0.15*2 + 0.08*2 + 0.04*3 + 0.02*1 + 0.01*4 = 1.5
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "ALU operations"),
            'load': InstructionCategory('load', 1.0, 1.0, "Load with delay slot"),
            'store': InstructionCategory('store', 1.0, 0, "Store"),
            'branch': InstructionCategory('branch', 2.0, 0, "Branch with delay slot"),
            'jump': InstructionCategory('jump', 2.0, 0, "Jump instructions"),
            'multiply': InstructionCategory('multiply', 3.0, 0, "Multiply"),
            'shift': InstructionCategory('shift', 1.0, 0, "Shift operations"),
            'divide': InstructionCategory('divide', 4.0, 0, "Divide (multi-cycle)"),
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
