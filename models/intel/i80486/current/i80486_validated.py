#!/usr/bin/env python3
"""
Intel 80486 Grey-Box Queueing Model
===================================

Architecture: Pipelined CISC (1989)
First x86 with on-chip cache and FPU.

Features:
  - 32-bit pipelined architecture
  - 8KB unified cache
  - On-chip FPU
  - Many single-cycle instructions

Target CPI: 2.0 (approaching RISC-like efficiency)
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


class I80486Model:
    """
    Intel 80486 Grey-Box Queueing Model

    First x86 with cache+FPU (1989)
    - 5-stage pipeline
    - 8KB unified cache
    - Many single-cycle instructions
    """

    name = "Intel 80486"
    manufacturer = "Intel"
    year = 1989
    clock_mhz = 25.0
    transistor_count = 1200000
    data_width = 32
    address_width = 32

    def __init__(self):
        # Many instructions now single-cycle with pipeline
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "ADD/SUB @1 cycle"),
            'data_transfer': InstructionCategory('data_transfer', 1.0, 0, "MOV @1 cycle"),
            'memory': InstructionCategory('memory', 2.0, 0, "MOV r,m @1-2 (cache hit)"),
            'control': InstructionCategory('control', 4.0, 0, "JMP @3-4, branch penalty"),
            'multiply': InstructionCategory('multiply', 13.0, 0, "MUL @13"),
            'divide': InstructionCategory('divide', 40.0, 0, "DIV @40"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.40,
                'memory': 0.15,
                'control': 0.13,
                'multiply': 0.01,
                'divide': 0.01,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.50,
                'data_transfer': 0.25,
                'memory': 0.12,
                'control': 0.10,
                'multiply': 0.02,
                'divide': 0.01,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.20,
                'data_transfer': 0.30,
                'memory': 0.35,
                'control': 0.13,
                'multiply': 0.01,
                'divide': 0.01,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.25,
                'data_transfer': 0.30,
                'memory': 0.12,
                'control': 0.31,
                'multiply': 0.01,
                'divide': 0.01,
            }, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.30,
                'data_transfer': 0.35,
                'memory': 0.20,
                'control': 0.13,
                'multiply': 0.01,
                'divide': 0.01,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.616987,
            'control': -2.219677,
            'data_transfer': 0.896555,
            'divide': -19.999973,
            'memory': -0.250076,
            'multiply': -6.499999
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        base_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

        # Apply correction terms (system identification)
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
