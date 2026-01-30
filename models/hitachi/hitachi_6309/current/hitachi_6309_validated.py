#!/usr/bin/env python3
"""
Hitachi 6309 Grey-Box Queueing Model
=====================================

Architecture: Enhanced 8-bit microprocessor (1982)
Queueing Model: Sequential execution, cycle-accurate

"The best 8-bit CPU ever made"

Features:
  - Enhanced Motorola 6809 with native mode features
  - Two 8-bit accumulators (A, B) combinable as 16-bit D
  - Additional registers: E, F (combinable as 16-bit W), V, 0, MD
  - Q = D:W (32-bit accumulator)
  - Two index registers (X, Y), two stack pointers (S, U)
  - Position-independent code support
  - Hardware 16x16 multiply instruction (MULD)
  - Hardware 32/16 divide instruction (DIVD, DIVQ)
  - Block transfer instructions (TFM)
  - Runs 6809 code 10% faster in emulation mode
  - Native mode for even faster execution
  - 2-25 cycles per instruction

Calibrated: 2026-01-29
Target CPI: ~3.0 for typical workloads (15% faster than 6809)
Used in: Tandy Color Computer 3, enhanced CoCo systems
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

class Hitachi6309Model(BaseProcessorModel):
    """
    Hitachi 6309 Grey-Box Queueing Model

    Architecture: Enhanced 8-bit CMOS microprocessor (1982)
    - Enhanced 6809 with additional registers and instructions
    - Native mode for faster execution
    - 16x16 multiply, 32/16 divide, block transfers
    - CPI ~3.0 for typical workloads (15% faster than 6809's 3.5)

    Modes:
    - Emulation mode: 6809-compatible, ~10% faster than 6809
    - Native mode: Access to all 6309 features, even faster
    """

    # Processor specifications
    name = "Hitachi 6309"
    manufacturer = "Hitachi"
    year = 1982
    clock_mhz = 2.0  # Typical clock, supports 1-3.5 MHz
    transistor_count = 12000  # Estimated, enhanced over 6809's 9000
    data_width = 8
    address_width = 16

    def __init__(self, mode: str = 'native'):
        """
        Initialize 6309 model.

        Args:
            mode: 'native' for full 6309 features, 'emulation' for 6809 compatibility
        """
        self.mode = mode

        if mode == 'native':
            self._init_native_mode()
        else:
            self._init_emulation_mode()

        self._init_workload_profiles()

        # Correction terms for system identification (initially zero)
        self.corrections = {
            'alu': -1.508170,
            'alu_16bit': -2.157300,
            'bit_manipulation': -4.841465,
            'block_transfer': -4.287143,
            'control': -0.574897,
            'data_transfer': 3.567910,
            'divide': -0.293685,
            'memory': -0.552564,
            'multiply_16x16': -12.856438,
            'multiply_8x8': -4.261231,
            'stack': 4.999948
        }

    def _init_native_mode(self):
        """
        Native mode instruction timings.

        Native mode advantages:
        - Faster multiply/divide with new instructions
        - Block transfer instructions (TFM)
        - Access to E, F, W, V, 0 registers
        - Additional addressing modes
        - Many instructions 1 cycle faster than 6809
        """
        # 6309 Native mode instruction timing
        # Most 6809 instructions are 1 cycle faster
        # LDA imm @2, LDA dir @3 (was 4), LDD imm @3
        # ADDA imm @2, MULD @25-28
        # JMP @3 (was 4), JSR @7 (was 8), RTS @4 (was 5), BEQ @3
        # TFM (block transfer) @6+3n
        # DIVD @25, DIVQ @34
        # 6309 Native mode instruction timing - calibrated for CPI ~3.0
        # Most 6809 instructions are 1 cycle faster in native mode
        # Timing based on community measurements and datasheet analysis
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1.9, 0,
                "ALU ops - ADDA imm @2, 1 cycle faster than 6809"),
            'alu_16bit': InstructionCategory('alu_16bit', 2.8, 0,
                "16-bit ALU - ADDD @3, native mode optimized"),
            'data_transfer': InstructionCategory('data_transfer', 2.3, 0,
                "LDA imm @2, LDD imm @3, LDW imm @4"),
            'memory': InstructionCategory('memory', 3.3, 0,
                "LDA dir @3, STA dir @3 (1 cycle faster)"),
            'control': InstructionCategory('control', 3.0, 0,
                "JMP @3, BEQ @3, JSR @7, RTS @4 (faster)"),
            'stack': InstructionCategory('stack', 4.2, 0,
                "PSHS/PULS @4+ (faster)"),
            'multiply_8x8': InstructionCategory('multiply_8x8', 10.0, 0,
                "MUL @10 (6809 compatible, slightly faster)"),
            'multiply_16x16': InstructionCategory('multiply_16x16', 26.0, 0,
                "MULD @25-28 (16x16->32, native mode only)"),
            'divide': InstructionCategory('divide', 28.0, 0,
                "DIVD @25 (16/8->8), DIVQ @34 (32/16->16)"),
            'block_transfer': InstructionCategory('block_transfer', 9.0, 0,
                "TFM @6+3n, average ~9 for small blocks"),
            'bit_manipulation': InstructionCategory('bit_manipulation', 5.0, 0,
                "Native mode bit operations - BAND, BOR, etc."),
        }

    def _init_emulation_mode(self):
        """
        Emulation mode instruction timings.

        Emulation mode runs 6809 code ~10% faster due to:
        - Improved internal architecture
        - Better bus timing
        - Still limited to 6809 instruction set
        """
        # Emulation mode: 6809 compatible but ~10% faster
        # Same instructions as 6809, slightly faster execution
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 2.2, 0,
                "ALU ops - ADDA imm @2, ~10% faster than 6809"),
            'data_transfer': InstructionCategory('data_transfer', 2.5, 0,
                "LDA imm @2, LDD imm @3"),
            'memory': InstructionCategory('memory', 3.9, 0,
                "LDA dir @4, STA dir @4, ~10% faster"),
            'control': InstructionCategory('control', 3.7, 0,
                "JMP @4, BEQ @3, JSR @7, RTS @5"),
            'stack': InstructionCategory('stack', 4.9, 0,
                "PSHS/PULS @5+, ~10% faster"),
            'multiply': InstructionCategory('multiply', 10.0, 0,
                "MUL @10 (slightly faster than 6809's 11)"),
        }

    def _init_workload_profiles(self):
        """Initialize workload profiles for both modes."""
        if self.mode == 'native':
            # Typical workload weights calibrated for CPI ~3.0
            # Expensive operations (multiply_16x16, divide) are rare in typical code
            # Most code is simple ALU, data movement, and control flow
            self.workload_profiles = {
                'typical': WorkloadProfile('typical', {
                    'alu': 0.32,           # Simple ALU ops dominate
                    'alu_16bit': 0.08,     # Some 16-bit math
                    'data_transfer': 0.25, # Load/store immediate
                    'memory': 0.15,        # Memory access
                    'control': 0.12,       # Branches/jumps
                    'stack': 0.04,         # Push/pull
                    'multiply_8x8': 0.02,  # Occasional 8x8 multiply
                    'multiply_16x16': 0.005, # Rare 16x16 multiply
                    'divide': 0.002,       # Very rare division
                    'block_transfer': 0.01,# Some block moves
                    'bit_manipulation': 0.013, # Occasional bit ops
                }, "Typical 6309 native mode workload"),
                'compute': WorkloadProfile('compute', {
                    'alu': 0.35,
                    'alu_16bit': 0.18,
                    'data_transfer': 0.18,
                    'memory': 0.10,
                    'control': 0.08,
                    'stack': 0.02,
                    'multiply_8x8': 0.04,
                    'multiply_16x16': 0.02,
                    'divide': 0.01,
                    'block_transfer': 0.01,
                    'bit_manipulation': 0.01,
                }, "Compute-intensive with 16-bit math"),
                'memory': WorkloadProfile('memory', {
                    'alu': 0.15,
                    'alu_16bit': 0.05,
                    'data_transfer': 0.18,
                    'memory': 0.35,
                    'control': 0.12,
                    'stack': 0.06,
                    'multiply_8x8': 0.01,
                    'multiply_16x16': 0.005,
                    'divide': 0.00,
                    'block_transfer': 0.06,
                    'bit_manipulation': 0.015,
                }, "Memory-intensive with block transfers"),
                'control': WorkloadProfile('control', {
                    'alu': 0.15,
                    'alu_16bit': 0.05,
                    'data_transfer': 0.12,
                    'memory': 0.13,
                    'control': 0.40,
                    'stack': 0.10,
                    'multiply_8x8': 0.02,
                    'multiply_16x16': 0.005,
                    'divide': 0.005,
                    'block_transfer': 0.01,
                    'bit_manipulation': 0.01,
                }, "Control-flow intensive"),
                'graphics': WorkloadProfile('graphics', {
                    'alu': 0.18,
                    'alu_16bit': 0.08,
                    'data_transfer': 0.15,
                    'memory': 0.25,
                    'control': 0.10,
                    'stack': 0.02,
                    'multiply_8x8': 0.05,
                    'multiply_16x16': 0.02,
                    'divide': 0.01,
                    'block_transfer': 0.10,
                    'bit_manipulation': 0.04,
                }, "Graphics/game workload with block transfers"),
            }
        else:
            # Emulation mode profiles (6809 compatible)
            self.workload_profiles = {
                'typical': WorkloadProfile('typical', {
                    'alu': 0.30,
                    'data_transfer': 0.25,
                    'memory': 0.20,
                    'control': 0.18,
                    'stack': 0.05,
                    'multiply': 0.02,
                }, "Typical 6809-compatible workload"),
                'compute': WorkloadProfile('compute', {
                    'alu': 0.40,
                    'data_transfer': 0.25,
                    'memory': 0.15,
                    'control': 0.12,
                    'stack': 0.03,
                    'multiply': 0.05,
                }, "Compute-intensive 6809 workload"),
                'memory': WorkloadProfile('memory', {
                    'alu': 0.15,
                    'data_transfer': 0.20,
                    'memory': 0.40,
                    'control': 0.15,
                    'stack': 0.08,
                    'multiply': 0.02,
                }, "Memory-intensive 6809 workload"),
                'control': WorkloadProfile('control', {
                    'alu': 0.15,
                    'data_transfer': 0.15,
                    'memory': 0.15,
                    'control': 0.40,
                    'stack': 0.12,
                    'multiply': 0.03,
                }, "Control-flow intensive 6809 workload"),
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
            processor=f"{self.name} ({self.mode} mode)",
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

        # Test 1: CPI within expected range for native mode
        result = self.analyze('typical')
        if self.mode == 'native':
            expected_cpi = 3.0  # 6309 native mode target CPI
        else:
            expected_cpi = 3.15  # Emulation mode (~10% faster than 6809's 3.5)

        cpi_error = abs(result.cpi - expected_cpi) / expected_cpi * 100
        tests.append({
            'name': f'CPI accuracy ({self.mode} mode)',
            'passed': cpi_error < 5.0,
            'expected': f'{expected_cpi} +/- 5%',
            'actual': f'{result.cpi:.2f} ({cpi_error:.1f}% error)'
        })

        # Test 2: 6309 should be faster than 6809
        if self.mode == 'native':
            m6809_cpi = 3.5
            speedup = m6809_cpi / result.cpi
            expected_speedup = 1.15  # At least 15% faster
            tests.append({
                'name': 'Speedup over M6809',
                'passed': speedup >= 1.10,  # At least 10% faster
                'expected': f'>= 1.10x speedup',
                'actual': f'{speedup:.2f}x'
            })

        # Test 3: Workload weights sum to 1.0
        for profile_name, profile in self.workload_profiles.items():
            weight_sum = sum(profile.category_weights.values())
            tests.append({
                'name': f'Weights sum ({profile_name})',
                'passed': 0.99 <= weight_sum <= 1.01,
                'expected': '1.0',
                'actual': f'{weight_sum:.2f}'
            })

        # Test 4: All cycle counts are positive and reasonable
        for cat_name, cat in self.instruction_categories.items():
            cycles = cat.total_cycles
            tests.append({
                'name': f'Cycle count ({cat_name})',
                'passed': 0.5 <= cycles <= 200.0,
                'expected': '0.5-200 cycles',
                'actual': f'{cycles:.1f}'
            })

        # Test 5: IPC is in valid range
        tests.append({
            'name': 'IPC range',
            'passed': 0.05 <= result.ipc <= 1.5,
            'expected': '0.05-1.5',
            'actual': f'{result.ipc:.3f}'
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

        # Test 7: Native mode specific - verify new instruction categories exist
        if self.mode == 'native':
            required_cats = ['multiply_16x16', 'divide', 'block_transfer']
            for cat in required_cats:
                tests.append({
                    'name': f'Native instruction ({cat})',
                    'passed': cat in self.instruction_categories,
                    'expected': 'Category exists',
                    'actual': 'Present' if cat in self.instruction_categories else 'Missing'
                })

        passed = sum(1 for t in tests if t['passed'])
        return {
            'tests': tests,
            'passed': passed,
            'total': len(tests),
            'accuracy_percent': 100.0 - cpi_error,
            'mode': self.mode
        }

    def compare_to_6809(self) -> Dict[str, Any]:
        """Compare performance to original M6809"""
        m6809_cpi = 3.5  # M6809 typical CPI

        result = self.analyze('typical')
        speedup = m6809_cpi / result.cpi

        return {
            'mode': self.mode,
            '6809_cpi': m6809_cpi,
            '6309_cpi': result.cpi,
            'speedup': speedup,
            'speedup_percent': (speedup - 1.0) * 100,
            'explanation': (
                f"6309 in {self.mode} mode is {speedup:.2f}x faster than 6809 "
                f"({(speedup-1)*100:.1f}% speedup)"
            )
        }

    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories

    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles

    def get_register_set(self) -> Dict[str, str]:
        """Return the 6309 register set"""
        return {
            # 6809-compatible registers
            'A': '8-bit accumulator A',
            'B': '8-bit accumulator B',
            'D': '16-bit accumulator (A:B)',
            'X': '16-bit index register',
            'Y': '16-bit index register',
            'S': '16-bit system stack pointer',
            'U': '16-bit user stack pointer',
            'PC': '16-bit program counter',
            'CC': '8-bit condition codes',
            'DP': '8-bit direct page register',
            # 6309-specific registers (native mode)
            'E': '8-bit accumulator E (native mode)',
            'F': '8-bit accumulator F (native mode)',
            'W': '16-bit accumulator (E:F, native mode)',
            'Q': '32-bit accumulator (D:W, native mode)',
            'V': '16-bit register V (native mode)',
            '0': 'Zero register (always 0, native mode)',
            'MD': 'Mode/error register (native mode)',
        }

    def get_new_instructions(self) -> Dict[str, str]:
        """Return 6309-specific instructions not in 6809"""
        return {
            # 16-bit multiply
            'MULD': '16x16->32 signed multiply (D * mem -> Q)',
            # Division
            'DIVD': '16/8->8 signed divide (D / mem -> A rem B)',
            'DIVQ': '32/16->16 signed divide (Q / mem -> D rem W)',
            # Block transfers
            'TFM': 'Block transfer (X+ to Y+, X- to Y-, X+ to Y, X to Y+)',
            # Bit manipulation
            'BAND': 'AND bit to CC',
            'BOR': 'OR bit to CC',
            'BEOR': 'XOR bit to CC',
            'BIAND': 'AND inverted bit to CC',
            'BIOR': 'OR inverted bit to CC',
            'BIEOR': 'XOR inverted bit to CC',
            'LDBT': 'Load bit to memory',
            'STBT': 'Store bit from CC',
            # Inter-register operations
            'ADDR': 'Add register to register',
            'ADCR': 'Add with carry register to register',
            'SUBR': 'Subtract register from register',
            'SBCR': 'Subtract with borrow register from register',
            'ANDR': 'AND register with register',
            'ORR': 'OR register with register',
            'EORR': 'XOR register with register',
            'CMPR': 'Compare register with register',
            # New load/store for new registers
            'LDE': 'Load E register',
            'LDF': 'Load F register',
            'LDW': 'Load W register',
            'LDQ': 'Load Q register (32-bit)',
            'STE': 'Store E register',
            'STF': 'Store F register',
            'STW': 'Store W register',
            'STQ': 'Store Q register (32-bit)',
            # Misc
            'SEXW': 'Sign extend W (8->16)',
            'NEGD': 'Negate D (two\'s complement)',
            'COMD': 'Complement D (one\'s complement)',
            'TSTD': 'Test D register',
        }


if __name__ == '__main__':
    print("=" * 60)
    print("Hitachi 6309 Model Validation")
    print("'The best 8-bit CPU ever made'")
    print("=" * 60)

    # Test native mode
    print("\n--- Native Mode ---")
    model_native = Hitachi6309Model(mode='native')
    result_native = model_native.analyze('typical')
    print(f"CPI: {result_native.cpi:.2f}")
    print(f"IPC: {result_native.ipc:.3f}")
    print(f"MIPS @ {model_native.clock_mhz} MHz: {result_native.ips/1e6:.3f}")
    print(f"Bottleneck: {result_native.bottleneck}")

    validation_native = model_native.validate()
    print(f"\nValidation: {validation_native['passed']}/{validation_native['total']} tests passed")
    print(f"Accuracy: {validation_native['accuracy_percent']:.1f}%")

    comparison = model_native.compare_to_6809()
    print(f"\n{comparison['explanation']}")

    # Test emulation mode
    print("\n--- Emulation Mode (6809 compatible) ---")
    model_emu = Hitachi6309Model(mode='emulation')
    result_emu = model_emu.analyze('typical')
    print(f"CPI: {result_emu.cpi:.2f}")
    print(f"IPC: {result_emu.ipc:.3f}")

    comparison_emu = model_emu.compare_to_6809()
    print(f"{comparison_emu['explanation']}")

    # Show failed tests if any
    all_passed = True
    for test in validation_native['tests']:
        if not test['passed']:
            all_passed = False
            print(f"\nFAILED: {test['name']}")
            print(f"  Expected: {test['expected']}")
            print(f"  Actual: {test['actual']}")

    if all_passed:
        print("\nAll validation tests PASSED!")

    print("\n" + "=" * 60)
    print("6309-specific registers:")
    for reg, desc in model_native.get_register_set().items():
        if 'native' in desc:
            print(f"  {reg}: {desc}")
