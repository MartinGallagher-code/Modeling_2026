#!/usr/bin/env python3
"""
Intel 80287 Grey-Box Queueing Model
===================================

Architecture: FPU Coprocessor (1983)
Math coprocessor for 80286.

Features:
  - Floating-point unit
  - Works with 80286
  - Very high CPI for FP operations

Target CPI: 100.0 (FPU operations are slow)
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


class I80287Model:
    """
    Intel 80287 Grey-Box Queueing Model

    FPU for 80286 (1983)
    - Floating-point coprocessor
    - Very high latency operations
    """

    name = "Intel 80287"
    manufacturer = "Intel"
    year = 1983
    clock_mhz = 8.0
    transistor_count = 45000
    data_width = 80
    address_width = 24

    def __init__(self):
        # FPU operations take many cycles
        self.instruction_categories = {
            'fp_transfer': InstructionCategory('fp_transfer', 20.0, 0, "FLD/FST @17-22"),
            'fp_add': InstructionCategory('fp_add', 85.0, 0, "FADD @80-90"),
            'fp_mul': InstructionCategory('fp_mul', 140.0, 0, "FMUL @130-145"),
            'fp_div': InstructionCategory('fp_div', 200.0, 0, "FDIV @190-210"),
            'fp_sqrt': InstructionCategory('fp_sqrt', 180.0, 0, "FSQRT @175-185"),
            'fp_trig': InstructionCategory('fp_trig', 250.0, 0, "FSIN/FCOS ~250"),
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

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'fp_add': 42.500000,
            'fp_div': -58.484048,
            'fp_mul': -47.650936,
            'fp_sqrt': 89.999993,
            'fp_transfer': 10.000000,
            'fp_trig': 124.999960
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
            bottleneck="fpu_latency",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
