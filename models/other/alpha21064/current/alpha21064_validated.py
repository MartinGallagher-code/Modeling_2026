#!/usr/bin/env python3
"""
DEC Alpha 21064 Grey-Box Queueing Model
========================================

64-bit superscalar RISC processor (1992)
- 2-way superscalar
- 7-stage pipeline
- 8KB I-cache, 8KB D-cache
- Target CPI: 1.0 (IPC ~1.0)
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


class Alpha21064Model(BaseProcessorModel):
    """
    DEC Alpha 21064 - First 64-bit RISC superscalar
    Target CPI: 1.0
    """

    name = "DEC Alpha 21064"
    manufacturer = "DEC"
    year = 1992
    clock_mhz = 150.0
    transistor_count = 1680000
    data_width = 64
    address_width = 64

    def __init__(self):
        # Superscalar RISC - calibrated for CPI 0.77 (IPC ~1.3)
        # 0.50*0.5 + 0.20*1.0 + 0.12*0.8 + 0.15*1.0 + 0.02*2.5 + 0.01*6.0 = 0.77
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 0.50, 0, "ALU ops (dual-issue)"),
            'load': InstructionCategory('load', 1.00, 0, "Load (cache hits)"),
            'store': InstructionCategory('store', 0.80, 0, "Store"),
            'branch': InstructionCategory('branch', 1.00, 0, "Branch (predicted)"),
            'multiply': InstructionCategory('multiply', 2.5, 0, "Integer multiply"),
            'divide': InstructionCategory('divide', 6.0, 0, "Integer divide"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.50, 'load': 0.20, 'store': 0.12,
                'branch': 0.15, 'multiply': 0.02, 'divide': 0.01,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.60, 'load': 0.14, 'store': 0.08,
                'branch': 0.12, 'multiply': 0.04, 'divide': 0.02,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.30, 'load': 0.35, 'store': 0.20,
                'branch': 0.10, 'multiply': 0.03, 'divide': 0.02,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.40, 'load': 0.15, 'store': 0.10,
                'branch': 0.30, 'multiply': 0.03, 'divide': 0.02,
            }, "Control-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.48, 'load': 0.22, 'store': 0.13,
                'branch': 0.12, 'multiply': 0.03, 'divide': 0.02,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -0.102734,
            'branch': 0.374239,
            'divide': -4.792678,
            'load': 0.659811,
            'multiply': -3.396953,
            'store': -0.473877
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
