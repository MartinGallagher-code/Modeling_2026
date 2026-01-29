#!/usr/bin/env python3
"""
Intel 80286 Grey-Box Queueing Model
===================================

Architecture: Protected Mode (1982)
First x86 with protected mode.

Features:
  - 16-bit data bus
  - Protected mode
  - Faster than 8086

Target CPI: 4.0
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


class I80286Model:
    """
    Intel 80286 Grey-Box Queueing Model

    IBM PC/AT CPU (1982)
    - 16-bit protected mode
    - Much faster than 8086
    """

    name = "Intel 80286"
    manufacturer = "Intel"
    year = 1982
    clock_mhz = 8.0
    transistor_count = 134000
    data_width = 16
    address_width = 24

    def __init__(self):
        # Faster than 8086 family
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.5, 0, "ADD/SUB @2-3 cycles"),
            'data_transfer': InstructionCategory('data_transfer', 2.5, 0, "MOV r,r @2-3"),
            'memory': InstructionCategory('memory', 6.0, 0, "MOV r,m @5-6"),
            'control': InstructionCategory('control', 9.0, 0, "JMP/CALL @7-9"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.40,
                'memory': 0.15,
                'control': 0.15,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.50,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.10,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.20,
                'data_transfer': 0.25,
                'memory': 0.40,
                'control': 0.15,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.30,
                'memory': 0.15,
                'control': 0.35,
            }, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.30,
                'data_transfer': 0.35,
                'memory': 0.20,
                'control': 0.15,
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
            bottleneck="protected_mode",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories}
        )
