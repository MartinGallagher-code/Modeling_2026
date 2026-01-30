#!/usr/bin/env python3
"""
Harris HC-55516 Grey-Box Queueing Model
=========================================

Architecture: CVSD (Continuously Variable Slope Delta) audio codec (1982)
Queueing Model: Sequential execution, codec pipeline

Features:
  - CVSD audio decoder/encoder chip
  - Used in Williams arcade games and pinball machines
  - Simple codec with minimal logic
  - 2 MHz clock
  - Produces speech and sound effects from compressed digital audio
  - Very simple pipeline: decode -> filter -> DAC

Calibrated: 2026-01-29
Target CPI: ~2.0 (simple codec, few operations per sample)
Used in: Defender, Robotron, Sinistar, Williams pinball machines
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

class HC55516Model(BaseProcessorModel):
    """
    Harris HC-55516 Grey-Box Queueing Model

    Architecture: CVSD audio codec (1982)
    - Continuously Variable Slope Delta modulation
    - Single-bit input, analog output
    - Adaptive step size for slope tracking
    - Very simple processing pipeline
    - CPI ~2.0 (minimal operations per sample)

    Used in Williams arcade and pinball for speech/sound playback.
    """

    name = "Harris HC-55516"
    manufacturer = "Harris"
    year = 1982
    clock_mhz = 2.0
    transistor_count = 1500  # Simple codec logic
    data_width = 1  # Single-bit CVSD
    address_width = 0  # No addressable memory

    def __init__(self):
        # HC-55516 CVSD codec timing
        # Very simple: each clock processes one bit of CVSD data
        #
        # Operations:
        #   Decode (CVSD bit decode + slope update): ~1.5 cycles
        #   Filter (syllabic filter / integrator): ~2 cycles
        #   DAC (analog output update): ~2 cycles
        #   Control (mode/clock control): ~1.5 cycles
        #   Timing (sample rate sync): ~3 cycles

        self.instruction_categories = {
            'decode': InstructionCategory('decode', 1.5, 0,
                "CVSD bit decode and slope adaptation @1.5 cycles"),
            'filter': InstructionCategory('filter', 2.0, 0,
                "Syllabic filter / integrator update @2 cycles"),
            'dac': InstructionCategory('dac', 2.0, 0,
                "DAC analog output update @2 cycles"),
            'control': InstructionCategory('control', 1.5, 0,
                "Mode and clock control @1.5 cycles"),
            'timing': InstructionCategory('timing', 3.0, 0,
                "Sample rate synchronization @3 cycles"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'decode': 0.30,
                'filter': 0.25,
                'dac': 0.20,
                'control': 0.15,
                'timing': 0.10,
            }, "Typical CVSD decode (speech playback)"),
            'continuous': WorkloadProfile('continuous', {
                'decode': 0.35,
                'filter': 0.30,
                'dac': 0.25,
                'control': 0.05,
                'timing': 0.05,
            }, "Continuous decode stream"),
            'idle': WorkloadProfile('idle', {
                'decode': 0.05,
                'filter': 0.05,
                'dac': 0.10,
                'control': 0.30,
                'timing': 0.50,
            }, "No active decode, waiting for data"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'control': 2.765750,
            'dac': 0.527239,
            'decode': -1.648180,
            'filter': 1.183966,
            'timing': -1.968476
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential codec pipeline model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        base_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

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
        """Run validation tests against known HC-55516 characteristics"""
        tests = []

        result = self.analyze('typical')
        expected_cpi = 2.0
        cpi_error = abs(result.cpi - expected_cpi) / expected_cpi * 100
        tests.append({
            'name': 'CPI accuracy',
            'passed': cpi_error < 5.0,
            'expected': f'{expected_cpi} +/- 5%',
            'actual': f'{result.cpi:.2f} ({cpi_error:.1f}% error)'
        })

        for profile_name, profile in self.workload_profiles.items():
            weight_sum = sum(profile.category_weights.values())
            tests.append({
                'name': f'Weights sum ({profile_name})',
                'passed': 0.99 <= weight_sum <= 1.01,
                'expected': '1.0',
                'actual': f'{weight_sum:.2f}'
            })

        for cat_name, cat in self.instruction_categories.items():
            cycles = cat.total_cycles
            tests.append({
                'name': f'Cycle count ({cat_name})',
                'passed': 0.5 <= cycles <= 10.0,
                'expected': '0.5-10 cycles',
                'actual': f'{cycles:.1f}'
            })

        tests.append({
            'name': 'IPC range',
            'passed': 0.2 <= result.ipc <= 1.0,
            'expected': '0.2-1.0',
            'actual': f'{result.ipc:.3f}'
        })

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

        tests.append({
            'name': 'Clock speed',
            'passed': abs(self.clock_mhz - 2.0) < 0.01,
            'expected': '2.0 MHz',
            'actual': f'{self.clock_mhz} MHz'
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


if __name__ == '__main__':
    model = HC55516Model()

    print(f"=== {model.name} Performance Model ===")
    print(f"Manufacturer: {model.manufacturer}")
    print(f"Year: {model.year}")
    print(f"Clock: {model.clock_mhz} MHz")
    print()

    for workload in model.workload_profiles:
        result = model.analyze(workload)
        print(f"{workload:16} - CPI: {result.cpi:.2f}, IPC: {result.ipc:.3f}, "
              f"IPS: {result.ips/1e6:.3f}M, Bottleneck: {result.bottleneck}")

    print()

    validation = model.validate()
    print(f"=== Validation Results ===")
    print(f"Passed: {validation['passed']}/{validation['total']}")
    print(f"Accuracy: {validation['accuracy_percent']:.1f}%")
    print()

    for test in validation['tests']:
        status = "PASS" if test['passed'] else "FAIL"
        print(f"  [{status}] {test['name']}: {test['actual']} (expected: {test['expected']})")
