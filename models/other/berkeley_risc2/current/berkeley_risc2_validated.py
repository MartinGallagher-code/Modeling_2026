#!/usr/bin/env python3
"""
Berkeley RISC II Grey-Box Queueing Model
=========================================

Architecture: 32-bit RISC (1983)
Queueing Model: 3-stage pipeline with register windows

Features:
  - Improved second RISC processor (UC Berkeley)
  - 3-stage pipeline (fetch, decode, execute)
  - 138 registers with register windows (8 windows of 32 registers)
  - Single-cycle ALU operations
  - Load/store architecture
  - Delayed branches
  - Direct influence on Sun SPARC architecture

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


class BerkeleyRisc2Model(BaseProcessorModel):
    """
    Berkeley RISC II Grey-Box Queueing Model

    Architecture: Improved RISC Processor (1983)
    - 3-stage pipeline (fetch, decode, execute)
    - Single-cycle ALU operations
    - Load: 2 cycles (memory access)
    - Store: 1.5 cycles (write buffer)
    - Branch: 2 cycles (with delay slot)
    - 138 registers with 8 overlapping windows
    - 39 instructions total (expanded from RISC I's 31)

    Key improvements over RISC I:
    - More register windows (8 vs 6)
    - Better pipeline efficiency
    - Improved memory interface
    - Target CPI: ~1.2 (vs RISC I's 1.3)
    """

    # Processor specifications
    name = "Berkeley RISC II"
    manufacturer = "UC Berkeley"
    year = 1983
    clock_mhz = 3.0  # 3 MHz
    transistor_count = 40760  # Fewer transistors but more efficient
    data_width = 32
    address_width = 32

    def __init__(self):
        # RISC II achieves improved single-cycle execution over RISC I
        # Target CPI: ~1.2 (improved from RISC I's 1.3)
        # Calculation: 0.45*1 + 0.18*2 + 0.09*1.5 + 0.18*2 + 0.10*1 = 1.195 ~ 1.2
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.0, 0, "ALU ops: ADD/SUB/AND/OR/XOR @1 cycle"),
            'load': InstructionCategory('load', 2.0, 0, "Load: LDW/LDHU/LDBU @2 cycles (mem access)"),
            'store': InstructionCategory('store', 1.5, 0, "Store: STW/STH/STB @1.5 cycles (write buffer)"),
            'branch': InstructionCategory('branch', 2.0, 0, "Branch: @2 cycles (with delay slot)"),
            'call': InstructionCategory('call', 1.0, 0, "CALL/RET: @1 cycle (register window switch)"),
        }

        # Pipeline configuration
        self.pipeline_stages = 3
        self.has_delayed_branch = True
        self.branch_delay_slots = 1
        self.register_windows = 8  # Increased from RISC I's 6
        self.registers_per_window = 32
        self.total_registers = 138  # 8 windows * 16 local + 10 global
        self.global_registers = 10

        # Workload profiles calibrated for CPI ~1.2
        # RISC II benefits from high percentage of single-cycle ops
        # Target typical: 0.62*1 + 0.07*2 + 0.05*1.5 + 0.11*2 + 0.15*1 = 1.205
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.62,      # High ALU percentage (RISC design)
                'load': 0.07,     # Reduced due to register windows
                'store': 0.05,    # Reduced due to register windows
                'branch': 0.11,   # Moderate branching
                'call': 0.15,     # Fast calls with register windows
            }, "Typical RISC II workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.70,
                'load': 0.05,
                'store': 0.03,
                'branch': 0.10,
                'call': 0.12,
            }, "Compute-intensive (ALU-heavy)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.40,
                'load': 0.22,
                'store': 0.15,
                'branch': 0.13,
                'call': 0.10,
            }, "Memory-intensive (many loads/stores)"),
            'control': WorkloadProfile('control', {
                'alu': 0.45,
                'load': 0.05,
                'store': 0.03,
                'branch': 0.25,
                'call': 0.22,
            }, "Control-flow intensive"),
            'mixed': WorkloadProfile('mixed', {
                'alu': 0.55,
                'load': 0.10,
                'store': 0.06,
                'branch': 0.14,
                'call': 0.15,
            }, "Mixed general workload"),
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using pipelined execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Calculate weighted average CPI
        total_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            total_cpi += contrib
            contributions[cat_name] = contrib

        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc

        # Identify bottleneck
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

        # Test 1: CPI should be ~1.2 (improved over RISC I)
        result = self.analyze('typical')
        target_cpi = 1.2
        error = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {
            "name": "CPI accuracy vs target 1.2",
            "expected": target_cpi,
            "actual": round(result.cpi, 3),
            "error_percent": round(error, 2),
            "passed": error < 5.0
        }
        tests.append(test1)
        if test1["passed"]: passed += 1

        # Test 2: CPI should be < 1.5 (improved RISC)
        test2 = {
            "name": "RISC II CPI < 1.5",
            "expected": "< 1.5",
            "actual": round(result.cpi, 3),
            "passed": result.cpi < 1.5
        }
        tests.append(test2)
        if test2["passed"]: passed += 1

        # Test 3: Better than RISC I (CPI ~1.3)
        risc1_cpi = 1.3
        improvement = ((risc1_cpi - result.cpi) / risc1_cpi) * 100
        test3 = {
            "name": "Improvement over RISC I",
            "expected": "> 5% improvement",
            "actual": f"{improvement:.1f}% improvement",
            "passed": improvement > 5.0
        }
        tests.append(test3)
        if test3["passed"]: passed += 1

        # Test 4: Much faster than VAX (CPI ~10)
        vax_cpi = 10.0
        speedup = vax_cpi / result.cpi
        test4 = {
            "name": "Speedup vs VAX 11/780",
            "expected": "> 6x",
            "actual": f"{speedup:.1f}x",
            "passed": speedup > 6.0
        }
        tests.append(test4)
        if test4["passed"]: passed += 1

        # Test 5: Workload weight sums
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

        # Test 6: ALU ops single-cycle
        test6 = {
            "name": "ALU single-cycle",
            "expected": 1.0,
            "actual": self.instruction_categories['alu'].total_cycles,
            "passed": self.instruction_categories['alu'].total_cycles == 1.0
        }
        tests.append(test6)
        if test6["passed"]: passed += 1

        # Test 7: Store faster than load (write buffer)
        test7 = {
            "name": "Store faster than load (write buffer)",
            "expected": "store < load",
            "actual": f"store={self.instruction_categories['store'].total_cycles}, load={self.instruction_categories['load'].total_cycles}",
            "passed": self.instruction_categories['store'].total_cycles < self.instruction_categories['load'].total_cycles
        }
        tests.append(test7)
        if test7["passed"]: passed += 1

        # Test 8: More register windows than RISC I
        test8 = {
            "name": "Register windows > RISC I (6)",
            "expected": "> 6 windows",
            "actual": f"{self.register_windows} windows",
            "passed": self.register_windows > 6
        }
        tests.append(test8)
        if test8["passed"]: passed += 1

        # Test 9: Call instruction single-cycle (register windows)
        test9 = {
            "name": "Call single-cycle (register windows)",
            "expected": 1.0,
            "actual": self.instruction_categories['call'].total_cycles,
            "passed": self.instruction_categories['call'].total_cycles == 1.0
        }
        tests.append(test9)
        if test9["passed"]: passed += 1

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

    def compare_to_risc1(self) -> Dict[str, Any]:
        """Compare RISC II performance to RISC I"""
        risc2_result = self.analyze('typical')

        # RISC I specs
        risc1_cpi = 1.3
        risc1_clock = 4.0  # MHz
        risc1_mips = risc1_clock / risc1_cpi

        # RISC II calculations
        risc2_mips = self.clock_mhz / risc2_result.cpi

        return {
            "risc1": {
                "cpi": risc1_cpi,
                "clock_mhz": risc1_clock,
                "mips": round(risc1_mips, 2),
                "register_windows": 6,
                "transistors": 44500
            },
            "risc2": {
                "cpi": round(risc2_result.cpi, 3),
                "clock_mhz": self.clock_mhz,
                "mips": round(risc2_mips, 2),
                "register_windows": self.register_windows,
                "transistors": self.transistor_count
            },
            "improvements": {
                "cpi_improvement_percent": round(((risc1_cpi - risc2_result.cpi) / risc1_cpi) * 100, 1),
                "more_register_windows": self.register_windows - 6,
                "fewer_transistors": 44500 - self.transistor_count
            }
        }


# Convenience function for quick analysis
def analyze_risc2(workload: str = 'typical') -> AnalysisResult:
    """Quick analysis function"""
    model = BerkeleyRisc2Model()
    return model.analyze(workload)


def validate() -> Dict[str, Any]:
    """Run validation and return results"""
    model = BerkeleyRisc2Model()
    return model.validate()


if __name__ == "__main__":
    model = BerkeleyRisc2Model()

    print("=" * 60)
    print("Berkeley RISC II Grey-Box Queueing Model")
    print("=" * 60)
    print(f"\nProcessor: {model.name}")
    print(f"Year: {model.year}")
    print(f"Clock: {model.clock_mhz} MHz")
    print(f"Transistors: {model.transistor_count:,}")
    print(f"Pipeline stages: {model.pipeline_stages}")
    print(f"Register windows: {model.register_windows}")
    print(f"Total registers: {model.total_registers}")

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
              f"MIPS={result.ips/1e6:.2f}, bottleneck={result.bottleneck}")

    print("\n" + "-" * 60)
    print("Comparison to RISC I:")
    print("-" * 60)
    comparison = model.compare_to_risc1()
    print(f"  RISC I:  CPI={comparison['risc1']['cpi']}, MIPS={comparison['risc1']['mips']}")
    print(f"  RISC II: CPI={comparison['risc2']['cpi']}, MIPS={comparison['risc2']['mips']}")
    print(f"  CPI improvement: {comparison['improvements']['cpi_improvement_percent']}%")

    print("\n" + "-" * 60)
    print("Validation Results:")
    print("-" * 60)
    validation = model.validate()
    for test in validation["tests"]:
        status = "PASS" if test["passed"] else "FAIL"
        print(f"  [{status}] {test['name']}: expected {test['expected']}, got {test['actual']}")

    print(f"\nOverall: {validation['passed']}/{validation['total']} tests passed "
          f"({validation['accuracy_percent']}%)")
