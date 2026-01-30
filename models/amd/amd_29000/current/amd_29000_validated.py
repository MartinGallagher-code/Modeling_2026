#!/usr/bin/env python3
"""
AMD Am29000 Grey-Box Queueing Model (Alternate Entry)
======================================================

32-bit RISC processor (1987)
- 192 registers
- 4-stage pipeline
- Dominated laser printer market
- Target CPI: 1.33 (IPC 0.75)
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
        ipc = 1.0 / cpi if cpi > 0 else 0.0
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                   base_cpi=base_cpi if base_cpi is not None else cpi,
                   correction_delta=correction_delta)

class BaseProcessorModel:
    pass


class Amd29000Model(BaseProcessorModel):
    """
    AMD Am29000 - RISC for Embedded/Graphics
    Target CPI: 1.33 (IPC 0.75)
    """

    name = "AMD Am29000"
    manufacturer = "AMD"
    year = 1987
    clock_mhz = 25.0
    transistor_count = 180000
    data_width = 32
    address_width = 32

    def __init__(self):
        # RISC - calibrated for CPI 1.33
        # 0.50*1.0 + 0.18*1.5 + 0.12*1.2 + 0.15*1.8 + 0.03*2.0 + 0.02*3.0 = 1.33
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "ALU operation"),
            'load': InstructionCategory('load', 1.5, 0, "Load"),
            'store': InstructionCategory('store', 1.2, 0, "Store"),
            'branch': InstructionCategory('branch', 1.8, 0, "Branch"),
            'multiply': InstructionCategory('multiply', 2.0, 0, "Multiply"),
            'call_return': InstructionCategory('call_return', 3.0, 0, "Call/Return"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.50, 'load': 0.18, 'store': 0.12,
                'branch': 0.15, 'multiply': 0.03, 'call_return': 0.02,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.60, 'load': 0.12, 'store': 0.08,
                'branch': 0.12, 'multiply': 0.06, 'call_return': 0.02,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.35, 'load': 0.28, 'store': 0.20,
                'branch': 0.10, 'multiply': 0.04, 'call_return': 0.03,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.40, 'load': 0.15, 'store': 0.10,
                'branch': 0.25, 'multiply': 0.03, 'call_return': 0.07,
            }, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.48, 'load': 0.18, 'store': 0.12,
                'branch': 0.15, 'multiply': 0.04, 'call_return': 0.03,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.330584,
            'branch': -0.471880,
            'call_return': -1.665057,
            'load': -0.168942,
            'multiply': -0.673776,
            'store': 0.128452
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

        # Apply correction terms (system identification)
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

        bottleneck = max(contributions, key=contributions.get)

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=corrected_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=contributions,
            base_cpi=base_cpi,
            correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles
