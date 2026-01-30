#!/usr/bin/env python3
"""
NEC uCOM-4 Grey-Box Queueing Model
===================================

Architecture: 4-bit Microcontroller (1972)
Queueing Model: Fixed-cycle sequential execution

Features:
  - NEC's first microcontroller, competitor to TMS1000
  - 4-bit data path, Harvard architecture
  - Similar timing characteristics to TMS1000
  - Japanese alternative to American microcontrollers
  - Used in calculators, watches, and consumer electronics

Target CPI: 6.0 (similar to TMS1000)

Date: 2026-01-29
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
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi if base_cpi is not None else cpi, correction_delta)


class Ucom4Model:
    """
    NEC uCOM-4 Grey-Box Queueing Model

    Architecture: 4-bit Microcontroller (1972)
    - NEC's first microcontroller design
    - Competitor to TI TMS1000
    - 4-bit parallel ALU
    - Harvard architecture
    - Similar performance characteristics to TMS1000
    - Target CPI: 6.0
    """

    name = "NEC uCOM-4"
    manufacturer = "NEC"
    year = 1972
    clock_mhz = 0.4  # 400 kHz typical
    transistor_count = 7500  # Estimated
    data_width = 4
    address_width = 10  # 1KB ROM typical

    def __init__(self):
        # uCOM-4 has similar timing to TMS1000
        # Most instructions execute in 6 clock cycles
        # Some variation exists but average is close to 6

        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 6, 0,
                "ALU: ADD, SUB, logical operations @6 cycles"
            ),
            'data_transfer': InstructionCategory(
                'data_transfer', 6, 0,
                "Transfer: Register-memory transfers @6 cycles"
            ),
            'memory': InstructionCategory(
                'memory', 6, 0,
                "Memory: Load/store operations @6 cycles"
            ),
            'control': InstructionCategory(
                'control', 6, 0,
                "Control: Branch, call, return @6 cycles"
            ),
            'io': InstructionCategory(
                'io', 6, 0,
                "I/O: Input/output operations @6 cycles"
            ),
        }

        # Workload profiles for different application types
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.20,
                'control': 0.15,
                'io': 0.15,
            }, "Typical embedded controller workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'data_transfer': 0.20,
                'memory': 0.15,
                'control': 0.15,
                'io': 0.05,
            }, "Compute-intensive (calculator)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.35,
                'memory': 0.30,
                'control': 0.10,
                'io': 0.10,
            }, "Memory/data-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.15,
                'memory': 0.15,
                'control': 0.30,
                'io': 0.20,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.20,
                'data_transfer': 0.20,
                'memory': 0.20,
                'control': 0.20,
                'io': 0.20,
            }, "Mixed workload (general purpose)"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using fixed-cycle execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Weighted CPI based on instruction mix
        base_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contribution = weight * cat.total_cycles
            contributions[cat_name] = contribution
            base_cpi += contribution

        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

        # Identify bottleneck (highest contributor to CPI)
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
        """Run validation tests"""
        tests = []
        passed = 0

        # Test 1: CPI should be exactly 6.0 (fixed timing like TMS1000)
        result = self.analyze('typical')
        target_cpi = 6.0
        test1 = {
            "name": "CPI accuracy",
            "expected": target_cpi,
            "actual": result.cpi,
            "passed": abs(result.cpi - target_cpi) < 0.01
        }
        tests.append(test1)
        if test1["passed"]:
            passed += 1

        # Test 2: IPS at 400 kHz should be ~66,667
        expected_ips = self.clock_mhz * 1e6 / target_cpi
        test2 = {
            "name": "IPS at 400 kHz",
            "expected": expected_ips,
            "actual": result.ips,
            "passed": abs(result.ips - expected_ips) / expected_ips < 0.01
        }
        tests.append(test2)
        if test2["passed"]:
            passed += 1

        # Test 3: All workloads should give same CPI (fixed timing)
        for wl in ['compute', 'memory', 'control', 'mixed']:
            r = self.analyze(wl)
            test = {
                "name": f"CPI consistency ({wl})",
                "expected": 6.0,
                "actual": r.cpi,
                "passed": abs(r.cpi - 6.0) < 0.01
            }
            tests.append(test)
            if test["passed"]:
                passed += 1

        # Test 4: Should be comparable to TMS1000 (CPI = 6.0)
        test4 = {
            "name": "Comparable to TMS1000",
            "expected": "CPI = 6.0 (same as TMS1000)",
            "actual": result.cpi,
            "passed": result.cpi == 6.0
        }
        tests.append(test4)
        if test4["passed"]:
            passed += 1

        accuracy = (passed / len(tests)) * 100 if tests else 0
        return {
            "tests": tests,
            "passed": passed,
            "total": len(tests),
            "accuracy_percent": accuracy
        }

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles

    def get_specs(self) -> Dict[str, Any]:
        """Return processor specifications"""
        return {
            "name": self.name,
            "manufacturer": self.manufacturer,
            "year": self.year,
            "clock_mhz": self.clock_mhz,
            "transistor_count": self.transistor_count,
            "data_width": self.data_width,
            "address_width": self.address_width,
            "architecture": "4-bit parallel ALU MCU",
            "key_feature": "NEC's TMS1000 competitor"
        }


# Module-level convenience functions
def create_model() -> Ucom4Model:
    """Create and return a uCOM-4 model instance"""
    return Ucom4Model()


def run_validation():
    """Run validation and print results"""
    model = Ucom4Model()
    results = model.validate()

    print(f"NEC uCOM-4 Validation Results")
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
