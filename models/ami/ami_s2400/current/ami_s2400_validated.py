#!/usr/bin/env python3
"""
AMI S2400 Grey-Box Queueing Model
===================================

Architecture: 4-bit Calculator Chip (1973)
Queueing Model: Weighted CPI with variable instruction timing

Features:
  - Improved S2000 series
  - Faster clock: 300 kHz (up from 200 kHz)
  - Slightly improved instruction timing

Target CPI: 7.0 (improved over S2000's 8.0)

Date: 2026-01-29
"""

try:
    from dataclasses import dataclass
except ImportError:
    pass

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
        ipc = 1.0 / cpi if cpi > 0 else 0.0
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                   base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)


class BaseProcessorModel:
    """Base class for processor models"""
    name = ""
    manufacturer = ""
    year = 0
    clock_mhz = 0.0

    def analyze(self, workload='typical'):
        raise NotImplementedError

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
            params[f"cat.{c}.base_cycles"] = cat.base_cycles
        for c, v in self.corrections.items():
            params[f"cor.{c}"] = v
        return params
    def set_parameters(self, params):
        for k, v in params.items():
            if k.startswith("cat.") and k.endswith(".base_cycles"):
                c = k[4:-12]
                if c in self.instruction_categories:
                    self.instruction_categories[c].base_cycles = v
            elif k.startswith("cor."):
                c = k[4:]
                self.corrections[c] = v
    def get_parameter_bounds(self):
        bounds = {}
        for c, cat in self.instruction_categories.items():
            bounds[f"cat.{c}.base_cycles"] = (0.1, cat.base_cycles * 5)
        for c in self.corrections:
            bounds[f"cor.{c}"] = (-50, 50)
        return bounds
    def get_parameter_metadata(self):
        return {k: {"type": "category" if k.startswith("cat.") else "correction"} for k in self.get_parameters()}
    def get_instruction_categories(self):
        return self.instruction_categories
    def get_workload_profiles(self):
        return self.workload_profiles
    def validate(self):
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}
class AmiS2400Model(BaseProcessorModel):
    """
    AMI S2400 Grey-Box Queueing Model

    Architecture: 4-bit Calculator Chip (1973)
    - Improved S2000 with faster clock and better timing
    - 300 kHz clock
    - Target CPI: 7.0
    """

    name = "AMI S2400"
    manufacturer = "American Microsystems Inc."
    year = 1973
    clock_mhz = 0.3  # 300 kHz
    transistor_count = 4000
    data_width = 4
    address_width = 10

    def __init__(self):
        # Improved over S2000: slightly faster per-instruction timing
        # Tuned for CPI=7.0: 0.20*5 + 0.20*6 + 0.20*8 + 0.20*9 + 0.20*7 = 7.0
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 5, 0,
                "ALU: ADD, SUB operations @5 cycles"
            ),
            'data_transfer': InstructionCategory(
                'data_transfer', 6, 0,
                "Transfer: Register transfers @6 cycles"
            ),
            'memory': InstructionCategory(
                'memory', 8, 0,
                "Memory: Load/store operations @8 cycles"
            ),
            'io': InstructionCategory(
                'io', 9, 0,
                "I/O: Display/keyboard operations @9 cycles"
            ),
            'control': InstructionCategory(
                'control', 7, 0,
                "Control: Branch, jump @7 cycles"
            ),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.20,
                'data_transfer': 0.20,
                'memory': 0.20,
                'io': 0.20,
                'control': 0.20,
            }, "Typical calculator workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'data_transfer': 0.20,
                'memory': 0.15,
                'io': 0.05,
                'control': 0.15,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.30,
                'memory': 0.30,
                'io': 0.10,
                'control': 0.15,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.15,
                'io': 0.25,
                'control': 0.30,
            }, "Control/IO-intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.20,
                'data_transfer': 0.20,
                'memory': 0.20,
                'io': 0.20,
                'control': 0.20,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -1.086824,
            'control': 3.579843,
            'data_transfer': 2.781417,
            'io': -2.869764,
            'memory': -2.404671
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        base_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contribution = weight * cat.total_cycles
            contributions[cat_name] = contribution
            base_cpi += contribution

        # Apply correction terms (system identification)
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
        tests = []
        passed = 0

        result = self.analyze('typical')
        target_cpi = 7.0
        error_pct = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {
            "name": "CPI accuracy (typical)",
            "expected": target_cpi,
            "actual": result.cpi,
            "error_percent": error_pct,
            "passed": error_pct < 5.0
        }
        tests.append(test1)
        if test1["passed"]: passed += 1

        for wl_name, wl in self.workload_profiles.items():
            weight_sum = sum(wl.category_weights.values())
            test = {
                "name": f"Weight sum ({wl_name})",
                "expected": 1.0,
                "actual": round(weight_sum, 6),
                "passed": abs(weight_sum - 1.0) < 0.001
            }
            tests.append(test)
            if test["passed"]: passed += 1

        for cat_name, cat in self.instruction_categories.items():
            test = {
                "name": f"Cycle range ({cat_name})",
                "expected_range": [5, 9],
                "actual": cat.total_cycles,
                "passed": 5 <= cat.total_cycles <= 9
            }
            tests.append(test)
            if test["passed"]: passed += 1

        for wl in ['compute', 'memory', 'control', 'mixed']:
            r = self.analyze(wl)
            test = {
                "name": f"CPI range ({wl})",
                "expected_range": [5.0, 9.0],
                "actual": r.cpi,
                "passed": 5.0 <= r.cpi <= 9.0
            }
            tests.append(test)
            if test["passed"]: passed += 1

        expected_ips = self.clock_mhz * 1e6 / target_cpi
        test5 = {
            "name": "IPS at 300 kHz",
            "expected": expected_ips,
            "actual": result.ips,
            "passed": abs(result.ips - expected_ips) / expected_ips < 0.05
        }
        tests.append(test5)
        if test5["passed"]: passed += 1

        accuracy = (passed / len(tests)) * 100 if tests else 0
        return {"tests": tests, "passed": passed, "total": len(tests), "accuracy_percent": accuracy}

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles

    def get_specs(self) -> Dict[str, Any]:
        return {
            "name": self.name, "manufacturer": self.manufacturer, "year": self.year,
            "clock_mhz": self.clock_mhz, "transistor_count": self.transistor_count,
            "data_width": self.data_width, "address_width": self.address_width,
            "architecture": "4-bit PMOS calculator chip",
            "key_feature": "Improved S2000 series with faster clock"
        }


def create_model() -> AmiS2400Model:
    return AmiS2400Model()


def run_validation():
    model = AmiS2400Model()
    results = model.validate()
    print(f"AMI S2400 Validation Results")
    print("=" * 40)
    print(f"Tests passed: {results['passed']}/{results['total']}")
    print(f"Accuracy: {results['accuracy_percent']:.1f}%")
    print()
    for test in results['tests']:
        status = "PASS" if test['passed'] else "FAIL"
        print(f"  [{status}] {test['name']}")
        if 'expected' in test:
            print(f"         Expected: {test['expected']}, Actual: {test['actual']}")
        elif 'expected_range' in test:
            print(f"         Range: {test['expected_range']}, Actual: {test['actual']}")
    return results


if __name__ == "__main__":
    run_validation()
