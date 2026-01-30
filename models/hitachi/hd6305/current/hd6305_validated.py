#!/usr/bin/env python3
"""
Hitachi HD6305 Grey-Box Queueing Model
========================================

Architecture: 6805-compatible MCU (1983)
Hitachi second-source of Motorola 6805 family.

Features:
  - 8-bit data bus
  - 4 MHz clock
  - ~10,000 transistors (CMOS)
  - 6805 instruction set compatible
  - Enhanced timer/counter peripherals

Target CPI: 3.5
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


class HD6305Model:
    """
    Hitachi HD6305 Grey-Box Queueing Model

    6805-compatible MCU (1983)
    - 8-bit architecture
    - 4 MHz clock
    - Hitachi second-source of Motorola 6805
    - Enhanced timer/counter peripherals
    """

    name = "Hitachi HD6305"
    manufacturer = "Hitachi"
    year = 1983
    clock_mhz = 4.0
    transistor_count = 10000
    data_width = 8
    address_width = 13

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 3.0, 0, "Basic ALU operations - 3 cycles"),
            'data_transfer': InstructionCategory('data_transfer', 3.0, 0, "Load/store operations - 3 cycles"),
            'memory': InstructionCategory('memory', 5.0, 0, "Extended memory access - 5 cycles"),
            'control': InstructionCategory('control', 4.0, 0, "Branch/jump operations - 4 cycles"),
            'timer': InstructionCategory('timer', 4.0, 0, "Timer/counter operations - 4 cycles"),
        }

        # Typical: 0.30*3 + 0.30*3 + 0.10*5 + 0.15*4 + 0.15*4 = 0.90+0.90+0.50+0.60+0.60 = 3.50
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.30,
                'memory': 0.10,
                'control': 0.15,
                'timer': 0.15,
            }, "Typical embedded control workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.50,
                'data_transfer': 0.25,
                'memory': 0.05,
                'control': 0.15,
                'timer': 0.05,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.40,
                'control': 0.10,
                'timer': 0.15,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.10,
                'control': 0.45,
                'timer': 0.10,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.10,
                'control': 0.15,
                'timer': 0.25,
            }, "Mixed timer/control workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -0.895954,
            'control': -0.289017,
            'data_transfer': 1.560694,
            'memory': 0.190751,
            'timer': -1.167630
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
            bottleneck="sequential",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi,
            correction_delta=correction_delta
        )
