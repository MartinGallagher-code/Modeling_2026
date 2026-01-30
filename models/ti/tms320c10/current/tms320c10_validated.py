#!/usr/bin/env python3
"""
TI TMS320C10 Grey-Box Queueing Model
=====================================

Target CPI: 1.5 (DSP, 1983)
Architecture: Digital Signal Processor

The TMS320C10 was the first low-cost DSP, designed
for efficient signal processing with single-cycle
multiply-accumulate operations.
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


class Tms320C10Model(BaseProcessorModel):
    """
    TI TMS320C10 Grey-Box Queueing Model

    Target CPI: 1.5
    Calibration: Weighted sum of instruction cycles
    """

    name = "TMS320C10"
    manufacturer = "Texas Instruments"
    year = 1983
    clock_mhz = 20.0

    def __init__(self):
        # Calibrated cycles to achieve CPI = 1.5
        # DSP: efficient single-cycle MAC, some multi-cycle ops
        # Calculation: 0.45*1 + 0.25*2 + 0.15*2 + 0.10*2 + 0.05*2 = 1.5
        self.instruction_categories = {
            'mac': InstructionCategory('mac', 1.0, 0, "Multiply-accumulate"),
            'alu': InstructionCategory('alu', 2.0, 0, "ALU operations"),
            'memory': InstructionCategory('memory', 1.0, 1.0, "Memory access"),
            'branch': InstructionCategory('branch', 2.0, 0, "Branch/jump"),
            'control': InstructionCategory('control', 2.0, 0, "Control instructions"),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'mac': 0.45,
                'alu': 0.25,
                'memory': 0.15,
                'branch': 0.10,
                'control': 0.05,
            }, "Typical DSP workload"),
            'compute': WorkloadProfile('compute', {
                'mac': 0.60,
                'alu': 0.22,
                'memory': 0.08,
                'branch': 0.07,
                'control': 0.03,
            }, "Compute-intensive DSP workload"),
            'memory': WorkloadProfile('memory', {
                'mac': 0.30,
                'alu': 0.15,
                'memory': 0.40,
                'branch': 0.10,
                'control': 0.05,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'mac': 0.30,
                'alu': 0.18,
                'memory': 0.15,
                'branch': 0.25,
                'control': 0.12,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'mac': 0.42,
                'alu': 0.23,
                'memory': 0.18,
                'branch': 0.12,
                'control': 0.05,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -0.503829,
            'branch': -0.532219,
            'control': -0.430986,
            'mac': 0.501774,
            'memory': -0.500467
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        total_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            total_cpi += contrib
            contributions[cat_name] = contrib
        bottleneck = max(contributions, key=contributions.get)
        # System identification: apply correction terms
        base_cpi = total_cpi
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

        return AnalysisResult.from_cpi(
            processor=self.name, workload=workload, cpi=corrected_cpi,
            clock_mhz=self.clock_mhz, bottleneck=bottleneck, utilizations=contributions,
            base_cpi=base_cpi, correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles
