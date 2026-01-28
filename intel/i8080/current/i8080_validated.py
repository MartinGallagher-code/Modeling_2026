#!/usr/bin/env python3
"""
Intel 8080 Grey-Box Queueing Model
==================================

Architecture: Sequential Execution (1974)
Industry standard 8-bit CPU.

Features:
  - 8-bit data bus
  - 4-18 cycles per instruction
  - No prefetch queue
  - Sequential execution

Target CPI: 9.2 (based on datasheet timing)
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


class I8080Model:
    """
    Intel 8080 Grey-Box Queueing Model

    Industry standard 8-bit CPU (1974)
    - 8-bit architecture
    - Instructions take 4-18 cycles
    - Sequential execution
    """

    name = "Intel 8080"
    manufacturer = "Intel"
    year = 1974
    clock_mhz = 2.0
    transistor_count = 4500
    data_width = 8
    address_width = 16

    def __init__(self):
        # From validation JSON timing tests
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 6.5, 0, "ADD/ADI @4-7 cycles avg 6.5"),
            'data_transfer': InstructionCategory('data_transfer', 7.0, 0, "MOV/MVI @5-7 cycles"),
            'memory': InstructionCategory('memory', 10.0, 0, "MOV r,M / MOV M,r @7-10"),
            'control': InstructionCategory('control', 15.0, 0, "JMP/CALL/RET @10-17"),
            'stack': InstructionCategory('stack', 11.0, 0, "PUSH/POP @10-11"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.30,
                'memory': 0.20,
                'control': 0.15,
                'stack': 0.10,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.10,
                'stack': 0.05,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.25,
                'memory': 0.40,
                'control': 0.10,
                'stack': 0.10,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.15,
                'control': 0.35,
                'stack': 0.15,
            }, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.25,
                'control': 0.15,
                'stack': 0.10,
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
