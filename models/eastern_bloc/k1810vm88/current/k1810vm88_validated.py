#!/usr/bin/env python3
"""
K1810VM88 Grey-Box Queueing Model
====================================

Architecture: 8/16-bit microprocessor (1980s)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - Soviet Intel 8088 clone
  - 8-bit external data bus, 16-bit internal
  - ~29,000 transistors
  - 5 MHz clock
  - Full 8088 instruction set compatibility
  - 4-byte instruction prefetch queue
  - Hardware multiply/divide
  - 3-30 cycles per instruction

Calibrated: 2026-01-29
Target CPI: ~5.0 for typical workloads
Used in: Soviet IBM PC/XT compatible computers
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

class K1810VM88Model(BaseProcessorModel):
    """
    K1810VM88 Grey-Box Queueing Model

    Architecture: 8/16-bit NMOS microprocessor (1980s)
    - Soviet Intel 8088 clone
    - 8-bit external bus (slower memory access than 8086)
    - 4-byte instruction prefetch queue
    - Full 8088 instruction set compatibility
    - CPI ~5.0 for typical workloads
    """

    # Processor specifications
    name = "K1810VM88"
    manufacturer = "Soviet Union"
    year = 1986
    clock_mhz = 5.0
    transistor_count = 29000
    data_width = 16  # Internal 16-bit, external 8-bit
    address_width = 20

    def __init__(self):
        # K1810VM88 instruction timing (8088 compatible)
        #
        # Same internal timing as 8086/8088 but 8-bit bus
        # causes additional memory access penalties:
        #   MOV reg,reg: 2 cycles
        #   MOV reg,imm: 4 cycles
        #   ADD reg,reg: 3 cycles
        #   JMP near: 15 cycles
        #   CALL near: 19 cycles
        #   MUL (8-bit): 70-77 cycles
        #   MUL (16-bit): 118-133 cycles
        #   REP MOVSB: 9+17/byte

        self.instruction_categories = {
            'alu': InstructionCategory('alu', 3.0, 0,
                "ALU ops - ADD reg,reg @3, INC @2, CMP @3, weighted ~3"),
            'data_transfer': InstructionCategory('data_transfer', 4.0, 0,
                "MOV reg,reg @2, MOV reg,imm @4, MOV reg,mem @8+EA, weighted ~4"),
            'memory': InstructionCategory('memory', 6.0, 0,
                "Memory ops with 8-bit bus penalty, EA calculation ~6"),
            'control': InstructionCategory('control', 5.0, 0,
                "JMP @15, CALL @19, RET @8, Jcc ~5 average"),
            'multiply': InstructionCategory('multiply', 30.0, 0,
                "MUL 8-bit @70-77, MUL 16-bit @118-133, DIV ~30 weighted avg"),
            'string': InstructionCategory('string', 8.0, 0,
                "REP MOVSB/STOSB with 8-bit bus overhead ~8"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.32,
                'data_transfer': 0.25,
                'memory': 0.12,
                'control': 0.20,
                'multiply': 0.02,
                'string': 0.09,
            }, "Typical K1810VM88 workload (PC/XT-compatible software)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.35,
                'data_transfer': 0.20,
                'memory': 0.10,
                'control': 0.15,
                'multiply': 0.10,
                'string': 0.10,
            }, "Compute-intensive with multiply"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.20,
                'memory': 0.30,
                'control': 0.12,
                'multiply': 0.03,
                'string': 0.20,
            }, "Memory-intensive (8-bit bus bottleneck)"),
            'control': WorkloadProfile('control', {
                'alu': 0.20,
                'data_transfer': 0.15,
                'memory': 0.10,
                'control': 0.40,
                'multiply': 0.02,
                'string': 0.13,
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
        expected_cpi = 5.0
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
