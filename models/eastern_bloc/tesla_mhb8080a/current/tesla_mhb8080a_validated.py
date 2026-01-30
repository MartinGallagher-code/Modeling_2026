#!/usr/bin/env python3
"""
Tesla MHB8080A Grey-Box Queueing Model
========================================

Architecture: 8-bit microprocessor (1982)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - Czechoslovak Intel 8080A clone by Tesla Piestany
  - 8-bit data bus, 16-bit address bus (64KB)
  - Full 8080 instruction set compatibility
  - 4-18 T-states per instruction
  - Used in PMI-80 and PMD 85 computers

Calibrated: 2026-01-29
Target CPI: ~7.5 for typical workloads (same as Intel 8080)
Used in: PMI-80, PMD 85, Tesla SAPI-1, various Czechoslovak computers
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

class TeslaMHB8080AModel(BaseProcessorModel):
    """
    Tesla MHB8080A Grey-Box Queueing Model

    Architecture: 8-bit NMOS microprocessor (1982)
    - Czechoslovak Intel 8080A clone by Tesla Piestany
    - Sequential execution (no pipeline)
    - Same instruction timing as Intel 8080
    - CPI ~7.5 for typical workloads
    """

    # Processor specifications
    name = "Tesla MHB8080A"
    manufacturer = "Tesla Piestany"
    year = 1982
    clock_mhz = 2.0  # 2 MHz typical
    transistor_count = 6000  # Same as 8080
    data_width = 8
    address_width = 16

    def __init__(self):
        # Tesla MHB8080A instruction timing identical to Intel 8080
        # Tesla Piestany maintained full timing compatibility
        #
        # Actual instruction timings (same as 8080):
        #   MOV r,r: 5 T-states
        #   MOV r,M: 7 T-states
        #   MVI r,d8: 7 T-states
        #   ADD r: 4 T-states
        #   ADD M: 7 T-states
        #   LDA addr: 13 T-states
        #   STA addr: 13 T-states
        #   LXI rp,d16: 10 T-states
        #   PUSH: 11 T-states
        #   POP: 10 T-states
        #   JMP addr: 10 T-states
        #   CALL addr: 17 T-states
        #   RET: 10 T-states
        #   IN/OUT: 10 T-states

        self.instruction_categories = {
            'alu': InstructionCategory('alu', 5.0, 0,
                "ALU ops - ADD/SUB r @4, ADD M @7, INC @5, weighted ~5"),
            'data_transfer': InstructionCategory('data_transfer', 5.5, 0,
                "MOV r,r @5, MVI @7, LXI @10 - weighted ~5.5"),
            'memory': InstructionCategory('memory', 10.0, 0,
                "LDA @13, STA @13, MOV r,M @7, LHLD @16, weighted ~10"),
            'io': InstructionCategory('io', 10.0, 0,
                "IN/OUT @10 T-states"),
            'control': InstructionCategory('control', 9.0, 0,
                "JMP @10, CALL @17, RET @10, conditional ~9"),
            'stack': InstructionCategory('stack', 10.5, 0,
                "PUSH @11, POP @10, XTHL @18, weighted ~10.5"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.25,
                'memory': 0.15,
                'io': 0.05,
                'control': 0.15,
                'stack': 0.10,
            }, "Typical MHB8080A workload (PMI-80/PMD 85 software)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.45,
                'data_transfer': 0.20,
                'memory': 0.12,
                'io': 0.03,
                'control': 0.13,
                'stack': 0.07,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.35,
                'io': 0.05,
                'control': 0.15,
                'stack': 0.10,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.15,
                'memory': 0.10,
                'io': 0.05,
                'control': 0.35,
                'stack': 0.15,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

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
        expected_cpi = 7.5  # Same as Intel 8080
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
