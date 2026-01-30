#!/usr/bin/env python3
"""
Western Digital WD2010 Grey-Box Queueing Model
================================================

Architecture: Hard Disk Controller (1983)
Winchester disk controller for ST-506/ST-412 interfaces.

Features:
  - 8-bit data bus
  - 5 MHz clock
  - ~15,000 transistors (NMOS)
  - ST-506/ST-412 hard disk interface
  - Hardware seek, format, and error checking
  - Used in IBM PC/XT and compatibles

Target CPI: 5.0
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
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                   base_cpi=base_cpi if base_cpi is not None else cpi,
                   correction_delta=correction_delta)


class WD2010Model:
    """
    Western Digital WD2010 Grey-Box Queueing Model

    Hard disk controller (1983)
    - 8-bit interface
    - 5 MHz clock
    - ST-506/ST-412 Winchester disk interface
    - Hardware seek, format, error correction
    """

    name = "Western Digital WD2010"
    manufacturer = "Western Digital"
    year = 1983
    clock_mhz = 5.0
    transistor_count = 15000
    data_width = 8
    address_width = 8

    def __init__(self):
        self.instruction_categories = {
            'command': InstructionCategory('command', 4.0, 0, "Command decode and dispatch - 4 cycles"),
            'data_transfer': InstructionCategory('data_transfer', 3.0, 0, "Sector data transfer - 3 cycles"),
            'seek': InstructionCategory('seek', 8.0, 0, "Head seek operations - 8 cycles"),
            'format': InstructionCategory('format', 10.0, 0, "Track format operations - 10 cycles"),
            'error_check': InstructionCategory('error_check', 5.0, 0, "ECC error checking - 5 cycles"),
        }

        # Typical: 0.30*4 + 0.20*3 + 0.15*8 + 0.05*10 + 0.30*5 = 1.20+0.60+1.20+0.50+1.50 = 5.00
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'command': 0.30,
                'data_transfer': 0.20,
                'seek': 0.15,
                'format': 0.05,
                'error_check': 0.30,
            }, "Typical disk I/O workload"),
            'compute': WorkloadProfile('compute', {
                'command': 0.25,
                'data_transfer': 0.15,
                'seek': 0.10,
                'format': 0.05,
                'error_check': 0.45,
            }, "Heavy error checking"),
            'memory': WorkloadProfile('memory', {
                'command': 0.15,
                'data_transfer': 0.45,
                'seek': 0.10,
                'format': 0.05,
                'error_check': 0.25,
            }, "Bulk data transfer"),
            'control': WorkloadProfile('control', {
                'command': 0.35,
                'data_transfer': 0.10,
                'seek': 0.30,
                'format': 0.10,
                'error_check': 0.15,
            }, "Seek-intensive random access"),
            'mixed': WorkloadProfile('mixed', {
                'command': 0.25,
                'data_transfer': 0.25,
                'seek': 0.20,
                'format': 0.05,
                'error_check': 0.25,
            }, "Mixed disk workload"),
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
