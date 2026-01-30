#!/usr/bin/env python3
"""
HP Saturn Grey-Box Queueing Model
==================================

Architecture: 4-bit CPU with 64-bit registers (1984)
Queueing Model: Sequential execution with variable instruction timing

Features:
  - Custom HP calculator CPU used in HP 71B and HP 48 series
  - 4-bit data path but 64-bit registers (16 nibbles)
  - BCD arithmetic native support
  - Nibble-serial architecture with variable-length fields
  - ~40,000 transistors

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
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)

    class BaseProcessorModel:
        pass


class HpSaturnModel(BaseProcessorModel):
    """
    HP Saturn Grey-Box Queueing Model

    Architecture: 4-bit nibble-serial CPU with 64-bit registers (1984)
    - Custom CMOS CPU designed for HP calculators
    - 4-bit data path processes 64-bit registers nibble by nibble
    - Native BCD arithmetic for calculator precision
    - Variable-length instruction encoding (2-21 nibbles)
    - Used in HP 71B, HP 48 series, HP 49 series
    """

    # Processor specifications
    name = "HP Saturn"
    manufacturer = "Hewlett-Packard"
    year = 1984
    clock_mhz = 0.64  # 640 kHz (early versions; later up to 4 MHz)
    transistor_count = 40000
    data_width = 4  # 4-bit data path
    register_width = 64  # 64-bit registers (16 nibbles)
    address_width = 20  # 1 MB address space

    def __init__(self):
        # Instruction categories with typical cycle counts
        # Saturn processes nibble-by-nibble, so operations on wide
        # fields take many cycles. BCD operations are multi-step.
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 8, 0,
                "ALU: ADD, SUB, INC, DEC on register fields @8 cycles avg"
            ),
            'register_op': InstructionCategory(
                'register_op', 4, 0,
                "Register: SWAP, COPY, CLR, nibble moves @4 cycles avg"
            ),
            'memory': InstructionCategory(
                'memory', 12, 0,
                "Memory: DAT0/DAT1 load/store via pointer @12 cycles avg"
            ),
            'control': InstructionCategory(
                'control', 6, 0,
                "Control: GOTO, GOSUB, RTN, conditional branches @6 cycles avg"
            ),
            'bcd': InstructionCategory(
                'bcd', 10, 0,
                "BCD: BCD arithmetic, digit adjust, field ops @10 cycles avg"
            ),
        }

        # Workload profiles
        # typical: 0.25*8 + 0.20*4 + 0.15*12 + 0.15*6 + 0.25*10 = 8.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'register_op': 0.20,
                'memory': 0.15,
                'control': 0.15,
                'bcd': 0.25,
            }, "Typical HP calculator workload (mixed computation)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.30,
                'register_op': 0.15,
                'memory': 0.10,
                'control': 0.10,
                'bcd': 0.35,
            }, "Heavy computation (scientific functions, BCD math)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'register_op': 0.20,
                'memory': 0.35,
                'control': 0.10,
                'bcd': 0.20,
            }, "Memory-intensive (stack/object operations)"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'register_op': 0.15,
                'memory': 0.15,
                'control': 0.40,
                'bcd': 0.15,
            }, "Control-flow heavy (RPL interpreter loop)"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -1.174622,
            'bcd': 1.316415,
            'control': -2.560000,
            'memory': 1.101793,
            'register_op': 0.916415
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using weighted instruction mix model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Calculate weighted CPI from instruction mix
        base_cpi = 0.0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            contributions[cat_name] = contrib
            base_cpi += contrib

        bottleneck = max(contributions, key=contributions.get)

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
            base_cpi=base_cpi,
            correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        """Run validation tests"""
        tests = []
        passed = 0

        # Test 1: Typical CPI should be ~8.0
        result = self.analyze('typical')
        target_cpi = 8.0
        error_pct = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {
            "name": "CPI accuracy (typical)",
            "expected": target_cpi,
            "actual": round(result.cpi, 4),
            "error_pct": round(error_pct, 2),
            "passed": error_pct < 5.0
        }
        tests.append(test1)
        if test1["passed"]: passed += 1

        # Test 2: IPS at 640 kHz
        expected_ips = self.clock_mhz * 1e6 / target_cpi
        test2 = {
            "name": "IPS at 640 kHz",
            "expected": round(expected_ips),
            "actual": round(result.ips),
            "passed": abs(result.ips - expected_ips) / expected_ips < 0.05
        }
        tests.append(test2)
        if test2["passed"]: passed += 1

        # Test 3: Compute workload should have higher CPI (more BCD)
        compute = self.analyze('compute')
        test3 = {
            "name": "Compute CPI > typical (heavier BCD)",
            "expected": "> 8.0",
            "actual": round(compute.cpi, 4),
            "passed": compute.cpi > target_cpi
        }
        tests.append(test3)
        if test3["passed"]: passed += 1

        # Test 4: Control workload should have lower CPI
        control = self.analyze('control')
        test4 = {
            "name": "Control CPI < typical (lighter ops)",
            "expected": "< 8.0",
            "actual": round(control.cpi, 4),
            "passed": control.cpi < target_cpi
        }
        tests.append(test4)
        if test4["passed"]: passed += 1

        # Test 5: All workloads produce valid CPI
        for wl_name in self.workload_profiles:
            r = self.analyze(wl_name)
            test = {
                "name": f"Valid CPI range ({wl_name})",
                "expected": "4.0 - 12.0",
                "actual": round(r.cpi, 4),
                "passed": 4.0 <= r.cpi <= 12.0
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
