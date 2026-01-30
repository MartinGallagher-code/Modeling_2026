#!/usr/bin/env python3
"""
Fairchild 9440 MICROFLAME Grey-Box Queueing Model
====================================================

Architecture: 16-bit microprocessor (1979)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - Data General Nova ISA on a single chip
  - I2L (Integrated Injection Logic) bipolar process
  - ~5000 transistors
  - 10 MHz clock
  - 16-bit data bus
  - Faster than original Data General Nova minicomputer
  - Full Nova instruction set compatibility
  - 4 accumulators (AC0-AC3)

Calibrated: 2026-01-29
Target CPI: 3.5 (16-bit register ops fast, memory slower)
Clock: 10 MHz
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

class Fairchild9440Model(BaseProcessorModel):
    """
    Fairchild 9440 MICROFLAME Grey-Box Queueing Model

    Architecture: 16-bit I2L bipolar microprocessor (1979)
    - Data General Nova ISA on a single chip
    - I2L (Integrated Injection Logic) process
    - 4 accumulators, 16-bit operations
    - Faster than original Nova minicomputer
    - CPI ~3.5 (register ops fast, memory slower)
    """

    # Processor specifications
    name = "Fairchild 9440"
    manufacturer = "Fairchild Semiconductor"
    year = 1979
    clock_mhz = 10.0
    transistor_count = 5000
    data_width = 16
    address_width = 15  # Nova architecture: 15-bit (32K words)

    def __init__(self):
        # Fairchild 9440 MICROFLAME instruction timing
        # Nova ISA with single-chip implementation
        # I2L bipolar process gives fast register operations
        #
        # Nova instruction set timing on 9440:
        #   ADD/SUB/COM/NEG (register): 2 cycles (fast register ALU)
        #   MOV (register-register): 2 cycles
        #   LDA (load accumulator from memory): 4 cycles
        #   STA (store accumulator to memory): 4 cycles
        #   ISZ (increment and skip if zero): 4 cycles
        #   DSZ (decrement and skip if zero): 4 cycles
        #   I/O instructions (DIA, DOA, etc.): 6 cycles
        #   JMP (jump): 3 cycles
        #   JSR (jump to subroutine): 5 cycles
        #   RET (return): 5 cycles
        #   SKP (skip): 2 cycles

        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.0, 0,
                "ADD/SUB/COM/NEG @2 cycles - 16-bit register ALU ops"),
            'data_transfer': InstructionCategory('data_transfer', 2.0, 0,
                "MOV AC,AC @2 cycles - register-to-register"),
            'memory': InstructionCategory('memory', 5.0, 0,
                "LDA/STA @5 cycles - 16-bit memory access with indirect addressing"),
            'io': InstructionCategory('io', 6.0, 0,
                "DIA/DOA/DIB/DOB @6 cycles - device I/O"),
            'control': InstructionCategory('control', 3.0, 0,
                "JMP @3, SKP @2 - branch and skip"),
            'stack': InstructionCategory('stack', 6.0, 0,
                "JSR @6, RET @6 - subroutine call/return with AC3 save"),
        }

        # Workload profiles for Nova-compatible minicomputer
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.20,
                'memory': 0.25,
                'io': 0.05,
                'control': 0.15,
                'stack': 0.10,
            }, "Typical Nova workload (general purpose computing)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.20,
                'memory': 0.15,
                'io': 0.02,
                'control': 0.15,
                'stack': 0.08,
            }, "Compute-intensive (scientific calculation)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.40,
                'io': 0.05,
                'control': 0.15,
                'stack': 0.10,
            }, "Memory-intensive (data processing)"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'data_transfer': 0.10,
                'memory': 0.15,
                'io': 0.10,
                'control': 0.35,
                'stack': 0.15,
            }, "Control-flow intensive (OS, I/O handling)"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -1.292350,
            'control': -1.958542,
            'data_transfer': 0.547641,
            'io': -0.568479,
            'memory': 2.320981,
            'stack': -0.444808
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        base_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            base_cpi += contrib
            contributions[cat_name] = contrib

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

        # Test 1: CPI within expected range
        result = self.analyze('typical')
        expected_cpi = 3.5
        cpi_error = abs(result.cpi - expected_cpi) / expected_cpi * 100
        tests.append({
            'name': 'CPI accuracy',
            'passed': cpi_error < 5.0,
            'expected': f'{expected_cpi} +/- 5%',
            'actual': f'{result.cpi:.2f} ({cpi_error:.1f}% error)'
        })

        # Test 2: Workload weights sum to 1.0
        for profile_name, profile in self.workload_profiles.items():
            weight_sum = sum(profile.category_weights.values())
            tests.append({
                'name': f'Weights sum ({profile_name})',
                'passed': 0.99 <= weight_sum <= 1.01,
                'expected': '1.0',
                'actual': f'{weight_sum:.2f}'
            })

        # Test 3: All cycle counts are positive and reasonable
        for cat_name, cat in self.instruction_categories.items():
            cycles = cat.total_cycles
            tests.append({
                'name': f'Cycle count ({cat_name})',
                'passed': 0.5 <= cycles <= 200.0,
                'expected': '0.5-200 cycles',
                'actual': f'{cycles:.1f}'
            })

        # Test 4: IPC is in valid range
        tests.append({
            'name': 'IPC range',
            'passed': 0.05 <= result.ipc <= 1.5,
            'expected': '0.05-1.5',
            'actual': f'{result.ipc:.3f}'
        })

        # Test 5: All workloads produce valid results
        for workload in self.workload_profiles.keys():
            try:
                r = self.analyze(workload)
                valid = r.cpi > 0 and r.ipc > 0 and r.ips > 0
                tests.append({
                    'name': f'Workload analysis ({workload})',
                    'passed': valid,
                    'expected': 'Valid CPI/IPC/IPS',
                    'actual': f'CPI={r.cpi:.2f}' if valid else 'Invalid'
                })
            except Exception as e:
                tests.append({
                    'name': f'Workload analysis ({workload})',
                    'passed': False,
                    'expected': 'No error',
                    'actual': str(e)
                })

        passed = sum(1 for t in tests if t['passed'])
        return {
            'tests': tests,
            'passed': passed,
            'total': len(tests),
            'accuracy_percent': 100.0 - cpi_error
        }

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles
