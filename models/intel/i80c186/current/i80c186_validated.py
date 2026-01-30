#!/usr/bin/env python3
"""
Intel 80C186 Grey-Box Queueing Model
=======================================

Architecture: 16-bit (1982)
Queueing Model: Sequential execution

Features:
  - CMOS 80186
  - 8086 superset
  - Integrated peripherals

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
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi if base_cpi is not None else cpi, correction_delta)

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

class I80c186Model(BaseProcessorModel):
    """Intel 80C186 - CMOS embedded 80186, billions in networking"""

    name = "Intel 80C186"
    manufacturer = "Intel"
    year = 1982
    clock_mhz = 8.0
    transistor_count = 55000
    data_width = 16
    address_width = 20

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 3.0, 0, "ALU reg @2-4c"),
            'data_transfer': InstructionCategory('data_transfer', 3.0, 0, "MOV/imm @2-4c"),
            'memory': InstructionCategory('memory', 8.0, 0, "Memory @6-10c"),
            'control': InstructionCategory('control', 10.0, 0, "Branch/call @8-14c"),
            'stack': InstructionCategory('stack', 9.0, 0, "Push/pop @8-10c"),
        }
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.252,
                'data_transfer': 0.251,
                'memory': 0.202,
                'control': 0.134,
                'stack': 0.161,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.352,
                'data_transfer': 0.226,
                'memory': 0.177,
                'control': 0.109,
                'stack': 0.136,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.227,
                'data_transfer': 0.351,
                'memory': 0.177,
                'control': 0.109,
                'stack': 0.136,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.227,
                'data_transfer': 0.226,
                'memory': 0.177,
                'control': 0.234,
                'stack': 0.136,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -3.072426,
            'control': -0.704426,
            'data_transfer': -0.864426,
            'memory': 3.290563,
            'stack': 3.148583
        }

    def analyze(self, workload='typical'):
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        base_cpi = sum(
            profile.category_weights[c] * self.instruction_categories[c].total_cycles
            for c in profile.category_weights
        )
        contributions = {c: profile.category_weights[c] * self.instruction_categories[c].total_cycles
                         for c in profile.category_weights}
        bottleneck = max(contributions, key=contributions.get)
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta
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
