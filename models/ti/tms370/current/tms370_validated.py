#!/usr/bin/env python3
"""
TI TMS370 Grey-Box Queueing Model
====================================

Architecture: Industrial MCU (1985)
Texas Instruments 8-bit industrial microcontroller.

Features:
  - 8-bit data bus
  - 8 MHz clock
  - ~30,000 transistors (CMOS)
  - Rich peripheral set for industrial control
  - Register-file based architecture

Target CPI: 3.0
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


class TMS370Model:
    """
    TI TMS370 Grey-Box Queueing Model

    Industrial MCU (1985)
    - 8-bit architecture
    - 8 MHz clock
    - Rich peripheral integration
    - Register-file based for efficient operation
    """

    name = "TI TMS370"
    manufacturer = "Texas Instruments"
    year = 1985
    clock_mhz = 8.0
    transistor_count = 30000
    data_width = 8
    address_width = 16

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.0, 0, "Register-to-register ALU - 2 cycles"),
            'data_transfer': InstructionCategory('data_transfer', 3.0, 0, "Data move operations - 3 cycles"),
            'memory': InstructionCategory('memory', 4.0, 0, "Memory access operations - 4 cycles"),
            'control': InstructionCategory('control', 3.0, 0, "Branch/call operations - 3 cycles"),
            'peripheral': InstructionCategory('peripheral', 5.0, 0, "Peripheral register access - 5 cycles"),
        }

        # Typical: 0.30*2 + 0.25*3 + 0.10*4 + 0.25*3 + 0.10*5 = 0.60+0.75+0.40+0.75+0.50 = 3.00
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.25,
                'memory': 0.10,
                'control': 0.25,
                'peripheral': 0.10,
            }, "Typical industrial control workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.50,
                'data_transfer': 0.25,
                'memory': 0.05,
                'control': 0.15,
                'peripheral': 0.05,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.35,
                'control': 0.10,
                'peripheral': 0.20,
            }, "Memory and peripheral intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.15,
                'memory': 0.10,
                'control': 0.45,
                'peripheral': 0.10,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.20,
                'peripheral': 0.15,
            }, "Mixed industrial workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        total_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            total_cpi += weight * cat.total_cycles

        # System identification: apply correction terms
        base_cpi = total_cpi
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
            bottleneck="sequential",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
