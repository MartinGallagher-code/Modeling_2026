#!/usr/bin/env python3
"""
TI TMS9985 Grey-Box Queueing Model
=====================================

Architecture: 16-bit (1978)
Queueing Model: Sequential execution

Features:
  - Single-chip TMS9900
  - 256B on-chip RAM

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

class Tms9985Model(BaseProcessorModel):
    """TI TMS9985 - Single-chip TMS9900 with 256B on-chip RAM"""

    name = "TI TMS9985"
    manufacturer = "Texas Instruments"
    year = 1978
    clock_mhz = 2.5
    transistor_count = 10000
    data_width = 16
    address_width = 16

    def __init__(self):
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 6.5, 0, "On-chip workspace @5-8c"),
            'data_transfer': InstructionCategory('data_transfer', 8.0, 0, "Mem moves @6-10c"),
            'memory': InstructionCategory('memory', 12.0, 0, "External mem @10-14c"),
            'control': InstructionCategory('control', 14.0, 0, "Branch/BLWP @10-20c"),
            'stack': InstructionCategory('stack', 15.0, 0, "Context switch @12-18c"),
        }
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.23,
                'data_transfer': 0.316,
                'memory': 0.203,
                'control': 0.135,
                'stack': 0.116,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.33,
                'data_transfer': 0.291,
                'memory': 0.178,
                'control': 0.11,
                'stack': 0.091,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.205,
                'data_transfer': 0.416,
                'memory': 0.178,
                'control': 0.11,
                'stack': 0.091,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.205,
                'data_transfer': 0.291,
                'memory': 0.178,
                'control': 0.235,
                'stack': 0.091,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 3.760129,
            'control': -3.739871,
            'data_transfer': 2.260129,
            'memory': -4.729860,
            'stack': -1.749881
        }

    def analyze(self, workload='typical'):
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        total_cpi = sum(
            profile.category_weights[c] * self.instruction_categories[c].total_cycles
            for c in profile.category_weights
        )
        contributions = {c: profile.category_weights[c] * self.instruction_categories[c].total_cycles
                         for c in profile.category_weights}
        bottleneck = max(contributions, key=contributions.get)
        # System identification: apply correction terms
        base_cpi = total_cpi
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
        target_cpi = 10.0
        result = self.analyze("typical")
        error_pct = abs(result.cpi - target_cpi) / target_cpi * 100
        passed = error_pct < 5.0
        return {
            "tests": [{
                "name": "typical_cpi",
                "target": target_cpi,
                "actual": round(result.cpi, 3),
                "error_pct": round(error_pct, 2),
                "passed": passed
            }],
            "passed": 1 if passed else 0,
            "total": 1,
            "accuracy_percent": round(100 - error_pct, 2)
        }

    def get_instruction_categories(self):
        return self.instruction_categories

    def get_workload_profiles(self):
        return self.workload_profiles


if __name__ == "__main__":
    model = Tms9985Model()
    print(f"=== {model.name} ({model.year}) ===")
    print(f"Clock: {model.clock_mhz} MHz, Transistors: {model.transistor_count:,}")
    print()
    for wl in ["typical", "compute", "memory", "control"]:
        r = model.analyze(wl)
        print(f"  {wl:12s}: CPI={r.cpi:.3f}  IPC={r.ipc:.3f}  IPS={r.ips:,.0f}  bottleneck={r.bottleneck}")
    print()
    v = model.validate()
    p = v["passed"]
    t = v["total"]
    a = v["accuracy_percent"]
    status = "PASSED" if p == t else "FAILED"
    print(f"Validation: {p}/{t} {status}, accuracy={a}%")
