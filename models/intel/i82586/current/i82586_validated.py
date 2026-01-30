#!/usr/bin/env python3
"""
Intel 82586 Grey-Box Queueing Model
======================================

Architecture: Ethernet Coprocessor (1983)
IEEE 802.3 Ethernet LAN coprocessor.

Features:
  - 16-bit data bus
  - 8 MHz clock
  - ~30,000 transistors (NMOS)
  - Full IEEE 802.3/Ethernet CSMA/CD
  - Command/status block architecture
  - DMA for frame buffer management

Target CPI: 5.0
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


class I82586Model(BaseProcessorModel):
    """
    Intel 82586 Grey-Box Queueing Model

    Ethernet coprocessor (1983)
    - 16-bit architecture
    - 8 MHz clock
    - IEEE 802.3 Ethernet CSMA/CD
    - Command block and DMA based operation
    """

    name = "Intel 82586"
    manufacturer = "Intel"
    year = 1983
    clock_mhz = 8.0
    transistor_count = 30000
    data_width = 16
    address_width = 24

    def __init__(self):
        self.instruction_categories = {
            'frame_process': InstructionCategory('frame_process', 4.0, 0, "Ethernet frame processing - 4 cycles"),
            'dma': InstructionCategory('dma', 6.0, 0, "DMA buffer management - 6 cycles"),
            'command': InstructionCategory('command', 8.0, 0, "Command block execution - 8 cycles"),
            'status': InstructionCategory('status', 3.0, 0, "Status reporting - 3 cycles"),
            'buffer': InstructionCategory('buffer', 5.0, 0, "Buffer chain management - 5 cycles"),
        }

        # Typical: 0.15*4 + 0.20*6 + 0.15*8 + 0.25*3 + 0.25*5 = 0.60+1.20+1.20+0.75+1.25 = 5.00
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'frame_process': 0.15,
                'dma': 0.20,
                'command': 0.15,
                'status': 0.25,
                'buffer': 0.25,
            }, "Typical Ethernet workload"),
            'compute': WorkloadProfile('compute', {
                'frame_process': 0.35,
                'dma': 0.15,
                'command': 0.20,
                'status': 0.15,
                'buffer': 0.15,
            }, "Heavy frame processing"),
            'memory': WorkloadProfile('memory', {
                'frame_process': 0.10,
                'dma': 0.40,
                'command': 0.05,
                'status': 0.10,
                'buffer': 0.35,
            }, "DMA/buffer heavy"),
            'control': WorkloadProfile('control', {
                'frame_process': 0.10,
                'dma': 0.10,
                'command': 0.40,
                'status': 0.25,
                'buffer': 0.15,
            }, "Command-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'frame_process': 0.20,
                'dma': 0.20,
                'command': 0.15,
                'status': 0.20,
                'buffer': 0.25,
            }, "Mixed network workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'buffer': -2.095455,
            'command': -2.004545,
            'dma': 0.904545,
            'frame_process': 0.359091,
            'status': 2.359091
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
            bottleneck="sequential",
            utilizations={cat: profile.category_weights[cat] for cat in self.instruction_categories},
            base_cpi=base_cpi,
            correction_delta=correction_delta
        )
