#!/usr/bin/env python3
"""
General Instrument PIC1650 Grey-Box Queueing Model
==================================================

Architecture: 8-bit Microcontroller (1977)
Queueing Model: Pipelined single-cycle execution

Features:
  - First PIC microcontroller
  - Harvard architecture (12-bit instruction, 8-bit data)
  - Most instructions: 1 instruction cycle (4 oscillator cycles)
  - Branch/call: 2 instruction cycles
  - 33 instructions total
  - 2-level hardware stack

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

class Pic1650Model(BaseProcessorModel):
    """
    GI PIC1650 Grey-Box Queueing Model

    Architecture: First PIC Microcontroller (1977)
    - Harvard architecture
    - Most instructions: 1 cycle (4 osc clocks)
    - Branch/call/skip: 2 cycles when taken
    - 512 words x 12-bit ROM
    - 32 bytes RAM
    - 33 instructions

    Target CPI: ~1.1 (mostly single-cycle with some branches)
    """

    # Processor specifications
    name = "PIC1650"
    manufacturer = "General Instrument"
    year = 1977
    clock_mhz = 0.25  # 1 MHz oscillator / 4 = 250 kHz instruction rate
    transistor_count = 3000  # Estimated
    data_width = 8
    address_width = 9  # 512 words

    def __init__(self):
        # PIC1650 has mostly single-cycle instructions
        # Only branches/calls take 2 cycles
        # Target CPI: ~1.1
        # Calculation: 0.35*1 + 0.25*1 + 0.15*1 + 0.10*1 + 0.10*2 + 0.05*2 = 1.15
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1, 0, "ALU: ADDWF, ANDWF, SUBWF @1 cycle"),
            'data_transfer': InstructionCategory('data_transfer', 1, 0, "Transfer: MOVF, MOVWF @1 cycle"),
            'bit_ops': InstructionCategory('bit_ops', 1, 0, "Bit: BCF, BSF, BTFSC @1 cycle"),
            'literal': InstructionCategory('literal', 1, 0, "Literal: MOVLW, ADDLW @1 cycle"),
            'branch': InstructionCategory('branch', 2, 0, "Branch: GOTO @2 cycles"),
            'call': InstructionCategory('call', 2, 0, "Call: CALL, RETLW @2 cycles"),
        }

        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.35,
                'data_transfer': 0.25,
                'bit_ops': 0.15,
                'literal': 0.10,
                'branch': 0.10,
                'call': 0.05,
            }, "Typical embedded controller workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.50,
                'data_transfer': 0.20,
                'bit_ops': 0.10,
                'literal': 0.10,
                'branch': 0.08,
                'call': 0.02,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.20,
                'data_transfer': 0.40,
                'bit_ops': 0.10,
                'literal': 0.15,
                'branch': 0.10,
                'call': 0.05,
            }, "Data-movement intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.15,
                'bit_ops': 0.20,
                'literal': 0.10,
                'branch': 0.25,
                'call': 0.10,
            }, "Control-flow and I/O intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.264141,
            'bit_ops': -0.312174,
            'branch': -0.509403,
            'call': -0.341125,
            'data_transfer': 0.513034,
            'literal': -1.058853
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using pipelined execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Calculate weighted average CPI
        base_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

        # Identify bottleneck
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
        tests = []
        passed = 0

        # Test 1: CPI should be ~1.15
        result = self.analyze('typical')
        target_cpi = 1.15
        error = abs(result.cpi - target_cpi) / target_cpi * 100
        test1 = {
            "name": "CPI accuracy vs target 1.15",
            "expected": target_cpi,
            "actual": result.cpi,
            "error_percent": error,
            "passed": error < 5.0
        }
        tests.append(test1)
        if test1["passed"]: passed += 1

        # Test 2: IPS at 250 kHz instruction rate
        expected_ips = 250000 / 1.15  # ~217,000
        test2 = {
            "name": "IPS approximately correct",
            "expected": f"~{int(expected_ips):,}",
            "actual": f"{int(result.ips):,}",
            "passed": abs(result.ips - expected_ips) / expected_ips < 0.05
        }
        tests.append(test2)
        if test2["passed"]: passed += 1

        # Test 3: Single-cycle instructions are 1 cycle
        for cat_name in ['alu', 'data_transfer', 'bit_ops', 'literal']:
            test = {
                "name": f"{cat_name} single-cycle",
                "expected": 1,
                "actual": self.instruction_categories[cat_name].total_cycles,
                "passed": self.instruction_categories[cat_name].total_cycles == 1
            }
            tests.append(test)
            if test["passed"]: passed += 1

        # Test 4: Branch/call are 2 cycles
        for cat_name in ['branch', 'call']:
            test = {
                "name": f"{cat_name} two-cycle",
                "expected": 2,
                "actual": self.instruction_categories[cat_name].total_cycles,
                "passed": self.instruction_categories[cat_name].total_cycles == 2
            }
            tests.append(test)
            if test["passed"]: passed += 1

        # Test 5: Workload weight sums
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
