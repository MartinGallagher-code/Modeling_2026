#!/usr/bin/env python3
"""
Rockwell PPS-4/1 Grey-Box Queueing Model
=========================================

Architecture: 4-bit Single-Chip Microcontroller (1976)
Queueing Model: Serial ALU with integrated peripherals

Features:
  - Single-chip variant of PPS-4 architecture
  - 4-bit serial ALU (inherited from PPS-4)
  - Integrated ROM, RAM, and I/O on single die
  - Slightly faster than original PPS-4 due to on-chip integration
  - Used in consumer electronics and appliances

Target CPI: 10.0 (improved from PPS-4's 12.0 due to on-chip integration)

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
            ipc = 1.0 / cpi if cpi > 0 else 0.0
            ips = clock_mhz * 1e6 * ipc
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                       base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)

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


class Pps41Model(BaseProcessorModel):
    """
    Rockwell PPS-4/1 Grey-Box Queueing Model

    Architecture: 4-bit Single-Chip MCU (1976)
    - Single-chip implementation of PPS-4 architecture
    - Serial ALU (inherited from PPS-4)
    - On-chip ROM, RAM, and I/O reduce external bus overhead
    - Slightly improved performance vs multi-chip PPS-4
    - Target CPI: 10.0 (vs PPS-4's 12.0)
    """

    name = "Rockwell PPS-4/1"
    manufacturer = "Rockwell International"
    year = 1976
    clock_mhz = 0.25  # 250 kHz typical (slightly faster than PPS-4)
    transistor_count = 6000  # Estimated (more than PPS-4 due to integration)
    data_width = 4
    address_width = 11  # 2KB ROM typical

    def __init__(self):
        # PPS-4/1 inherits serial ALU from PPS-4 but benefits from
        # on-chip integration reducing memory access overhead
        # Instruction timing slightly improved over PPS-4

        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 12, 0,
                "ALU: Serial ADD/SUB (bit-by-bit processing) @12 cycles"
            ),
            'memory': InstructionCategory(
                'memory', 9, 0,
                "Memory: On-chip load/store @9 cycles (faster than PPS-4)"
            ),
            'branch': InstructionCategory(
                'branch', 10, 0,
                "Branch: Conditional/unconditional jumps @10 cycles"
            ),
            'io': InstructionCategory(
                'io', 8, 0,
                "I/O: On-chip I/O operations @8 cycles"
            ),
        }

        # Workload profiles for different application types
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'memory': 0.30,
                'branch': 0.25,
                'io': 0.20,
            }, "Typical embedded workload (consumer electronics)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'memory': 0.25,
                'branch': 0.20,
                'io': 0.10,
            }, "Compute-intensive (calculator-style)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.20,
                'memory': 0.45,
                'branch': 0.20,
                'io': 0.15,
            }, "Memory-intensive (data processing)"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'memory': 0.20,
                'branch': 0.35,
                'io': 0.30,
            }, "Control-intensive (appliance controller)"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.25,
                'memory': 0.25,
                'branch': 0.25,
                'io': 0.25,
            }, "Mixed workload (general purpose)"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -2.000000,
            'branch': 0.000000,
            'io': 2.000000,
            'memory': 1.000000
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using serial execution model with on-chip integration benefits"""
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

        # System identification: apply correction terms
        base_cpi = total_cpi
        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=corrected_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=contributions,
            base_cpi=base_cpi, correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        """Run validation tests"""
        tests = []
        passed = 0

        # Test 1: Typical workload CPI should be close to 10.0
        result = self.analyze('typical')
        target_cpi = 10.0
        error_pct = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {
            "name": "CPI accuracy (typical)",
            "expected": target_cpi,
            "actual": result.cpi,
            "error_percent": error_pct,
            "passed": error_pct < 5.0
        }
        tests.append(test1)
        if test1["passed"]:
            passed += 1

        # Test 2: IPS at 250 kHz should be ~25,000 at CPI=10
        expected_ips = self.clock_mhz * 1e6 / target_cpi
        ips_error = abs(result.ips - expected_ips) / expected_ips * 100
        test2 = {
            "name": "IPS at 250 kHz",
            "expected": expected_ips,
            "actual": result.ips,
            "error_percent": ips_error,
            "passed": ips_error < 10.0
        }
        tests.append(test2)
        if test2["passed"]:
            passed += 1

        # Test 3: Should be faster than PPS-4 (CPI < 12.0)
        test3 = {
            "name": "Faster than PPS-4",
            "expected": "CPI < 12.0",
            "actual": result.cpi,
            "passed": result.cpi < 12.0
        }
        tests.append(test3)
        if test3["passed"]:
            passed += 1

        # Test 4: All workloads should be in reasonable CPI range
        for wl in ['compute', 'memory', 'control', 'mixed']:
            r = self.analyze(wl)
            test = {
                "name": f"CPI range ({wl})",
                "expected_range": [8.0, 12.0],
                "actual": r.cpi,
                "passed": 8.0 <= r.cpi <= 12.0
            }
            tests.append(test)
            if test["passed"]:
                passed += 1

        # Test 5: Serial ALU should be bottleneck in compute workload
        compute_result = self.analyze('compute')
        test5 = {
            "name": "Serial ALU bottleneck (compute)",
            "expected": "alu",
            "actual": compute_result.bottleneck,
            "passed": compute_result.bottleneck == "alu"
        }
        tests.append(test5)
        if test5["passed"]:
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
            "architecture": "4-bit single-chip serial ALU MCU",
            "key_feature": "Single-chip integration of PPS-4 architecture"
        }


# Module-level convenience functions
def create_model() -> Pps41Model:
    """Create and return a PPS-4/1 model instance"""
    return Pps41Model()


def run_validation():
    """Run validation and print results"""
    model = Pps41Model()
    results = model.validate()

    print(f"Rockwell PPS-4/1 Validation Results")
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
