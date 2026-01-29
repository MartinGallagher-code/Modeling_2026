#!/usr/bin/env python3
"""
Rockwell PPS-4 Grey-Box Queueing Model
======================================

Architecture: 4-bit Serial ALU (1972)
The third commercial microprocessor (after Intel 4004 and 4040).

Features:
  - 4-bit data bus with serial ALU
  - Serial bit processing (1 bit at a time)
  - Very slow compared to later processors
  - 200 kHz typical clock
  - Used in calculators, pinball machines, POS terminals

Target CPI: 12.0 (serial bit processing is inherently slow)
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

    @classmethod
    def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations):
        ipc = 1.0 / cpi
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations)


class Pps4Model:
    """
    Rockwell PPS-4 Grey-Box Queueing Model

    Third commercial microprocessor (1972)
    - 4-bit architecture with serial ALU
    - All operations process 1 bit at a time
    - Much slower than parallel ALU designs
    - Instructions take 1-4 instruction cycles
    - Each instruction cycle = multiple clock cycles
    """

    name = "Rockwell PPS-4"
    manufacturer = "Rockwell International"
    year = 1972
    clock_mhz = 0.2  # 200 kHz typical
    transistor_count = 5000  # Estimated
    data_width = 4
    address_width = 12  # 4KB ROM addressing

    def __init__(self):
        # PPS-4 serial ALU means bit-serial operations
        # Each 4-bit operation requires multiple passes through the serial ALU
        # Instruction timing varies from 1 to 4 instruction cycles
        # Each instruction cycle is approximately 5 clock cycles

        # Instruction categories based on PPS-4 architecture
        # Serial ALU operations are particularly slow
        # Tuned to achieve target CPI of ~12.0 for typical workload
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 14, 0,
                "ALU: ADD/SUB via serial bit processing @14 cycles"
            ),
            'memory': InstructionCategory(
                'memory', 11, 0,
                "Memory: Load/Store operations @11 cycles"
            ),
            'branch': InstructionCategory(
                'branch', 12, 0,
                "Branch: Conditional/unconditional jumps @12 cycles"
            ),
            'io': InstructionCategory(
                'io', 10, 0,
                "I/O: Discrete I/O operations @10 cycles"
            ),
        }

        # Workload profiles for different application types
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'memory': 0.30,
                'branch': 0.25,
                'io': 0.15,
            }, "Typical embedded workload (calculator/controller)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.50,
                'memory': 0.25,
                'branch': 0.15,
                'io': 0.10,
            }, "Compute-intensive (calculator arithmetic)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.20,
                'memory': 0.45,
                'branch': 0.20,
                'io': 0.15,
            }, "Memory-intensive (data manipulation)"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'memory': 0.20,
                'branch': 0.35,
                'io': 0.25,
            }, "Control-intensive (pinball machine logic)"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.30,
                'memory': 0.30,
                'branch': 0.20,
                'io': 0.20,
            }, "Mixed workload (POS terminal)"),
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using serial execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Weighted CPI based on instruction mix
        total_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contribution = weight * cat.total_cycles
            contributions[cat_name] = contribution
            total_cpi += contribution

        # Identify bottleneck (highest contributor to CPI)
        bottleneck = max(contributions, key=contributions.get)

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=total_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=contributions
        )

    def validate(self) -> Dict[str, Any]:
        """Run validation tests"""
        tests = []
        passed = 0

        # Test 1: Typical workload CPI should be close to 12.0
        result = self.analyze('typical')
        target_cpi = 12.0
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

        # Test 2: IPS at 200 kHz should be reasonable (~16,667 at CPI=12)
        expected_ips = self.clock_mhz * 1e6 / target_cpi
        ips_error = abs(result.ips - expected_ips) / expected_ips * 100
        test2 = {
            "name": "IPS at 200 kHz",
            "expected": expected_ips,
            "actual": result.ips,
            "error_percent": ips_error,
            "passed": ips_error < 10.0
        }
        tests.append(test2)
        if test2["passed"]: passed += 1

        # Test 3: Compute workload should have higher CPI due to ALU-heavy mix
        compute_result = self.analyze('compute')
        test3 = {
            "name": "Compute workload CPI",
            "expected_range": [11.0, 14.0],
            "actual": compute_result.cpi,
            "passed": 11.0 <= compute_result.cpi <= 14.0
        }
        tests.append(test3)
        if test3["passed"]: passed += 1

        # Test 4: All workloads should be in reasonable CPI range
        for wl in ['memory', 'control', 'mixed']:
            r = self.analyze(wl)
            test = {
                "name": f"CPI range ({wl})",
                "expected_range": [10.0, 14.0],
                "actual": r.cpi,
                "passed": 10.0 <= r.cpi <= 14.0
            }
            tests.append(test)
            if test["passed"]: passed += 1

        # Test 5: Serial ALU should be bottleneck in compute workload
        test5 = {
            "name": "Serial ALU bottleneck (compute)",
            "expected": "alu",
            "actual": compute_result.bottleneck,
            "passed": compute_result.bottleneck == "alu"
        }
        tests.append(test5)
        if test5["passed"]: passed += 1

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
            "architecture": "4-bit serial ALU",
            "key_feature": "Serial bit processing (1 bit at a time)"
        }


# Module-level convenience functions
def create_model() -> Pps4Model:
    """Create and return a PPS-4 model instance"""
    return Pps4Model()


def run_validation():
    """Run validation and print results"""
    model = Pps4Model()
    results = model.validate()

    print(f"Rockwell PPS-4 Validation Results")
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
