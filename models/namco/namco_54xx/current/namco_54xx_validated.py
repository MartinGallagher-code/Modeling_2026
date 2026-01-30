#!/usr/bin/env python3
"""
Namco 54xx Grey-Box Queueing Model
===================================

Architecture: Custom 4-bit sound generator chip (1981)
Queueing Model: Sequential execution, state-machine based

Features:
  - Custom chip for noise and waveform sound generation
  - Used in Galaga, Bosconian, and related Namco arcade games
  - ~3000 transistors, 1.5 MHz clock
  - Noise generator, waveform synthesis, mixing, and DAC output
  - Produces explosions, engine noise, and other sound effects

Calibrated: 2026-01-29
Target CPI: ~6.0 for typical workloads
Used in: Galaga, Bosconian, Dig Dug, and other Namco arcade boards
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
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations,
                       base_cpi=base_cpi if base_cpi is not None else cpi,
                       correction_delta=correction_delta)

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

class Namco54xxModel(BaseProcessorModel):
    """
    Namco 54xx Grey-Box Queueing Model

    Architecture: Custom 4-bit sound generator (1981)
    - Noise generation (LFSR-based)
    - Waveform synthesis
    - Audio channel mixing
    - DAC output
    - ~3000 transistors
    - CPI ~6.0 for typical workloads (complex audio processing)
    """

    name = "Namco 54xx"
    manufacturer = "Namco"
    year = 1981
    clock_mhz = 1.5
    transistor_count = 3000
    data_width = 4
    address_width = 8

    def __init__(self):
        # Namco 54xx sound generator timing
        # Based on MAME emulation and audio waveform analysis
        #
        # Operations:
        #   Noise gen (LFSR noise generation): ~5 cycles
        #   Waveform (waveform table lookup/synthesis): ~6 cycles
        #   Mix (channel mixing): ~4 cycles
        #   I/O (command input, status): ~5 cycles
        #   Control (state machine): ~4 cycles
        #   DAC (digital-to-analog output): ~8 cycles

        self.instruction_categories = {
            'noise_gen': InstructionCategory('noise_gen', 5.0, 0,
                "LFSR-based noise generation @5 cycles"),
            'waveform': InstructionCategory('waveform', 6.0, 0,
                "Waveform table lookup and synthesis @6 cycles"),
            'mix': InstructionCategory('mix', 4.0, 0,
                "Audio channel mixing @4 cycles"),
            'io': InstructionCategory('io', 5.0, 0,
                "Command input and status output @5 cycles"),
            'control': InstructionCategory('control', 4.0, 0,
                "Sound state machine control @4 cycles"),
            'dac': InstructionCategory('dac', 8.0, 0,
                "Digital-to-analog conversion output @8 cycles"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'noise_gen': 0.20,
                'waveform': 0.20,
                'mix': 0.15,
                'io': 0.15,
                'control': 0.15,
                'dac': 0.15,
            }, "Typical gameplay sound generation"),
            'noise_heavy': WorkloadProfile('noise_heavy', {
                'noise_gen': 0.35,
                'waveform': 0.10,
                'mix': 0.15,
                'io': 0.10,
                'control': 0.10,
                'dac': 0.20,
            }, "Heavy noise generation (explosions)"),
            'waveform_heavy': WorkloadProfile('waveform_heavy', {
                'noise_gen': 0.10,
                'waveform': 0.35,
                'mix': 0.15,
                'io': 0.10,
                'control': 0.10,
                'dac': 0.20,
            }, "Waveform-heavy synthesis (music/tones)"),
            'idle': WorkloadProfile('idle', {
                'noise_gen': 0.05,
                'waveform': 0.05,
                'mix': 0.05,
                'io': 0.15,
                'control': 0.40,
                'dac': 0.30,
            }, "Idle/silent state"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'control': 3.233572,
            'dac': -3.116467,
            'io': -0.114483,
            'mix': -0.297440,
            'noise_gen': 2.235557,
            'waveform': 1.235557
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
        """Run validation tests against known 54xx characteristics"""
        tests = []

        result = self.analyze('typical')
        expected_cpi = 6.0
        cpi_error = abs(result.cpi - expected_cpi) / expected_cpi * 100
        tests.append({
            'name': 'CPI accuracy',
            'passed': cpi_error < 10.0,
            'expected': f'{expected_cpi} +/- 10%',
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
                'passed': 1.0 <= cycles <= 15.0,
                'expected': '1-15 cycles',
                'actual': f'{cycles:.1f}'
            })

        tests.append({
            'name': 'IPC range',
            'passed': 0.05 <= result.ipc <= 0.5,
            'expected': '0.05-0.5',
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
            'passed': abs(self.clock_mhz - 1.5) < 0.01,
            'expected': '1.5 MHz',
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
    model = Namco54xxModel()

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
