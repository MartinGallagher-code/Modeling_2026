#!/usr/bin/env python3
"""
MC14500B Grey-Box Queueing Model
=================================

Architecture: 1-bit Industrial Control Unit (1976)
Queueing Model: Fixed-cycle single-clock execution

Notes:
  - 1-bit datapath, 16 instructions, 4-bit opcode
  - ALL instructions execute in exactly 1 clock cycle
  - No pipeline, no cache, no program counter (external)
  - ~500 transistors, CMOS, up to 1 MHz @ 5V (4 MHz @ 15V)
  - Designed for ladder/relay logic replacement

Calibrated: 2026-01-29
Status: Validated (trivially accurate - fixed 1-cycle timing)
Sources:
  - Motorola MC14500B Industrial Control Unit Handbook (1977)
  - Ken Shirriff reverse-engineering (righto.com, 2021)
  - WikiChip MC14500B specifications
"""

from dataclasses import dataclass
from typing import Dict, Any

try:
    from common.base_model import BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult
except ImportError:
    @dataclass
    class InstructionCategory:
        name: str
        base_cycles: float
        memory_cycles: float = 0.0
        description: str = ""
        @property
        def total_cycles(self) -> float:
            return self.base_cycles + self.memory_cycles

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
            ipc = 1.0 / cpi if cpi > 0 else 0.0
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

class Mc14500bModel(BaseProcessorModel):
    """
    Motorola MC14500B 1-bit Industrial Control Unit

    Architecture: 1-bit combinational processor (1976)
    - 16 instructions, 4-bit opcode, ALL execute in 1 clock cycle
    - 1-bit Result Register (RR) accumulator
    - No program counter - external sequencer handles addressing
    - JMP/RTN are output flags, not internal branches
    - IEN/OEN enable/disable input and output respectively

    Instruction set (all 1 cycle):
      0000 NOPO  - No operation (outputs active)
      0001 LD    - Load RR from data bus
      0010 LDC   - Load complement of data into RR
      0011 AND   - RR = RR AND data
      0100 ANDC  - RR = RR AND (NOT data)
      0101 OR    - RR = RR OR data
      0110 ORC   - RR = RR OR (NOT data)
      0111 XNOR  - RR = RR XNOR data
      1000 STO   - Store RR to data bus
      1001 STOC  - Store complement of RR
      1010 IEN   - Input enable register = data
      1011 OEN   - Output enable register = data
      1100 JMP   - Set JMP flag output (external handles jump)
      1101 RTN   - Set RTN flag output (external handles return)
      1110 SKZ   - Skip next if RR = 0
      1111 NOPF  - No operation (outputs inactive)

    CPI = 1.0 for ALL instructions and workloads.
    At 1 MHz: 1,000,000 IPS.
    """

    # Processor specifications
    name = "MC14500B"
    manufacturer = "Motorola"
    year = 1976
    clock_mhz = 1.0  # Up to 1 MHz @ 5V, 4 MHz @ 15V
    transistor_count = 500
    data_width = 1

    def __init__(self):
        # MC14500B has FIXED instruction timing - all 16 instructions = 1 cycle
        # This is the simplest possible model
        self.fixed_cycles = 1

        # Instruction categories - all same cycle count (1), different frequencies
        # CPI is always 1.0 regardless of workload mix
        self.instruction_categories: Dict[str, InstructionCategory] = {
            'logic': InstructionCategory('logic', 1, 0, 'Boolean ops: AND, ANDC, OR, ORC, XNOR @1 cycle'),
            'load_store': InstructionCategory('load_store', 1, 0, 'Data: LD, LDC, STO, STOC @1 cycle'),
            'control': InstructionCategory('control', 1, 0, 'Control: JMP, RTN, SKZ, IEN, OEN @1 cycle'),
            'nop': InstructionCategory('nop', 1, 0, 'No-op: NOPO, NOPF @1 cycle'),
        }

        # Workload profiles - don't affect CPI due to fixed timing
        self.workload_profiles: Dict[str, WorkloadProfile] = {
            'typical': WorkloadProfile('typical', {
                'logic': 0.35,
                'load_store': 0.30,
                'control': 0.30,
                'nop': 0.05,
            }, 'Industrial control ladder-logic scan loop'),
            'logic_heavy': WorkloadProfile('logic_heavy', {
                'logic': 0.55,
                'load_store': 0.25,
                'control': 0.15,
                'nop': 0.05,
            }, 'Boolean computation heavy'),
            'control': WorkloadProfile('control', {
                'logic': 0.20,
                'load_store': 0.20,
                'control': 0.55,
                'nop': 0.05,
            }, 'Control-flow and I/O intensive'),
            'io': WorkloadProfile('io', {
                'logic': 0.15,
                'load_store': 0.50,
                'control': 0.30,
                'nop': 0.05,
            }, 'I/O sense/actuation heavy'),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {cat: 0.0 for cat in self.instruction_categories}

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using fixed-cycle execution model."""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        # MC14500B always has CPI = 1.0 (fixed timing, all instructions 1 cycle)
        base_cpi = float(self.fixed_cycles)

        # Calculate category contributions for analysis
        contributions: Dict[str, float] = {}
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
            correction_delta=correction_delta,
        )

    def validate(self) -> Dict[str, Any]:
        """Run validation tests."""
        tests = []
        passed = 0

        # Test 1: CPI should be exactly 1.0 (all instructions 1 cycle)
        result = self.analyze('typical')
        test1 = {
            'name': 'CPI accuracy (fixed 1-cycle)',
            'expected': 1.0,
            'actual': result.cpi,
            'passed': abs(result.cpi - 1.0) < 0.01,
        }
        tests.append(test1)
        if test1['passed']:
            passed += 1

        # Test 2: IPS at 1 MHz should be exactly 1,000,000
        expected_ips = 1_000_000
        test2 = {
            'name': 'IPS at 1 MHz',
            'expected': expected_ips,
            'actual': result.ips,
            'passed': abs(result.ips - expected_ips) / expected_ips < 0.01,
        }
        tests.append(test2)
        if test2['passed']:
            passed += 1

        # Test 3: All workloads should give same CPI (fixed timing)
        for wl in ['logic_heavy', 'control', 'io']:
            r = self.analyze(wl)
            test = {
                'name': f'CPI consistency ({wl})',
                'expected': 1.0,
                'actual': r.cpi,
                'passed': abs(r.cpi - 1.0) < 0.01,
            }
            tests.append(test)
            if test['passed']:
                passed += 1

        # Test 4: Weight sums
        for name, profile in self.workload_profiles.items():
            s = sum(profile.category_weights.values())
            test = {
                'name': f'Weights sum ({name})',
                'passed': 0.99 <= s <= 1.01,
                'expected': '1.0',
                'actual': f'{s:.2f}',
            }
            tests.append(test)
            if test['passed']:
                passed += 1

        # Test 5: All categories have exactly 1 cycle
        for cname, cat in self.instruction_categories.items():
            test = {
                'name': f'Fixed cycle count ({cname})',
                'passed': cat.total_cycles == 1.0,
                'expected': '1.0',
                'actual': f'{cat.total_cycles:.1f}',
            }
            tests.append(test)
            if test['passed']:
                passed += 1

        return {
            'tests': tests,
            'passed': passed,
            'total': len(tests),
            'accuracy_percent': (passed / len(tests)) * 100 if tests else 0,
        }

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles
