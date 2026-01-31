#!/usr/bin/env python3
"""
WISC CPU/32 Grey-Box Queueing Model
=====================================

Architecture: 32-bit Writable Instruction Set Computer (1988)
Queueing Model: Sequential execution, stack-based

Features:
  - 32-bit evolution of the WISC CPU/16
  - 8 MHz clock (2x the CPU/16)
  - Writable microcode store (RAM-based)
  - Stack-oriented architecture with wider data path
  - Improved microcode engine over CPU/16
  - Lower CPI than CPU/16 due to optimizations

Calibrated: 2026-01-29
Target CPI: ~2.0 (improved over CPU/16's 2.5)
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional

try:
    from common.base_model import BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult, CacheConfig
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
    class CacheConfig:
        has_cache: bool = False
        l1_latency: float = 1.0
        l1_hit_rate: float = 0.95
        l2_latency: float = 10.0
        l2_hit_rate: float = 0.90
        has_l2: bool = False
        dram_latency: float = 50.0
        def effective_memory_penalty(self):
            if not self.has_cache: return 0.0
            l1_miss = 1.0 - self.l1_hit_rate
            if self.has_l2:
                l2_miss = 1.0 - self.l2_hit_rate
                return l1_miss * (self.l2_hit_rate * (self.l2_latency - self.l1_latency) + l2_miss * (self.dram_latency - self.l1_latency))
            return l1_miss * (self.dram_latency - self.l1_latency)


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

class WISC32Model(BaseProcessorModel):
    """
    WISC CPU/32 Grey-Box Queueing Model

    Architecture: 32-bit Writable Instruction Set Computer (1988)
    - 32-bit stack-oriented architecture
    - Improved microcode engine vs CPU/16
    - 8 MHz clock
    - Writable control store
    - CPI ~2.0 (faster than CPU/16)
    """

    name = "WISC CPU/32"
    manufacturer = "Phil Koopman (Carnegie Mellon)"
    year = 1988
    clock_mhz = 8.0
    transistor_count = 0  # TTL discrete
    data_width = 32
    address_width = 32

    def __init__(self):
        # WISC CPU/32 instruction timing
        # Improved over CPU/16 with wider data path and faster microcode
        #
        # Operations:
        #   Stack ops (push, pop, dup, swap): ~1.5 cycles
        #   ALU (add, sub, and, or, 32-bit): ~1.5 cycles
        #   Memory (load, store, 32-bit): ~2.5 cycles
        #   Control (branch, call, return): ~2.5 cycles
        #   Microcode (custom microcode execution): ~2 cycles

        self.instruction_categories = {
            'stack_ops': InstructionCategory('stack_ops', 1.5, 0,
                "Stack operations: push/pop/dup/swap @1.5 cycles"),
            'alu': InstructionCategory('alu', 1.5, 0,
                "32-bit ALU operations @1.5 cycles"),
            'memory': InstructionCategory('memory', 2.5, 0,
                "32-bit memory load/store @2.5 cycles"),
            'control': InstructionCategory('control', 2.5, 0,
                "Branch/call/return @2.5 cycles"),
            'microcode': InstructionCategory('microcode', 2.0, 0,
                "Custom microcode instruction execution @2 cycles"),
        }

        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'stack_ops': 0.30,
                'alu': 0.25,
                'memory': 0.20,
                'control': 0.15,
                'microcode': 0.10,
            }, "Typical Forth-like stack machine workload"),
            'compute': WorkloadProfile('compute', {
                'stack_ops': 0.25,
                'alu': 0.40,
                'memory': 0.15,
                'control': 0.10,
                'microcode': 0.10,
            }, "Compute-intensive (32-bit arithmetic)"),
            'stack_heavy': WorkloadProfile('stack_heavy', {
                'stack_ops': 0.45,
                'alu': 0.15,
                'memory': 0.15,
                'control': 0.15,
                'microcode': 0.10,
            }, "Stack-intensive workload"),
            'custom_isa': WorkloadProfile('custom_isa', {
                'stack_ops': 0.20,
                'alu': 0.15,
                'memory': 0.15,
                'control': 0.10,
                'microcode': 0.40,
            }, "Heavy use of custom microcode instructions"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -0.19023420074349345,
            'control': 0.13550185873605855,
            'memory': 0.1509498141263931,
            'microcode': 0.030895910780668914,
            'stack_ops': 0.18184572490706197,
        }

        # Cache configuration for memory hierarchy modeling
        self.cache_config = CacheConfig(
            has_cache=True,
            l1_latency=1.0,
            l1_hit_rate=0.9130,
            dram_latency=8.0,
        )
        self.memory_categories = ['memory']

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential stack machine execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # Apply cache miss penalty to memory-accessing categories
        if hasattr(self, 'cache_config') and self.cache_config and self.cache_config.has_cache:
            penalty = self.cache_config.effective_memory_penalty()
            for cat_name in getattr(self, 'memory_categories', []):
                if cat_name in self.instruction_categories:
                    self.instruction_categories[cat_name].memory_cycles = penalty


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
        """Run validation tests against known WISC CPU/32 characteristics"""
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
                'passed': 1.0 <= cycles <= 10.0,
                'expected': '1-10 cycles',
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

        # CPU/32 should be faster than CPU/16
        tests.append({
            'name': 'Faster than CPU/16',
            'passed': result.cpi < 2.5,
            'expected': 'CPI < 2.5 (CPU/16 baseline)',
            'actual': f'{result.cpi:.2f}'
        })

        tests.append({
            'name': 'Clock speed',
            'passed': abs(self.clock_mhz - 8.0) < 0.1,
            'expected': '8.0 MHz',
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
    model = WISC32Model()

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
