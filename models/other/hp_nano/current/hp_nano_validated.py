#!/usr/bin/env python3
"""
HP Nanoprocessor Grey-Box Queueing Model
==========================================

Architecture: Sequential Execution (1977)
Queueing Model: Serial M/M/1 chain

Features:
  - 8-bit proprietary HP MCU
  - No ALU multiplication, limited arithmetic
  - ~4000 transistors
  - Used in HP instruments and calculators
  - 1 MHz clock

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

class HpNanoModel(BaseProcessorModel):
    """
    HP Nanoprocessor Grey-Box Queueing Model

    Architecture: Sequential Execution (Era: 1977)
    - HP proprietary 8-bit controller
    - No multiply/divide hardware
    - Simple ALU (increment, decrement, complement, AND, OR)
    - ~4000 transistors
    - CPI = sum of stage times

    The HP Nanoprocessor was a proprietary 8-bit MCU designed by HP for use
    in their instruments and calculators. It had a very simple instruction
    set with no multiplication capability, relying on software routines
    for complex arithmetic.
    """

    # Processor specifications
    name = "HP Nanoprocessor"
    manufacturer = "Hewlett-Packard"
    year = 1977
    clock_mhz = 1.0
    transistor_count = 4000
    data_width = 8
    address_width = 11  # 2K address space

    def __init__(self):
        # Stage timing (cycles)
        self.stage_timing = {
            'fetch': 2,      # Instruction fetch
            'decode': 1,     # Decode
            'execute': 1,    # Execute
            'memory': 2,     # Memory access
            'writeback': 0,  # Register writeback
        }

        # Instruction categories - Simple HP proprietary ISA
        # Calibrated for CPI = 4.0
        # Calculation: 0.25*3 + 0.20*3 + 0.20*5 + 0.15*4 + 0.20*5
        #            = 0.75 + 0.60 + 1.00 + 0.60 + 1.00 = 3.95
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 3, 0, "ALU operations (INC, DEC, AND, OR, CPL)"),
            'data_transfer': InstructionCategory('data_transfer', 3, 0, "Data transfer (load, store registers)"),
            'memory': InstructionCategory('memory', 5, 0, "Memory access (indirect addressing)"),
            'io': InstructionCategory('io', 4, 0, "I/O operations (device control)"),
            'control': InstructionCategory('control', 5, 0, "Control flow (branch, jump, skip)"),
        }

        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.20,
                'memory': 0.20,
                'io': 0.15,
                'control': 0.20,
            }, "Typical instrument control workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'data_transfer': 0.20,
                'memory': 0.15,
                'io': 0.05,
                'control': 0.15,
            }, "Compute-intensive workload"),
            'io_heavy': WorkloadProfile('io_heavy', {
                'alu': 0.10,
                'data_transfer': 0.15,
                'memory': 0.15,
                'io': 0.40,
                'control': 0.20,
            }, "I/O-intensive instrument control"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.15,
                'io': 0.15,
                'control': 0.40,
            }, "Control-flow intensive workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -1.521662,
            'control': 0.265536,
            'data_transfer': 1.873848,
            'io': -0.291904,
            'memory': 0.231622
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Calculate weighted average CPI
        base_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

        # Identify bottleneck (highest contribution)
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contributions[cat_name] = weight * cat.total_cycles
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
        results = {
            "processor": self.name,
            "target_cpi": 4.0,
            "tests": [],
            "passed": 0,
            "total": 0,
            "accuracy_percent": None
        }

        # Test typical workload CPI
        analysis = self.analyze('typical')
        expected_cpi = 4.0
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
            ("alu", 3),
            ("data_transfer", 3),
            ("memory", 5),
            ("io", 4),
            ("control", 5),
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
