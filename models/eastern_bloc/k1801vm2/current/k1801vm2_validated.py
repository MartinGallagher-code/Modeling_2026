#!/usr/bin/env python3
"""
K1801VM2 Grey-Box Queueing Model
====================================

Architecture: 16-bit microprocessor (1983)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - Enhanced Soviet PDP-11 compatible microprocessor
  - 16-bit data bus
  - ~25,000 transistors
  - 8 MHz clock
  - Extended PDP-11 instruction set with floating point support
  - 2-10 cycles per instruction

Calibrated: 2026-01-29
Target CPI: ~4.0 for typical workloads
Used in: DVK-3, DVK-4 and other Soviet minicomputer systems
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

class K1801VM2Model(BaseProcessorModel):
    """
    K1801VM2 Grey-Box Queueing Model

    Architecture: 16-bit NMOS microprocessor (1983)
    - Enhanced Soviet PDP-11 compatible
    - Improved execution speed over VM1
    - Floating point support
    - CPI ~4.0 for typical workloads
    """

    # Processor specifications
    name = "K1801VM2"
    manufacturer = "Soviet Union"
    year = 1983
    clock_mhz = 8.0
    transistor_count = 25000
    data_width = 16
    address_width = 16

    def __init__(self):
        # K1801VM2 instruction timing (enhanced PDP-11 compatible)
        #
        # Improved over VM1 with faster execution:
        #   MOV Rn,Rn: 1-2 cycles
        #   ADD Rn,Rn: 2 cycles
        #   ADD Rn,(Rn): 4 cycles
        #   JMP: 3-4 cycles
        #   JSR: 5-6 cycles
        #   RTS: 4 cycles
        #   Memory indirect: 5-8 cycles
        #   FADD: 8-12 cycles

        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.0, 0,
                "ALU ops - ADD Rn,Rn @2, INC @1, CMP @2, weighted ~2"),
            'data_transfer': InstructionCategory('data_transfer', 3.0, 0,
                "MOV Rn,Rn @1-2, MOV Rn,(Rn) @3, MOV Rn,imm @3, weighted ~3"),
            'memory': InstructionCategory('memory', 6.0, 0,
                "Memory indirect modes, deferred addressing ~6"),
            'control': InstructionCategory('control', 4.0, 0,
                "JMP @3-4, JSR @5-6, RTS @4, Bcc @3, weighted ~4"),
            'float': InstructionCategory('float', 10.0, 0,
                "FADD @8-12, FMUL @10-14, floating point ops ~10"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.30,
                'data_transfer': 0.25,
                'memory': 0.125,
                'control': 0.225,
                'float': 0.10,
            }, "Typical K1801VM2 workload (enhanced PDP-11 software)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.35,
                'data_transfer': 0.20,
                'memory': 0.10,
                'control': 0.15,
                'float': 0.20,
            }, "Compute-intensive with floating point"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.25,
                'memory': 0.35,
                'control': 0.15,
                'float': 0.10,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.15,
                'data_transfer': 0.15,
                'memory': 0.10,
                'control': 0.50,
                'float': 0.10,
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

        result = self.analyze('typical')
        expected_cpi = 4.0
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
                'passed': 0.5 <= cycles <= 200.0,
                'expected': '0.5-200 cycles',
                'actual': f'{cycles:.1f}'
            })

        tests.append({
            'name': 'IPC range',
            'passed': 0.05 <= result.ipc <= 1.5,
            'expected': '0.05-1.5',
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
