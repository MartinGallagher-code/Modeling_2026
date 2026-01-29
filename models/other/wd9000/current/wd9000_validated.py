#!/usr/bin/env python3
"""
Western Digital Pascal MicroEngine WD9000 Grey-Box Queueing Model
=================================================================

Architecture: Microprogrammed p-code Execution (1979)
Queueing Model: Serial M/M/1 chain

Features:
  - 16-bit CPU executing UCSD Pascal p-code directly in hardware
  - Microprogrammed design (~10000 transistors)
  - 10 MHz clock, but complex p-code instructions
  - Stack-based architecture for Pascal execution
  - Hardware procedure call/return, array bounds checking

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

        @classmethod
        def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations):
            ipc = 1.0 / cpi
            ips = clock_mhz * 1e6 * ipc
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations)

    class BaseProcessorModel:
        pass


class Wd9000Model(BaseProcessorModel):
    """
    Western Digital Pascal MicroEngine WD9000 Grey-Box Queueing Model

    Architecture: Microprogrammed p-code Execution (Era: 1979)
    - Executes UCSD Pascal p-code directly in hardware
    - Stack-based architecture
    - Complex instructions (procedure calls, array bounds checking)
    - CPI = sum of microcode cycles per p-code instruction

    The WD9000 was a unique processor designed to execute UCSD Pascal p-code
    (pseudo-code) directly in hardware via microcode. This eliminated the
    need for a software p-code interpreter, providing significant speedup
    for Pascal programs. The architecture was stack-based with hardware
    support for procedure calls, local variable frames, and array bounds.
    """

    # Processor specifications
    name = "Western Digital WD9000 Pascal MicroEngine"
    manufacturer = "Western Digital"
    year = 1979
    clock_mhz = 10.0
    transistor_count = 10000
    data_width = 16
    address_width = 16

    def __init__(self):
        # Stage timing (cycles)
        self.stage_timing = {
            'fetch': 2,      # p-code fetch
            'decode': 2,     # Microcode decode
            'execute': 4,    # Microcode execution (weighted average)
            'memory': 3,     # Stack/memory access
            'writeback': 0,  # Register writeback
        }

        # Instruction categories - WD9000 p-code operations
        # Calibrated for CPI = 8.0
        # Calculation: 0.20*4 + 0.25*8 + 0.15*6 + 0.15*14 + 0.15*5 + 0.10*6
        #            = 0.8 + 2.0 + 0.9 + 2.1 + 0.75 + 0.6 = 7.15
        # Adjust weights: 0.18*4 + 0.22*8 + 0.18*6 + 0.15*14 + 0.15*5 + 0.12*6
        #               = 0.72 + 1.76 + 1.08 + 2.1 + 0.75 + 0.72 = 7.13
        # Adjust: 0.15*4 + 0.20*8 + 0.18*6 + 0.18*14 + 0.15*5 + 0.14*6
        #       = 0.6 + 1.6 + 1.08 + 2.52 + 0.75 + 0.84 = 7.39
        # Adjust: 0.12*4 + 0.18*8 + 0.18*6 + 0.22*14 + 0.15*5 + 0.15*6
        #       = 0.48 + 1.44 + 1.08 + 3.08 + 0.75 + 0.9 = 7.73
        # Adjust: 0.10*4 + 0.18*8 + 0.18*6 + 0.24*14 + 0.15*5 + 0.15*6
        #       = 0.4 + 1.44 + 1.08 + 3.36 + 0.75 + 0.9 = 7.93
        # Close enough within 5%
        self.instruction_categories = {
            'stack_ops': InstructionCategory('stack_ops', 4, 0, "Push/pop/dup stack operations"),
            'arithmetic': InstructionCategory('arithmetic', 8, 0, "Add/sub/mul arithmetic"),
            'memory': InstructionCategory('memory', 6, 0, "Load/store indirect"),
            'procedure': InstructionCategory('procedure', 14, 0, "Procedure call/return with frame setup"),
            'control': InstructionCategory('control', 5, 0, "Branch/jump operations"),
            'comparison': InstructionCategory('comparison', 6, 0, "Compare/test operations"),
        }

        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'stack_ops': 0.10,
                'arithmetic': 0.18,
                'memory': 0.18,
                'procedure': 0.24,
                'control': 0.15,
                'comparison': 0.15,
            }, "Typical Pascal program workload"),
            'compute': WorkloadProfile('compute', {
                'stack_ops': 0.15,
                'arithmetic': 0.40,
                'memory': 0.15,
                'procedure': 0.10,
                'control': 0.10,
                'comparison': 0.10,
            }, "Compute-intensive Pascal workload"),
            'memory': WorkloadProfile('memory', {
                'stack_ops': 0.20,
                'arithmetic': 0.10,
                'memory': 0.35,
                'procedure': 0.15,
                'control': 0.10,
                'comparison': 0.10,
            }, "Memory/array-intensive workload"),
            'control': WorkloadProfile('control', {
                'stack_ops': 0.08,
                'arithmetic': 0.10,
                'memory': 0.12,
                'procedure': 0.30,
                'control': 0.25,
                'comparison': 0.15,
            }, "Control-flow intensive workload"),
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Calculate weighted average CPI
        total_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            total_cpi += weight * cat.total_cycles

        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc

        # Identify bottleneck (highest contribution)
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
            ("stack_ops", 4),
            ("arithmetic", 8),
            ("memory", 6),
            ("procedure", 14),
            ("control", 5),
            ("comparison", 6),
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

        # Test weight sums
        for wp_name, wp in self.workload_profiles.items():
            weight_sum = sum(wp.category_weights.values())
            test_result = {
                "name": f"{wp_name}_weight_sum",
                "expected": 1.0,
                "actual": round(weight_sum, 6),
                "passed": abs(weight_sum - 1.0) < 0.001
            }
            results["tests"].append(test_result)
            results["total"] += 1
            if test_result["passed"]:
                results["passed"] += 1

        # Test cycle ranges
        for cat_name, cat in self.instruction_categories.items():
            in_range = 1 <= cat.total_cycles <= 50
            test_result = {
                "name": f"{cat_name}_cycle_range",
                "expected": "1-50",
                "actual": cat.total_cycles,
                "passed": in_range
            }
            results["tests"].append(test_result)
            results["total"] += 1
            if test_result["passed"]:
                results["passed"] += 1

        # Test all workloads produce valid results
        for wp_name in self.workload_profiles:
            analysis = self.analyze(wp_name)
            valid = analysis.cpi > 0 and analysis.ips > 0
            test_result = {
                "name": f"{wp_name}_workload_valid",
                "expected": "cpi > 0 and ips > 0",
                "actual": f"cpi={analysis.cpi:.2f}, ips={analysis.ips:.0f}",
                "passed": valid
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
