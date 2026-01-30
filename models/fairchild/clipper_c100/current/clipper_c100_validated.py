#!/usr/bin/env python3
"""
Fairchild Clipper C100 Grey-Box Queueing Model
================================================

Target CPI: 1.5 (32-bit RISC, 1985)
Architecture: RISC with separate I/D caches
Clock: 33 MHz, ~132,000 transistors

The Clipper C100 was Fairchild's RISC processor featuring
separate instruction and data caches, a load/store architecture,
and pipelined execution for high throughput.
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
    def total_cycles(self):
        return self.base_cycles + self.memory_cycles


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


class ClipperC100Model(BaseProcessorModel):
    """
    Fairchild Clipper C100 Grey-Box Queueing Model

    Target CPI: 1.5
    Calibration: Weighted sum of instruction cycles
    """

    name = "Clipper C100"
    manufacturer = "Fairchild"
    year = 1985
    clock_mhz = 33.0

    def __init__(self):
        # Calibrated cycles to achieve CPI = 1.5
        # RISC architecture with pipelined execution
        # Typical: 0.40*1 + 0.20*2 + 0.175*1 + 0.15*2 + 0.075*3
        #        = 0.40 + 0.40 + 0.175 + 0.30 + 0.225 = 1.50
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "ALU register operations"),
            'load': InstructionCategory('load', 2.0, 0, "Load from memory/cache"),
            'store': InstructionCategory('store', 1.0, 0, "Store to memory/cache"),
            'branch': InstructionCategory('branch', 2.0, 0, "Branch/jump"),
            'float': InstructionCategory('float', 3.0, 0, "Floating-point operations"),
        }

        # Workload profiles - weights sum to 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.400,
                'load': 0.200,
                'store': 0.175,
                'branch': 0.150,
                'float': 0.075,
            }, "Typical RISC workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'load': 0.10,
                'store': 0.08,
                'branch': 0.12,
                'float': 0.25,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.20,
                'load': 0.35,
                'store': 0.25,
                'branch': 0.10,
                'float': 0.10,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.30,
                'load': 0.12,
                'store': 0.08,
                'branch': 0.40,
                'float': 0.10,
            }, "Control-flow intensive workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

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


def validate():
    model = ClipperC100Model()
    results = {}
    for workload in ['typical', 'compute', 'memory', 'control']:
        result = model.analyze(workload)
        results[workload] = {
            'cpi': result.cpi,
            'ipc': result.ipc,
            'ips': result.ips,
            'bottleneck': result.bottleneck,
        }
    return results


if __name__ == '__main__':
    model = ClipperC100Model()
    print(f"=== {model.name} ({model.year}) ===")
    print(f"Clock: {model.clock_mhz} MHz")
    print()
    for workload in ['typical', 'compute', 'memory', 'control']:
        result = model.analyze(workload)
        print(f"{workload:10s}: CPI={result.cpi:.3f}  IPC={result.ipc:.3f}  "
              f"IPS={result.ips:,.0f}  Bottleneck={result.bottleneck}")
