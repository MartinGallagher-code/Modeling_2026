#!/usr/bin/env python3
"""
AT&T DSP32C Grey-Box Queueing Model
===================================

Architecture: 32-bit floating-point, 50 MIPS, Bell Labs telecom
Year: 1988, Clock: 50.0 MHz

Target CPI: 1.1
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


class AttDsp32cModel:
    """
    AT&T DSP32C Grey-Box Queueing Model

    32-bit floating-point, 50 MIPS, Bell Labs telecom (1988)
    - 32-bit float
    - 50 MIPS
    - Bell Labs design
    """

    name = "AT&T DSP32C"
    manufacturer = "AT&T"
    year = 1988
    clock_mhz = 50.0
    transistor_count = 300000
    data_width = 32
    address_width = 32

    def __init__(self):
        self.instruction_categories = {
            'mac': InstructionCategory('mac', 1.0, 0, "Multiply-accumulate"),
            'alu': InstructionCategory('alu', 1.0, 0, "ALU/logic"),
            'load': InstructionCategory('load', 1.0, 0, "Data load"),
            'store': InstructionCategory('store', 1.0, 0, "Data store"),
            'branch': InstructionCategory('branch', 1.0, 0, "Branch/loop"),
            'special': InstructionCategory('special', 2.0, 0, "Special function"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'mac': 0.4,
                'alu': 0.2,
                'load': 0.15,
                'store': 0.1,
                'branch': 0.1,
                'special': 0.05,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'mac': 0.55,
                'alu': 0.2,
                'load': 0.1,
                'store': 0.05,
                'branch': 0.05,
                'special': 0.05,
            }, "Compute workload"),
            'memory': WorkloadProfile('memory', {
                'mac': 0.25,
                'alu': 0.15,
                'load': 0.25,
                'store': 0.2,
                'branch': 0.1,
                'special': 0.05,
            }, "Memory workload"),
            'control': WorkloadProfile('control', {
                'mac': 0.25,
                'alu': 0.15,
                'load': 0.15,
                'store': 0.1,
                'branch': 0.25,
                'special': 0.1,
            }, "Control workload"),
            'mixed': WorkloadProfile('mixed', {
                'mac': 0.35,
                'alu': 0.2,
                'load': 0.15,
                'store': 0.1,
                'branch': 0.1,
                'special': 0.1,
            }, "Mixed workload"),
        }

        self.corrections = {
            'mac': 0.050000,
            'alu': 0.050000,
            'load': 0.050000,
            'store': 0.050000,
            'branch': 0.050000,
            'special': 0.050000,
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
            bottleneck="memory_bandwidth",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
