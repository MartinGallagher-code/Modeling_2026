#!/usr/bin/env python3
"""
Intel iAPX 432 Grey-Box Queueing Model
======================================

Architecture: Object-Oriented (1981)
Intel's ambitious "mainframe on a chip" project.

Features:
  - Capability-based object-oriented architecture
  - Hardware support for garbage collection
  - Notoriously slow due to architectural complexity
  - Considered a commercial failure

Target CPI: 50.0 (very slow due to complex object-oriented overhead)
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


class IAPX432Model:
    """
    Intel iAPX 432 Grey-Box Queueing Model

    Object-Oriented "Mainframe on a Chip" (1981)
    - Capability-based addressing
    - Hardware garbage collection
    - Very slow - 1/10 the speed of 8086
    """

    name = "Intel iAPX 432"
    manufacturer = "Intel"
    year = 1981
    clock_mhz = 8.0
    transistor_count = 160000
    data_width = 32
    address_width = 32

    def __init__(self):
        # Very high cycle counts due to object-oriented overhead
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 25.0, 0, "ALU ops @25 (with object checks)"),
            'data_transfer': InstructionCategory('data_transfer', 35.0, 0, "Object access @35"),
            'memory': InstructionCategory('memory', 60.0, 0, "Memory @60 (capability check)"),
            'control': InstructionCategory('control', 50.0, 0, "Control flow @50"),
            'object_ops': InstructionCategory('object_ops', 120.0, 0, "Object creation/GC @120"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.30,
                'memory': 0.20,
                'control': 0.15,
                'object_ops': 0.10,
            }, "Typical OO workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.15,
                'object_ops': 0.05,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.30,
                'memory': 0.35,
                'control': 0.10,
                'object_ops': 0.10,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.30,
                'object_ops': 0.10,
            }, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.25,
                'data_transfer': 0.30,
                'memory': 0.20,
                'control': 0.15,
                'object_ops': 0.10,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -6.575237,
            'control': -19.421544,
            'data_transfer': 11.670329,
            'memory': 3.517065,
            'object_ops': 11.963684
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
            bottleneck="oo_overhead",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi,
            correction_delta=correction_delta
        )
