#!/usr/bin/env python3
"""
INMOS T414 Transputer Grey-Box Queueing Model
==============================================

Target CPI: 2.0 (Transputer, 1985)
Architecture: Stack-based with hardware links

The T414 was a transputer - a processor designed for
parallel processing with built-in communication links.
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


class T414Model(BaseProcessorModel):
    """
    INMOS T414 Transputer Grey-Box Queueing Model

    Target CPI: 2.0
    Calibration: Weighted sum of instruction cycles
    """

    name = "T414"
    manufacturer = "INMOS"
    year = 1985
    clock_mhz = 15.0

    def __init__(self):
        # Calibrated cycles to achieve CPI = 2.0
        # Stack-based transputer, efficient instruction encoding
        # Calculation: 0.40*1.5 + 0.18*2.5 + 0.18*2 + 0.14*2.5 + 0.06*2 + 0.04*3 = 2.0
        self.instruction_categories = {
            'stack_ops': InstructionCategory('stack_ops', 1.5, 0, "Stack operations"),
            'memory': InstructionCategory('memory', 1.5, 1.0, "Memory access"),
            'alu': InstructionCategory('alu', 2.0, 0, "ALU operations"),
            'branch': InstructionCategory('branch', 2.5, 0, "Branch/jump"),
            'link_ops': InstructionCategory('link_ops', 2.0, 0, "Communication link operations"),
            'complex': InstructionCategory('complex', 3.0, 0, "Complex instructions"),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'stack_ops': 0.40,
                'memory': 0.18,
                'alu': 0.18,
                'branch': 0.14,
                'link_ops': 0.06,
                'complex': 0.04,
            }, "Typical transputer workload"),
            'compute': WorkloadProfile('compute', {
                'stack_ops': 0.35,
                'memory': 0.12,
                'alu': 0.35,
                'branch': 0.10,
                'link_ops': 0.05,
                'complex': 0.03,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'stack_ops': 0.30,
                'memory': 0.40,
                'alu': 0.12,
                'branch': 0.10,
                'link_ops': 0.05,
                'complex': 0.03,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'stack_ops': 0.35,
                'memory': 0.15,
                'alu': 0.10,
                'branch': 0.30,
                'link_ops': 0.05,
                'complex': 0.05,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'stack_ops': 0.38,
                'memory': 0.22,
                'alu': 0.18,
                'branch': 0.12,
                'link_ops': 0.06,
                'complex': 0.04,
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
