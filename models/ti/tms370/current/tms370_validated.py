#!/usr/bin/env python3
"""
TI TMS370 Grey-Box Queueing Model
====================================

Architecture: Industrial MCU (1985)
Texas Instruments 8-bit industrial microcontroller.

Features:
  - 8-bit data bus
  - 8 MHz clock
  - ~30,000 transistors (CMOS)
  - Rich peripheral set for industrial control
  - Register-file based architecture

Target CPI: 3.0
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


class TMS370Model(BaseProcessorModel):
    """
    TI TMS370 Grey-Box Queueing Model

    Industrial MCU (1985)
    - 8-bit architecture
    - 8 MHz clock
    - Rich peripheral integration
    - Register-file based for efficient operation
    """

    name = "TI TMS370"
    manufacturer = "Texas Instruments"
    year = 1985
    clock_mhz = 8.0
    transistor_count = 30000
    data_width = 8
    address_width = 16

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.0, 0, "Register-to-register ALU - 2 cycles"),
            'data_transfer': InstructionCategory('data_transfer', 3.0, 0, "Data move operations - 3 cycles"),
            'memory': InstructionCategory('memory', 4.0, 0, "Memory access operations - 4 cycles"),
            'control': InstructionCategory('control', 3.0, 0, "Branch/call operations - 3 cycles"),
            'peripheral': InstructionCategory('peripheral', 5.0, 0, "Peripheral register access - 5 cycles"),
        }

        # Typical: 0.30*2 + 0.25*3 + 0.10*4 + 0.25*3 + 0.10*5 = 0.60+0.75+0.40+0.75+0.50 = 3.00
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.25,
                'memory': 0.10,
                'control': 0.25,
                'peripheral': 0.10,
            }, "Typical industrial control workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.50,
                'data_transfer': 0.25,
                'memory': 0.05,
                'control': 0.15,
                'peripheral': 0.05,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.35,
                'control': 0.10,
                'peripheral': 0.20,
            }, "Memory and peripheral intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.15,
                'memory': 0.10,
                'control': 0.45,
                'peripheral': 0.10,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.20,
                'peripheral': 0.15,
            }, "Mixed industrial workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 1.000000,
            'control': -0.000000,
            'data_transfer': -0.000000,
            'memory': -1.000000,
            'peripheral': -2.000000
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        total_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            total_cpi += weight * cat.total_cycles

        # System identification: apply correction terms
        base_cpi = total_cpi
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
