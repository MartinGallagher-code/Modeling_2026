#!/usr/bin/env python3
"""
ARM1 Grey-Box Queueing Model
=============================

First ARM processor (1985)
- 3-stage pipeline
- No cache
- Target CPI: 1.8
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


class Arm1Model(BaseProcessorModel):
    """
    ARM1 - First ARM Processor
    Target CPI: 1.8
    """

    name = "ARM1"
    manufacturer = "Acorn"
    year = 1985
    clock_mhz = 8.0
    transistor_count = 25000
    data_width = 32
    address_width = 26

    def __init__(self):
        # ARM1: 3-stage pipeline, calibrated for CPI 1.8
        # 0.52*1.0 + 0.20*2.8 + 0.12*2.2 + 0.16*3.3 = 0.52 + 0.56 + 0.264 + 0.528 = 1.87
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "Data processing"),
            'load': InstructionCategory('load', 2.8, 0, "LDR"),
            'store': InstructionCategory('store', 2.2, 0, "STR"),
            'branch': InstructionCategory('branch', 3.2, 0, "Branch"),
            'multiply': InstructionCategory('multiply', 3.0, 0, "Multiply/complex ALU"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.47, 'load': 0.20, 'store': 0.12, 'branch': 0.16,
                'multiply': 0.05,}, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.54, 'load': 0.14, 'store': 0.10, 'branch': 0.14,
                'multiply': 0.08,}, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.29, 'load': 0.32, 'store': 0.22, 'branch': 0.14,
                'multiply': 0.03,}, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.4, 'load': 0.15, 'store': 0.10, 'branch': 0.33,
                'multiply': 0.02,}, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.46, 'load': 0.22, 'store': 0.13, 'branch': 0.15,
                'multiply': 0.04,}, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -0.8630500000000011,
            'branch': 0.2044499999999991,
            'load': 6.124450000000002,
            'multiply': 0.7819500000000046,
            'store': -8.725550000000002,
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        base_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            base_cpi += contrib
            contributions[cat_name] = contrib

        # Apply correction terms (system identification)
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

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

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles
