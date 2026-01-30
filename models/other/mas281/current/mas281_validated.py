#!/usr/bin/env python3
"""
Marconi Elliot MAS281 Grey-Box Queueing Model
================================================

Architecture: 16-bit (1979)
Queueing Model: Sequential execution

Features:
  - British military
  - Naval systems
  - Real-time

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
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)

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

class Mas281Model(BaseProcessorModel):
    """Marconi Elliot MAS281 - British military 16-bit for naval systems"""

    name = "Marconi Elliot MAS281"
    manufacturer = "Marconi"
    year = 1979
    clock_mhz = 5.0
    transistor_count = 12000
    data_width = 16
    address_width = 16

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 3.0, 0, "16-bit ALU @2-4c"),
            'data_transfer': InstructionCategory('data_transfer', 3.0, 0, "Transfers @2-4c"),
            'memory': InstructionCategory('memory', 5.5, 0, "Memory @4-7c"),
            'control': InstructionCategory('control', 6.0, 0, "Branch/call @5-8c"),
            'stack': InstructionCategory('stack', 6.0, 0, "Stack @5-7c"),
        }
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.229,
                'data_transfer': 0.23,
                'memory': 0.199,
                'control': 0.171,
                'stack': 0.171,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.329,
                'data_transfer': 0.205,
                'memory': 0.174,
                'control': 0.146,
                'stack': 0.146,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.204,
                'data_transfer': 0.33,
                'memory': 0.174,
                'control': 0.146,
                'stack': 0.146,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.204,
                'data_transfer': 0.205,
                'memory': 0.174,
                'control': 0.271,
                'stack': 0.146,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 1.351815,
            'control': -1.648185,
            'data_transfer': 1.351815,
            'memory': -0.861581,
            'stack': -0.974789
        }

    def analyze(self, workload='typical'):
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        base_cpi = sum(
            profile.category_weights[c] * self.instruction_categories[c].total_cycles
            for c in profile.category_weights
        )
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta
        contributions = {c: profile.category_weights[c] * self.instruction_categories[c].total_cycles
                         for c in profile.category_weights}
        bottleneck = max(contributions, key=contributions.get)
        return AnalysisResult.from_cpi(
            self.name, workload, corrected_cpi, self.clock_mhz, bottleneck, contributions, base_cpi=base_cpi, correction_delta=correction_delta
        )

    def validate(self):
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles
