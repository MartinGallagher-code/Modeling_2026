#!/usr/bin/env python3
"""
Monolithic Memories 6701 Grey-Box Queueing Model
=================================================

Architecture: 4-bit slice ALU (1975)
Queueing Model: Single-cycle microinstructions

Features:
  - 4-bit slice ALU similar to AMD Am2901
  - Bipolar technology for high speed
  - Single-cycle microinstructions
  - 16 general-purpose registers
  - Part of the 67xx bit-slice family
  - Competitor to AMD Am2900 family

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

        @classmethod
        def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations):
            ipc = 1.0 / cpi
            ips = clock_mhz * 1e6 * ipc
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations)

    class BaseProcessorModel:
        pass


class Mm6701Model(BaseProcessorModel):
    """
    Monolithic Memories 6701 Grey-Box Queueing Model

    Architecture: 4-bit Slice ALU (1975)
    - Bipolar Schottky technology
    - Single-cycle microinstructions
    - 16 general-purpose registers
    - Carry look-ahead support
    - Compatible with Am2901-style systems

    Target CPI: 1.0 (per microinstruction)
    All operations execute in a single clock cycle due to
    the bit-slice architecture where microinstructions are
    executed directly by hardware.

    Similar to AMD Am2901 but from Monolithic Memories (later
    acquired by AMD). Part of the competitive bit-slice market
    of the mid-1970s.
    """

    # Processor specifications
    name = "Monolithic Memories 6701"
    manufacturer = "Monolithic Memories"
    year = 1975
    clock_mhz = 8.0  # 8 MHz typical (125ns cycle)
    transistor_count = 180  # Approximate per slice
    data_width = 4  # 4-bit slice
    address_width = 4

    def __init__(self):
        # Bit-slice: all operations are single-cycle microinstructions
        # Target CPI: 1.0
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "ALU ops: ADD/SUB/AND/OR/XOR @1 cycle"),
            'shift': InstructionCategory('shift', 1.0, 0, "Shift: SHL/SHR @1 cycle"),
            'pass': InstructionCategory('pass', 1.0, 0, "Pass through: data routing @1 cycle"),
            'zero': InstructionCategory('zero', 1.0, 0, "Zero/Clear operations @1 cycle"),
        }

        # Configuration
        self.registers = 16
        self.carry_lookahead = True
        self.technology = "Bipolar Schottky"

        # Workload profiles - all result in CPI = 1.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.60,
                'shift': 0.20,
                'pass': 0.15,
                'zero': 0.05,
            }, "Typical microcode workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.75,
                'shift': 0.15,
                'pass': 0.08,
                'zero': 0.02,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.40,
                'shift': 0.15,
                'pass': 0.40,
                'zero': 0.05,
            }, "Memory/data movement intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.50,
                'shift': 0.10,
                'pass': 0.30,
                'zero': 0.10,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.55,
                'shift': 0.20,
                'pass': 0.20,
                'zero': 0.05,
            }, "Mixed workload"),
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze performance for a given workload profile"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Calculate weighted average CPI
        total_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            total_cpi += contrib
            contributions[cat_name] = contrib

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

        # Test 1: CPI should be exactly 1.0 (bit-slice single-cycle)
        result = self.analyze('typical')
        target_cpi = 1.0
        error = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {
            "name": "CPI accuracy vs target 1.0",
            "expected": target_cpi,
            "actual": round(result.cpi, 3),
            "error_percent": round(error, 2),
            "passed": error < 1.0  # Very strict for bit-slice
        }
        tests.append(test1)
        if test1["passed"]: passed += 1

        # Test 2: All instruction categories should be 1 cycle
        for cat_name, cat in self.instruction_categories.items():
            test = {
                "name": f"{cat_name} single-cycle",
                "expected": 1.0,
                "actual": cat.total_cycles,
                "passed": cat.total_cycles == 1.0
            }
            tests.append(test)
            if test["passed"]: passed += 1

        # Test 3: Workload weight sums
        for wl_name, profile in self.workload_profiles.items():
            weight_sum = sum(profile.category_weights.values())
            test = {
                "name": f"Weight sum ({wl_name})",
                "expected": 1.0,
                "actual": round(weight_sum, 3),
                "passed": abs(weight_sum - 1.0) < 0.001
            }
            tests.append(test)
            if test["passed"]: passed += 1

        # Test 4: CPI consistent across all workloads (should all be 1.0)
        for wl_name in self.workload_profiles:
            wl_result = self.analyze(wl_name)
            test = {
                "name": f"CPI=1.0 for {wl_name} workload",
                "expected": 1.0,
                "actual": round(wl_result.cpi, 3),
                "passed": abs(wl_result.cpi - 1.0) < 0.001
            }
            tests.append(test)
            if test["passed"]: passed += 1

        # Test 5: Comparable to Am2901 (also CPI 1.0)
        am2901_cpi = 1.0
        test5 = {
            "name": "Comparable to AMD Am2901",
            "expected": f"CPI = {am2901_cpi}",
            "actual": f"CPI = {result.cpi}",
            "passed": result.cpi == am2901_cpi
        }
        tests.append(test5)
        if test5["passed"]: passed += 1

        # Test 6: 16 registers
        test6 = {
            "name": "16 registers per slice",
            "expected": 16,
            "actual": self.registers,
            "passed": self.registers == 16
        }
        tests.append(test6)
        if test6["passed"]: passed += 1

        # Test 7: 4-bit data width
        test7 = {
            "name": "4-bit slice width",
            "expected": 4,
            "actual": self.data_width,
            "passed": self.data_width == 4
        }
        tests.append(test7)
        if test7["passed"]: passed += 1

        accuracy = (passed / len(tests)) * 100 if tests else 0
        return {
            "tests": tests,
            "passed": passed,
            "total": len(tests),
            "accuracy_percent": round(accuracy, 1)
        }

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles

    def compare_to_am2901(self) -> Dict[str, Any]:
        """Compare MM6701 to AMD Am2901"""
        mm6701_result = self.analyze('typical')

        return {
            "mm6701": {
                "cpi": round(mm6701_result.cpi, 3),
                "clock_mhz": self.clock_mhz,
                "mops": round(self.clock_mhz / mm6701_result.cpi, 2),
                "registers": self.registers,
                "data_width": self.data_width,
                "transistors": self.transistor_count,
                "manufacturer": "Monolithic Memories",
                "year": 1975
            },
            "am2901": {
                "cpi": 1.0,
                "clock_mhz": 10.0,
                "mops": 10.0,
                "registers": 16,
                "data_width": 4,
                "transistors": 200,
                "manufacturer": "AMD",
                "year": 1975
            },
            "comparison": {
                "architecture": "Both are 4-bit slice ALUs",
                "performance": "Similar single-cycle execution",
                "market": "Competing products in bit-slice market",
                "note": "Monolithic Memories later acquired by AMD"
            }
        }


# Convenience function for quick analysis
def analyze_mm6701(workload: str = 'typical') -> AnalysisResult:
    """Quick analysis function"""
    model = Mm6701Model()
    return model.analyze(workload)


def validate() -> Dict[str, Any]:
    """Run validation and return results"""
    model = Mm6701Model()
    return model.validate()


if __name__ == "__main__":
    model = Mm6701Model()

    print("=" * 60)
    print("Monolithic Memories 6701 Grey-Box Queueing Model")
    print("=" * 60)
    print(f"\nProcessor: {model.name}")
    print(f"Year: {model.year}")
    print(f"Clock: {model.clock_mhz} MHz")
    print(f"Transistors: ~{model.transistor_count}")
    print(f"Data width: {model.data_width}-bit slice")
    print(f"Registers: {model.registers}")
    print(f"Technology: {model.technology}")

    print("\n" + "-" * 60)
    print("Instruction Categories:")
    print("-" * 60)
    for name, cat in model.instruction_categories.items():
        print(f"  {name:10s}: {cat.total_cycles:.1f} cycles - {cat.description}")

    print("\n" + "-" * 60)
    print("Workload Analysis:")
    print("-" * 60)
    for wl_name in model.workload_profiles:
        result = model.analyze(wl_name)
        print(f"  {wl_name:12s}: CPI={result.cpi:.3f}, IPC={result.ipc:.3f}, "
              f"MOPS={result.ips/1e6:.2f}, bottleneck={result.bottleneck}")

    print("\n" + "-" * 60)
    print("Comparison to AMD Am2901:")
    print("-" * 60)
    comparison = model.compare_to_am2901()
    print(f"  MM6701:  CPI={comparison['mm6701']['cpi']}, "
          f"MOPS={comparison['mm6701']['mops']}")
    print(f"  Am2901:  CPI={comparison['am2901']['cpi']}, "
          f"MOPS={comparison['am2901']['mops']}")

    print("\n" + "-" * 60)
    print("Validation Results:")
    print("-" * 60)
    validation = model.validate()
    for test in validation["tests"]:
        status = "PASS" if test["passed"] else "FAIL"
        print(f"  [{status}] {test['name']}: expected {test['expected']}, got {test['actual']}")

    print(f"\nOverall: {validation['passed']}/{validation['total']} tests passed "
          f"({validation['accuracy_percent']}%)")
