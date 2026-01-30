#!/usr/bin/env python3
"""
Western Digital WD16 Grey-Box Queueing Model
=============================================

Target CPI: 5.0 (LSI-11 compatible, 1977)
Architecture: DEC PDP-11 compatible microprocessor

The WD16 was Western Digital's LSI-11 compatible processor,
offering PDP-11 instruction set compatibility in a single chip.
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


class Wd16Model(BaseProcessorModel):
    """
    Western Digital WD16 Grey-Box Queueing Model

    Target CPI: 5.0
    Calibration: Weighted sum of instruction cycles
    """

    name = "WD16"
    manufacturer = "Western Digital"
    year = 1977
    clock_mhz = 3.3

    def __init__(self):
        # Calibrated cycles to achieve CPI = 5.0
        # PDP-11 compatible architecture
        # Calculation: 0.25*3 + 0.18*5 + 0.15*6 + 0.12*6 + 0.10*5 + 0.08*6 + 0.07*5 + 0.05*8 = 4.91
        self.instruction_categories = {
            'register_ops': InstructionCategory('register_ops', 3.0, 0, "Register-to-register"),
            'immediate': InstructionCategory('immediate', 5.0, 0, "Immediate operand"),
            'memory_read': InstructionCategory('memory_read', 6.0, 0, "Load from memory"),
            'memory_write': InstructionCategory('memory_write', 6.0, 0, "Store to memory"),
            'branch': InstructionCategory('branch', 5.0, 0, "Branch/conditional"),
            'jsr': InstructionCategory('jsr', 6.0, 0, "Subroutine call/return"),
            'byte': InstructionCategory('byte', 5.0, 0, "Byte operations"),
            'trap': InstructionCategory('trap', 8.0, 0, "Trap/interrupt"),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'register_ops': 0.25,
                'immediate': 0.18,
                'memory_read': 0.15,
                'memory_write': 0.12,
                'branch': 0.10,
                'jsr': 0.08,
                'byte': 0.07,
                'trap': 0.05,
            }, "Typical embedded workload"),
            'compute': WorkloadProfile('compute', {
                'register_ops': 0.40,
                'immediate': 0.25,
                'memory_read': 0.10,
                'memory_write': 0.08,
                'branch': 0.08,
                'jsr': 0.04,
                'byte': 0.03,
                'trap': 0.02,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'register_ops': 0.15,
                'immediate': 0.10,
                'memory_read': 0.32,
                'memory_write': 0.25,
                'branch': 0.06,
                'jsr': 0.05,
                'byte': 0.05,
                'trap': 0.02,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'register_ops': 0.18,
                'immediate': 0.12,
                'memory_read': 0.12,
                'memory_write': 0.08,
                'branch': 0.22,
                'jsr': 0.18,
                'byte': 0.05,
                'trap': 0.05,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'register_ops': 0.28,
                'immediate': 0.18,
                'memory_read': 0.16,
                'memory_write': 0.12,
                'branch': 0.10,
                'jsr': 0.07,
                'byte': 0.06,
                'trap': 0.03,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'branch': 0.124169,
            'byte': -1.453353,
            'immediate': 0.533046,
            'jsr': 1.093407,
            'memory_read': -0.237952,
            'memory_write': 0.242948,
            'register_ops': 0.553514,
            'trap': -4.518852
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
