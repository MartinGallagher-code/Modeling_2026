#!/usr/bin/env python3
"""
MOS6510 Grey-Box Queueing Model
================================

Architecture: 8-bit microprocessor (1982)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - 6502 core with identical instruction timing
  - Added 8-bit I/O port at addresses $00-$01
  - 8-bit data bus, 16-bit address bus
  - No pipeline, no cache
  - 2-7 cycles per instruction

Calibrated: 2026-01-28
Target CPI: ~3.0 for typical workloads (cross-validated, same as 6502)
Used in: Commodore 64, Commodore 128
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

class Mos6510Model(BaseProcessorModel):
    """
    MOS6510 Grey-Box Queueing Model

    Architecture: 8-bit NMOS microprocessor (1982)
    - 6502 core with identical instruction timing
    - Added I/O port for bank switching (C64 memory management)
    - CPI ~3.0 for typical workloads (cross-validated, same as 6502)
    """

    # Processor specifications
    name = "MOS6510"
    manufacturer = "MOS Technology"
    year = 1982
    clock_mhz = 1.0  # ~1 MHz in C64 (actually 0.985 MHz NTSC, 0.985 MHz PAL)
    transistor_count = 3510  # Same as 6502
    data_width = 8
    address_width = 16

    def __init__(self):
        # Instruction timing identical to 6502 (cross-validated)
        # From MOS Technology datasheet and VICE emulator validation
        # Same timings as cross-validated 6502 model
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.3, 0,
                "ALU ops: INX/DEX @2, ADC imm @2, ADC zp @3, CMP @2-3"),
            'data_transfer': InstructionCategory('data_transfer', 2.8, 0,
                "LDA imm @2, LDA zp @3, LDA abs @4, TAX @2 - weighted"),
            'memory': InstructionCategory('memory', 4.0, 0,
                "STA zp @3, STA abs @4, indexed @4-5, indirect @5-6"),
            'control': InstructionCategory('control', 2.6, 0,
                "Branch avg @2.55 (50% taken), JMP @3"),
            'stack': InstructionCategory('stack', 3.5, 0,
                "PHA @3, PLA @4, JSR @6, RTS @6 - weighted avg"),
        }

        # Workload profiles (same as 6502)
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.15,
                'memory': 0.30,
                'control': 0.20,
                'stack': 0.10,
            }, "Typical 6510 workload (C64 games/demos)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.20,
                'memory': 0.20,
                'control': 0.15,
                'stack': 0.05,
            }, "Compute-intensive (math routines)"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.25,
                'memory': 0.40,
                'control': 0.12,
                'stack': 0.08,
            }, "Memory-intensive (graphics, data copy)"),
            'control': WorkloadProfile('control', {
                'alu': 0.18,
                'data_transfer': 0.12,
                'memory': 0.20,
                'control': 0.35,
                'stack': 0.15,
            }, "Control-flow intensive (game logic)"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -0.679601,
            'control': 0.445395,
            'data_transfer': 0.629443,
            'memory': -0.081198,
            'stack': 0.107643
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        base_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            base_cpi += weight * cat.total_cycles

        # Apply correction terms from system identification
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
        """Run validation tests against known 6510 characteristics"""
        tests = []

        # Test 1: CPI within expected range (target 3.0, cross-validated same as 6502)
        result = self.analyze('typical')
        expected_cpi = 3.0
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

        # Test 3: All cycle counts are positive and reasonable (1-10 for 6510/6502)
        for cat_name, cat in self.instruction_categories.items():
            cycles = cat.total_cycles
            tests.append({
                'name': f'Cycle count ({cat_name})',
                'passed': 1.0 <= cycles <= 10.0,
                'expected': '1-10 cycles',
                'actual': f'{cycles:.1f}'
            })

        # Test 4: IPC is in valid range for 6510 (0.2 - 0.5 typical)
        tests.append({
            'name': 'IPC range',
            'passed': 0.15 <= result.ipc <= 0.6,
            'expected': '0.15-0.6',
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
