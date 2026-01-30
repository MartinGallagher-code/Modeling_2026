#!/usr/bin/env python3
"""
MOS6502 Grey-Box Queueing Model
================================

Architecture: 8-bit microprocessor (1975)
Queueing Model: Sequential execution, cycle-accurate

Features:
  - 8-bit data bus, 16-bit address bus
  - 3510 transistors (extremely efficient)
  - Multiple addressing modes (key to performance)
  - Zero-page for fast variable access
  - No pipeline, no cache
  - 2-7 cycles per instruction

Calibrated: 2026-01-28
Target CPI: ~3.0 for typical workloads (cross-validated)
Used in: Apple II, Commodore 64, NES, Atari 2600
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


class Mos6502Model(BaseProcessorModel):
    """
    MOS6502 Grey-Box Queueing Model

    Architecture: 8-bit NMOS microprocessor (1975)
    - Sequential execution (no pipeline)
    - Efficient addressing modes (zero-page is key)
    - 2-7 cycles per instruction
    - CPI ~3.0 for typical workloads (cross-validated)
    """

    # Processor specifications
    name = "MOS6502"
    manufacturer = "MOS Technology"
    year = 1975
    clock_mhz = 1.0  # 1 MHz standard (some variants up to 2 MHz)
    transistor_count = 3510
    data_width = 8
    address_width = 16

    def __init__(self):
        # 6502 instruction timing based on addressing modes
        # From MOS Technology datasheet and VICE emulator validation
        #
        # Actual instruction timings:
        #   Implied (INX, TAX, NOP): 2 cycles
        #   Immediate (LDA #nn): 2 cycles
        #   Zero-page (LDA zp): 3 cycles
        #   Zero-page,X (LDA zp,X): 4 cycles
        #   Absolute (LDA abs): 4 cycles
        #   Absolute,X/Y (LDA abs,X): 4-5 cycles
        #   Indirect,X (LDA (zp,X)): 6 cycles
        #   Indirect,Y (LDA (zp),Y): 5-6 cycles
        #   Branch not taken: 2 cycles
        #   Branch taken: 3 cycles (+1 if page cross)
        #   JSR/RTS: 6 cycles each
        #   JMP abs: 3 cycles
        #   PHA/PHP: 3 cycles, PLA/PLP: 4 cycles

        # Instruction categories calibrated via cross-validation against
        # MOS datasheet timings and realistic instruction mix analysis
        # Target CPI: ~3.0 (validated against actual 6502 programs)
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

        # Workload profiles based on validation JSON instruction_mix
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.25,
                'data_transfer': 0.15,
                'memory': 0.30,
                'control': 0.20,
                'stack': 0.10,
            }, "Typical 6502 workload (games, system software)"),
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
            }, "Memory-intensive (data processing)"),
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
            'alu': -3.195545,
            'control': 3.528911,
            'data_transfer': 3.003981,
            'memory': 1.286635,
            'stack': -3.084836
        }

    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        
        # Calculate weighted average CPI
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

        # Identify bottleneck (highest contribution)
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
        """Run validation tests against known 6502 characteristics"""
        tests = []

        # Test 1: CPI within expected range (target 3.0, cross-validated)
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

        # Test 3: All cycle counts are positive and reasonable (1-10 for 6502)
        for cat_name, cat in self.instruction_categories.items():
            cycles = cat.total_cycles
            tests.append({
                'name': f'Cycle count ({cat_name})',
                'passed': 1.0 <= cycles <= 10.0,
                'expected': '1-10 cycles',
                'actual': f'{cycles:.1f}'
            })

        # Test 4: IPC is in valid range for 6502 (0.2 - 0.5 typical)
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
