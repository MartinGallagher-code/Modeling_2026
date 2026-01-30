#!/usr/bin/env python3
"""
Panafacom MN1610 Grey-Box Queueing Model
=========================================

Architecture: Sequential Execution (1975)
Queueing Model: Serial M/M/1 chain

Features:
  - 16-bit CPU - one of Japan's first 16-bit microprocessors
  - Single instruction at a time
  - No instruction prefetch
  - No pipeline
  - Direct memory access on every instruction
  - General-purpose minicomputer-like architecture

Generated: 2026-01-29
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional

# Import from common (adjust path as needed)
try:
    from common.base_model import BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult
except ImportError:
    # Fallback definitions if common not available
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


class Mn1610Model(BaseProcessorModel):
    """
    Panafacom MN1610 Grey-Box Queueing Model

    Architecture: Sequential Execution (Era: 1975)
    - No instruction overlap
    - Serial stage execution
    - CPI = sum of stage times

    The MN1610 was one of Japan's first 16-bit microprocessors, developed
    by Panafacom (a joint venture of Matsushita, Fujitsu, and NEC).
    It featured a minicomputer-like architecture with 16-bit data bus.
    """

    # Processor specifications
    name = "Panafacom MN1610"
    manufacturer = "Panafacom"
    year = 1975
    clock_mhz = 2.0  # Typical clock speed
    transistor_count = 6000  # Estimated for 1975 16-bit CPU
    data_width = 16
    address_width = 16

    def __init__(self):
        # Stage timing (cycles)
        self.stage_timing = {
            'fetch': 3,      # Instruction fetch (16-bit)
            'decode': 1,     # Decode
            'execute': 3,    # Execute (weighted average)
            'memory': 3,     # Memory access (for load/store)
            'writeback': 0,  # Register writeback
        }

        # Instruction categories - MN1610 was an early 16-bit processor
        # Calibrated for CPI = 8.0
        # Calculation: 0.30*5 + 0.15*7 + 0.25*10 + 0.15*10 + 0.10*10 + 0.05*14 = 8.05
        self.instruction_categories = {
            'register_ops': InstructionCategory('register_ops', 5, 0, "Register-to-register"),
            'immediate': InstructionCategory('immediate', 7, 0, "Immediate operand"),
            'memory_read': InstructionCategory('memory_read', 10, 0, "Load from memory"),
            'memory_write': InstructionCategory('memory_write', 10, 0, "Store to memory"),
            'branch': InstructionCategory('branch', 10, 0, "Branch/jump"),
            'call_return': InstructionCategory('call_return', 14, 0, "Subroutine call/return"),
        }

        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'register_ops': 0.30,
                'immediate': 0.15,
                'memory_read': 0.25,
                'memory_write': 0.15,
                'branch': 0.10,
                'call_return': 0.05,
            }, "Typical mixed workload"),
            'compute': WorkloadProfile('compute', {
                'register_ops': 0.50,
                'immediate': 0.25,
                'memory_read': 0.10,
                'memory_write': 0.05,
                'branch': 0.08,
                'call_return': 0.02,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'register_ops': 0.15,
                'immediate': 0.10,
                'memory_read': 0.40,
                'memory_write': 0.25,
                'branch': 0.05,
                'call_return': 0.05,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'register_ops': 0.20,
                'immediate': 0.10,
                'memory_read': 0.15,
                'memory_write': 0.10,
                'branch': 0.30,
                'call_return': 0.15,
            }, "Control-flow intensive workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'branch': -1.553086,
            'call_return': -6.999967,
            'immediate': -3.247850,
            'memory_read': 0.412589,
            'memory_write': -4.999814,
            'register_ops': 5.000000
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
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

        # Identify bottleneck (highest contribution)
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
            base_cpi=base_cpi, correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        """Run validation tests"""
        results = {
            "processor": self.name,
            "target_cpi": 8.0,
            "tests": [],
            "passed": 0,
            "total": 0,
            "accuracy_percent": None
        }

        # Test typical workload CPI
        analysis = self.analyze('typical')
        expected_cpi = 8.0
        error_pct = abs(analysis.cpi - expected_cpi) / expected_cpi * 100

        test_result = {
            "name": "typical_workload_cpi",
            "expected": expected_cpi,
            "actual": analysis.cpi,
            "error_percent": error_pct,
            "passed": error_pct < 5.0
        }
        results["tests"].append(test_result)
        results["total"] += 1
        if test_result["passed"]:
            results["passed"] += 1

        # Test instruction category timing
        timing_tests = [
            ("register_ops", 5),
            ("immediate", 7),
            ("memory_read", 10),
            ("memory_write", 10),
            ("branch", 10),
            ("call_return", 14),
        ]

        for cat_name, expected_cycles in timing_tests:
            cat = self.instruction_categories[cat_name]
            test_result = {
                "name": f"{cat_name}_timing",
                "expected": expected_cycles,
                "actual": cat.total_cycles,
                "passed": cat.total_cycles == expected_cycles
            }
            results["tests"].append(test_result)
            results["total"] += 1
            if test_result["passed"]:
                results["passed"] += 1

        results["accuracy_percent"] = (results["passed"] / results["total"]) * 100
        return results

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles
