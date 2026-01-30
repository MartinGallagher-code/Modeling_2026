#!/usr/bin/env python3
"""
Sega 315-5313 VDP Grey-Box Queueing Model
=========================================

Architecture: Genesis/Mega Drive video, dual playfields
Year: 1988, Clock: 13.42 MHz

Target CPI: 3.0
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


class Sega3155313Model:
    """
    Sega 315-5313 VDP Grey-Box Queueing Model

    Genesis/Mega Drive video, dual playfields (1988)
    - Dual playfields
    - 80 sprites
    - DMA transfers
    """

    name = "Sega 315-5313 VDP"
    manufacturer = "Sega/Yamaha"
    year = 1988
    clock_mhz = 13.42
    transistor_count = 120000
    data_width = 16
    address_width = 16

    def __init__(self):
        self.instruction_categories = {
            'draw': InstructionCategory('draw', 3.0, 0, "Drawing command"),
            'pixel': InstructionCategory('pixel', 2.0, 0, "Pixel operation"),
            'register': InstructionCategory('register', 1.0, 0, "Register access"),
            'memory': InstructionCategory('memory', 3.0, 0, "Memory transfer"),
            'branch': InstructionCategory('branch', 4.0, 0, "Flow control"),
            'blit': InstructionCategory('blit', 2.0, 0, "Block transfer"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'draw': 0.25,
                'pixel': 0.3,
                'register': 0.1,
                'memory': 0.2,
                'branch': 0.05,
                'blit': 0.1,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'draw': 0.35,
                'pixel': 0.3,
                'register': 0.05,
                'memory': 0.15,
                'branch': 0.05,
                'blit': 0.1,
            }, "Compute workload"),
            'memory': WorkloadProfile('memory', {
                'draw': 0.15,
                'pixel': 0.2,
                'register': 0.1,
                'memory': 0.35,
                'branch': 0.05,
                'blit': 0.15,
            }, "Memory workload"),
            'control': WorkloadProfile('control', {
                'draw': 0.2,
                'pixel': 0.2,
                'register': 0.15,
                'memory': 0.15,
                'branch': 0.2,
                'blit': 0.1,
            }, "Control workload"),
            'mixed': WorkloadProfile('mixed', {
                'draw': 0.25,
                'pixel': 0.25,
                'register': 0.1,
                'memory': 0.2,
                'branch': 0.1,
                'blit': 0.1,
            }, "Mixed workload"),
        }

        self.corrections = {
            'draw': 0.550000,
            'pixel': 0.550000,
            'register': 0.550000,
            'memory': 0.550000,
            'branch': 0.550000,
            'blit': 0.550000,
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
            bottleneck="sprite_engine",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi, correction_delta=correction_delta
        )
