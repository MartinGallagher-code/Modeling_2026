#!/usr/bin/env python3
"""
Zilog Z8530 SCC Grey-Box Queueing Model
=========================================

Architecture: Serial Communications Controller (1981)
Dual-channel serial controller supporting multiple protocols.

Features:
  - 8-bit data bus
  - 6 MHz clock
  - ~15,000 transistors (NMOS)
  - Dual HDLC/SDLC/async serial channels
  - CRC generation/checking hardware
  - DMA support

Target CPI: 4.0
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


class Z8530Model:
    """
    Zilog Z8530 SCC Grey-Box Queueing Model

    Serial Communications Controller (1981)
    - 8-bit interface
    - 6 MHz clock
    - Dual-channel HDLC/SDLC/async serial
    - Hardware CRC and DMA support
    """

    name = "Zilog Z8530 SCC"
    manufacturer = "Zilog"
    year = 1981
    clock_mhz = 6.0
    transistor_count = 15000
    data_width = 8
    address_width = 8

    def __init__(self):
        self.instruction_categories = {
            'register_io': InstructionCategory('register_io', 2.0, 0, "Register read/write - 2 cycles"),
            'frame_process': InstructionCategory('frame_process', 6.0, 0, "Frame assembly/disassembly - 6 cycles"),
            'crc': InstructionCategory('crc', 4.0, 0, "CRC generation/checking - 4 cycles"),
            'control': InstructionCategory('control', 3.0, 0, "Command/status processing - 3 cycles"),
            'dma': InstructionCategory('dma', 5.0, 0, "DMA transfer operations - 5 cycles"),
        }

        # Typical: 0.20*2 + 0.20*6 + 0.20*4 + 0.20*3 + 0.20*5 = 0.40+1.20+0.80+0.60+1.00 = 4.00
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'register_io': 0.20,
                'frame_process': 0.20,
                'crc': 0.20,
                'control': 0.20,
                'dma': 0.20,
            }, "Typical serial communication workload"),
            'compute': WorkloadProfile('compute', {
                'register_io': 0.15,
                'frame_process': 0.30,
                'crc': 0.30,
                'control': 0.10,
                'dma': 0.15,
            }, "Heavy frame/CRC processing"),
            'memory': WorkloadProfile('memory', {
                'register_io': 0.10,
                'frame_process': 0.15,
                'crc': 0.10,
                'control': 0.15,
                'dma': 0.50,
            }, "DMA-heavy bulk transfer"),
            'control': WorkloadProfile('control', {
                'register_io': 0.30,
                'frame_process': 0.10,
                'crc': 0.10,
                'control': 0.40,
                'dma': 0.10,
            }, "Control/status polling intensive"),
            'mixed': WorkloadProfile('mixed', {
                'register_io': 0.25,
                'frame_process': 0.20,
                'crc': 0.15,
                'control': 0.20,
                'dma': 0.20,
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
            base_cpi=base_cpi,
            correction_delta=correction_delta
        )
