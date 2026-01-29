#!/usr/bin/env python3
"""
Intel 80387 Grey-Box Queueing Model
===================================

Architecture: FPU Coprocessor (1987)
Math coprocessor for 80386.

Features:
  - Floating-point unit
  - Works with 80386
  - Faster than 80287

Target CPI: 50.0 (faster than 80287)
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


class I80387Model:
    """
    Intel 80387 Grey-Box Queueing Model

    FPU for 80386 (1987)
    - Faster than 80287
    - Better pipelining
    """

    name = "Intel 80387"
    manufacturer = "Intel"
    year = 1987
    clock_mhz = 16.0
    transistor_count = 120000
    data_width = 80
    address_width = 32

    def __init__(self):
        # FPU operations - faster than 80287
        self.instruction_categories = {
            'fp_transfer': InstructionCategory('fp_transfer', 16.0, 0, "FLD/FST @14-18"),
            'fp_add': InstructionCategory('fp_add', 35.0, 0, "FADD @30-40"),
            'fp_mul': InstructionCategory('fp_mul', 65.0, 0, "FMUL @60-70"),
            'fp_div': InstructionCategory('fp_div', 100.0, 0, "FDIV @95-105"),
            'fp_sqrt': InstructionCategory('fp_sqrt', 140.0, 0, "FSQRT ~140"),
            'fp_trig': InstructionCategory('fp_trig', 175.0, 0, "FSIN/FCOS ~175"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'fp_transfer': 0.30,
                'fp_add': 0.30,
                'fp_mul': 0.25,
                'fp_div': 0.10,
                'fp_sqrt': 0.03,
                'fp_trig': 0.02,
            }, "Typical FP workload"),
            'compute': WorkloadProfile('compute', {
                'fp_transfer': 0.20,
                'fp_add': 0.35,
                'fp_mul': 0.30,
                'fp_div': 0.10,
                'fp_sqrt': 0.03,
                'fp_trig': 0.02,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'fp_transfer': 0.50,
                'fp_add': 0.25,
                'fp_mul': 0.15,
                'fp_div': 0.05,
                'fp_sqrt': 0.03,
                'fp_trig': 0.02,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'fp_transfer': 0.30,
                'fp_add': 0.30,
                'fp_mul': 0.25,
                'fp_div': 0.10,
                'fp_sqrt': 0.03,
                'fp_trig': 0.02,
            }, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'fp_transfer': 0.30,
                'fp_add': 0.30,
                'fp_mul': 0.25,
                'fp_div': 0.10,
                'fp_sqrt': 0.03,
                'fp_trig': 0.02,
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
            bottleneck="fpu_latency",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories}
        )
