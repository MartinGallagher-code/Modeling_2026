#!/usr/bin/env python3
"""
Motorola 6805R2 Grey-Box Queueing Model
=========================================

Architecture: Appliance MCU (1982)
Low-cost microcontroller for household appliance control.

Features:
  - 8-bit data bus
  - 2 MHz clock
  - ~8,000 transistors (NMOS)
  - Minimal pin count for cost-sensitive applications
  - Built-in oscillator, timer, I/O ports

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

    @classmethod
    def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations):
        ipc = 1.0 / cpi
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations)


class M6805R2Model:
    """
    Motorola 6805R2 Grey-Box Queueing Model

    Appliance MCU (1982)
    - 8-bit architecture (6805 family)
    - 2 MHz clock
    - Low-cost appliance controller
    - Minimal transistor count for cost reduction
    """

    name = "Motorola 6805R2"
    manufacturer = "Motorola"
    year = 1982
    clock_mhz = 2.0
    transistor_count = 8000
    data_width = 8
    address_width = 13

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 3.0, 0, "Basic ALU operations - 3 cycles"),
            'data_transfer': InstructionCategory('data_transfer', 3.0, 0, "Load/store operations - 3 cycles"),
            'memory': InstructionCategory('memory', 5.0, 0, "Extended memory access - 5 cycles"),
            'control': InstructionCategory('control', 4.0, 0, "Branch/jump operations - 4 cycles"),
            'bit_ops': InstructionCategory('bit_ops', 3.0, 0, "Bit test/set/clear - 3 cycles"),
        }

        # Typical: 0.25*3 + 0.20*3 + 0.15*5 + 0.20*4 + 0.20*3 = 0.75+0.60+0.75+0.80+0.60 = 3.50
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.20,
                'memory': 0.15,
                'control': 0.20,
                'bit_ops': 0.20,
            }, "Typical appliance control workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'data_transfer': 0.25,
                'memory': 0.05,
                'control': 0.15,
                'bit_ops': 0.10,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.40,
                'control': 0.10,
                'bit_ops': 0.15,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.10,
                'control': 0.45,
                'bit_ops': 0.15,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.20,
                'data_transfer': 0.20,
                'memory': 0.15,
                'control': 0.20,
                'bit_ops': 0.25,
            }, "Mixed I/O control workload"),
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        total_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            total_cpi += weight * cat.total_cycles

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=total_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck="sequential",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories}
        )
