#!/usr/bin/env python3
"""
Intel 8044 Grey-Box Queueing Model
====================================

Architecture: RUPI Factory Controller (1980)
Remote Universal Peripheral Interface for industrial automation.

Features:
  - 8-bit data bus
  - 6 MHz clock
  - ~20,000 transistors (NMOS)
  - SDLC/HDLC serial protocol engine
  - Based on MCS-48 core with serial extensions

Target CPI: 3.5
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


class I8044Model:
    """
    Intel 8044 Grey-Box Queueing Model

    RUPI factory controller (1980)
    - 8-bit architecture (MCS-48 based)
    - 6 MHz clock
    - Integrated SDLC/HDLC serial protocol engine
    - Designed for industrial BITBUS networks
    """

    name = "Intel 8044"
    manufacturer = "Intel"
    year = 1980
    clock_mhz = 6.0
    transistor_count = 20000
    data_width = 8
    address_width = 16

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.0, 0, "Basic ALU operations - 2 cycles"),
            'data_transfer': InstructionCategory('data_transfer', 3.0, 0, "Data move operations - 3 cycles"),
            'serial_io': InstructionCategory('serial_io', 6.0, 0, "Serial I/O protocol handling - 6 cycles"),
            'control': InstructionCategory('control', 3.0, 0, "Branch/call operations - 3 cycles"),
            'protocol': InstructionCategory('protocol', 5.0, 0, "SDLC/HDLC protocol processing - 5 cycles"),
        }

        # Typical: 0.25*2 + 0.25*3 + 0.15*6 + 0.20*3 + 0.15*5 = 0.50+0.75+0.90+0.60+0.75 = 3.50
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'serial_io': 0.15,
                'control': 0.20,
                'protocol': 0.15,
            }, "Typical factory communication workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.30,
                'serial_io': 0.05,
                'control': 0.15,
                'protocol': 0.10,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'serial_io': 0.30,
                'control': 0.10,
                'protocol': 0.25,
            }, "Heavy serial/protocol workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.20,
                'serial_io': 0.10,
                'control': 0.40,
                'protocol': 0.10,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'serial_io': 0.20,
                'control': 0.15,
                'protocol': 0.15,
            }, "Mixed communication workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

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
            bottleneck="sequential",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
