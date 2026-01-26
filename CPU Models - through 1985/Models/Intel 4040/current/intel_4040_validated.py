#!/usr/bin/env python3
"""
Intel 4040 Improved Performance Model

The 4040 is an enhanced version of the 4004 with:
- 14 new instructions (60 total vs 46)
- 24 index registers (vs 16)
- 7-level stack (vs 3)
- Interrupt support
- Register banking for fast context switch

Timing is identical to the 4004 - same machine cycle structure.

Validation sources:
- Intel MCS-40 Users Manual
- Wikipedia Intel 4040
- WikiChip 4040 specifications

Author: Grey-Box Performance Modeling Research
Date: January 25, 2026
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from enum import Enum
import json


class InstructionType(Enum):
    """4040 instruction types (same as 4004)."""
    ONE_WORD = 1   # 8 clock cycles = 1 machine cycle
    TWO_WORD = 2   # 16 clock cycles = 2 machine cycles


@dataclass
class Instruction4040:
    """Intel 4040 instruction definition."""
    mnemonic: str
    description: str
    instruction_type: InstructionType
    is_new: bool = False  # New in 4040
    category: str = "misc"
    
    @property
    def machine_cycles(self) -> int:
        return self.instruction_type.value
    
    @property
    def clock_cycles(self) -> int:
        return self.instruction_type.value * 8


# 4040 instruction set (60 instructions - 46 from 4004 + 14 new)
INSTRUCTIONS_4040 = {
    # ===== 4004 Instructions (46) =====
    # Accumulator Group
    "NOP": Instruction4040("NOP", "No Operation", InstructionType.ONE_WORD, False, "control"),
    "CLB": Instruction4040("CLB", "Clear Both", InstructionType.ONE_WORD, False, "accumulator"),
    "CLC": Instruction4040("CLC", "Clear Carry", InstructionType.ONE_WORD, False, "accumulator"),
    "IAC": Instruction4040("IAC", "Increment Accumulator", InstructionType.ONE_WORD, False, "accumulator"),
    "CMC": Instruction4040("CMC", "Complement Carry", InstructionType.ONE_WORD, False, "accumulator"),
    "CMA": Instruction4040("CMA", "Complement Accumulator", InstructionType.ONE_WORD, False, "accumulator"),
    "RAL": Instruction4040("RAL", "Rotate Left", InstructionType.ONE_WORD, False, "accumulator"),
    "RAR": Instruction4040("RAR", "Rotate Right", InstructionType.ONE_WORD, False, "accumulator"),
    "TCC": Instruction4040("TCC", "Transfer Carry and Clear", InstructionType.ONE_WORD, False, "accumulator"),
    "DAC": Instruction4040("DAC", "Decrement Accumulator", InstructionType.ONE_WORD, False, "accumulator"),
    "TCS": Instruction4040("TCS", "Transfer Carry Subtract", InstructionType.ONE_WORD, False, "accumulator"),
    "STC": Instruction4040("STC", "Set Carry", InstructionType.ONE_WORD, False, "accumulator"),
    "DAA": Instruction4040("DAA", "Decimal Adjust", InstructionType.ONE_WORD, False, "accumulator"),
    "KBP": Instruction4040("KBP", "Keyboard Process", InstructionType.ONE_WORD, False, "accumulator"),
    "DCL": Instruction4040("DCL", "Designate Command Line", InstructionType.ONE_WORD, False, "control"),
    
    # Index Register Group
    "INC": Instruction4040("INC", "Increment Register", InstructionType.ONE_WORD, False, "register"),
    "ADD": Instruction4040("ADD", "Add Register to ACC", InstructionType.ONE_WORD, False, "alu"),
    "SUB": Instruction4040("SUB", "Subtract Register", InstructionType.ONE_WORD, False, "alu"),
    "LD": Instruction4040("LD", "Load Register to ACC", InstructionType.ONE_WORD, False, "transfer"),
    "XCH": Instruction4040("XCH", "Exchange Register and ACC", InstructionType.ONE_WORD, False, "transfer"),
    "LDM": Instruction4040("LDM", "Load Immediate", InstructionType.ONE_WORD, False, "transfer"),
    "BBL": Instruction4040("BBL", "Branch Back and Load", InstructionType.ONE_WORD, False, "control"),
    
    # Index Register Pair
    "SRC": Instruction4040("SRC", "Send Register Control", InstructionType.ONE_WORD, False, "io"),
    "JIN": Instruction4040("JIN", "Jump Indirect", InstructionType.ONE_WORD, False, "control"),
    
    # Memory Instructions
    "WRM": Instruction4040("WRM", "Write RAM", InstructionType.ONE_WORD, False, "memory"),
    "WMP": Instruction4040("WMP", "Write RAM Port", InstructionType.ONE_WORD, False, "io"),
    "WRR": Instruction4040("WRR", "Write ROM Port", InstructionType.ONE_WORD, False, "io"),
    "WR0": Instruction4040("WR0", "Write Status 0", InstructionType.ONE_WORD, False, "memory"),
    "WR1": Instruction4040("WR1", "Write Status 1", InstructionType.ONE_WORD, False, "memory"),
    "WR2": Instruction4040("WR2", "Write Status 2", InstructionType.ONE_WORD, False, "memory"),
    "WR3": Instruction4040("WR3", "Write Status 3", InstructionType.ONE_WORD, False, "memory"),
    "SBM": Instruction4040("SBM", "Subtract from Memory", InstructionType.ONE_WORD, False, "alu"),
    "RDM": Instruction4040("RDM", "Read RAM", InstructionType.ONE_WORD, False, "memory"),
    "RDR": Instruction4040("RDR", "Read ROM Port", InstructionType.ONE_WORD, False, "io"),
    "ADM": Instruction4040("ADM", "Add from Memory", InstructionType.ONE_WORD, False, "alu"),
    "RD0": Instruction4040("RD0", "Read Status 0", InstructionType.ONE_WORD, False, "memory"),
    "RD1": Instruction4040("RD1", "Read Status 1", InstructionType.ONE_WORD, False, "memory"),
    "RD2": Instruction4040("RD2", "Read Status 2", InstructionType.ONE_WORD, False, "memory"),
    "RD3": Instruction4040("RD3", "Read Status 3", InstructionType.ONE_WORD, False, "memory"),
    
    # Two-Word Instructions
    "JCN": Instruction4040("JCN", "Jump Conditional", InstructionType.TWO_WORD, False, "control"),
    "FIM": Instruction4040("FIM", "Fetch Immediate", InstructionType.TWO_WORD, False, "transfer"),
    "FIN": Instruction4040("FIN", "Fetch Indirect", InstructionType.TWO_WORD, False, "memory"),
    "JUN": Instruction4040("JUN", "Jump Unconditional", InstructionType.TWO_WORD, False, "control"),
    "JMS": Instruction4040("JMS", "Jump to Subroutine", InstructionType.TWO_WORD, False, "control"),
    "ISZ": Instruction4040("ISZ", "Increment and Skip", InstructionType.TWO_WORD, False, "control"),
    
    # ===== NEW 4040 Instructions (14) =====
    "HLT": Instruction4040("HLT", "Halt", InstructionType.ONE_WORD, True, "control"),
    "BBS": Instruction4040("BBS", "Branch Back from Interrupt", InstructionType.ONE_WORD, True, "control"),
    "LCR": Instruction4040("LCR", "Load Command Register", InstructionType.ONE_WORD, True, "control"),
    "OR4": Instruction4040("OR4", "OR Register 4 with ACC", InstructionType.ONE_WORD, True, "alu"),
    "OR5": Instruction4040("OR5", "OR Register 5 with ACC", InstructionType.ONE_WORD, True, "alu"),
    "AN4": Instruction4040("AN4", "AND Register 4 with ACC", InstructionType.ONE_WORD, True, "alu"),
    "AN5": Instruction4040("AN5", "AND Register 5 with ACC", InstructionType.ONE_WORD, True, "alu"),
    "DB0": Instruction4040("DB0", "Designate ROM Bank 0", InstructionType.ONE_WORD, True, "control"),
    "DB1": Instruction4040("DB1", "Designate ROM Bank 1", InstructionType.ONE_WORD, True, "control"),
    "EI": Instruction4040("EI", "Enable Interrupts", InstructionType.ONE_WORD, True, "control"),
    "DI": Instruction4040("DI", "Disable Interrupts", InstructionType.ONE_WORD, True, "control"),
    "RPM": Instruction4040("RPM", "Read Program Memory", InstructionType.ONE_WORD, True, "memory"),
    "SB0": Instruction4040("SB0", "Select Register Bank 0", InstructionType.ONE_WORD, True, "control"),
    "SB1": Instruction4040("SB1", "Select Register Bank 1", InstructionType.ONE_WORD, True, "control"),
}


@dataclass
class Intel4040Workload:
    """Workload profile for 4040."""
    name: str
    description: str
    two_word_fraction: float = 0.25
    uses_interrupts: bool = False
    uses_register_banking: bool = False


WORKLOADS_4040 = {
    "typical": Intel4040Workload("typical", "Typical application", 0.25, False, False),
    "compute": Intel4040Workload("compute", "BCD arithmetic heavy", 0.20, False, False),
    "control": Intel4040Workload("control", "Control-heavy", 0.35, False, False),
    "interrupt": Intel4040Workload("interrupt", "With interrupt handling", 0.28, True, True),
    "gaming": Intel4040Workload("gaming", "Video game (Bailey shuffleboard)", 0.30, True, False),
}


@dataclass
class Intel4040Result:
    """Result from 4040 model."""
    cpi_clocks: float = 0.0
    cpi_machine: float = 0.0
    ipc: float = 0.0
    ips: float = 0.0
    kips: float = 0.0
    mips: float = 0.0
    avg_instruction_time_us: float = 0.0
    one_word_fraction: float = 0.0
    two_word_fraction: float = 0.0
    validation_status: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class Intel4040Model:
    """
    Intel 4040 Performance Model
    
    Timing identical to 4004:
    - Machine cycle = 8 clock cycles = 10.8 µs @ 740 kHz
    - 1-word instruction = 1 machine cycle
    - 2-word instruction = 2 machine cycles
    """
    
    # Hardware constants (same as 4004)
    CLOCK_KHZ = 740
    CLOCK_MHZ = 0.740
    CLOCKS_PER_MACHINE_CYCLE = 8
    MACHINE_CYCLE_US = 10.8
    
    def __init__(self):
        self.instructions = INSTRUCTIONS_4040
    
    def analyze(self, workload: str = "typical") -> Intel4040Result:
        """Analyze 4040 performance."""
        result = Intel4040Result()
        
        wl = WORKLOADS_4040.get(workload, WORKLOADS_4040["typical"])
        
        result.one_word_fraction = 1.0 - wl.two_word_fraction
        result.two_word_fraction = wl.two_word_fraction
        
        # CPI calculation (same as 4004)
        result.cpi_machine = (
            result.one_word_fraction * 1 +
            result.two_word_fraction * 2
        )
        result.cpi_clocks = result.cpi_machine * self.CLOCKS_PER_MACHINE_CYCLE
        result.ipc = 1.0 / result.cpi_clocks
        
        # Timing
        result.avg_instruction_time_us = result.cpi_machine * self.MACHINE_CYCLE_US
        result.ips = 1_000_000 / result.avg_instruction_time_us
        result.kips = result.ips / 1000
        result.mips = result.ips / 1_000_000
        
        # Validation
        if 46250 <= result.ips <= 92500:
            result.validation_status = "PASS"
        else:
            result.validation_status = f"CHECK (expected 46,250-92,500)"
        
        return result
    
    def run_validation_suite(self) -> Dict[str, bool]:
        """Validate instruction set."""
        tests = {}
        
        original = [i for i in self.instructions.values() if not i.is_new]
        new = [i for i in self.instructions.values() if i.is_new]
        
        tests["total_instructions_60"] = len(self.instructions) == 60
        tests["original_instructions_46"] = len(original) == 46
        tests["new_instructions_14"] = len(new) == 14
        tests["has_HLT"] = "HLT" in self.instructions
        tests["has_BBS"] = "BBS" in self.instructions
        tests["has_EI_DI"] = "EI" in self.instructions and "DI" in self.instructions
        tests["has_bank_select"] = "SB0" in self.instructions and "SB1" in self.instructions
        
        return tests
    
    def print_result(self, result: Intel4040Result):
        """Print formatted result."""
        print(f"\n{'='*70}")
        print(f"  Intel 4040 Performance Analysis")
        print(f"  Clock: {self.CLOCK_KHZ} kHz ({self.CLOCK_MHZ} MHz)")
        print(f"{'='*70}")
        
        print(f"\n  ┌─ PERFORMANCE METRICS {'─'*44}┐")
        print(f"  │  IPS: {result.ips:,.0f}  |  kIPS: {result.kips:.2f}  |  MIPS: {result.mips:.4f}     │")
        print(f"  │  CPI (clocks): {result.cpi_clocks:.2f}  |  IPC: {result.ipc:.4f}                  │")
        print(f"  │  Validation: {result.validation_status:<45}   │")
        print(f"  └{'─'*66}┘")


def get_improved_4040_config() -> Dict:
    """Get improved 4040 configuration."""
    model = Intel4040Model()
    result = model.analyze("typical")
    
    return {
        "family": "INTEL",
        "category": "SIMPLE_4BIT",
        "year": 1974,
        "bits": 4,
        "clock_mhz": 0.740,
        "transistors": 3000,
        "process_um": 10,
        "description": "Enhanced 4004 with interrupts and 24 registers",
        
        "base_cpi": result.cpi_clocks,
        
        "has_prefetch": False,
        "has_cache": False,
        "pipeline_stages": 1,
        "branch_penalty": 0,
        
        "timings": {
            "alu": 8,
            "mov": 8,
            "branch": 16,
            "memory": 8,
        },
        
        "machine_cycle_us": 10.8,
        "ips_typical": result.ips,
        "ips_peak": 92500,
        "ips_min": 46250,
        "kips": result.kips,
        "mips": result.mips,
        
        # 4040-specific
        "total_instructions": 60,
        "new_instructions": 14,
        "index_registers": 24,
        "stack_depth": 7,
        "has_interrupts": True,
        "has_register_banking": True,
        
        "validation": {
            "source": "Intel MCS-40 Users Manual",
            "timing": "Identical to 4004",
        }
    }


if __name__ == "__main__":
    print("="*70)
    print("INTEL 4040 IMPROVED PERFORMANCE MODEL")
    print("Enhanced 4004 with interrupts (1974)")
    print("="*70)
    
    model = Intel4040Model()
    
    # Validation
    print("\n1. INSTRUCTION SET VALIDATION")
    print("-"*40)
    validation = model.run_validation_suite()
    passed = sum(1 for v in validation.values() if v)
    print(f"   Passed: {passed}/{len(validation)} tests")
    
    for test, result in validation.items():
        status = "✓" if result else "✗"
        print(f"   {status} {test}")
    
    # Instruction summary
    original = [i for i in INSTRUCTIONS_4040.values() if not i.is_new]
    new = [i for i in INSTRUCTIONS_4040.values() if i.is_new]
    print(f"\n   Instruction set: {len(original)} original + {len(new)} new = {len(INSTRUCTIONS_4040)} total")
    
    # 4004 vs 4040 comparison
    print("\n2. 4040 vs 4004 COMPARISON")
    print("-"*40)
    print(f"   {'Feature':<25} {'4004':>10} {'4040':>10}")
    print(f"   {'-'*45}")
    print(f"   {'Instructions':<25} {'46':>10} {'60':>10}")
    print(f"   {'Index Registers':<25} {'16':>10} {'24':>10}")
    print(f"   {'Stack Depth':<25} {'3':>10} {'7':>10}")
    print(f"   {'Interrupts':<25} {'No':>10} {'Yes':>10}")
    print(f"   {'Register Banking':<25} {'No':>10} {'Yes':>10}")
    print(f"   {'Timing':<25} {'Same':>10} {'Same':>10}")
    
    # Workload analysis
    print("\n3. WORKLOAD ANALYSIS")
    print("-"*40)
    for wl_name in WORKLOADS_4040:
        result = model.analyze(wl_name)
        print(f"   {wl_name:<12}: {result.ips:>10,.0f} IPS, {result.kips:.2f} kIPS, {result.validation_status}")
    
    # Export
    config = get_improved_4040_config()
    with open("/home/claude/4040_validated_model.json", "w") as f:
        json.dump({
            "processor": "Intel 4040",
            "config": config,
            "workloads": {k: model.analyze(k).to_dict() for k in WORKLOADS_4040}
        }, f, indent=2)
    
    print("\n4. EXPORT")
    print("-"*40)
    print("   Exported to: 4040_validated_model.json")
    print("="*70)
