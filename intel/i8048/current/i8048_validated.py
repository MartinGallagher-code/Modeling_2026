#!/usr/bin/env python3
"""
Intel 8048 Grey-Box Queueing Model
==================================

Architecture: Microcontroller (1976)
First single-chip microcontroller.

Features:
  - 8-bit data bus
  - Integrated RAM, ROM, I/O
  - Most instructions 1-2 cycles (machine cycles)
  - Very efficient for embedded control

Target CPI: 1.5 (most instructions single-cycle)
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


class I8048Model:
    """
    Intel 8048 Grey-Box Queueing Model

    First microcontroller (1976)
    - 8-bit architecture
    - Most instructions 1-2 machine cycles
    - Optimized for embedded control
    """

    name = "Intel 8048"
    manufacturer = "Intel"
    year = 1976
    clock_mhz = 6.0
    transistor_count = 6000
    data_width = 8
    address_width = 12

    def __init__(self):
        # Most instructions are 1-2 cycles (machine cycles)
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "ADD/SUB @1 cycle"),
            'data_transfer': InstructionCategory('data_transfer', 1.0, 0, "MOV @1 cycle"),
            'memory': InstructionCategory('memory', 2.5, 0, "MOVX @2.5 cycles"),
            'control': InstructionCategory('control', 2.5, 0, "JMP/CALL @2.5 cycles"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.40,
                'memory': 0.10,
                'control': 0.20,
            }, "Typical microcontroller workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.50,
                'data_transfer': 0.30,
                'memory': 0.05,
                'control': 0.15,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.20,
                'data_transfer': 0.30,
                'memory': 0.35,
                'control': 0.15,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.30,
                'memory': 0.10,
                'control': 0.40,
            }, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.30,
                'data_transfer': 0.35,
                'memory': 0.15,
                'control': 0.20,
            }, "Mixed workload"),
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
