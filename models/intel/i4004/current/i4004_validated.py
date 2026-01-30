#!/usr/bin/env python3
"""
Intel 4004 Grey-Box Queueing Model
==================================

Architecture: Sequential Execution (1971)
The world's first commercial microprocessor.

Features:
  - 4-bit data bus
  - Sequential instruction execution
  - 8-16 cycles per instruction
  - 740 kHz clock

Target CPI: 10.8 (based on datasheet timing)
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


class I4004Model(BaseProcessorModel):
    """
    Intel 4004 Grey-Box Queueing Model

    First commercial microprocessor (1971)
    - 4-bit architecture
    - All instructions 8 or 16 cycles (1 or 2 machine cycles)
    - Sequential execution only
    """

    name = "Intel 4004"
    manufacturer = "Intel"
    year = 1971
    clock_mhz = 0.74
    transistor_count = 2300
    data_width = 4
    address_width = 12

    def __init__(self):
        # Instruction categories from datasheet
        # 1 machine cycle = 8 clock cycles (10.8 µs at 740 kHz)
        # 2 machine cycles = 16 clock cycles
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 10.0, 0, "ADD/SUB @10 cycles"),
            'data_transfer': InstructionCategory('data_transfer', 8.0, 0, "LD/XCH @8 cycles"),
            'control': InstructionCategory('control', 16.0, 0, "JUN/JCN/FIM avg ~16"),
            'memory': InstructionCategory('memory', 8.0, 0, "Memory ops @8"),
        }

        # Workload profiles based on validation JSON instruction mix
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.35,
                'control': 0.25,
                'memory': 0.10,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.50,
                'data_transfer': 0.25,
                'control': 0.15,
                'memory': 0.10,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.20,
                'data_transfer': 0.30,
                'control': 0.20,
                'memory': 0.30,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.25,
                'control': 0.45,
                'memory': 0.10,
            }, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.30,
                'data_transfer': 0.30,
                'control': 0.25,
                'memory': 0.15,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.800000,
            'control': -5.200000,
            'data_transfer': 2.800000,
            'memory': 2.800000
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Simple weighted CPI
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
