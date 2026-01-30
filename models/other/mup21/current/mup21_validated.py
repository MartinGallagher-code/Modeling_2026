#!/usr/bin/env python3
"""
MuP21 Grey-Box Queueing Model
================================

Architecture: Minimal Forth Chip (1985)
Ultra-minimal Forth processor designed by Chuck Moore.

Features:
  - 21-bit data bus
  - 50 MHz clock
  - ~7,000 transistors (CMOS)
  - Extreme minimalism
  - Hardware data and return stacks
  - Four instructions packed per 20-bit word
  - Video and I/O coprocessor features

Target CPI: 1.3
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


class MuP21Model:
    """
    MuP21 Grey-Box Queueing Model

    Minimal Forth chip (1985)
    - 21-bit architecture
    - 50 MHz clock
    - Ultra-minimal design (~7,000 transistors)
    - Four instructions packed per word
    - Designed by Chuck Moore
    """

    name = "MuP21"
    manufacturer = "Chuck Moore"
    year = 1985
    clock_mhz = 50.0
    transistor_count = 7000
    data_width = 21
    address_width = 21

    def __init__(self):
        self.instruction_categories = {
            'stack_op': InstructionCategory('stack_op', 1.0, 0, "Stack push/pop/dup/swap - 1 cycle"),
            'alu': InstructionCategory('alu', 1.0, 0, "ALU operations on TOS - 1 cycle"),
            'memory': InstructionCategory('memory', 2.0, 0, "Memory fetch/store - 2 cycles"),
            'control': InstructionCategory('control', 1.0, 0, "Branch/call operations - 1 cycle"),
            'io': InstructionCategory('io', 3.0, 0, "I/O and video operations - 3 cycles"),
        }

        # Typical: 0.35*1 + 0.30*1 + 0.10*2 + 0.15*1 + 0.10*3 = 0.35+0.30+0.20+0.15+0.30 = 1.30
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'stack_op': 0.35,
                'alu': 0.30,
                'memory': 0.10,
                'control': 0.15,
                'io': 0.10,
            }, "Typical Forth workload"),
            'compute': WorkloadProfile('compute', {
                'stack_op': 0.30,
                'alu': 0.45,
                'memory': 0.05,
                'control': 0.15,
                'io': 0.05,
            }, "Compute-intensive Forth"),
            'memory': WorkloadProfile('memory', {
                'stack_op': 0.20,
                'alu': 0.15,
                'memory': 0.35,
                'control': 0.10,
                'io': 0.20,
            }, "Memory and I/O intensive"),
            'control': WorkloadProfile('control', {
                'stack_op': 0.20,
                'alu': 0.20,
                'memory': 0.10,
                'control': 0.40,
                'io': 0.10,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'stack_op': 0.30,
                'alu': 0.25,
                'memory': 0.15,
                'control': 0.15,
                'io': 0.15,
            }, "Mixed Forth with I/O"),
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
