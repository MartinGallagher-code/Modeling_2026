#!/usr/bin/env python3
"""
Fujitsu MB8841 Grey-Box Queueing Model
========================================

Architecture: 4-bit microcontroller (1977)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - 4-bit MCU used in Namco arcade games
  - ~3000 transistors, NMOS technology
  - Harvard architecture (separate program/data memory)
  - 1KB ROM, 32 nibbles RAM
  - 64 instructions
  - 1 MHz clock
  - Used in Galaga, Xevious, Bosconian arcade cabinets

Calibrated: 2026-01-29
Target CPI: 4.0 (most instructions 3-5 cycles, I/O 6-8)
Clock: 1 MHz
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
            ipc = 1.0 / cpi if cpi > 0 else 0.0
            ips = clock_mhz * 1e6 * ipc
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                       base_cpi=base_cpi if base_cpi is not None else cpi, correction_delta=correction_delta)

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

class MB8841Model(BaseProcessorModel):
    """
    Fujitsu MB8841 Grey-Box Queueing Model

    Architecture: 4-bit NMOS microcontroller (1977)
    - Harvard architecture (separate program/data memory)
    - 1KB ROM, 32 nibbles RAM
    - 64 instructions, 1 MHz clock
    - Used in Namco arcade games (Galaga, Xevious, Bosconian)
    - CPI ~4.0 for typical arcade game workloads
    """

    # Processor specifications
    name = "MB8841"
    manufacturer = "Fujitsu"
    year = 1977
    clock_mhz = 1.0
    transistor_count = 3000
    data_width = 4
    address_width = 10  # 1KB ROM address space

    def __init__(self):
        # MB8841 instruction timing
        # Most instructions are 3-5 machine cycles
        # I/O port operations are slower at 6-8 cycles
        # Harvard architecture means separate instruction/data fetches
        #
        # Typical instruction timings:
        #   ADD/SUB/INC/DEC: 3 cycles (4-bit ALU operations)
        #   MOV (register): 3 cycles
        #   LD/ST (RAM): 4 cycles (nibble access to 32-nibble RAM)
        #   IN/OUT (port): 6 cycles (external I/O operations)
        #   JMP/CALL: 5 cycles (branch with pipeline flush)
        #   RET: 5 cycles (return from subroutine)

        self.instruction_categories = {
            'alu': InstructionCategory('alu', 3.0, 0,
                "ADD/SUB/INC/DEC @3 cycles - 4-bit arithmetic"),
            'data_transfer': InstructionCategory('data_transfer', 3.0, 0,
                "MOV register @3 cycles - register-to-register"),
            'memory': InstructionCategory('memory', 4.0, 0,
                "LD/ST @4 cycles - 32-nibble RAM access"),
            'io': InstructionCategory('io', 6.0, 0,
                "IN/OUT @6 cycles - external port operations"),
            'control': InstructionCategory('control', 5.0, 0,
                "JMP/CALL/RET @5 cycles - branch and subroutine"),
        }

        # Workload profiles for arcade game MCU
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.20,
                'memory': 0.20,
                'io': 0.15,
                'control': 0.15,
            }, "Typical arcade game MCU workload (Galaga-class)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'data_transfer': 0.20,
                'memory': 0.15,
                'io': 0.05,
                'control': 0.15,
            }, "Compute-intensive (score calculation, collision)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.25,
                'memory': 0.35,
                'io': 0.10,
                'control': 0.15,
            }, "Memory-intensive (sprite data manipulation)"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.15,
                'memory': 0.15,
                'io': 0.15,
                'control': 0.35,
            }, "Control-flow intensive (game state machine)"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -0.285692,
            'control': -0.158877,
            'data_transfer': 0.424473,
            'io': -0.184240,
            'memory': 0.511403
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

        # Apply correction terms (system identification)
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
        expected_cpi = 4.0
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
