#!/usr/bin/env python3
"""
Mostek MK5005 Grey-Box Queueing Model
=======================================

Architecture: 4-bit Calculator-on-a-Chip (1972)
Queueing Model: Sequential execution with variable instruction timing

Features:
  - Early single-chip calculator IC
  - 4-bit serial data path
  - PMOS technology, very slow by modern standards
  - Integrated display driver and keyboard scanner
  - ~3,000 transistors

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


class Mk5005Model(BaseProcessorModel):
    """
    Mostek MK5005 Grey-Box Queueing Model

    Architecture: 4-bit Serial Calculator-on-a-Chip (1972)
    - Early PMOS calculator IC by Mostek
    - 4-bit serial BCD data path
    - Shift-register based architecture
    - Integrated keyboard scanning and display multiplexing
    - One of the earliest calculator-on-a-chip designs
    """

    # Processor specifications
    name = "MK5005"
    manufacturer = "Mostek"
    year = 1972
    clock_mhz = 0.2  # 200 kHz typical
    transistor_count = 3000
    data_width = 4
    address_width = 10  # Very limited address space

    def __init__(self):
        # Instruction categories with typical cycle counts
        # Early PMOS is very slow; everything takes many cycles
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 8, 0,
                "ALU: ADD, SUB (4-bit serial) @8 cycles avg"
            ),
            'bcd': InstructionCategory(
                'bcd', 10, 0,
                "BCD: Multi-digit BCD ops, decimal correct @10 cycles avg"
            ),
            'shift': InstructionCategory(
                'shift', 6, 0,
                "Shift: Shift register rotate, digit shift @6 cycles avg"
            ),
            'control': InstructionCategory(
                'control', 7, 0,
                "Control: Branch, conditional skip @7 cycles avg"
            ),
            'display': InstructionCategory(
                'display', 12, 0,
                "Display: Display scan, segment drive, blanking @12 cycles avg"
            ),
        }

        # Workload profiles
        # typical: 0.20*8 + 0.15*10 + 0.15*6 + 0.20*7 + 0.30*12 = 9.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.20,
                'bcd': 0.15,
                'shift': 0.15,
                'control': 0.20,
                'display': 0.30,
            }, "Typical four-function calculator workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.30,
                'bcd': 0.35,
                'shift': 0.15,
                'control': 0.10,
                'display': 0.10,
            }, "Heavy arithmetic (chain calculations)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'bcd': 0.10,
                'shift': 0.40,
                'control': 0.15,
                'display': 0.20,
            }, "Shift-register intensive (data movement)"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'bcd': 0.10,
                'shift': 0.15,
                'control': 0.35,
                'display': 0.25,
            }, "Control-flow heavy (keyboard scan, state machine)"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -4.080337,
            'bcd': 2.854929,
            'control': 2.025529,
            'display': -1.698004,
            'shift': 3.280823
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using weighted instruction mix model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        base_cpi = 0.0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            contributions[cat_name] = contrib
            base_cpi += contrib

        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta
        bottleneck = max(contributions, key=contributions.get)

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

        # Test 1: Typical CPI should be ~9.0
        result = self.analyze('typical')
        target_cpi = 9.0
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

        # Test 2: IPS at 200 kHz
        expected_ips = self.clock_mhz * 1e6 / target_cpi
        test2 = {
            "name": "IPS at 200 kHz",
            "expected": round(expected_ips),
            "actual": round(result.ips),
            "passed": abs(result.ips - expected_ips) / expected_ips < 0.05
        }
        tests.append(test2)
        if test2["passed"]: passed += 1

        # Test 3: Compute workload should have different CPI
        compute = self.analyze('compute')
        test3 = {
            "name": "Compute CPI differs from typical",
            "expected": "!= 9.0",
            "actual": round(compute.cpi, 4),
            "passed": abs(compute.cpi - target_cpi) > 0.1
        }
        tests.append(test3)
        if test3["passed"]: passed += 1

        # Test 4: All workloads produce valid CPI
        for wl_name in self.workload_profiles:
            r = self.analyze(wl_name)
            test = {
                "name": f"Valid CPI range ({wl_name})",
                "expected": "6.0 - 12.0",
                "actual": round(r.cpi, 4),
                "passed": 6.0 <= r.cpi <= 12.0
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
