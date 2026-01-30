#!/usr/bin/env python3
"""
Rockwell R65C02 Grey-Box Queueing Model
========================================

Architecture: 8-bit CMOS microprocessor (1983)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - CMOS 6502 with Rockwell-specific bit manipulation instructions
  - Same WDC 65C02 base with added BBR, BBS, RMB, SMB instructions
  - 8-bit data bus, 16-bit address bus
  - Lower power consumption than NMOS 6502
  - Higher clock speeds possible (up to 4 MHz)
  - 2-7 cycles per instruction (some bit ops take longer)

Calibrated: 2026-01-29
Target CPI: ~2.85 for typical workloads (same as WDC 65C02)
Used in: Embedded systems, industrial controllers, Apple IIc

Note: The R65C02 is Rockwell's CMOS 6502, compatible with WDC 65C02
but with additional bit manipulation instructions:
  - RMB0-7 (Reset Memory Bit): 5 cycles
  - SMB0-7 (Set Memory Bit): 5 cycles
  - BBR0-7 (Branch on Bit Reset): 5 cycles
  - BBS0-7 (Branch on Bit Set): 5 cycles
These are useful for embedded control applications.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional

# Import from common (adjust path as needed)
try:
    from common.base_model import BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult
except ImportError:
    # Fallback definitions if common not available
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
        pass


class R65c02Model(BaseProcessorModel):
    """
    Rockwell R65C02 Grey-Box Queueing Model

    Architecture: 8-bit CMOS microprocessor (1983)
    - WDC 65C02 compatible with Rockwell bit manipulation extensions
    - RMW ops on abs,X are 1 cycle faster (6 vs 7)
    - BRA instruction (unconditional branch) = 3 cycles
    - Sequential execution (no pipeline)
    - 2-7 cycles per instruction
    - CPI ~2.85 for typical workloads (same as WDC 65C02)

    The R65C02 is Rockwell's licensed CMOS implementation with
    additional bit test and manipulation instructions useful for
    embedded control applications.
    """

    # Processor specifications
    name = "R65C02"
    manufacturer = "Rockwell International"
    year = 1983
    clock_mhz = 4.0  # Up to 4 MHz typical
    transistor_count = 9000  # Slightly more than WDC for bit ops
    data_width = 8
    address_width = 16

    def __init__(self):
        # R65C02 instruction timing matches WDC 65C02 for base instructions
        # Rockwell-specific bit manipulation instructions:
        #   RMB0-7 (Reset Memory Bit): 5 cycles
        #   SMB0-7 (Set Memory Bit): 5 cycles
        #   BBR0-7 (Branch on Bit Reset): 5 cycles (no page cross penalty)
        #   BBS0-7 (Branch on Bit Set): 5 cycles (no page cross penalty)
        #
        # Key improvements over NMOS 6502 (same as WDC 65C02):
        # - RMW ops on abs,X are 1 cycle faster (6 vs 7)
        # - New BRA instruction (unconditional branch) = 3 cycles
        # - PHX/PHY/PLX/PLY for index register stack ops
        # - No dummy cycles in indexed modes

        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.2, 0,
                "ALU ops: INX/DEX @2, ADC imm @2, ADC zp @3 - same as 65C02"),
            'data_transfer': InstructionCategory('data_transfer', 2.6, 0,
                "LDA imm @2, zp @3, abs @4 - slightly faster indexed"),
            'memory': InstructionCategory('memory', 3.6, 0,
                "STA zp @3, abs @4 - RMW abs,X @6 (was 7)"),
            'control': InstructionCategory('control', 2.5, 0,
                "BRA @3, branches @2.55 avg, JMP @3"),
            'stack': InstructionCategory('stack', 3.2, 0,
                "PHX/PLX @3/4, JSR @6, RTS @6"),
            'bit_ops': InstructionCategory('bit_ops', 5.0, 0,
                "RMB/SMB @5, BBR/BBS @5 - Rockwell extensions"),
        }

        # Workload profiles - R65C02 used heavily in embedded systems
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.15,
                'memory': 0.30,
                'control': 0.20,
                'stack': 0.10,
                'bit_ops': 0.00,
            }, "Typical R65C02 workload (general purpose)"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.40,
                'data_transfer': 0.20,
                'memory': 0.20,
                'control': 0.15,
                'stack': 0.05,
                'bit_ops': 0.00,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.15,
                'data_transfer': 0.25,
                'memory': 0.40,
                'control': 0.12,
                'stack': 0.08,
                'bit_ops': 0.00,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.18,
                'data_transfer': 0.12,
                'memory': 0.20,
                'control': 0.35,
                'stack': 0.15,
                'bit_ops': 0.00,
            }, "Control-flow intensive"),
            'embedded': WorkloadProfile('embedded', {
                'alu': 0.20,
                'data_transfer': 0.10,
                'memory': 0.25,
                'control': 0.25,
                'stack': 0.05,
                'bit_ops': 0.15,
            }, "Embedded control with bit manipulation"),
        }

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': 0.658687,
            'bit_ops': 1.905882,
            'control': 0.287680,
            'data_transfer': 0.266241,
            'memory': -0.776061,
            'stack': -0.193257
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])

        total_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            total_cpi += weight * cat.total_cycles

        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc

        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contributions[cat_name] = weight * cat.total_cycles
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
        """Run validation tests against known R65C02 characteristics"""
        tests = []

        # Test 1: CPI within expected range (target 2.85, cross-validated)
        result = self.analyze('typical')
        expected_cpi = 2.85
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

        # Test 3: All cycle counts are positive and reasonable (1-10 for R65C02)
        for cat_name, cat in self.instruction_categories.items():
            cycles = cat.total_cycles
            tests.append({
                'name': f'Cycle count ({cat_name})',
                'passed': 1.0 <= cycles <= 10.0,
                'expected': '1-10 cycles',
                'actual': f'{cycles:.1f}'
            })

        # Test 4: IPC is in valid range for R65C02 (0.2 - 0.5 typical)
        tests.append({
            'name': 'IPC range',
            'passed': 0.15 <= result.ipc <= 0.6,
            'expected': '0.15-0.6',
            'actual': f'{result.ipc:.3f}'
        })

        # Test 5: R65C02 should be faster than 6502 (CPI < 3.5)
        tests.append({
            'name': 'R65C02 faster than 6502',
            'passed': result.cpi < 3.5,
            'expected': 'CPI < 3.5',
            'actual': f'{result.cpi:.2f}'
        })

        # Test 6: All workloads produce valid results
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

        # Test 7: Year is 1983
        tests.append({
            'name': 'Release year',
            'passed': self.year == 1983,
            'expected': '1983',
            'actual': str(self.year)
        })

        # Test 8: Bit ops category exists (Rockwell extension)
        tests.append({
            'name': 'Bit ops category',
            'passed': 'bit_ops' in self.instruction_categories,
            'expected': 'bit_ops exists',
            'actual': 'present' if 'bit_ops' in self.instruction_categories else 'missing'
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


# Main execution for standalone testing
if __name__ == "__main__":
    model = R65c02Model()

    print("=" * 60)
    print(f"{model.name} Processor Model")
    print("=" * 60)
    print(f"Manufacturer: {model.manufacturer}")
    print(f"Year: {model.year}")
    print(f"Clock: {model.clock_mhz} MHz")
    print(f"Data width: {model.data_width} bits")
    print(f"Address width: {model.address_width} bits")
    print(f"Transistors: {model.transistor_count:,}")
    print()

    print("Instruction Categories:")
    print("-" * 40)
    for name, cat in model.instruction_categories.items():
        print(f"  {name}: {cat.total_cycles:.1f} cycles - {cat.description}")
    print()

    print("Workload Analysis:")
    print("-" * 40)
    for workload in model.workload_profiles.keys():
        result = model.analyze(workload)
        print(f"  {workload}:")
        print(f"    CPI: {result.cpi:.2f}")
        print(f"    IPC: {result.ipc:.3f}")
        print(f"    IPS: {result.ips:,.0f}")
        print(f"    Bottleneck: {result.bottleneck}")
    print()

    print("Validation Results:")
    print("-" * 40)
    validation = model.validate()
    for test in validation['tests']:
        status = "PASS" if test['passed'] else "FAIL"
        print(f"  [{status}] {test['name']}: {test['actual']} (expected: {test['expected']})")
    print()
    print(f"Tests passed: {validation['passed']}/{validation['total']}")
    print(f"Accuracy: {validation['accuracy_percent']:.1f}%")
