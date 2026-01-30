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


class WD2010Model(BaseProcessorModel):
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
        self.corrections = {
            'command': 0.876274,
            'data_transfer': 3.246762,
            'error_check': -1.317994,
            'format': -1.105680,
            'seek': -3.077017
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
