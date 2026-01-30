#!/usr/bin/env python3
"""
Intel 2920 Grey-Box Queueing Model
====================================

Architecture: 25-bit analog signal processor (1979)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - First Intel DSP attempt
  - 25-bit data path for analog signal processing
  - On-chip ADC (8-bit) and DAC (8-bit)
  - NO hardware multiplier
  - 192 x 24-bit program ROM
  - 40 x 25-bit data RAM
  - 5 MHz clock, each instruction takes 400ns (2 internal cycles)
  - ~50 signal processing instructions

Calibrated: 2026-01-29
Target CPI: 5.0 (typical DSP workloads, no multiply = many cycles for MAC)
Clock: 5 MHz
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

class Intel2920Model(BaseProcessorModel):
    """
    Intel 2920 Grey-Box Queueing Model

    Architecture: 25-bit analog signal processor (1979)
    - First Intel DSP attempt
    - On-chip ADC/DAC but NO hardware multiplier
    - Sequential execution, 400ns per instruction minimum
    - CPI ~5.0 for typical DSP workloads (no multiply = software MAC)
    """

    # Processor specifications
    name = "Intel 2920"
    manufacturer = "Intel"
    year = 1979
    clock_mhz = 5.0
    transistor_count = 15000  # Estimated for NMOS signal processor
    data_width = 25
    address_width = 8  # 192-word program ROM, 40-word data RAM

    def __init__(self):
        # Intel 2920 instruction timing
        # Base instruction execution: 400ns = 2 cycles at 5MHz internal
        # No hardware multiplier means MAC operations require
        # multiple shift-and-add sequences
        #
        # Actual instruction timings:
        #   ADD/SUB: 400ns (2 cycles)
        #   LDA/STA: 400ns (2 cycles) - data RAM access
        #   ABA (analog input): 800ns (4 cycles) - includes ADC conversion
        #   ENA (analog output): 800ns (4 cycles) - includes DAC conversion
        #   JMP/JNZ: 600ns (3 cycles)
        #   SHL/SHR: 400ns (2 cycles) - single bit shift

        self.instruction_categories = {
            'arithmetic': InstructionCategory('arithmetic', 7.0, 0,
                "ADD/SUB @2 base, but effective ~7 due to software multiply (no HW multiplier)"),
            'data_transfer': InstructionCategory('data_transfer', 3.0, 0,
                "LDA/STA @2 base + overhead for limited RAM addressing"),
            'adc_dac': InstructionCategory('adc_dac', 8.0, 0,
                "ADC/DAC conversion @4 base + setup/hold time overhead"),
            'control': InstructionCategory('control', 3.5, 0,
                "JMP/JNZ/NOP @3-4 cycles (600-800ns)"),
            'shift': InstructionCategory('shift', 3.0, 0,
                "SHL/SHR @2 base + multi-bit shift requires repeated operations"),
        }

        # Workload profiles for analog signal processing
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'arithmetic': 0.30,
                'data_transfer': 0.25,
                'adc_dac': 0.15,
                'control': 0.10,
                'shift': 0.20,
            }, "Typical analog signal processing (filter, gain control)"),
            'compute': WorkloadProfile('compute', {
                'arithmetic': 0.45,
                'data_transfer': 0.15,
                'adc_dac': 0.05,
                'control': 0.10,
                'shift': 0.25,
            }, "Compute-intensive (software MAC emulation)"),
            'memory': WorkloadProfile('memory', {
                'arithmetic': 0.20,
                'data_transfer': 0.40,
                'adc_dac': 0.10,
                'control': 0.10,
                'shift': 0.20,
            }, "Data-movement heavy"),
            'control': WorkloadProfile('control', {
                'arithmetic': 0.20,
                'data_transfer': 0.20,
                'adc_dac': 0.10,
                'control': 0.35,
                'shift': 0.15,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'adc_dac': -3.151580,
            'arithmetic': -1.163013,
            'control': 1.546133,
            'data_transfer': 2.507465,
            'shift': 0.200807
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
            base_cpi=base_cpi, correction_delta=correction_delta
        )

    def validate(self) -> Dict[str, Any]:
        """Run validation tests"""
        tests = []

        # Test 1: CPI within expected range
        result = self.analyze('typical')
        expected_cpi = 5.0
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
