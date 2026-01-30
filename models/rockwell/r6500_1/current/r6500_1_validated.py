#!/usr/bin/env python3
"""
Rockwell R6500/1 Grey-Box Queueing Model
==========================================

Architecture: Sequential Execution (1978)
Queueing Model: Serial M/M/1 chain

Features:
  - Single-chip 6502 MCU
  - Same instruction timing as MOS 6502
  - 1 MHz clock
  - 2KB ROM, 64 bytes RAM on-chip
  - On-chip I/O ports and timer

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
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations, base_cpi if base_cpi is not None else cpi, correction_delta)

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

class R6500_1Model(BaseProcessorModel):
    """
    Rockwell R6500/1 Grey-Box Queueing Model

    Architecture: Sequential Execution (Era: 1978)
    - Single-chip 6502 MCU
    - Same instruction set and timing as MOS 6502
    - On-chip ROM (2KB), RAM (64 bytes), I/O ports, timer
    - CPI = sum of stage times

    The R6500/1 was Rockwell's single-chip microcontroller based on the
    MOS 6502 core. It integrated ROM, RAM, I/O, and timer on a single
    chip for embedded applications, with identical instruction timing
    to the standard 6502.
    """

    # Processor specifications
    name = "Rockwell R6500/1"
    manufacturer = "Rockwell"
    year = 1978
    clock_mhz = 1.0
    transistor_count = 10000  # Estimated for 6502 + peripherals
    data_width = 8
    address_width = 16

    def __init__(self):
        # Stage timing (cycles) - same as 6502
        self.stage_timing = {
            'fetch': 1,      # Instruction fetch
            'decode': 1,     # Decode
            'execute': 1,    # Execute
            'memory': 1,     # Memory access
            'writeback': 0,  # Register writeback
        }

        # Instruction categories - same as 6502
        # Calibrated for CPI = 3.0 (same as 6502)
        # Calculation: 0.30*2 + 0.20*3 + 0.20*4 + 0.15*3 + 0.15*3
        #            = 0.60 + 0.60 + 0.80 + 0.45 + 0.45 = 2.90
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2, 0, "ALU operations (ADC, SBC, AND, ORA, EOR)"),
            'data_transfer': InstructionCategory('data_transfer', 3, 0, "Data transfer (LDA, STA, TAX, TXA)"),
            'memory': InstructionCategory('memory', 4, 0, "Memory operations (indirect, indexed)"),
            'control': InstructionCategory('control', 3, 0, "Control flow (BNE, BEQ, JMP, JSR)"),
            'stack': InstructionCategory('stack', 3, 0, "Stack operations (PHA, PLA, JSR/RTS)"),
        }

        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.20,
                'memory': 0.20,
                'control': 0.15,
                'stack': 0.15,
            }, "Typical embedded 6502 workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'data_transfer': 0.20,
                'memory': 0.15,
                'control': 0.10,
                'stack': 0.10,
            }, "Compute-intensive workload"),
            'io_heavy': WorkloadProfile('io_heavy', {
                'alu': 0.15,
                'data_transfer': 0.25,
                'memory': 0.30,
                'control': 0.15,
                'stack': 0.15,
            }, "I/O-intensive embedded workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.15,
                'control': 0.35,
                'stack': 0.20,
            }, "Control-flow intensive workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.885947,
            'control': 0.101130,
            'data_transfer': 0.445456,
            'memory': -1.071033,
            'stack': -0.372255
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

        # System identification: apply correction terms
        base_cpi = total_cpi
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
            base_cpi=base_cpi, correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        """Run validation tests"""
        results = {
            "processor": self.name,
            "target_cpi": 3.0,
            "tests": [],
            "passed": 0,
            "total": 0,
            "accuracy_percent": None
        }

        # Test typical workload CPI
        analysis = self.analyze('typical')
        expected_cpi = 3.0
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
            ("alu", 2),
            ("data_transfer", 3),
            ("memory", 4),
            ("control", 3),
            ("stack", 3),
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
