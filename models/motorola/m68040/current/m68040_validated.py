#!/usr/bin/env python3
"""
M68040 Grey-Box Queueing Model
===============================

Architecture: 32-bit microprocessor (1990)
Queueing Model: Deeply pipelined with caches

Features:
  - 6-stage integer pipeline
  - On-chip FPU (first 68k with integrated FPU)
  - 4KB instruction cache, 4KB data cache
  - Approaching 1 IPC for integer code
  - 1.2M transistors

Calibrated: 2026-01-28
Target CPI: ~2.0 for typical workloads
Used in: Mac Quadra, Amiga 4000, NeXTstation Turbo
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

class M68040Model(BaseProcessorModel):
    """
    M68040 Grey-Box Queueing Model

    Architecture: 32-bit CMOS microprocessor (1990)
    - 6-stage pipeline, on-chip FPU
    - 4KB I-cache, 4KB D-cache
    - CPI ~2.0 for typical workloads
    """

    # Processor specifications
    name = "M68040"
    manufacturer = "Motorola"
    year = 1990
    clock_mhz = 25.0
    transistor_count = 1200000
    data_width = 32
    address_width = 32

    def __init__(self):
        # M68040 timing - deeply pipelined
        # Most integer ops @1 cycle, some @2-3
        # FP ops much faster than external 68881/882
        self.instruction_categories = {
            'alu_reg': InstructionCategory('alu_reg', 1.0, 0,
                "ADD/SUB Dn,Dn @1 cycle"),
            'data_transfer': InstructionCategory('data_transfer', 1.0, 0,
                "MOVE Dn,Dn @1 cycle"),
            'memory': InstructionCategory('memory', 2.5, 0,
                "Memory ops @2-3 with cache hit"),
            'control': InstructionCategory('control', 2.5, 0,
                "BRA taken @3, not taken @1"),
            'multiply': InstructionCategory('multiply', 5.0, 0,
                "MULU.L @5 cycles (pipelined)"),
            'divide': InstructionCategory('divide', 38.0, 0,
                "DIVU.L @38 cycles"),
            'fp_ops': InstructionCategory('fp_ops', 4.0, 0,
                "FP add/mul @3-5, integrated FPU"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu_reg': 0.30,
                'data_transfer': 0.30,
                'memory': 0.20,
                'control': 0.15,
                'multiply': 0.02,
                'divide': 0.01,
                'fp_ops': 0.02,
            }, "Typical M68040 workload"),
            'compute': WorkloadProfile('compute', {
                'alu_reg': 0.40,
                'data_transfer': 0.25,
                'memory': 0.15,
                'control': 0.10,
                'multiply': 0.05,
                'divide': 0.02,
                'fp_ops': 0.03,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu_reg': 0.15,
                'data_transfer': 0.20,
                'memory': 0.45,
                'control': 0.12,
                'multiply': 0.03,
                'divide': 0.02,
                'fp_ops': 0.03,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu_reg': 0.20,
                'data_transfer': 0.20,
                'memory': 0.15,
                'control': 0.38,
                'multiply': 0.03,
                'divide': 0.02,
                'fp_ops': 0.02,
            }, "Control-flow intensive"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu_reg': -2.247432,
            'control': -0.206328,
            'data_transfer': 3.477866,
            'divide': -17.670297,
            'fp_ops': -4.686469,
            'memory': -0.547174,
            'multiply': -4.515698
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using deeply pipelined execution model"""
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
        """Run validation tests"""
        tests = []

        # Test 1: CPI within expected range
        result = self.analyze('typical')
        expected_cpi = 2.0  # M68040 target CPI
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
