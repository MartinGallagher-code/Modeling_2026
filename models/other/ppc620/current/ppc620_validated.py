#!/usr/bin/env python3
"""
PowerPC 620 Grey-Box Queueing Model
===================================

Architecture: 64-bit PowerPC, first 64-bit PPC
Year: 1994, Clock: 133.0 MHz

Target CPI: 0.8
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
                   base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)


class Ppc620Model:
    """
    PowerPC 620 Grey-Box Queueing Model

    64-bit PowerPC, first 64-bit PPC (1994)
    - 4-issue superscalar
    - 64-bit
    - 32KB I+D cache
    """

    name = "PowerPC 620"
    manufacturer = "Motorola/IBM"
    year = 1994
    clock_mhz = 133.0
    transistor_count = 7000000
    data_width = 64
    address_width = 64

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "ALU/logic ops"),
            'load': InstructionCategory('load', 1.0, 0, "Load from memory"),
            'store': InstructionCategory('store', 1.0, 0, "Store to memory"),
            'branch': InstructionCategory('branch', 1.0, 0, "Branch/jump"),
            'multiply': InstructionCategory('multiply', 2.0, 0, "Multiply"),
            'divide': InstructionCategory('divide', 12.0, 0, "Divide"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.35,
                'load': 0.25,
                'store': 0.15,
                'branch': 0.2,
                'multiply': 0.03,
                'divide': 0.02,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'load': 0.15,
                'store': 0.1,
                'branch': 0.15,
                'multiply': 0.1,
                'divide': 0.05,
            }, "Compute workload"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.2,
                'load': 0.35,
                'store': 0.25,
                'branch': 0.15,
                'multiply': 0.03,
                'divide': 0.02,
            }, "Memory workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.25,
                'load': 0.15,
                'store': 0.1,
                'branch': 0.45,
                'multiply': 0.03,
                'divide': 0.02,
            }, "Control workload"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.3,
                'load': 0.25,
                'store': 0.15,
                'branch': 0.2,
                'multiply': 0.05,
                'divide': 0.05,
            }, "Mixed workload"),
        }

        self.corrections = {
            'alu': -0.450000,
            'load': -0.450000,
            'store': -0.450000,
            'branch': -0.450000,
            'multiply': -0.450000,
            'divide': -0.450000,
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        base_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=corrected_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck="issue_width",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
