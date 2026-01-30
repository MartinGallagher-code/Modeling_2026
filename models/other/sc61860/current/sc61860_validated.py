#!/usr/bin/env python3
"""
Sharp SC61860 Grey-Box Queueing Model
======================================

Architecture: 8-bit Pocket Computer CPU (1980)
Queueing Model: Sequential execution with variable instruction timing

Features:
  - Custom Sharp CPU used in PC-1211, PC-1245, PC-1500 pocket computers
  - 8-bit data path with 96 bytes internal RAM
  - LCD display controller integration
  - 512 bytes internal ROM for character generator
  - ~8,000 transistors

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

class Sc61860Model(BaseProcessorModel):
    """
    Sharp SC61860 Grey-Box Queueing Model

    Architecture: 8-bit pocket computer CPU (1980)
    - Custom Sharp CMOS CPU for pocket computers
    - 8-bit data path, accumulator-based architecture
    - 96 bytes internal RAM, 2KB-24KB external ROM
    - Integrated LCD display controller
    - Used in Sharp PC-1211, PC-1245, PC-1500 series
    """

    # Processor specifications
    name = "SC61860"
    manufacturer = "Sharp"
    year = 1980
    clock_mhz = 0.576  # 576 kHz
    transistor_count = 8000
    data_width = 8
    address_width = 16  # 64 KB address space

    def __init__(self):
        # Instruction categories with typical cycle counts
        self.instruction_categories = {
            'alu': InstructionCategory(
                'alu', 3, 0,
                "ALU: ADD, SUB, AND, OR, CMP @3 cycles avg"
            ),
            'data_transfer': InstructionCategory(
                'data_transfer', 4, 0,
                "Transfer: LD, ST, MOV between registers @4 cycles avg"
            ),
            'memory': InstructionCategory(
                'memory', 6, 0,
                "Memory: External memory access, indirect @6 cycles avg"
            ),
            'control': InstructionCategory(
                'control', 5, 0,
                "Control: JP, CALL, RET, conditional branches @5 cycles avg"
            ),
            'display': InstructionCategory(
                'display', 8, 0,
                "Display: LCD controller operations @8 cycles avg"
            ),
        }

        # Workload profiles
        # typical: 0.24*3 + 0.25*4 + 0.10*6 + 0.20*5 + 0.21*8 = 5.0
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.24,
                'data_transfer': 0.25,
                'memory': 0.10,
                'control': 0.20,
                'display': 0.21,
            }, "Typical pocket computer BASIC interpreter workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.20,
                'memory': 0.10,
                'control': 0.15,
                'display': 0.15,
            }, "Compute-intensive (math, scientific calculations)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.30,
                'memory': 0.30,
                'control': 0.10,
                'display': 0.15,
            }, "Memory-intensive (array/string operations)"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.10,
                'control': 0.40,
                'display': 0.20,
            }, "Control-flow heavy (BASIC interpreter loop, UI)"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 2.028711,
            'control': -0.240075,
            'data_transfer': 0.417834,
            'display': -2.238236,
            'memory': -0.733047
        }

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
        tests = []
        passed = 0

        # Test 1: Typical CPI should be ~5.0
        result = self.analyze('typical')
        target_cpi = 5.0
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

        # Test 2: IPS at 576 kHz
        expected_ips = self.clock_mhz * 1e6 / target_cpi
        test2 = {
            "name": "IPS at 576 kHz",
            "expected": round(expected_ips),
            "actual": round(result.ips),
            "passed": abs(result.ips - expected_ips) / expected_ips < 0.05
        }
        tests.append(test2)
        if test2["passed"]: passed += 1

        # Test 3: Compute workload should have lower CPI (more ALU)
        compute = self.analyze('compute')
        test3 = {
            "name": "Compute CPI < typical (more fast ALU ops)",
            "expected": "< 5.0",
            "actual": round(compute.cpi, 4),
            "passed": compute.cpi < target_cpi
        }
        tests.append(test3)
        if test3["passed"]: passed += 1

        # Test 4: Memory workload should have higher CPI
        memory = self.analyze('memory')
        test4 = {
            "name": "Memory CPI > typical (more memory ops)",
            "expected": "> 5.0",
            "actual": round(memory.cpi, 4),
            "passed": memory.cpi > target_cpi
        }
        tests.append(test4)
        if test4["passed"]: passed += 1

        # Test 5: All workloads produce valid CPI
        for wl_name in self.workload_profiles:
            r = self.analyze(wl_name)
            test = {
                "name": f"Valid CPI range ({wl_name})",
                "expected": "3.0 - 8.0",
                "actual": round(r.cpi, 4),
                "passed": 3.0 <= r.cpi <= 8.0
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
