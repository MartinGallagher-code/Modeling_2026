#!/usr/bin/env python3
"""
NEC V30 Grey-Box Queueing Model
===============================

Architecture: 16-bit x86 Compatible (1984)
Queueing Model: Prefetch Queue (improved 8086)

Features:
  - Pin-compatible 8086 replacement
  - 16-bit external data bus (vs V20's 8-bit)
  - ~30% faster than 8086 at same clock
  - Hardware multiply/divide (3-4x faster)
  - Improved microcode efficiency
  - 8080 emulation mode

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

class NecV30Model(BaseProcessorModel):
    """
    NEC V30 Grey-Box Queueing Model

    Architecture: Improved 8086 (1984)
    - ~30% faster than 8086 overall
    - 16-bit external data bus (like 8086, unlike V20's 8-bit)
    - Hardware multiply/divide (3-4x faster)
    - 50% duty cycle (vs 33% on 8086)
    - Dual internal 16-bit buses
    - Improved effective address calculation

    Cross-validated against 8086 with documented speedup factors.
    V30 is the 16-bit bus sibling of V20 (V20 is 8088-compatible, V30 is 8086-compatible).
    """

    # Processor specifications
    name = "NEC V30"
    manufacturer = "NEC"
    year = 1984
    clock_mhz = 10.0  # Typical (8-16 MHz available)
    transistor_count = 63000
    data_width = 16
    address_width = 20
    external_bus_width = 16  # Key difference from V20 (8-bit)

    def __init__(self):
        # V30 is ~30% faster than 8086 overall
        # 8086 CPI ~4.5, so V30 target CPI ~3.025 (measured)
        # V30 has same internal timing as V20, but 16-bit bus means faster memory access
        # Calculation: 0.30*2.0 + 0.20*2.5 + 0.20*4 + 0.15*2.5 + 0.10*4 + 0.05*7.0 = 3.025
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 3.0, 0, "ALU: ADD/SUB reg,reg @2, with mem @3-4, avg ~3"),
            'data_transfer': InstructionCategory('data_transfer', 3.5, 0, "MOV reg,reg @2, MOV reg,mem @3-6 avg"),
            'memory': InstructionCategory('memory', 5, 0, "Memory ops with EA calculation + bus cycles"),
            'control': InstructionCategory('control', 4, 0, "JMP @2, Jcc @3-8 avg ~4, CALL @4-6"),
            'multiply': InstructionCategory('multiply', 6, 0, "MUL @27-28 (was 118-128 on 8086) - weighted avg"),
            'divide': InstructionCategory('divide', 9.0, 0, "DIV improved ~3x over 8086 - weighted avg"),
        }

        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.20,
                'memory': 0.20,
                'control': 0.15,
                'multiply': 0.10,
                'divide': 0.05,
            }, "Typical PC workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'data_transfer': 0.15,
                'memory': 0.10,
                'control': 0.10,
                'multiply': 0.15,
                'divide': 0.05,
            }, "Compute-intensive (benefits most from V30)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.35,
                'memory': 0.35,
                'control': 0.10,
                'multiply': 0.03,
                'divide': 0.02,
            }, "Memory-intensive (V30 16-bit bus advantage)"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.15,
                'memory': 0.15,
                'control': 0.40,
                'multiply': 0.05,
                'divide': 0.05,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.25,
                'control': 0.15,
                'multiply': 0.05,
                'divide': 0.05,
            }, "Mixed workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 6.000000,
            'control': 8.000000,
            'data_transfer': 7.000000,
            'divide': 18.000000,
            'memory': 10.000000,
            'multiply': 8.161780
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using prefetch queue model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Calculate weighted average CPI
        base_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

        # Identify bottleneck
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contributions[cat_name] = weight * cat.total_cycles
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

        # Test 1: CPI should be ~3.2 (30% faster than 8086's 4.5)
        result = self.analyze('typical')
        target_cpi = 3.2
        error = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {
            "name": "CPI accuracy vs target 3.2",
            "expected": target_cpi,
            "actual": result.cpi,
            "error_percent": error,
            "passed": error < 10.0
        }
        tests.append(test1)
        if test1["passed"]: passed += 1

        # Test 2: Should be ~30% faster than 8086 (CPI 4.5)
        speedup = 4.5 / result.cpi
        expected_speedup = 1.30
        test2 = {
            "name": "Speedup vs 8086",
            "expected": f"{expected_speedup:.2f}x",
            "actual": f"{speedup:.2f}x",
            "passed": 1.25 <= speedup <= 1.50
        }
        tests.append(test2)
        if test2["passed"]: passed += 1

        # Test 3: Should be comparable to V20 (slightly faster due to 16-bit bus)
        # V20 CPI ~3.4, V30 should be slightly faster for memory workloads
        v30_memory = self.analyze('memory')
        test3 = {
            "name": "V30 memory workload CPI",
            "expected": "< 3.4 (faster than V20 due to 16-bit bus)",
            "actual": f"{v30_memory.cpi:.2f}",
            "passed": v30_memory.cpi < 3.5
        }
        tests.append(test3)
        if test3["passed"]: passed += 1

        # Test 4: Workload weight sums
        for wl_name, profile in self.workload_profiles.items():
            weight_sum = sum(profile.category_weights.values())
            test = {
                "name": f"Weight sum ({wl_name})",
                "expected": 1.0,
                "actual": weight_sum,
                "passed": abs(weight_sum - 1.0) < 0.001
            }
            tests.append(test)
            if test["passed"]: passed += 1

        # Test 5: Cycle counts in valid range
        for cat_name, cat in self.instruction_categories.items():
            test = {
                "name": f"Cycle range ({cat_name})",
                "expected": "1-20",
                "actual": cat.total_cycles,
                "passed": 1 <= cat.total_cycles <= 20
            }
            tests.append(test)
            if test["passed"]: passed += 1

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


if __name__ == "__main__":
    model = NecV30Model()

    print(f"=== {model.name} Model ===")
    print(f"Year: {model.year}")
    print(f"Clock: {model.clock_mhz} MHz")
    print(f"External Bus: {model.external_bus_width}-bit")
    print()

    print("Instruction Categories:")
    for name, cat in model.instruction_categories.items():
        print(f"  {name}: {cat.total_cycles} cycles - {cat.description}")
    print()

    print("Workload Analysis:")
    for wl_name in model.workload_profiles:
        result = model.analyze(wl_name)
        print(f"  {wl_name}: CPI={result.cpi:.2f}, IPC={result.ipc:.3f}, "
              f"MIPS={result.ips/1e6:.2f}, bottleneck={result.bottleneck}")
    print()

    print("Validation:")
    validation = model.validate()
    for test in validation["tests"]:
        status = "PASS" if test["passed"] else "FAIL"
        print(f"  [{status}] {test['name']}: expected={test['expected']}, actual={test['actual']}")
    print(f"\nOverall: {validation['passed']}/{validation['total']} tests passed "
          f"({validation['accuracy_percent']:.1f}%)")
