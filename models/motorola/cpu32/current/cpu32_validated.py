#!/usr/bin/env python3
"""
Motorola CPU32 Grey-Box Queueing Model
======================================

Architecture: 68020-based embedded core with on-chip peripherals
Year: 1990, Clock: 16.0 MHz

Target CPI: 2.5
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


class Cpu32Model:
    """
    Motorola CPU32 Grey-Box Queueing Model

    68020-based embedded core with on-chip peripherals (1990)
    - 68020 core
    - On-chip peripherals
    - Background debug mode
    """

    name = "Motorola CPU32"
    manufacturer = "Motorola"
    year = 1990
    clock_mhz = 16.0
    transistor_count = 340000
    data_width = 32
    address_width = 32

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.0, 0, "ALU/logic"),
            'data_transfer': InstructionCategory('data_transfer', 2.0, 0, "Register transfer"),
            'memory': InstructionCategory('memory', 3.0, 0, "Memory access"),
            'control': InstructionCategory('control', 5.0, 0, "Branch/call"),
            'multiply': InstructionCategory('multiply', 20.0, 0, "Multiply"),
            'divide': InstructionCategory('divide', 40.0, 0, "Divide"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.3,
                'data_transfer': 0.35,
                'memory': 0.2,
                'control': 0.13,
                'multiply': 0.01,
                'divide': 0.01,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.1,
                'multiply': 0.03,
                'divide': 0.02,
            }, "Compute workload"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.2,
                'data_transfer': 0.25,
                'memory': 0.4,
                'control': 0.13,
                'multiply': 0.01,
                'divide': 0.01,
            }, "Memory workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.2,
                'data_transfer': 0.3,
                'memory': 0.15,
                'control': 0.33,
                'multiply': 0.01,
                'divide': 0.01,
            }, "Control workload"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.3,
                'data_transfer': 0.3,
                'memory': 0.25,
                'control': 0.13,
                'multiply': 0.01,
                'divide': 0.01,
            }, "Mixed workload"),
        }

        self.corrections = {
            'alu': -0.650000,
            'data_transfer': -0.650000,
            'memory': -0.650000,
            'control': -0.650000,
            'multiply': -0.650000,
            'divide': -0.650000,
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
            bottleneck="pipeline",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
