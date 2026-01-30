#!/usr/bin/env python3
"""
Novix NC4000 Grey-Box Queueing Model
======================================

Architecture: Forth-on-a-Chip (1983)
First single-chip Forth processor, designed by Chuck Moore.

Features:
  - 16-bit data bus
  - 8 MHz clock
  - ~16,000 transistors (CMOS)
  - Sequential execution
  - Hardware data and return stacks
  - Single-cycle Forth primitives
  - Direct Forth word execution

Target CPI: 1.5
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


class NC4000Model:
    """
    Novix NC4000 Grey-Box Queueing Model

    Forth-on-a-chip (1983)
    - 16-bit architecture
    - 8 MHz clock
    - First single-chip Forth processor
    - Hardware dual stacks
    - Designed by Chuck Moore
    """

    name = "Novix NC4000"
    manufacturer = "Novix"
    year = 1983
    clock_mhz = 8.0
    transistor_count = 16000
    data_width = 16
    address_width = 16

    def __init__(self):
        self.instruction_categories = {
            'stack_op': InstructionCategory('stack_op', 1.0, 0, "Stack push/pop/dup/swap - 1 cycle"),
            'alu': InstructionCategory('alu', 1.0, 0, "ALU operations on TOS - 1 cycle"),
            'memory': InstructionCategory('memory', 3.0, 0, "Memory fetch/store - 3 cycles"),
            'control': InstructionCategory('control', 2.0, 0, "Branch/loop operations - 2 cycles"),
            'call_return': InstructionCategory('call_return', 1.0, 0, "Subroutine call/return - 1 cycle"),
        }

        # Typical: 0.30*1 + 0.25*1 + 0.20*3 + 0.10*2 + 0.15*1 = 0.30+0.25+0.60+0.20+0.15 = 1.50
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'stack_op': 0.30,
                'alu': 0.25,
                'memory': 0.20,
                'control': 0.10,
                'call_return': 0.15,
            }, "Typical Forth workload"),
            'compute': WorkloadProfile('compute', {
                'stack_op': 0.25,
                'alu': 0.45,
                'memory': 0.10,
                'control': 0.10,
                'call_return': 0.10,
            }, "Compute-intensive Forth"),
            'memory': WorkloadProfile('memory', {
                'stack_op': 0.15,
                'alu': 0.10,
                'memory': 0.45,
                'control': 0.10,
                'call_return': 0.20,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'stack_op': 0.15,
                'alu': 0.15,
                'memory': 0.15,
                'control': 0.35,
                'call_return': 0.20,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'stack_op': 0.25,
                'alu': 0.25,
                'memory': 0.20,
                'control': 0.15,
                'call_return': 0.15,
            }, "Mixed Forth workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

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
