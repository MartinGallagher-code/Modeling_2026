#!/usr/bin/env python3
"""
NEC V60 Grey-Box Queueing Model
=================================

Architecture: Sequential/Pipelined Execution (1986)
Queueing Model: Serial M/M/1 chain

Features:
  - Japan's first major 32-bit microprocessor
  - New proprietary ISA (not x86 compatible)
  - ~375,000 transistors
  - 16 MHz clock
  - Floating point and string instructions

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

class NecV60Model(BaseProcessorModel):
    """
    NEC V60 Grey-Box Queueing Model

    Architecture: Sequential/Early Pipeline Execution (Era: 1986)
    - Japan's first major 32-bit microprocessor
    - New proprietary ISA (not x86 compatible)
    - ~375,000 transistors
    - On-chip floating point
    - String manipulation instructions
    - CPI = sum of stage times

    The NEC V60 was Japan's first significant 32-bit microprocessor,
    featuring a completely new instruction set architecture (not x86
    compatible like NEC's V20/V30). It included on-chip floating point
    and was used in NEC workstations and embedded systems.
    """

    # Processor specifications
    name = "NEC V60"
    manufacturer = "NEC"
    year = 1986
    clock_mhz = 16.0
    transistor_count = 375000
    data_width = 32
    address_width = 32  # 4GB address space

    def __init__(self):
        # Stage timing (cycles)
        self.stage_timing = {
            'fetch': 1,      # Instruction fetch (32-bit bus)
            'decode': 1,     # Decode
            'execute': 1,    # Execute
            'memory': 1,     # Memory access
            'writeback': 0,  # Register writeback
        }

        # Instruction categories - NEC V60 proprietary ISA
        # Calibrated for CPI = 3.0
        # Calculation: 0.30*2 + 0.20*2 + 0.20*4 + 0.15*3 + 0.05*8 + 0.10*6
        #            = 0.60 + 0.40 + 0.80 + 0.45 + 0.40 + 0.60 = 3.25
        # Adjust: 0.30*2 + 0.25*2 + 0.20*4 + 0.15*3 + 0.05*8 + 0.05*6
        #       = 0.60 + 0.50 + 0.80 + 0.45 + 0.40 + 0.30 = 3.05
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2, 0, "ALU operations (ADD, SUB, MUL, AND, OR) - 32-bit"),
            'data_transfer': InstructionCategory('data_transfer', 2, 0, "Data transfer (MOV, MOVEA) - 32-bit"),
            'memory': InstructionCategory('memory', 4, 0, "Memory operations (load/store, indexed)"),
            'control': InstructionCategory('control', 3, 0, "Control flow (BR, Bcc, JSR, RET)"),
            'float': InstructionCategory('float', 8, 0, "Floating point operations (FADD, FMUL)"),
            'string': InstructionCategory('string', 6, 0, "String manipulation (MOVS, CMPS)"),
        }

        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.25,
                'memory': 0.20,
                'control': 0.15,
                'float': 0.05,
                'string': 0.05,
            }, "Typical 32-bit workstation workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'data_transfer': 0.20,
                'memory': 0.15,
                'control': 0.10,
                'float': 0.05,
                'string': 0.05,
            }, "Compute-intensive workload"),
            'float_heavy': WorkloadProfile('float_heavy', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.20,
                'control': 0.10,
                'float': 0.30,
                'string': 0.10,
            }, "Floating-point intensive workload"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.35,
                'control': 0.10,
                'float': 0.05,
                'string': 0.20,
            }, "Memory and string intensive workload"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.15,
                'memory': 0.15,
                'control': 0.35,
                'float': 0.05,
                'string': 0.10,
            }, "Control-flow intensive workload"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

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
            base_cpi=base_cpi,
            correction_delta=correction_delta
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
            ("data_transfer", 2),
            ("memory", 4),
            ("control", 3),
            ("float", 8),
            ("string", 6),
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
