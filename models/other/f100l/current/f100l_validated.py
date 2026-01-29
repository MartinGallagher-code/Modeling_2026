#!/usr/bin/env python3
"""
Ferranti F100-L Grey-Box Queueing Model
========================================

Target CPI: 4.0 (British military 16-bit, 1976)
Architecture: 16-bit bipolar microprocessor

The F100-L was a British-designed military-grade 16-bit processor,
known for its radiation-hardened variants used in aerospace applications.
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


class F100lModel(BaseProcessorModel):
    """
    Ferranti F100-L Grey-Box Queueing Model

    Target CPI: 4.0
    Calibration: Weighted sum of instruction cycles
    """

    name = "F100L"
    manufacturer = "Ferranti"
    year = 1976
    clock_mhz = 1.0

    def __init__(self):
        # Calibrated cycles to achieve CPI = 4.0
        # Efficient military-grade 16-bit architecture
        # Calculation: 0.30*3 + 0.18*5 + 0.15*4 + 0.12*4 + 0.10*4 + 0.08*4 + 0.04*5 + 0.03*4 = 3.92
        self.instruction_categories = {
            'alu_ops': InstructionCategory('alu_ops', 3.0, 0, "ALU operations"),
            'memory_read': InstructionCategory('memory_read', 5.0, 0, "Load from memory"),
            'memory_write': InstructionCategory('memory_write', 4.0, 0, "Store to memory"),
            'branch': InstructionCategory('branch', 4.0, 0, "Branch/conditional"),
            'jump': InstructionCategory('jump', 4.0, 0, "Jump/subroutine"),
            'shift': InstructionCategory('shift', 4.0, 0, "Shift operations"),
            'io': InstructionCategory('io', 5.0, 0, "I/O operations"),
            'control': InstructionCategory('control', 4.0, 0, "Control instructions"),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu_ops': 0.30,
                'memory_read': 0.18,
                'memory_write': 0.15,
                'branch': 0.12,
                'jump': 0.10,
                'shift': 0.08,
                'io': 0.04,
                'control': 0.03,
            }, "Typical embedded workload"),
            'compute': WorkloadProfile('compute', {
                'alu_ops': 0.45,
                'memory_read': 0.12,
                'memory_write': 0.10,
                'branch': 0.10,
                'jump': 0.08,
                'shift': 0.10,
                'io': 0.03,
                'control': 0.02,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'alu_ops': 0.18,
                'memory_read': 0.35,
                'memory_write': 0.28,
                'branch': 0.08,
                'jump': 0.04,
                'shift': 0.03,
                'io': 0.02,
                'control': 0.02,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'alu_ops': 0.20,
                'memory_read': 0.12,
                'memory_write': 0.08,
                'branch': 0.25,
                'jump': 0.18,
                'shift': 0.06,
                'io': 0.05,
                'control': 0.06,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'alu_ops': 0.32,
                'memory_read': 0.18,
                'memory_write': 0.14,
                'branch': 0.12,
                'jump': 0.10,
                'shift': 0.07,
                'io': 0.04,
                'control': 0.03,
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
