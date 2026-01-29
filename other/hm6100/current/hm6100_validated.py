#!/usr/bin/env python3
"""
Harris HM6100 Grey-Box Queueing Model
======================================

Architecture: Faster CMOS PDP-8 (1978)
Queueing Model: Multi-state sequential execution

Features:
  - Faster CMOS implementation of PDP-8/E
  - Second-source to Intersil 6100
  - Improved process for faster operation
  - 12-bit word size
  - Full PDP-8/E instruction set compatibility

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


class Hm6100Model(BaseProcessorModel):
    """
    Harris HM6100 Grey-Box Queueing Model

    Architecture: Faster CMOS PDP-8 (1978)
    - Second-source to Intersil 6100
    - Faster process technology
    - Same 12-bit word size and instruction set
    - CPI ~8.0 states (vs Intersil's 10.5)

    Target CPI: ~8.0 states
    At 4 MHz (400ns/state): ~313 KIPS
    """

    # Processor specifications
    name = "Harris HM6100"
    manufacturer = "Harris"
    year = 1978
    clock_mhz = 4.0  # 4 MHz
    transistor_count = 4500  # Slightly improved over IM6100
    data_width = 12
    address_width = 12  # 4K words

    def __init__(self):
        # HM6100 instruction timing in states - faster than IM6100
        # Target CPI: ~8.0 states
        # Calculation: 0.25*8 + 0.25*8 + 0.15*9 + 0.15*9 + 0.10*8 + 0.10*5 = 8.0
        self.instruction_categories = {
            'arithmetic': InstructionCategory('arithmetic', 8, 0, "TAD direct @8, indirect @12 states"),
            'logic': InstructionCategory('logic', 8, 0, "AND direct @8, indirect @12 states"),
            'memory': InstructionCategory('memory', 9, 0, "DCA @9, ISZ @12 states avg"),
            'jump': InstructionCategory('jump', 9, 0, "JMP @8, JMS @9 direct, +4 indirect"),
            'io': InstructionCategory('io', 8, 0, "IOT @8 states"),
            'operate': InstructionCategory('operate', 5, 0, "OPR group @5 states"),
        }

        # Workload profiles (same as Intersil 6100)
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'arithmetic': 0.25,
                'logic': 0.25,
                'memory': 0.15,
                'jump': 0.15,
                'io': 0.10,
                'operate': 0.10,
            }, "Typical PDP-8 workload"),
            'compute': WorkloadProfile('compute', {
                'arithmetic': 0.40,
                'logic': 0.30,
                'memory': 0.10,
                'jump': 0.10,
                'io': 0.05,
                'operate': 0.05,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'arithmetic': 0.15,
                'logic': 0.10,
                'memory': 0.40,
                'jump': 0.15,
                'io': 0.10,
                'operate': 0.10,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'arithmetic': 0.15,
                'logic': 0.15,
                'memory': 0.15,
                'jump': 0.35,
                'io': 0.15,
                'operate': 0.05,
            }, "Control-flow intensive"),
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using multi-state execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Calculate weighted average CPI (in states)
        total_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            total_cpi += weight * cat.total_cycles

        # Convert states to effective IPS
        # Each state = 400ns at 4 MHz (faster than IM6100's 500ns)
        state_time_us = 0.4  # microseconds
        ips = 1e6 / (total_cpi * state_time_us)
        ipc = 1.0 / total_cpi  # States per instruction

        # Identify bottleneck
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contributions[cat_name] = weight * cat.total_cycles
        bottleneck = max(contributions, key=contributions.get)

        return AnalysisResult(
            processor=self.name,
            workload=workload,
            ipc=ipc,
            cpi=total_cpi,
            ips=ips,
            bottleneck=bottleneck,
            utilizations=contributions
        )

    def validate(self) -> Dict[str, Any]:
        """Run validation tests"""
        tests = []
        passed = 0

        # Test 1: CPI should be ~8.0 states
        result = self.analyze('typical')
        target_cpi = 8.0
        error = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {
            "name": "CPI accuracy vs target 8.0 states",
            "expected": target_cpi,
            "actual": result.cpi,
            "error_percent": error,
            "passed": error < 5.0
        }
        tests.append(test1)
        if test1["passed"]: passed += 1

        # Test 2: CPI in valid range (5-12 states)
        test2 = {
            "name": "CPI in valid range (5-12)",
            "expected": "5-12 states",
            "actual": result.cpi,
            "passed": 5 <= result.cpi <= 12
        }
        tests.append(test2)
        if test2["passed"]: passed += 1

        # Test 3: IPS approximately correct (~312 KIPS)
        state_time_us = 0.4
        expected_ips = 1e6 / (target_cpi * state_time_us)
        test3 = {
            "name": "IPS approximately correct",
            "expected": f"~{int(expected_ips):,}",
            "actual": f"{int(result.ips):,}",
            "passed": abs(result.ips - expected_ips) / expected_ips < 0.10
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

        # Test 5: OPR is fastest (5 states)
        test5 = {
            "name": "OPR fastest at 5 states",
            "expected": 5,
            "actual": self.instruction_categories['operate'].total_cycles,
            "passed": self.instruction_categories['operate'].total_cycles == 5
        }
        tests.append(test5)
        if test5["passed"]: passed += 1

        # Test 6: Faster than Intersil 6100 (CPI < 10.5)
        test6 = {
            "name": "Faster than Intersil 6100 (CPI < 10.5)",
            "expected": "< 10.5",
            "actual": result.cpi,
            "passed": result.cpi < 10.5
        }
        tests.append(test6)
        if test6["passed"]: passed += 1

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
