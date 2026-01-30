#!/usr/bin/env python3
"""
Z8000 Grey-Box Queueing Model
==============================

Architecture: 16-bit microprocessor (1979)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - 16-bit data bus, 16-bit address bus (Z8001: segmented, Z8002: non-segmented)
  - General-purpose register set (16 x 16-bit)
  - Regular instruction encoding
  - 3-100+ cycles per instruction (complex ops)

Calibrated: 2026-01-28
Target CPI: ~4.5 for typical workloads
Used in: Olivetti M20, some Unix workstations
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

class Z8000Model(BaseProcessorModel):
    """
    Z8000 Grey-Box Queueing Model

    Architecture: 16-bit NMOS microprocessor (1979)
    - Different architecture from Z80 (not compatible)
    - 16 general-purpose 16-bit registers
    - Regular orthogonal instruction set
    - CPI ~4.5 for typical workloads
    """

    # Processor specifications
    name = "Z8000"
    manufacturer = "Zilog"
    year = 1979
    clock_mhz = 4.0
    transistor_count = 17500
    data_width = 16
    address_width = 16  # Z8002 non-segmented; Z8001 has 23-bit segmented

    def __init__(self):
        # Z8000 instruction timing calibrated to expected CPI 4.5
        # Reference: ADD R,R @4, LD R,R @3, JP @7
        # Fast 16-bit register ops, orthogonal instruction set
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 3.2, 0,
                "ALU ops - ADD/SUB/INC/DEC weighted avg"),
            'data_transfer': InstructionCategory('data_transfer', 2.8, 0,
                "LD R,R @3 cycles - fast 16-bit register moves"),
            'memory': InstructionCategory('memory', 5.0, 0,
                "Memory ops - various addressing modes"),
            'control': InstructionCategory('control', 4.8, 0,
                "JP @7, JR faster, weighted avg"),
            'stack': InstructionCategory('stack', 8.0, 0,
                "PUSH/POP 16-bit registers"),
            'block': InstructionCategory('block', 9.0, 0,
                "Block transfer operations"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.20,
                'control': 0.15,
                'stack': 0.10,
                'block': 0.05,
            }, "Typical Z8000 workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.12,
                'stack': 0.05,
                'block': 0.03,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.35,
                'control': 0.12,
                'stack': 0.08,
                'block': 0.10,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.18,
                'data_transfer': 0.15,
                'memory': 0.15,
                'control': 0.35,
                'stack': 0.12,
                'block': 0.05,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.529863,
            'block': 0.646775,
            'control': 0.175109,
            'data_transfer': -1.304053,
            'memory': 0.303614,
            'stack': 1.042199
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
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

        ipc = 1.0 / corrected_cpi if corrected_cpi > 0 else 0.0
        ips = self.clock_mhz * 1e6 * ipc

        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contributions[cat_name] = weight * cat.total_cycles
        bottleneck = max(contributions, key=contributions.get)

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=corrected_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=contributions,
            base_cpi=base_cpi,
            correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles
