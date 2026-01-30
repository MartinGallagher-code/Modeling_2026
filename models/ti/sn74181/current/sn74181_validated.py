#!/usr/bin/env python3
"""
TI SN74181 Grey-Box Queueing Model
====================================

Architecture: 4-bit ALU (combinational logic, 1970)
Queueing Model: Single-cycle combinational operations

Features:
  - First single-chip 4-bit ALU
  - 75 transistors, TTL technology
  - 16 arithmetic + 16 logic functions (32 total)
  - Propagation delay ~22ns typical
  - NOT a CPU - combinational logic building block
  - Used in PDP-11, Data General Nova, many minicomputers
  - Carry lookahead for fast ripple-free addition

Calibrated: 2026-01-29
Target CPI: 1.0 (single-cycle combinational operations)
Clock equivalent: ~45 MHz (1/22ns propagation delay)
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

class SN74181Model(BaseProcessorModel):
    """
    TI SN74181 Grey-Box Queueing Model

    Architecture: 4-bit combinational ALU (1970)
    - NOT a CPU - pure combinational logic block
    - All operations complete in single propagation delay
    - 16 arithmetic functions + 16 logic functions
    - CPI = 1.0 (all operations are single-cycle)
    """

    # Processor specifications
    name = "SN74181"
    manufacturer = "Texas Instruments"
    year = 1970
    clock_mhz = 45.0  # Equivalent: 1/22ns propagation delay
    transistor_count = 75
    data_width = 4
    address_width = 0  # No address bus - combinational logic

    def __init__(self):
        # SN74181 is purely combinational - all operations single cycle
        # The 32 functions (16 arithmetic + 16 logic) all complete
        # within a single propagation delay (~22ns typical)
        #
        # Arithmetic functions (M=0): A, A+1, A+B, A+B+1, A-B-1, etc.
        # Logic functions (M=1): NOT A, A AND B, A OR B, A XOR B, etc.
        # Carry propagation adds minimal delay with lookahead

        self.instruction_categories = {
            'arithmetic': InstructionCategory('arithmetic', 1.0, 0,
                "ADD, SUB, compare, increment - 16 arithmetic functions @1 cycle"),
            'logic': InstructionCategory('logic', 1.0, 0,
                "AND, OR, XOR, NOT - 16 logic functions @1 cycle"),
            'shift': InstructionCategory('shift', 1.0, 0,
                "Carry propagation / shift through cascaded slices @1 cycle"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'arithmetic': 0.50,
                'logic': 0.35,
                'shift': 0.15,
            }, "Typical ALU workload in minicomputer datapath"),
            'compute': WorkloadProfile('compute', {
                'arithmetic': 0.70,
                'logic': 0.20,
                'shift': 0.10,
            }, "Arithmetic-heavy computation"),
            'memory': WorkloadProfile('memory', {
                'arithmetic': 0.40,
                'logic': 0.30,
                'shift': 0.30,
            }, "Address calculation heavy"),
            'control': WorkloadProfile('control', {
                'arithmetic': 0.30,
                'logic': 0.55,
                'shift': 0.15,
            }, "Logic/comparison heavy control flow"),
            'mixed': WorkloadProfile('mixed', {
                'arithmetic': 0.45,
                'logic': 0.40,
                'shift': 0.15,
            }, "Mixed arithmetic and logic"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using single-cycle combinational model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        total_cpi = 0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contrib = weight * cat.total_cycles
            total_cpi += contrib
            contributions[cat_name] = contrib

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

        # Test 1: CPI within expected range
        result = self.analyze('typical')
        expected_cpi = 1.0
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
