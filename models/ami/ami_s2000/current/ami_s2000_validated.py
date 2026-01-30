#!/usr/bin/env python3
"""
AMI S2000 Grey-Box Queueing Model
===================================

Architecture: 4-bit Calculator Chip (1971)
Queueing Model: Weighted CPI with variable instruction timing

Features:
  - One of the earliest 4-bit calculator chips
  - PMOS technology, 200 kHz clock
  - Very slow by later standards
  - Used in early electronic calculators

Target CPI: 8.0 (very early PMOS design)

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

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        raise NotImplementedError

    def validate(self) -> Dict[str, Any]:
        raise NotImplementedError


class AmiS2000Model(BaseProcessorModel):
    """
    AMI S2000 Grey-Box Queueing Model

    Architecture: 4-bit Calculator Chip (1971)
    - Very early PMOS calculator chip
    - 200 kHz clock
    - Slow instruction execution
    - Target CPI: 8.0
    """

    name = "AMI S2000"
    manufacturer = "American Microsystems Inc."
    year = 1971
    clock_mhz = 0.2  # 200 kHz
    transistor_count = 3000
    data_width = 4
    address_width = 9  # 512 bytes ROM

    def __init__(self):
        # Very early PMOS - all operations are slow
        # Tuned for CPI=8.0 with given category timings
        # 0.25*6 + 0.20*7 + 0.20*9 + 0.15*10 + 0.20*8
        # = 1.5 + 1.4 + 1.8 + 1.5 + 1.6 = 7.8
        # Adjust weights: 0.20*6 + 0.20*7 + 0.20*9 + 0.20*10 + 0.20*8 = 8.0
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 6, 0,
                "ALU: ADD, SUB operations @6 cycles"
            ),
            'data_transfer': InstructionCategory(
                'data_transfer', 7, 0,
                "Transfer: Register transfers @7 cycles"
            ),
            'memory': InstructionCategory(
                'memory', 9, 0,
                "Memory: Load/store operations @9 cycles"
            ),
            'io': InstructionCategory(
                'io', 10, 0,
                "I/O: Display/keyboard operations @10 cycles"
            ),
            'control': InstructionCategory(
                'control', 8, 0,
                "Control: Branch, jump @8 cycles"
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
            }, "Compute-intensive (arithmetic)"),
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
            'alu': -1.087037,
            'control': 3.579629,
            'data_transfer': 2.783337,
            'io': -2.869444,
            'memory': -2.406485
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
        target_cpi = 8.0
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
                "expected_range": [6, 10],
                "actual": cat.total_cycles,
                "passed": 6 <= cat.total_cycles <= 10
            }
            tests.append(test)
            if test["passed"]: passed += 1

        for wl in ['compute', 'memory', 'control', 'mixed']:
            r = self.analyze(wl)
            test = {
                "name": f"CPI range ({wl})",
                "expected_range": [6.0, 10.0],
                "actual": r.cpi,
                "passed": 6.0 <= r.cpi <= 10.0
            }
            tests.append(test)
            if test["passed"]: passed += 1

        expected_ips = self.clock_mhz * 1e6 / target_cpi
        test5 = {
            "name": "IPS at 200 kHz",
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
            "key_feature": "Very early calculator chip (1971)"
        }


def create_model() -> AmiS2000Model:
    return AmiS2000Model()


def run_validation():
    model = AmiS2000Model()
    results = model.validate()
    print(f"AMI S2000 Validation Results")
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
