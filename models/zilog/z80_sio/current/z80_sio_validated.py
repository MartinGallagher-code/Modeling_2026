#!/usr/bin/env python3
"""
Zilog Z80-SIO Grey-Box Queueing Model
=======================================

Architecture: Serial I/O Controller (1977)
Dual-channel serial I/O for Z80 systems.

Features:
  - 8-bit data bus
  - 4 MHz clock
  - ~8,000 transistors (NMOS)
  - Dual async/sync serial channels
  - Interrupt-driven operation
  - Z80 bus compatible

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


class Z80SIOModel:
    """
    Zilog Z80-SIO Grey-Box Queueing Model

    Serial I/O controller (1977)
    - 8-bit interface
    - 4 MHz clock
    - Dual async/sync serial channels
    - Z80 bus and interrupt compatible
    """

    name = "Zilog Z80-SIO"
    manufacturer = "Zilog"
    year = 1977
    clock_mhz = 4.0
    transistor_count = 8000
    data_width = 8
    address_width = 8

    def __init__(self):
        self.instruction_categories = {
            'register_io': InstructionCategory('register_io', 2.0, 0, "Register read/write - 2 cycles"),
            'char_process': InstructionCategory('char_process', 4.0, 0, "Character processing - 4 cycles"),
            'sync': InstructionCategory('sync', 5.0, 0, "Sync pattern detection - 5 cycles"),
            'control': InstructionCategory('control', 3.0, 0, "Mode/command processing - 3 cycles"),
            'interrupt': InstructionCategory('interrupt', 4.0, 0, "Interrupt handling - 4 cycles"),
        }

        # Typical: 0.25*2 + 0.25*4 + 0.15*5 + 0.15*3 + 0.20*4 = 0.50+1.00+0.75+0.45+0.80 = 3.50
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'register_io': 0.25,
                'char_process': 0.25,
                'sync': 0.15,
                'control': 0.15,
                'interrupt': 0.20,
            }, "Typical serial I/O workload"),
            'compute': WorkloadProfile('compute', {
                'register_io': 0.15,
                'char_process': 0.40,
                'sync': 0.20,
                'control': 0.10,
                'interrupt': 0.15,
            }, "Heavy character processing"),
            'memory': WorkloadProfile('memory', {
                'register_io': 0.35,
                'char_process': 0.20,
                'sync': 0.10,
                'control': 0.10,
                'interrupt': 0.25,
            }, "Register polling intensive"),
            'control': WorkloadProfile('control', {
                'register_io': 0.20,
                'char_process': 0.15,
                'sync': 0.10,
                'control': 0.40,
                'interrupt': 0.15,
            }, "Control/configuration intensive"),
            'mixed': WorkloadProfile('mixed', {
                'register_io': 0.20,
                'char_process': 0.25,
                'sync': 0.20,
                'control': 0.15,
                'interrupt': 0.20,
            }, "Mixed serial workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'char_process': -1.299719,
            'control': -0.921619,
            'interrupt': 4.999376,
            'register_io': -3.738368,
            'sync': 2.622081
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
            bottleneck="sequential",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi,
            correction_delta=correction_delta
        )
