#!/usr/bin/env python3
"""
KR580VM1 Grey-Box Queueing Model
==================================

Architecture: 8-bit microprocessor (1980)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - Soviet 8080 EXTENSION (NOT a direct clone)
  - Extends Intel 8080 with 128KB addressing (vs 64KB)
  - Bank-switching mechanism for extended memory
  - 8-bit data bus, 17-bit effective address space
  - Full 8080 instruction set plus bank management instructions
  - Similar base timing to 8080 but extra bank-switch overhead

Calibrated: 2026-01-29
Target CPI: ~8.0 for typical workloads (slightly slower than 8080's 7.5 due to bank management)
Used in: Soviet industrial controllers, Elektronika BK series peripherals
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

class KR580VM1Model(BaseProcessorModel):
    """
    KR580VM1 Grey-Box Queueing Model

    Architecture: 8-bit NMOS microprocessor (1980)
    - Soviet 8080 extension with 128KB bank-switched memory
    - NOT a direct clone - extends the 8080 ISA
    - Sequential execution (no pipeline)
    - Base timing similar to 8080, plus bank-switch overhead
    - CPI ~8.0 for typical workloads
    """

    # Processor specifications
    name = "KR580VM1"
    manufacturer = "Soviet Union (various fabs)"
    year = 1980
    clock_mhz = 2.5  # 2.5 MHz typical
    transistor_count = 6500  # Slightly more than 8080 due to bank logic
    data_width = 8
    address_width = 17  # 128KB via bank switching

    def __init__(self):
        # KR580VM1 extends Intel 8080 timing
        # Base instructions have same timing as 8080
        # Bank-switch instructions add overhead
        #
        # Base instruction timings (same as 8080):
        #   MOV r,r: 5 states
        #   MOV r,M: 7 states
        #   ADD r: 4 states
        #   ADD M: 7 states
        #   MVI r,d8: 7 states
        #   LDA addr: 13 states
        #   JMP addr: 10 states
        #   CALL addr: 17 states
        #   RET: 10 states
        #   IN/OUT: 10 states
        #
        # Bank-switch extension:
        #   Bank select: ~12 states (new instruction)
        #   Cross-bank transfer adds overhead

        self.instruction_categories = {
            'alu': InstructionCategory('alu', 5.5, 0,
                "ALU ops - ADD/SUB r @4, ADD M @7, INC @5, weighted ~5.5"),
            'data_transfer': InstructionCategory('data_transfer', 5.5, 0,
                "MOV r,r @5, MVI @7, LXI @10 - weighted ~5.5"),
            'memory': InstructionCategory('memory', 10.0, 0,
                "LDA @13, STA @13, MOV r,M @7, LHLD @16, weighted ~10"),
            'io': InstructionCategory('io', 10.0, 0,
                "IN/OUT @10 states"),
            'control': InstructionCategory('control', 9.0, 0,
                "JMP @10, CALL @17, RET @10, conditional ~9"),
            'bank_switch': InstructionCategory('bank_switch', 14.0, 0,
                "Bank select ~14, cross-bank operations with overhead"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.25,
                'memory': 0.20,
                'io': 0.05,
                'control': 0.15,
                'bank_switch': 0.10,
            }, "Typical KR580VM1 workload (using extended memory)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.25,
                'memory': 0.15,
                'io': 0.03,
                'control': 0.12,
                'bank_switch': 0.05,
            }, "Compute-intensive (minimal bank switching)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.30,
                'io': 0.05,
                'control': 0.15,
                'bank_switch': 0.20,
            }, "Memory-intensive with heavy bank switching"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.15,
                'memory': 0.15,
                'io': 0.05,
                'control': 0.35,
                'bank_switch': 0.10,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -0.805853,
            'bank_switch': -3.122597,
            'control': -0.436687,
            'data_transfer': -0.711880,
            'io': -2.719535,
            'memory': -1.051136
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        base_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

        correction_delta = sum(
            self.corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

        ipc = 1.0 / corrected_cpi
        ips = self.clock_mhz * 1e6 * ipc

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
        tests = []

        # Test 1: CPI within expected range
        result = self.analyze('typical')
        expected_cpi = 8.0  # Slightly slower than 8080's 7.5 due to bank management
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
