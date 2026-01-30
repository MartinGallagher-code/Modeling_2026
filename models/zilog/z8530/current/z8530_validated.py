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
from typing import Dict, List, Any, Optional

try:
    from common.base_model import BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult
except ImportError:
    from dataclasses import dataclass

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

    class BaseProcessorModel:
        def get_corrections(self):
            return getattr(self, 'corrections', {})
        def set_corrections(self, corrections):
            self.corrections = corrections
        def compute_correction_delta(self, workload='typical'):
            profile = self.workload_profiles.get(workload, list(self.workload_profiles.values())[0])
            return sum(self.corrections.get(c, 0) * profile.category_weights.get(c, 0) for c in self.corrections)
        def compute_residuals(self, measured_cpi_dict):
            return {w: self.analyze(w).cpi - m for w, m in measured_cpi_dict.items()}
        def compute_loss(self, measured_cpi_dict):
            residuals = self.compute_residuals(measured_cpi_dict)
            return sum(r**2 for r in residuals.values()) / len(residuals) if residuals else 0
        def get_parameters(self):
            params = {}
            for c, cat in self.instruction_categories.items():
                params[f'cat.{c}.base_cycles'] = cat.base_cycles
            for c, v in self.corrections.items():
                params[f'cor.{c}'] = v
            return params
        def set_parameters(self, params):
            for k, v in params.items():
                if k.startswith('cat.') and k.endswith('.base_cycles'):
                    c = k[4:-12]
                    if c in self.instruction_categories:
                        self.instruction_categories[c].base_cycles = v
                elif k.startswith('cor.'):
                    c = k[4:]
                    self.corrections[c] = v
        def get_parameter_bounds(self):
            bounds = {}
            for c, cat in self.instruction_categories.items():
                bounds[f'cat.{c}.base_cycles'] = (0.1, cat.base_cycles * 5)
            for c in self.corrections:
                bounds[f'cor.{c}'] = (-50, 50)
            return bounds
        def get_parameter_metadata(self):
            return {k: {'type': 'category' if k.startswith('cat.') else 'correction'} for k in self.get_parameters()}
        def get_instruction_categories(self):
            return self.instruction_categories
        def get_workload_profiles(self):
            return self.workload_profiles
        def validate(self):
            return {'tests': [], 'passed': 0, 'total': 0, 'accuracy_percent': None}


class Z8530Model(BaseProcessorModel):
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
        self.corrections = {
            'control': -2.437039,
            'crc': 2.167891,
            'dma': -0.239507,
            'frame_process': -1.646904,
            'register_io': 2.155559
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
