#!/usr/bin/env python3
"""
East German U880 Grey-Box Queueing Model
==========================================

Architecture: 8-bit microprocessor (1980)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - Z80 clone by VEB Mikroelektronik Erfurt (East Germany)
  - Full Z80 instruction set compatibility
  - Same timing as Zilog Z80
  - 8500 transistors, NMOS technology
  - 2.5 MHz clock (same as Z80A)
  - Used throughout Eastern Bloc computing
  - Block transfer/search instructions (LDIR, CPIR, etc.)
  - Two register sets (main + alternate)

Calibrated: 2026-01-29
Target CPI: 5.5 (identical to Z80)
Clock: 2.5 MHz
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

class U880Model(BaseProcessorModel):
    """
    East German U880 Grey-Box Queueing Model

    Architecture: 8-bit NMOS microprocessor (1980)
    - Z80 clone by VEB Mikroelektronik Erfurt
    - Full Z80 instruction set and timing compatibility
    - Sequential execution (no pipeline)
    - CPI = 5.5 (identical to Z80)
    """

    # Processor specifications
    name = "U880"
    manufacturer = "VEB Mikroelektronik Erfurt"
    year = 1980
    clock_mhz = 2.5  # Same as Z80
    transistor_count = 8500  # Same as Z80
    data_width = 8
    address_width = 16

    def __init__(self):
        # U880 instruction timing is IDENTICAL to Z80
        # This is a pin-compatible, timing-compatible clone
        #
        # Actual instruction timings (same as Z80):
        #   LD r,r: 4 cycles
        #   LD r,n: 7 cycles
        #   LD r,(HL): 7 cycles
        #   LD (HL),r: 7 cycles
        #   LD A,(nn): 13 cycles
        #   ADD A,r: 4 cycles
        #   ADD A,n: 7 cycles
        #   ADD HL,rr: 11 cycles
        #   INC r: 4 cycles
        #   JP nn: 10 cycles
        #   JR e: 12/7 cycles (taken/not taken)
        #   CALL nn: 17 cycles
        #   RET: 10 cycles
        #   PUSH: 11 cycles
        #   POP: 10 cycles
        #   LDIR: 21/16 cycles (BC!=0/BC=0)

        # Instruction categories - EXACT same as Z80
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 4.0, 0,
                "ALU ops - ADD/SUB/INC/DEC register @4, immediate @7"),
            'data_transfer': InstructionCategory('data_transfer', 4.0, 0,
                "LD r,r @4, LD r,n @7 - weighted for register-heavy code"),
            'memory': InstructionCategory('memory', 5.8, 0,
                "LD r,(HL) @7, LD (HL),r @7 - (HL) most common"),
            'control': InstructionCategory('control', 5.5, 0,
                "JP @10, JR @9.5 avg, CALL/RET less frequent"),
            'stack': InstructionCategory('stack', 10.0, 0,
                "PUSH @11, POP @10"),
            'block': InstructionCategory('block', 12.0, 0,
                "LDIR/LDDR @21/16, weighted for typical use"),
        }

        # Workload profiles - SAME as Z80
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.20,
                'control': 0.15,
                'stack': 0.10,
                'block': 0.05,
            }, "Typical U880 workload (Eastern Bloc computing)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.12,
                'stack': 0.05,
                'block': 0.03,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.35,
                'control': 0.12,
                'stack': 0.08,
                'block': 0.10,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.18,
                'data_transfer': 0.15,
                'memory': 0.15,
                'control': 0.35,
                'stack': 0.12,
                'block': 0.05,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.304196,
            'block': 2.628901,
            'control': 3.043924,
            'data_transfer': 1.251871,
            'memory': 3.416820,
            'stack': -3.488146
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
        expected_cpi = 5.5  # Same as Z80
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
