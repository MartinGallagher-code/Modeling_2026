#!/usr/bin/env python3
"""
Intersil 6100 (IM6100) Grey-Box Queueing Model
=============================================

Architecture: 12-bit CMOS (PDP-8 on a chip) (1975)
Queueing Model: Multi-state sequential execution

Features:
  - CMOS PDP-8/E instruction set implementation
  - 12-bit word size
  - Variable instruction timing (6-22 states)
  - Fully static design (can halt indefinitely)
  - 4K word address space (expandable to 32K)

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

class Intersil6100Model(BaseProcessorModel):
    """
    Intersil 6100 Grey-Box Queueing Model

    Architecture: PDP-8 on a Chip (1975)
    - 12-bit word size
    - 8 basic instructions (PDP-8/E compatible)
    - Variable timing: 6-22 states per instruction
    - Direct/indirect/autoindex addressing modes
    - CMOS - fully static operation

    Target CPI: ~12 states (weighted average)
    At 4 MHz: ~333 KIPS
    """

    # Processor specifications
    name = "Intersil 6100"
    manufacturer = "Intersil"
    year = 1975
    clock_mhz = 4.0  # 4 MHz at 5V
    transistor_count = 4000  # Estimated for CMOS
    data_width = 12
    address_width = 12  # 4K words

    def __init__(self):
        # IM6100 instruction timing in states (500ns each at 4 MHz)
        # Mix of direct and indirect addressing assumed
        # Target CPI: ~12 states
        # Calculation: 0.25*10 + 0.25*10 + 0.15*12 + 0.15*12 + 0.10*12 + 0.10*6 = 10.5
        self.instruction_categories = {
            'arithmetic': InstructionCategory('arithmetic', 10, 0, "TAD direct @10, indirect @15 states"),
            'logic': InstructionCategory('logic', 10, 0, "AND direct @10, indirect @15 states"),
            'memory': InstructionCategory('memory', 12, 0, "DCA @11, ISZ @16 states avg"),
            'jump': InstructionCategory('jump', 12, 0, "JMP @10, JMS @11 direct, +5 indirect"),
            'io': InstructionCategory('io', 12, 0, "IOT @12 states"),
            'operate': InstructionCategory('operate', 6, 0, "OPR group @6 states"),
        }

        # Workload profiles
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

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'arithmetic': 8.565965,
            'io': 24.000000,
            'jump': 19.454143,
            'logic': 14.674849,
            'memory': 24.000000,
            'operate': 12.000000
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using multi-state execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Calculate weighted average CPI (in states)
        base_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

        # Identify bottleneck
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
        tests = []
        passed = 0

        # Test 1: CPI should be ~10.5 states
        result = self.analyze('typical')
        target_cpi = 10.5
        error = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {
            "name": "CPI accuracy vs target 10.5 states",
            "expected": target_cpi,
            "actual": result.cpi,
            "error_percent": error,
            "passed": error < 5.0
        }
        tests.append(test1)
        if test1["passed"]: passed += 1

        # Test 2: CPI in valid range (6-22 states)
        test2 = {
            "name": "CPI in valid range (6-22)",
            "expected": "6-22 states",
            "actual": result.cpi,
            "passed": 6 <= result.cpi <= 22
        }
        tests.append(test2)
        if test2["passed"]: passed += 1

        # Test 3: IPS approximately correct (~190 KIPS)
        state_time_us = 0.5
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

        # Test 5: OPR is fastest (6 states)
        test5 = {
            "name": "OPR fastest at 6 states",
            "expected": 6,
            "actual": self.instruction_categories['operate'].total_cycles,
            "passed": self.instruction_categories['operate'].total_cycles == 6
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
