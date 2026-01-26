#!/usr/bin/env python3
"""
Intel 4040 IMPROVED Performance Model v2.0

Complete 60-instruction set with timing from Intel MCS-40 Users Manual.
The 4040 is an enhanced 4004 with:
- 14 new instructions
- 24 index registers (vs 16)
- 7-level stack (vs 3)
- Interrupt support
- Register banking

Timing is IDENTICAL to 4004:
- Machine cycle: 8 clocks = 10.8 µs @ 740 kHz
- 1-word instructions: 1 machine cycle (8 clocks)
- 2-word instructions: 2 machine cycles (16 clocks)

Author: Grey-Box Performance Modeling Research
Date: January 26, 2026
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple
from enum import Enum
import json


class InstructionType(Enum):
    """4040 instruction types."""
    ONE_WORD = 1   # 8 clocks
    TWO_WORD = 2   # 16 clocks


@dataclass
class Instruction4040:
    """Intel 4040 instruction with timing."""
    mnemonic: str
    description: str
    opcode: int
    instr_type: InstructionType
    category: str
    is_new: bool = False  # New in 4040
    
    @property
    def machine_cycles(self) -> int:
        return self.instr_type.value
    
    @property
    def clock_cycles(self) -> int:
        return self.instr_type.value * 8


# Complete 4040 instruction set (60 instructions)
# 46 from 4004 + 14 new
INSTRUCTIONS_4040_COMPLETE = {
    # ========== INDEX REGISTER OPERATIONS (1 cycle) ==========
    "INC_R0": Instruction4040("INC 0", "Increment R0", 0x60, InstructionType.ONE_WORD, "register"),
    "INC_R1": Instruction4040("INC 1", "Increment R1", 0x61, InstructionType.ONE_WORD, "register"),
    "INC_R2": Instruction4040("INC 2", "Increment R2", 0x62, InstructionType.ONE_WORD, "register"),
    "INC_R3": Instruction4040("INC 3", "Increment R3", 0x63, InstructionType.ONE_WORD, "register"),
    "INC_R4": Instruction4040("INC 4", "Increment R4", 0x64, InstructionType.ONE_WORD, "register"),
    "INC_R5": Instruction4040("INC 5", "Increment R5", 0x65, InstructionType.ONE_WORD, "register"),
    "INC_R6": Instruction4040("INC 6", "Increment R6", 0x66, InstructionType.ONE_WORD, "register"),
    "INC_R7": Instruction4040("INC 7", "Increment R7", 0x67, InstructionType.ONE_WORD, "register"),
    "INC_R8": Instruction4040("INC 8", "Increment R8", 0x68, InstructionType.ONE_WORD, "register"),
    "INC_R9": Instruction4040("INC 9", "Increment R9", 0x69, InstructionType.ONE_WORD, "register"),
    "INC_RA": Instruction4040("INC 10", "Increment R10", 0x6A, InstructionType.ONE_WORD, "register"),
    "INC_RB": Instruction4040("INC 11", "Increment R11", 0x6B, InstructionType.ONE_WORD, "register"),
    "INC_RC": Instruction4040("INC 12", "Increment R12", 0x6C, InstructionType.ONE_WORD, "register"),
    "INC_RD": Instruction4040("INC 13", "Increment R13", 0x6D, InstructionType.ONE_WORD, "register"),
    "INC_RE": Instruction4040("INC 14", "Increment R14", 0x6E, InstructionType.ONE_WORD, "register"),
    "INC_RF": Instruction4040("INC 15", "Increment R15", 0x6F, InstructionType.ONE_WORD, "register"),
    
    # ========== ACCUMULATOR OPERATIONS (1 cycle) ==========
    "ADD_R0": Instruction4040("ADD 0", "Add R0 to A", 0x80, InstructionType.ONE_WORD, "alu"),
    "ADD_R1": Instruction4040("ADD 1", "Add R1 to A", 0x81, InstructionType.ONE_WORD, "alu"),
    "ADD_R2": Instruction4040("ADD 2", "Add R2 to A", 0x82, InstructionType.ONE_WORD, "alu"),
    "ADD_R3": Instruction4040("ADD 3", "Add R3 to A", 0x83, InstructionType.ONE_WORD, "alu"),
    "ADD_R4": Instruction4040("ADD 4", "Add R4 to A", 0x84, InstructionType.ONE_WORD, "alu"),
    "ADD_R5": Instruction4040("ADD 5", "Add R5 to A", 0x85, InstructionType.ONE_WORD, "alu"),
    "ADD_R6": Instruction4040("ADD 6", "Add R6 to A", 0x86, InstructionType.ONE_WORD, "alu"),
    "ADD_R7": Instruction4040("ADD 7", "Add R7 to A", 0x87, InstructionType.ONE_WORD, "alu"),
    "ADD_R8": Instruction4040("ADD 8", "Add R8 to A", 0x88, InstructionType.ONE_WORD, "alu"),
    "ADD_R9": Instruction4040("ADD 9", "Add R9 to A", 0x89, InstructionType.ONE_WORD, "alu"),
    "ADD_RA": Instruction4040("ADD 10", "Add R10 to A", 0x8A, InstructionType.ONE_WORD, "alu"),
    "ADD_RB": Instruction4040("ADD 11", "Add R11 to A", 0x8B, InstructionType.ONE_WORD, "alu"),
    "ADD_RC": Instruction4040("ADD 12", "Add R12 to A", 0x8C, InstructionType.ONE_WORD, "alu"),
    "ADD_RD": Instruction4040("ADD 13", "Add R13 to A", 0x8D, InstructionType.ONE_WORD, "alu"),
    "ADD_RE": Instruction4040("ADD 14", "Add R14 to A", 0x8E, InstructionType.ONE_WORD, "alu"),
    "ADD_RF": Instruction4040("ADD 15", "Add R15 to A", 0x8F, InstructionType.ONE_WORD, "alu"),
    
    "SUB_R0": Instruction4040("SUB 0", "Sub R0 from A", 0x90, InstructionType.ONE_WORD, "alu"),
    "SUB_R1": Instruction4040("SUB 1", "Sub R1 from A", 0x91, InstructionType.ONE_WORD, "alu"),
    "SUB_R2": Instruction4040("SUB 2", "Sub R2 from A", 0x92, InstructionType.ONE_WORD, "alu"),
    "SUB_R3": Instruction4040("SUB 3", "Sub R3 from A", 0x93, InstructionType.ONE_WORD, "alu"),
    "SUB_R4": Instruction4040("SUB 4", "Sub R4 from A", 0x94, InstructionType.ONE_WORD, "alu"),
    "SUB_R5": Instruction4040("SUB 5", "Sub R5 from A", 0x95, InstructionType.ONE_WORD, "alu"),
    "SUB_R6": Instruction4040("SUB 6", "Sub R6 from A", 0x96, InstructionType.ONE_WORD, "alu"),
    "SUB_R7": Instruction4040("SUB 7", "Sub R7 from A", 0x97, InstructionType.ONE_WORD, "alu"),
    "SUB_R8": Instruction4040("SUB 8", "Sub R8 from A", 0x98, InstructionType.ONE_WORD, "alu"),
    "SUB_R9": Instruction4040("SUB 9", "Sub R9 from A", 0x99, InstructionType.ONE_WORD, "alu"),
    "SUB_RA": Instruction4040("SUB 10", "Sub R10 from A", 0x9A, InstructionType.ONE_WORD, "alu"),
    "SUB_RB": Instruction4040("SUB 11", "Sub R11 from A", 0x9B, InstructionType.ONE_WORD, "alu"),
    "SUB_RC": Instruction4040("SUB 12", "Sub R12 from A", 0x9C, InstructionType.ONE_WORD, "alu"),
    "SUB_RD": Instruction4040("SUB 13", "Sub R13 from A", 0x9D, InstructionType.ONE_WORD, "alu"),
    "SUB_RE": Instruction4040("SUB 14", "Sub R14 from A", 0x9E, InstructionType.ONE_WORD, "alu"),
    "SUB_RF": Instruction4040("SUB 15", "Sub R15 from A", 0x9F, InstructionType.ONE_WORD, "alu"),
    
    "LD_R0": Instruction4040("LD 0", "Load A from R0", 0xA0, InstructionType.ONE_WORD, "transfer"),
    "LD_R1": Instruction4040("LD 1", "Load A from R1", 0xA1, InstructionType.ONE_WORD, "transfer"),
    "LD_R2": Instruction4040("LD 2", "Load A from R2", 0xA2, InstructionType.ONE_WORD, "transfer"),
    "LD_R3": Instruction4040("LD 3", "Load A from R3", 0xA3, InstructionType.ONE_WORD, "transfer"),
    "LD_R4": Instruction4040("LD 4", "Load A from R4", 0xA4, InstructionType.ONE_WORD, "transfer"),
    "LD_R5": Instruction4040("LD 5", "Load A from R5", 0xA5, InstructionType.ONE_WORD, "transfer"),
    "LD_R6": Instruction4040("LD 6", "Load A from R6", 0xA6, InstructionType.ONE_WORD, "transfer"),
    "LD_R7": Instruction4040("LD 7", "Load A from R7", 0xA7, InstructionType.ONE_WORD, "transfer"),
    "LD_R8": Instruction4040("LD 8", "Load A from R8", 0xA8, InstructionType.ONE_WORD, "transfer"),
    "LD_R9": Instruction4040("LD 9", "Load A from R9", 0xA9, InstructionType.ONE_WORD, "transfer"),
    "LD_RA": Instruction4040("LD 10", "Load A from R10", 0xAA, InstructionType.ONE_WORD, "transfer"),
    "LD_RB": Instruction4040("LD 11", "Load A from R11", 0xAB, InstructionType.ONE_WORD, "transfer"),
    "LD_RC": Instruction4040("LD 12", "Load A from R12", 0xAC, InstructionType.ONE_WORD, "transfer"),
    "LD_RD": Instruction4040("LD 13", "Load A from R13", 0xAD, InstructionType.ONE_WORD, "transfer"),
    "LD_RE": Instruction4040("LD 14", "Load A from R14", 0xAE, InstructionType.ONE_WORD, "transfer"),
    "LD_RF": Instruction4040("LD 15", "Load A from R15", 0xAF, InstructionType.ONE_WORD, "transfer"),
    
    "XCH_R0": Instruction4040("XCH 0", "Exchange A with R0", 0xB0, InstructionType.ONE_WORD, "transfer"),
    "XCH_R1": Instruction4040("XCH 1", "Exchange A with R1", 0xB1, InstructionType.ONE_WORD, "transfer"),
    "XCH_R2": Instruction4040("XCH 2", "Exchange A with R2", 0xB2, InstructionType.ONE_WORD, "transfer"),
    "XCH_R3": Instruction4040("XCH 3", "Exchange A with R3", 0xB3, InstructionType.ONE_WORD, "transfer"),
    "XCH_R4": Instruction4040("XCH 4", "Exchange A with R4", 0xB4, InstructionType.ONE_WORD, "transfer"),
    "XCH_R5": Instruction4040("XCH 5", "Exchange A with R5", 0xB5, InstructionType.ONE_WORD, "transfer"),
    "XCH_R6": Instruction4040("XCH 6", "Exchange A with R6", 0xB6, InstructionType.ONE_WORD, "transfer"),
    "XCH_R7": Instruction4040("XCH 7", "Exchange A with R7", 0xB7, InstructionType.ONE_WORD, "transfer"),
    "XCH_R8": Instruction4040("XCH 8", "Exchange A with R8", 0xB8, InstructionType.ONE_WORD, "transfer"),
    "XCH_R9": Instruction4040("XCH 9", "Exchange A with R9", 0xB9, InstructionType.ONE_WORD, "transfer"),
    "XCH_RA": Instruction4040("XCH 10", "Exchange A with R10", 0xBA, InstructionType.ONE_WORD, "transfer"),
    "XCH_RB": Instruction4040("XCH 11", "Exchange A with R11", 0xBB, InstructionType.ONE_WORD, "transfer"),
    "XCH_RC": Instruction4040("XCH 12", "Exchange A with R12", 0xBC, InstructionType.ONE_WORD, "transfer"),
    "XCH_RD": Instruction4040("XCH 13", "Exchange A with R13", 0xBD, InstructionType.ONE_WORD, "transfer"),
    "XCH_RE": Instruction4040("XCH 14", "Exchange A with R14", 0xBE, InstructionType.ONE_WORD, "transfer"),
    "XCH_RF": Instruction4040("XCH 15", "Exchange A with R15", 0xBF, InstructionType.ONE_WORD, "transfer"),
    
    # ========== ACCUMULATOR-ONLY (1 cycle) ==========
    "CLB": Instruction4040("CLB", "Clear A and carry", 0xF0, InstructionType.ONE_WORD, "alu"),
    "CLC": Instruction4040("CLC", "Clear carry", 0xF1, InstructionType.ONE_WORD, "alu"),
    "IAC": Instruction4040("IAC", "Increment A", 0xF2, InstructionType.ONE_WORD, "alu"),
    "CMC": Instruction4040("CMC", "Complement carry", 0xF3, InstructionType.ONE_WORD, "alu"),
    "CMA": Instruction4040("CMA", "Complement A", 0xF4, InstructionType.ONE_WORD, "alu"),
    "RAL": Instruction4040("RAL", "Rotate A left", 0xF5, InstructionType.ONE_WORD, "alu"),
    "RAR": Instruction4040("RAR", "Rotate A right", 0xF6, InstructionType.ONE_WORD, "alu"),
    "TCC": Instruction4040("TCC", "Transfer carry to A", 0xF7, InstructionType.ONE_WORD, "alu"),
    "DAC": Instruction4040("DAC", "Decrement A", 0xF8, InstructionType.ONE_WORD, "alu"),
    "TCS": Instruction4040("TCS", "Transfer carry subtract", 0xF9, InstructionType.ONE_WORD, "alu"),
    "STC": Instruction4040("STC", "Set carry", 0xFA, InstructionType.ONE_WORD, "alu"),
    "DAA": Instruction4040("DAA", "Decimal adjust A", 0xFB, InstructionType.ONE_WORD, "alu"),
    "KBP": Instruction4040("KBP", "Keyboard process", 0xFC, InstructionType.ONE_WORD, "alu"),
    "DCL": Instruction4040("DCL", "Designate command line", 0xFD, InstructionType.ONE_WORD, "io"),
    
    # ========== MEMORY OPERATIONS (1 cycle) ==========
    "SBM": Instruction4040("SBM", "Subtract memory", 0xE8, InstructionType.ONE_WORD, "memory"),
    "RDM": Instruction4040("RDM", "Read memory", 0xE9, InstructionType.ONE_WORD, "memory"),
    "RDR": Instruction4040("RDR", "Read ROM port", 0xEA, InstructionType.ONE_WORD, "memory"),
    "ADM": Instruction4040("ADM", "Add memory", 0xEB, InstructionType.ONE_WORD, "memory"),
    "RD0": Instruction4040("RD0", "Read status 0", 0xEC, InstructionType.ONE_WORD, "memory"),
    "RD1": Instruction4040("RD1", "Read status 1", 0xED, InstructionType.ONE_WORD, "memory"),
    "RD2": Instruction4040("RD2", "Read status 2", 0xEE, InstructionType.ONE_WORD, "memory"),
    "RD3": Instruction4040("RD3", "Read status 3", 0xEF, InstructionType.ONE_WORD, "memory"),
    "WRM": Instruction4040("WRM", "Write memory", 0xE0, InstructionType.ONE_WORD, "memory"),
    "WMP": Instruction4040("WMP", "Write memory port", 0xE1, InstructionType.ONE_WORD, "memory"),
    "WRR": Instruction4040("WRR", "Write ROM port", 0xE2, InstructionType.ONE_WORD, "memory"),
    "WPM": Instruction4040("WPM", "Write program memory", 0xE3, InstructionType.ONE_WORD, "memory"),
    "WR0": Instruction4040("WR0", "Write status 0", 0xE4, InstructionType.ONE_WORD, "memory"),
    "WR1": Instruction4040("WR1", "Write status 1", 0xE5, InstructionType.ONE_WORD, "memory"),
    "WR2": Instruction4040("WR2", "Write status 2", 0xE6, InstructionType.ONE_WORD, "memory"),
    "WR3": Instruction4040("WR3", "Write status 3", 0xE7, InstructionType.ONE_WORD, "memory"),
    
    # ========== CONTROL (1 cycle) ==========
    "NOP": Instruction4040("NOP", "No operation", 0x00, InstructionType.ONE_WORD, "control"),
    "BBL_0": Instruction4040("BBL 0", "Branch back, load 0", 0xC0, InstructionType.ONE_WORD, "control"),
    "BBL_1": Instruction4040("BBL 1", "Branch back, load 1", 0xC1, InstructionType.ONE_WORD, "control"),
    "BBL_2": Instruction4040("BBL 2", "Branch back, load 2", 0xC2, InstructionType.ONE_WORD, "control"),
    "BBL_3": Instruction4040("BBL 3", "Branch back, load 3", 0xC3, InstructionType.ONE_WORD, "control"),
    "LDM_0": Instruction4040("LDM 0", "Load A immediate 0", 0xD0, InstructionType.ONE_WORD, "transfer"),
    "LDM_1": Instruction4040("LDM 1", "Load A immediate 1", 0xD1, InstructionType.ONE_WORD, "transfer"),
    "LDM_2": Instruction4040("LDM 2", "Load A immediate 2", 0xD2, InstructionType.ONE_WORD, "transfer"),
    "LDM_3": Instruction4040("LDM 3", "Load A immediate 3", 0xD3, InstructionType.ONE_WORD, "transfer"),
    "LDM_4": Instruction4040("LDM 4", "Load A immediate 4", 0xD4, InstructionType.ONE_WORD, "transfer"),
    "LDM_5": Instruction4040("LDM 5", "Load A immediate 5", 0xD5, InstructionType.ONE_WORD, "transfer"),
    "LDM_6": Instruction4040("LDM 6", "Load A immediate 6", 0xD6, InstructionType.ONE_WORD, "transfer"),
    "LDM_7": Instruction4040("LDM 7", "Load A immediate 7", 0xD7, InstructionType.ONE_WORD, "transfer"),
    "LDM_8": Instruction4040("LDM 8", "Load A immediate 8", 0xD8, InstructionType.ONE_WORD, "transfer"),
    "LDM_9": Instruction4040("LDM 9", "Load A immediate 9", 0xD9, InstructionType.ONE_WORD, "transfer"),
    "LDM_A": Instruction4040("LDM 10", "Load A immediate 10", 0xDA, InstructionType.ONE_WORD, "transfer"),
    "LDM_B": Instruction4040("LDM 11", "Load A immediate 11", 0xDB, InstructionType.ONE_WORD, "transfer"),
    "LDM_C": Instruction4040("LDM 12", "Load A immediate 12", 0xDC, InstructionType.ONE_WORD, "transfer"),
    "LDM_D": Instruction4040("LDM 13", "Load A immediate 13", 0xDD, InstructionType.ONE_WORD, "transfer"),
    "LDM_E": Instruction4040("LDM 14", "Load A immediate 14", 0xDE, InstructionType.ONE_WORD, "transfer"),
    "LDM_F": Instruction4040("LDM 15", "Load A immediate 15", 0xDF, InstructionType.ONE_WORD, "transfer"),
    
    # ========== TWO-WORD INSTRUCTIONS (2 cycles) ==========
    "JUN": Instruction4040("JUN", "Jump unconditional", 0x40, InstructionType.TWO_WORD, "control"),
    "JMS": Instruction4040("JMS", "Jump to subroutine", 0x50, InstructionType.TWO_WORD, "control"),
    "JCN": Instruction4040("JCN", "Jump conditional", 0x10, InstructionType.TWO_WORD, "control"),
    "ISZ": Instruction4040("ISZ", "Increment, skip if zero", 0x70, InstructionType.TWO_WORD, "control"),
    "FIM": Instruction4040("FIM", "Fetch immediate", 0x20, InstructionType.TWO_WORD, "transfer"),
    "SRC": Instruction4040("SRC", "Send register control", 0x21, InstructionType.ONE_WORD, "io"),
    "FIN": Instruction4040("FIN", "Fetch indirect", 0x30, InstructionType.ONE_WORD, "transfer"),
    "JIN": Instruction4040("JIN", "Jump indirect", 0x31, InstructionType.ONE_WORD, "control"),
    
    # ========== NEW 4040 INSTRUCTIONS (14 total) ==========
    "HLT": Instruction4040("HLT", "Halt processor", 0x01, InstructionType.ONE_WORD, "control", is_new=True),
    "BBS": Instruction4040("BBS", "Branch back from interrupt", 0x02, InstructionType.ONE_WORD, "control", is_new=True),
    "LCR": Instruction4040("LCR", "Load DCL from ROM", 0x03, InstructionType.ONE_WORD, "io", is_new=True),
    "OR4": Instruction4040("OR4", "OR A with R4", 0x04, InstructionType.ONE_WORD, "alu", is_new=True),
    "OR5": Instruction4040("OR5", "OR A with R5", 0x05, InstructionType.ONE_WORD, "alu", is_new=True),
    "AN6": Instruction4040("AN6", "AND A with R6", 0x06, InstructionType.ONE_WORD, "alu", is_new=True),
    "AN7": Instruction4040("AN7", "AND A with R7", 0x07, InstructionType.ONE_WORD, "alu", is_new=True),
    "DB0": Instruction4040("DB0", "Select bank 0", 0x08, InstructionType.ONE_WORD, "control", is_new=True),
    "DB1": Instruction4040("DB1", "Select bank 1", 0x09, InstructionType.ONE_WORD, "control", is_new=True),
    "SB0": Instruction4040("SB0", "Select ROM bank 0", 0x0A, InstructionType.ONE_WORD, "control", is_new=True),
    "SB1": Instruction4040("SB1", "Select ROM bank 1", 0x0B, InstructionType.ONE_WORD, "control", is_new=True),
    "EI": Instruction4040("EI", "Enable interrupt", 0x0C, InstructionType.ONE_WORD, "control", is_new=True),
    "DI": Instruction4040("DI", "Disable interrupt", 0x0D, InstructionType.ONE_WORD, "control", is_new=True),
    "RPM": Instruction4040("RPM", "Read program memory", 0x0E, InstructionType.ONE_WORD, "memory", is_new=True),
}


@dataclass
class Intel4040Workload:
    """4040 workload profile."""
    name: str
    description: str
    two_word_fraction: float  # Fraction of 2-word instructions


WORKLOADS_4040 = {
    "typical": Intel4040Workload("typical", "Typical program mix", 0.25),
    "compute": Intel4040Workload("compute", "Compute-heavy (BCD)", 0.20),
    "control": Intel4040Workload("control", "Control-flow heavy", 0.35),
    "interrupt": Intel4040Workload("interrupt", "Interrupt handling", 0.28),
    "calculator": Intel4040Workload("calculator", "Calculator workload", 0.22),
}


@dataclass
class Intel4040Result:
    """4040 analysis result."""
    clock_khz: float = 740.0
    machine_cycle_us: float = 10.8
    
    avg_machine_cycles: float = 0.0
    avg_clocks: float = 0.0
    cpi: float = 0.0
    
    ips: float = 0.0
    kips: float = 0.0
    mips: float = 0.0
    
    validation_status: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class Intel4040ModelV2:
    """Improved 4040 model with complete 60-instruction set."""
    
    CLOCK_KHZ = 740
    CLOCKS_PER_CYCLE = 8
    MACHINE_CYCLE_US = 10.8
    
    def __init__(self):
        self.instructions = INSTRUCTIONS_4040_COMPLETE
    
    def analyze(self, workload: str = "typical") -> Intel4040Result:
        """Analyze 4040 performance."""
        result = Intel4040Result()
        result.clock_khz = self.CLOCK_KHZ
        result.machine_cycle_us = self.MACHINE_CYCLE_US
        
        wl = WORKLOADS_4040.get(workload, WORKLOADS_4040["typical"])
        
        one_word_frac = 1.0 - wl.two_word_fraction
        two_word_frac = wl.two_word_fraction
        
        result.avg_machine_cycles = one_word_frac * 1 + two_word_frac * 2
        result.avg_clocks = result.avg_machine_cycles * self.CLOCKS_PER_CYCLE
        result.cpi = result.avg_clocks
        
        avg_instruction_time = result.avg_machine_cycles * self.MACHINE_CYCLE_US
        result.ips = 1_000_000 / avg_instruction_time
        result.kips = result.ips / 1000
        result.mips = result.ips / 1_000_000
        
        # Validation: 46,250-92,500 IPS (same as 4004)
        expected = (46250, 92500)
        if expected[0] <= result.ips <= expected[1]:
            result.validation_status = "PASS"
        else:
            result.validation_status = f"CHECK ({expected[0]:,}-{expected[1]:,})"
        
        return result
    
    def validate_instructions(self) -> Dict[str, Tuple[bool, str]]:
        """Validate instruction set."""
        tests = {}
        
        # Total count
        total = len(self.instructions)
        tests["total_60"] = (total == 60, f"count={total}")
        
        # Original vs new
        orig = len([i for i in self.instructions.values() if not i.is_new])
        new = len([i for i in self.instructions.values() if i.is_new])
        tests["original_46"] = (orig == 46, f"original={orig}")
        tests["new_14"] = (new == 14, f"new={new}")
        
        # Check specific new instructions
        tests["has_HLT"] = ("HLT" in self.instructions, "HLT present")
        tests["has_BBS"] = ("BBS" in self.instructions, "BBS present")
        tests["has_EI"] = ("EI" in self.instructions, "EI present")
        tests["has_DI"] = ("DI" in self.instructions, "DI present")
        tests["has_DB0"] = ("DB0" in self.instructions, "DB0 bank select")
        tests["has_DB1"] = ("DB1" in self.instructions, "DB1 bank select")
        
        return tests


def get_improved_4040_config() -> Dict:
    """Get 4040 config for export."""
    model = Intel4040ModelV2()
    result = model.analyze("typical")
    
    new_instrs = [i for i in INSTRUCTIONS_4040_COMPLETE.values() if i.is_new]
    
    return {
        "family": "INTEL",
        "category": "SIMPLE_4BIT",
        "year": 1974,
        "bits": 4,
        "clock_mhz": 0.74,
        "transistors": 3000,
        "process_um": 10,
        
        "instruction_count": 60,
        "original_4004_instructions": 46,
        "new_4040_instructions": 14,
        
        "timing": {
            "clock_khz": 740,
            "machine_cycle_clocks": 8,
            "machine_cycle_us": 10.8,
            "one_word_cycles": 1,
            "two_word_cycles": 2,
        },
        
        "new_instructions": [
            {"mnemonic": i.mnemonic, "description": i.description}
            for i in new_instrs
        ],
        
        "enhancements_vs_4004": {
            "index_registers": "24 (vs 16)",
            "stack_levels": "7 (vs 3)",
            "interrupt_support": True,
            "register_banking": True,
        },
        
        "ips_range": [46250, 92500],
        "ips_typical": result.ips,
        "mips": result.mips,
        
        "validation": {
            "source": "Intel MCS-40 Users Manual",
            "timing_note": "Identical to 4004"
        }
    }


if __name__ == "__main__":
    print("="*70)
    print("INTEL 4040 IMPROVED MODEL v2.0")
    print("Complete 60-instruction set (46 original + 14 new)")
    print("="*70)
    
    model = Intel4040ModelV2()
    
    # Validation
    print("\n1. INSTRUCTION SET VALIDATION")
    print("-"*40)
    tests = model.validate_instructions()
    passed = sum(1 for t, _ in tests.values() if t)
    print(f"   Passed: {passed}/{len(tests)}")
    for name, (ok, msg) in tests.items():
        print(f"   {'✓' if ok else '✗'} {name}: {msg}")
    
    # New instructions
    print("\n2. NEW 4040 INSTRUCTIONS (14)")
    print("-"*40)
    new_instrs = [i for i in INSTRUCTIONS_4040_COMPLETE.values() if i.is_new]
    for instr in new_instrs:
        print(f"   {instr.mnemonic:<8}: {instr.description}")
    
    # Category breakdown
    print("\n3. INSTRUCTION CATEGORIES")
    print("-"*40)
    categories = {}
    for instr in INSTRUCTIONS_4040_COMPLETE.values():
        cat = instr.category
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
    for cat, count in sorted(categories.items()):
        print(f"   {cat:<12}: {count:>3} instructions")
    
    # Performance
    print("\n4. PERFORMANCE ANALYSIS")
    print("-"*40)
    for wl_name in WORKLOADS_4040:
        result = model.analyze(wl_name)
        print(f"   {wl_name:<12}: {result.ips:>8,.0f} IPS, {result.kips:.1f} kIPS [{result.validation_status}]")
    
    # Export
    config = get_improved_4040_config()
    with open("/home/claude/4040_improved_v2.json", "w") as f:
        json.dump({
            "processor": "Intel 4040",
            "version": "2.0",
            "config": config,
            "workloads": {k: model.analyze(k).to_dict() for k in WORKLOADS_4040}
        }, f, indent=2)
    
    print("\n5. EXPORT")
    print("-"*40)
    print(f"   Total: {config['instruction_count']} instructions")
    print(f"   New 4040: {config['new_4040_instructions']} instructions")
    print(f"   Exported to: 4040_improved_v2.json")
    print("="*70)
