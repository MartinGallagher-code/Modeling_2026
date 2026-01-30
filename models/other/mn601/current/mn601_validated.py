#!/usr/bin/env python3
"""
Data General mN601 Grey-Box Queueing Model
===========================================

Target CPI: 4.0 (microNova architecture, 1977)
Architecture: Single-chip Nova minicomputer

The mN601 (microNova) was a single-chip implementation of Data General's
Nova minicomputer architecture, offering good performance for its time.
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


class Mn601Model(BaseProcessorModel):
    """
    Data General mN601 Grey-Box Queueing Model

    Target CPI: 4.0
    Calibration: Weighted sum of instruction cycles
    """

    name = "MN601"
    manufacturer = "Data General"
    year = 1977
    clock_mhz = 4.0

    def __init__(self):
        # Calibrated cycles to achieve CPI = 4.0
        # Efficient Nova minicomputer architecture
        # Calculation: 0.30*3 + 0.18*5 + 0.15*4 + 0.12*4 + 0.10*5 + 0.08*4 + 0.04*5 + 0.03*6 = 3.98
        self.instruction_categories = {
            'alu_ops': InstructionCategory('alu_ops', 3.0, 0, "ALU operations"),
            'memory_read': InstructionCategory('memory_read', 5.0, 0, "Load from memory"),
            'memory_write': InstructionCategory('memory_write', 4.0, 0, "Store to memory"),
            'jump': InstructionCategory('jump', 4.0, 0, "Jump instructions"),
            'io': InstructionCategory('io', 5.0, 0, "I/O operations"),
            'skip': InstructionCategory('skip', 4.0, 0, "Skip instructions"),
            'shift': InstructionCategory('shift', 5.0, 0, "Shift operations"),
            'stack': InstructionCategory('stack', 6.0, 0, "Stack operations"),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu_ops': 0.30,
                'memory_read': 0.18,
                'memory_write': 0.15,
                'jump': 0.12,
                'io': 0.10,
                'skip': 0.08,
                'shift': 0.04,
                'stack': 0.03,
            }, "Typical embedded workload"),
            'compute': WorkloadProfile('compute', {
                'alu_ops': 0.45,
                'memory_read': 0.15,
                'memory_write': 0.10,
                'jump': 0.10,
                'io': 0.05,
                'skip': 0.08,
                'shift': 0.05,
                'stack': 0.02,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'alu_ops': 0.18,
                'memory_read': 0.35,
                'memory_write': 0.28,
                'jump': 0.08,
                'io': 0.04,
                'skip': 0.03,
                'shift': 0.02,
                'stack': 0.02,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'alu_ops': 0.20,
                'memory_read': 0.12,
                'memory_write': 0.08,
                'jump': 0.25,
                'io': 0.08,
                'skip': 0.18,
                'shift': 0.04,
                'stack': 0.05,
            }, "Control-flow intensive workload"),
            'mixed': WorkloadProfile('mixed', {
                'alu_ops': 0.32,
                'memory_read': 0.20,
                'memory_write': 0.14,
                'jump': 0.12,
                'io': 0.08,
                'skip': 0.07,
                'shift': 0.04,
                'stack': 0.03,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu_ops': 0.872034,
            'io': -1.205959,
            'jump': 0.896513,
            'memory_read': -0.372233,
            'memory_write': -0.875174,
            'shift': 0.666506,
            'skip': -1.265856,
            'stack': -2.523655
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
