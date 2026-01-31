#!/usr/bin/env python3
"""
Weitek 1064/1065 Grey-Box Queueing Model
===========================================

Architecture: 32-bit (1985)
Queueing Model: Sequential execution

Features:
  - FPU pair
  - Pipelined FP
  - Cray/workstation

Date: 2026-01-29
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
            ipc = 1.0 / cpi
            ips = clock_mhz * 1e6 * ipc
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                       base_cpi=base_cpi if base_cpi is not None else cpi,
                       correction_delta=correction_delta)

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

class Weitek1064Model(BaseProcessorModel):
    """Weitek 1064/1065 - High-speed FPU pair for workstations and Cray"""

    name = "Weitek 1064/1065"
    manufacturer = "Weitek"
    year = 1985
    clock_mhz = 15.0
    transistor_count = 40000
    data_width = 32
    address_width = 32

    def __init__(self):
        self.instruction_categories = {
            'fp_add': InstructionCategory('fp_add', 2.5, 0, "FP add @2-3c"),
            'fp_mul': InstructionCategory('fp_mul', 3.0, 0, "FP mul @3c"),
            'fp_div': InstructionCategory('fp_div', 4.0, 0, "FP div @3-5c"),
            'data_transfer': InstructionCategory('data_transfer', 2.5, 0, "Bus transfer @2-3c"),
        }
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'fp_add': 0.32,
                'fp_mul': 0.03,
                'fp_div': 0.319,
                'data_transfer': 0.331,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'fp_add': 0.39,
                'fp_mul': 0.06,
                'fp_div': 0.286,
                'data_transfer': 0.264,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'fp_add': 0.352,
                'fp_mul': 0.015,
                'fp_div': 0.296,
                'data_transfer': 0.337,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'fp_add': 0.312,
                'fp_mul': 0.005,
                'fp_div': 0.276,
                'data_transfer': 0.407,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'data_transfer': -1.1761065074335888,
            'fp_add': 2.715558128198878,
            'fp_div': -0.25227029003167856,
            'fp_mul': -13.090437484767255,
        }

    def analyze(self, workload='typical'):
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        base_cpi = sum(
            profile.category_weights[c] * self.instruction_categories[c].total_cycles
            for c in profile.category_weights
        )
        contributions = {c: profile.category_weights[c] * self.instruction_categories[c].total_cycles
                         for c in profile.category_weights}
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta
        bottleneck = max(contributions, key=contributions.get)
        return AnalysisResult.from_cpi(
            self.name, workload, corrected_cpi, self.clock_mhz, bottleneck, contributions,
            base_cpi=base_cpi, correction_delta=correction_delta
        )

    def validate(self):
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles
