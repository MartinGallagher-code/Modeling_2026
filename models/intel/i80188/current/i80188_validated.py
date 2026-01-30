#!/usr/bin/env python3
"""
Intel 80188 Grey-Box Queueing Model
===================================

Architecture: Enhanced Prefetch Queue (1982)
8-bit bus version of 80186.

Features:
  - 8-bit external data bus
  - Integrated peripherals
  - Slightly slower than 80186

Target CPI: 4.2 (8-bit bus penalty)
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


class I80188Model:
    """
    Intel 80188 Grey-Box Queueing Model

    8-bit bus 80186 (1982)
    - 8-bit external bus
    - Slightly slower than 80186
    """

    name = "Intel 80188"
    manufacturer = "Intel"
    year = 1982
    clock_mhz = 8.0
    transistor_count = 55000
    data_width = 8
    address_width = 20

    def __init__(self):
        # Slightly slower than 80186
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.2, 0, "ADD/SUB @2 cycles"),
            'data_transfer': InstructionCategory('data_transfer', 2.2, 0, "MOV r,r @2"),
            'memory': InstructionCategory('memory', 6.5, 0, "MOV r,m @6-7 (8-bit bus)"),
            'control': InstructionCategory('control', 9.5, 0, "JMP/CALL ~9-12"),
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
            'alu': 2.112338,
            'control': -5.000000,
            'data_transfer': 1.677701,
            'memory': -2.300454
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
            bottleneck="8bit_bus",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
