#!/usr/bin/env python3
"""
Intel 80386 Grey-Box Queueing Model
===================================

Architecture: 32-bit Protected Mode (1985)
First 32-bit x86.

Features:
  - 32-bit data bus
  - Virtual 8086 mode
  - Paging support

Target CPI: 4.5
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


class I80386Model:
    """
    Intel 80386 Grey-Box Queueing Model

    First 32-bit x86 (1985)
    - Full 32-bit architecture
    - No on-chip cache
    """

    name = "Intel 80386"
    manufacturer = "Intel"
    year = 1985
    clock_mhz = 16.0
    transistor_count = 275000
    data_width = 32
    address_width = 32

    def __init__(self):
        # 32-bit operations, but no cache
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.5, 0, "ADD/SUB @2-3 cycles"),
            'data_transfer': InstructionCategory('data_transfer', 2.5, 0, "MOV r,r @2-3"),
            'memory': InstructionCategory('memory', 5.0, 0, "MOV r,m @4-5"),
            'control': InstructionCategory('control', 9.0, 0, "JMP/CALL @7-9"),
            'multiply': InstructionCategory('multiply', 14.0, 0, "MUL @14"),
            'divide': InstructionCategory('divide', 40.0, 0, "DIV @40"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.35,
                'memory': 0.20,
                'control': 0.13,
                'multiply': 0.01,
                'divide': 0.01,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.10,
                'multiply': 0.03,
                'divide': 0.02,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.20,
                'data_transfer': 0.25,
                'memory': 0.40,
                'control': 0.13,
                'multiply': 0.01,
                'divide': 0.01,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.30,
                'memory': 0.15,
                'control': 0.33,
                'multiply': 0.01,
                'divide': 0.01,
            }, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.30,
                'data_transfer': 0.30,
                'memory': 0.25,
                'control': 0.13,
                'multiply': 0.01,
                'divide': 0.01,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.916312,
            'control': -4.970663,
            'data_transfer': 2.742023,
            'divide': -19.999912,
            'memory': -0.694724,
            'multiply': -6.991336
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
            bottleneck="no_cache",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
