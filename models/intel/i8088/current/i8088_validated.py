#!/usr/bin/env python3
"""
Intel 8088 Grey-Box Queueing Model
==================================

Architecture: Prefetch Queue (1979)
8-bit bus version of 8086 (IBM PC CPU).

Features:
  - 8-bit external data bus (16-bit internal)
  - 4-byte prefetch queue
  - Slower than 8086 due to bus bottleneck

Target CPI: 5.2 (slower than 8086 due to 8-bit bus)
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


class I8088Model:
    """
    Intel 8088 Grey-Box Queueing Model

    IBM PC CPU (1979)
    - 8-bit external bus (16-bit internal)
    - 4-byte prefetch queue
    - ~15% slower than 8086
    """

    name = "Intel 8088"
    manufacturer = "Intel"
    year = 1979
    clock_mhz = 4.77
    transistor_count = 29000
    data_width = 8
    address_width = 20

    def __init__(self):
        # Slightly slower than 8086 due to 8-bit bus
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 3.0, 0, "ADD/SUB @3 effective"),
            'data_transfer': InstructionCategory('data_transfer', 3.0, 0, "MOV r,r @3"),
            'memory': InstructionCategory('memory', 8.0, 0, "MOV r,m @8 (8-bit bus)"),
            'control': InstructionCategory('control', 11.0, 0, "JMP/CALL ~11-15"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.35,
                'memory': 0.20,
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
                'data_transfer': 0.20,
                'memory': 0.45,
                'control': 0.15,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.40,
            }, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.30,
                'data_transfer': 0.30,
                'memory': 0.25,
                'control': 0.15,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -1.994207,
            'control': -2.830204,
            'data_transfer': 3.574021,
            'memory': -1.079106
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
            bottleneck="8bit_bus",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi,
            correction_delta=correction_delta
        )
