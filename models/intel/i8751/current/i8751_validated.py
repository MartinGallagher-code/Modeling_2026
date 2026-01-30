#!/usr/bin/env python3
"""
Intel 8751 Grey-Box Queueing Model
==================================

Architecture: Microcontroller (1980)
EPROM version of 8051.

Features:
  - Same as 8051 but with EPROM
  - 12 clock cycles per machine cycle

Target CPI: 12.0
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


class I8751Model:
    """
    Intel 8751 Grey-Box Queueing Model

    EPROM version of 8051 (1980)
    - Same timing as 8051
    """

    name = "Intel 8751"
    manufacturer = "Intel"
    year = 1980
    clock_mhz = 12.0
    transistor_count = 128000
    data_width = 8
    address_width = 16

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 12.0, 0, "ADD/SUB @12 clocks"),
            'data_transfer': InstructionCategory('data_transfer', 12.0, 0, "MOV @12 clocks"),
            'memory': InstructionCategory('memory', 12.0, 0, "MOVX @12 (single machine cycle)"),
            'control': InstructionCategory('control', 12.0, 0, "JMP/CALL @12 clocks"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.40,
                'memory': 0.10,
                'control': 0.20,
            }, "Typical workload"),
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
