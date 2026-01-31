#!/usr/bin/env python3
"""
Plessey MIPROC Grey-Box Queueing Model
========================================

Architecture: Sequential Execution (1975)
Queueing Model: Serial M/M/1 chain

Features:
  - PDP-11 compatible 16-bit processor
  - Used in NATO crypto equipment
  - ~8000 transistors
  - 5 MHz clock
  - Military/defense applications

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

class MiprocModel(BaseProcessorModel):
    """
    Plessey MIPROC Grey-Box Queueing Model

    Architecture: Sequential Execution (Era: 1975)
    - PDP-11 compatible instruction set
    - 16-bit data path
    - ~8000 transistors
    - Used in NATO cryptographic equipment
    - CPI = sum of stage times

    The Plessey MIPROC was a single-chip implementation of a PDP-11
    compatible processor, developed for military and defense applications.
    It was notably used in NATO cryptographic equipment, taking advantage
    of the PDP-11's well-proven instruction set architecture.
    """

    # Processor specifications
    name = "Plessey MIPROC"
    manufacturer = "Plessey"
    year = 1975
    clock_mhz = 5.0
    transistor_count = 8000
    data_width = 16
    address_width = 16

    def __init__(self):
        # Stage timing (cycles)
        self.stage_timing = {
            'fetch': 2,      # Instruction fetch (16-bit)
            'decode': 1,     # Decode
            'execute': 2,    # Execute
            'memory': 3,     # Memory access
            'writeback': 0,  # Register writeback
        }

        # Instruction categories - PDP-11 compatible
        # Calibrated for CPI = 5.0
        # Calculation: 0.25*3 + 0.20*3 + 0.15*6 + 0.10*7 + 0.20*5 + 0.10*6
        #            = 0.75 + 0.60 + 0.90 + 0.70 + 1.00 + 0.60 = 4.55
        # Adjust: 0.20*3 + 0.15*3 + 0.20*6 + 0.10*7 + 0.20*5 + 0.15*6
        #       = 0.60 + 0.45 + 1.20 + 0.70 + 1.00 + 0.90 = 4.85
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 3, 0, "ALU operations (ADD, SUB, BIC, BIS)"),
            'data_transfer': InstructionCategory('data_transfer', 3, 0, "Data transfer (MOV register)"),
            'memory': InstructionCategory('memory', 6, 0, "Memory operations (MOV memory, autoincrement)"),
            'io': InstructionCategory('io', 7, 0, "I/O operations (device register access)"),
            'control': InstructionCategory('control', 5, 0, "Control flow (BR, BNE, JMP, JSR)"),
            'stack': InstructionCategory('stack', 6, 0, "Stack operations (JSR, RTS, MARK)"),
        }

        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.20,
                'io': 0.10,
                'control': 0.25,
                'stack': 0.15,
            }, "Typical PDP-11 compatible workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.20,
                'memory': 0.15,
                'io': 0.05,
                'control': 0.15,
                'stack': 0.05,
            }, "Compute-intensive workload"),
            'crypto': WorkloadProfile('crypto', {
                'alu': 0.35,
                'data_transfer': 0.15,
                'memory': 0.20,
                'io': 0.10,
                'control': 0.10,
                'stack': 0.10,
            }, "Cryptographic processing workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.10,
                'data_transfer': 0.10,
                'memory': 0.15,
                'io': 0.10,
                'control': 0.35,
                'stack': 0.20,
            }, "Control-flow intensive workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 3.12495600140797,
            'control': 0.5033438929954206,
            'data_transfer': 0.03965739762992279,
            'io': -1.153701748210721,
            'memory': -2.1681332864015137,
            'stack': -1.0102076733544438,
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
            "target_cpi": 5.0,
            "tests": [],
            "passed": 0,
            "total": 0,
            "accuracy_percent": None
        }

        # Test typical workload CPI
        analysis = self.analyze('typical')
        expected_cpi = 5.0
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
            ("memory", 6),
            ("io", 7),
            ("control", 5),
            ("stack", 6),
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
