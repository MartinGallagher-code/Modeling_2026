#!/usr/bin/env python3
"""
RCA CDP1806 Grey-Box Queueing Model
====================================

Architecture: Final COSMAC (1985)
Queueing Model: Serial M/M/1 chain

Features:
  - Final enhanced COSMAC variant
  - Faster clock support (up to 5 MHz)
  - Additional instructions
  - Improved bus timing
  - Compatible with 1802/1804 instruction set

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

class Cdp1806Model(BaseProcessorModel):
    """
    RCA CDP1806 Grey-Box Queueing Model

    Architecture: Final COSMAC (Era: 1985)
    - Enhanced COSMAC with faster clock
    - Additional instructions
    - Improved bus timing
    - CPI ~8.0 (vs 1802's 12.0, 1804's 10.0)

    Target CPI: ~8.0
    At 5 MHz: ~625 KIPS
    """

    # Processor specifications
    name = "RCA CDP1806"
    manufacturer = "RCA"
    year = 1985
    clock_mhz = 5.0  # Up to 5 MHz
    transistor_count = 8000  # More transistors for enhanced features
    data_width = 8
    address_width = 16

    def __init__(self):
        # CDP1806 instruction timing - fastest COSMAC
        # Calibrated for CPI = 8.0
        # Calculation: 0.30*5 + 0.15*8 + 0.25*9 + 0.15*9 + 0.10*10 + 0.05*14 = 8.0
        self.instruction_categories = {
            'register_ops': InstructionCategory('register_ops', 5, 0, "Register-to-register (fastest COSMAC)"),
            'immediate': InstructionCategory('immediate', 8, 0, "Immediate operand"),
            'memory_read': InstructionCategory('memory_read', 9, 0, "Load from memory"),
            'memory_write': InstructionCategory('memory_write', 9, 0, "Store to memory"),
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
            'branch': -1.500573,
            'call_return': -6.999997,
            'immediate': 0.297599,
            'memory_read': -1.008001,
            'memory_write': -0.887084,
            'register_ops': 2.801601
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
        tests = []
        passed = 0

        # Test 1: CPI should be ~8.0
        result = self.analyze('typical')
        target_cpi = 8.0
        error = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {
            "name": "CPI accuracy vs target 8.0",
            "expected": target_cpi,
            "actual": result.cpi,
            "error_percent": error,
            "passed": error < 5.0
        }
        tests.append(test1)
        if test1["passed"]: passed += 1

        # Test 2: CPI in valid range (5-14 cycles)
        test2 = {
            "name": "CPI in valid range (5-14)",
            "expected": "5-14 cycles",
            "actual": result.cpi,
            "passed": 5 <= result.cpi <= 14
        }
        tests.append(test2)
        if test2["passed"]: passed += 1

        # Test 3: IPS approximately correct (~625 KIPS)
        expected_ips = self.clock_mhz * 1e6 / target_cpi
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

        # Test 5: Faster than 1804 (CPI < 10)
        test5 = {
            "name": "Faster than 1804 (CPI < 10)",
            "expected": "< 10",
            "actual": result.cpi,
            "passed": result.cpi < 10
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
