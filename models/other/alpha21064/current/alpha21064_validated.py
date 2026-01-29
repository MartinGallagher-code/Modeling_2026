#!/usr/bin/env python3
"""
DEC Alpha 21064 Grey-Box Queueing Model
========================================

64-bit superscalar RISC processor (1992)
- 2-way superscalar
- 7-stage pipeline
- 8KB I-cache, 8KB D-cache
- Target CPI: 1.0 (IPC ~1.0)
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


class Alpha21064Model(BaseProcessorModel):
    """
    DEC Alpha 21064 - First 64-bit RISC superscalar
    Target CPI: 1.0
    """

    name = "DEC Alpha 21064"
    manufacturer = "DEC"
    year = 1992
    clock_mhz = 150.0
    transistor_count = 1680000
    data_width = 64
    address_width = 64

    def __init__(self):
        # Superscalar RISC - calibrated for CPI 0.77 (IPC ~1.3)
        # 0.50*0.5 + 0.20*1.0 + 0.12*0.8 + 0.15*1.0 + 0.02*2.5 + 0.01*6.0 = 0.77
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 0.50, 0, "ALU ops (dual-issue)"),
            'load': InstructionCategory('load', 1.00, 0, "Load (cache hits)"),
            'store': InstructionCategory('store', 0.80, 0, "Store"),
            'branch': InstructionCategory('branch', 1.00, 0, "Branch (predicted)"),
            'multiply': InstructionCategory('multiply', 2.5, 0, "Integer multiply"),
            'divide': InstructionCategory('divide', 6.0, 0, "Integer divide"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.50, 'load': 0.20, 'store': 0.12,
                'branch': 0.15, 'multiply': 0.02, 'divide': 0.01,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.60, 'load': 0.14, 'store': 0.08,
                'branch': 0.12, 'multiply': 0.04, 'divide': 0.02,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.30, 'load': 0.35, 'store': 0.20,
                'branch': 0.10, 'multiply': 0.03, 'divide': 0.02,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.40, 'load': 0.15, 'store': 0.10,
                'branch': 0.30, 'multiply': 0.03, 'divide': 0.02,
            }, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.48, 'load': 0.22, 'store': 0.13,
                'branch': 0.12, 'multiply': 0.03, 'divide': 0.02,
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
