#!/usr/bin/env python3
"""
Berkeley RISC I Grey-Box Queueing Model
=======================================

Architecture: 32-bit RISC (1982)
Queueing Model: 2-stage pipeline with register windows

Features:
  - First RISC processor (UC Berkeley)
  - 2-stage pipeline (fetch/decode + execute)
  - 78 registers with register windows (6 windows)
  - Delayed branches
  - Load/store architecture
  - Precursor to SPARC

Date: 2026-01-28
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


class BerkeleyRisc1Model(BaseProcessorModel):
    """
    Berkeley RISC I Grey-Box Queueing Model

    Architecture: First RISC Processor (1982)
    - 2-stage pipeline
    - Most instructions: 1 cycle
    - Load/Store: 2 cycles
    - Delayed branches (branch delay slot)
    - 78 registers with 6 overlapping windows
    - 31 instructions total

    Target CPI: 1.2-1.5 (realistic with memory access)
    """

    # Processor specifications
    name = "Berkeley RISC I"
    manufacturer = "UC Berkeley"
    year = 1982
    clock_mhz = 4.0  # 4 MHz
    transistor_count = 44500
    data_width = 32
    address_width = 32

    def __init__(self):
        # RISC I achieves near single-cycle execution
        # Target CPI: ~1.3 (accounting for loads/stores and branches)
        # Calculation: 0.40*1 + 0.20*2 + 0.10*2 + 0.20*1 + 0.10*1 = 1.3
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1, 0, "ALU ops: ADD/SUB/AND/OR @1 cycle"),
            'load': InstructionCategory('load', 2, 0, "Load: LDW @2 cycles (mem access)"),
            'store': InstructionCategory('store', 2, 0, "Store: STW @2 cycles (mem access)"),
            'branch': InstructionCategory('branch', 1, 0, "Branch: @1 cycle (delay slot filled)"),
            'call': InstructionCategory('call', 1, 0, "CALL: @1 cycle (register window switch)"),
        }

        # Pipeline configuration
        self.pipeline_stages = 2
        self.has_delayed_branch = True
        self.branch_delay_slots = 1
        self.register_windows = 6
        self.registers_per_window = 14
        self.global_registers = 10

        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.40,
                'load': 0.20,
                'store': 0.10,
                'branch': 0.20,
                'call': 0.10,
            }, "Typical RISC workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.60,
                'load': 0.15,
                'store': 0.05,
                'branch': 0.15,
                'call': 0.05,
            }, "Compute-intensive (ALU-heavy)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.25,
                'load': 0.35,
                'store': 0.25,
                'branch': 0.10,
                'call': 0.05,
            }, "Memory-intensive (many loads/stores)"),
            'control': WorkloadProfile('control', {
                'alu': 0.30,
                'load': 0.15,
                'store': 0.05,
                'branch': 0.35,
                'call': 0.15,
            }, "Control-flow intensive"),
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using pipelined execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Calculate weighted average CPI
        total_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            total_cpi += weight * cat.total_cycles

        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc

        # Identify bottleneck
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contributions[cat_name] = weight * cat.total_cycles
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

        # Test 1: CPI should be ~1.3 (near single-cycle)
        result = self.analyze('typical')
        target_cpi = 1.3
        error = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {
            "name": "CPI accuracy vs target 1.3",
            "expected": target_cpi,
            "actual": result.cpi,
            "error_percent": error,
            "passed": error < 5.0
        }
        tests.append(test1)
        if test1["passed"]: passed += 1

        # Test 2: CPI should be < 2.0 (RISC principle)
        test2 = {
            "name": "RISC CPI < 2.0",
            "expected": "< 2.0",
            "actual": result.cpi,
            "passed": result.cpi < 2.0
        }
        tests.append(test2)
        if test2["passed"]: passed += 1

        # Test 3: Much faster than VAX (CPI ~10)
        vax_cpi = 10.0
        speedup = vax_cpi / result.cpi
        test3 = {
            "name": "Speedup vs VAX 11/780",
            "expected": "> 5x",
            "actual": f"{speedup:.1f}x",
            "passed": speedup > 5.0
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

        # Test 5: ALU ops single-cycle
        test5 = {
            "name": "ALU single-cycle",
            "expected": 1,
            "actual": self.instruction_categories['alu'].total_cycles,
            "passed": self.instruction_categories['alu'].total_cycles == 1
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
