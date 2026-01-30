#!/usr/bin/env python3
"""
NEC uPD1007C Grey-Box Queueing Model
======================================

Architecture: 4-bit Calculator CPU (1978)
Queueing Model: Sequential execution with variable instruction timing

Features:
  - Custom NEC calculator CPU used in Casio calculators
  - 4-bit data path with BCD arithmetic
  - Integrated display driver
  - Low-power CMOS design for battery operation
  - ~6,000 transistors

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

class Upd1007cModel(BaseProcessorModel):
    """
    NEC uPD1007C Grey-Box Queueing Model

    Architecture: 4-bit Calculator CPU (1978)
    - Custom NEC CMOS calculator CPU
    - 4-bit data path with native BCD arithmetic
    - Integrated LCD/LED display driver
    - Designed for Casio scientific and programmable calculators
    - Low-power CMOS for battery-operated devices
    """

    # Processor specifications
    name = "uPD1007C"
    manufacturer = "NEC"
    year = 1978
    clock_mhz = 0.5  # 500 kHz typical
    transistor_count = 6000
    data_width = 4
    address_width = 12  # 4 KB address space

    def __init__(self):
        # Instruction categories with typical cycle counts
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 5, 0,
                "ALU: ADD, SUB, INC, DEC, CMP @5 cycles avg"
            ),
            'bcd': InstructionCategory(
                'bcd', 7, 0,
                "BCD: Multi-digit BCD arithmetic, DAA @7 cycles avg"
            ),
            'memory': InstructionCategory(
                'memory', 6, 0,
                "Memory: Load/store to register file @6 cycles avg"
            ),
            'control': InstructionCategory(
                'control', 4, 0,
                "Control: Branch, skip, call/return @4 cycles avg"
            ),
            'display': InstructionCategory(
                'display', 9, 0,
                "Display: LCD segment drive, scan @9 cycles avg"
            ),
        }

        # Workload profiles
        # typical: 0.20*5 + 0.20*7 + 0.20*6 + 0.24*4 + 0.16*9 = 6.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.20,
                'bcd': 0.20,
                'memory': 0.20,
                'control': 0.24,
                'display': 0.16,
            }, "Typical Casio calculator workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.25,
                'bcd': 0.40,
                'memory': 0.10,
                'control': 0.15,
                'display': 0.10,
            }, "Heavy scientific computation (trig, log)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'bcd': 0.15,
                'memory': 0.35,
                'control': 0.15,
                'display': 0.20,
            }, "Memory-intensive (program/data access)"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'bcd': 0.10,
                'memory': 0.15,
                'control': 0.40,
                'display': 0.20,
            }, "Control-flow heavy (key scan, menu navigation)"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using weighted instruction mix model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        base_cpi = 0.0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            contributions[cat_name] = contrib
            base_cpi += contrib

        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

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
        tests = []
        passed = 0

        # Test 1: Typical CPI should be ~6.0
        result = self.analyze('typical')
        target_cpi = 6.0
        error_pct = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {
            "name": "CPI accuracy (typical)",
            "expected": target_cpi,
            "actual": round(result.cpi, 4),
            "error_pct": round(error_pct, 2),
            "passed": error_pct < 5.0
        }
        tests.append(test1)
        if test1["passed"]: passed += 1

        # Test 2: IPS at 500 kHz
        expected_ips = self.clock_mhz * 1e6 / target_cpi
        test2 = {
            "name": "IPS at 500 kHz",
            "expected": round(expected_ips),
            "actual": round(result.ips),
            "passed": abs(result.ips - expected_ips) / expected_ips < 0.05
        }
        tests.append(test2)
        if test2["passed"]: passed += 1

        # Test 3: Compute workload should have higher CPI (more BCD)
        compute = self.analyze('compute')
        test3 = {
            "name": "Compute CPI > typical (heavier BCD)",
            "expected": "> 6.0",
            "actual": round(compute.cpi, 4),
            "passed": compute.cpi > target_cpi
        }
        tests.append(test3)
        if test3["passed"]: passed += 1

        # Test 4: Control workload should have lower CPI
        control = self.analyze('control')
        test4 = {
            "name": "Control CPI < typical (lighter ops)",
            "expected": "< 6.0",
            "actual": round(control.cpi, 4),
            "passed": control.cpi < target_cpi
        }
        tests.append(test4)
        if test4["passed"]: passed += 1

        # Test 5: All workloads produce valid CPI
        for wl_name in self.workload_profiles:
            r = self.analyze(wl_name)
            test = {
                "name": f"Valid CPI range ({wl_name})",
                "expected": "4.0 - 9.0",
                "actual": round(r.cpi, 4),
                "passed": 4.0 <= r.cpi <= 9.0
            }
            tests.append(test)
            if test["passed"]: passed += 1

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
