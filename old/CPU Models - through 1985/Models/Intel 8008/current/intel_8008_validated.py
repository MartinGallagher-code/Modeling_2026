#!/usr/bin/env python3
"""
Intel 8008 IMPROVED Performance Model v2.0

Complete instruction timing database based on:
- Intel 8008 Users Manual (1972)
- CPU-World corrected timing
- petsd.net 8008 reference

KEY TIMING FACTS (validated):
- Each T-state = 2 clock cycles (UNIQUE to 8008, unlike 8080)
- Instructions: 5-11 T-states = 10-22 clock cycles
- 8008 @ 500 kHz: 22,500-50,000 IPS
- 8008-1 @ 800 kHz: 36,000-80,000 IPS

Author: Grey-Box Performance Modeling Research
Date: January 26, 2026
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple
from enum import Enum
import json


@dataclass
class Instruction8008:
    """Intel 8008 instruction with validated timing."""
    mnemonic: str
    description: str
    opcode: int           # Base opcode
    t_states: int         # T-states (NOT clock cycles!)
    bytes: int            # Instruction length
    category: str
    condition: str = ""   # For conditional instructions
    
    @property
    def clock_cycles(self) -> int:
        """Each T-state = 2 clock cycles in 8008."""
        return self.t_states * 2
    
    @property
    def time_us_500khz(self) -> float:
        """Execution time at 500 kHz."""
        return self.t_states * 4.0  # 4 µs per T-state at 500 kHz
    
    @property
    def time_us_800khz(self) -> float:
        """Execution time at 800 kHz (8008-1)."""
        return self.t_states * 2.5  # 2.5 µs per T-state at 800 kHz


# Complete Intel 8008 instruction set with validated timing
# Reference: Intel 8008 Users Manual, petsd.net
INSTRUCTIONS_8008_COMPLETE = {
    # ========== INDEX REGISTER INSTRUCTIONS (5 T-states) ==========
    # MOV r1,r2 - Move register to register
    "MOV_A_A": Instruction8008("MOV A,A", "Move A to A (NOP)", 0xC0, 5, 1, "transfer"),
    "MOV_A_B": Instruction8008("MOV A,B", "Move B to A", 0xC1, 5, 1, "transfer"),
    "MOV_A_C": Instruction8008("MOV A,C", "Move C to A", 0xC2, 5, 1, "transfer"),
    "MOV_A_D": Instruction8008("MOV A,D", "Move D to A", 0xC3, 5, 1, "transfer"),
    "MOV_A_E": Instruction8008("MOV A,E", "Move E to A", 0xC4, 5, 1, "transfer"),
    "MOV_A_H": Instruction8008("MOV A,H", "Move H to A", 0xC5, 5, 1, "transfer"),
    "MOV_A_L": Instruction8008("MOV A,L", "Move L to A", 0xC6, 5, 1, "transfer"),
    
    "MOV_B_A": Instruction8008("MOV B,A", "Move A to B", 0xC8, 5, 1, "transfer"),
    "MOV_B_B": Instruction8008("MOV B,B", "Move B to B", 0xC9, 5, 1, "transfer"),
    "MOV_B_C": Instruction8008("MOV B,C", "Move C to B", 0xCA, 5, 1, "transfer"),
    "MOV_B_D": Instruction8008("MOV B,D", "Move D to B", 0xCB, 5, 1, "transfer"),
    "MOV_B_E": Instruction8008("MOV B,E", "Move E to B", 0xCC, 5, 1, "transfer"),
    "MOV_B_H": Instruction8008("MOV B,H", "Move H to B", 0xCD, 5, 1, "transfer"),
    "MOV_B_L": Instruction8008("MOV B,L", "Move L to B", 0xCE, 5, 1, "transfer"),
    
    "MOV_C_A": Instruction8008("MOV C,A", "Move A to C", 0xD0, 5, 1, "transfer"),
    "MOV_C_B": Instruction8008("MOV C,B", "Move B to C", 0xD1, 5, 1, "transfer"),
    "MOV_C_C": Instruction8008("MOV C,C", "Move C to C", 0xD2, 5, 1, "transfer"),
    "MOV_C_D": Instruction8008("MOV C,D", "Move D to C", 0xD3, 5, 1, "transfer"),
    "MOV_C_E": Instruction8008("MOV C,E", "Move E to C", 0xD4, 5, 1, "transfer"),
    "MOV_C_H": Instruction8008("MOV C,H", "Move H to C", 0xD5, 5, 1, "transfer"),
    "MOV_C_L": Instruction8008("MOV C,L", "Move L to C", 0xD6, 5, 1, "transfer"),
    
    "MOV_D_A": Instruction8008("MOV D,A", "Move A to D", 0xD8, 5, 1, "transfer"),
    "MOV_D_B": Instruction8008("MOV D,B", "Move B to D", 0xD9, 5, 1, "transfer"),
    "MOV_D_C": Instruction8008("MOV D,C", "Move C to D", 0xDA, 5, 1, "transfer"),
    "MOV_D_D": Instruction8008("MOV D,D", "Move D to D", 0xDB, 5, 1, "transfer"),
    "MOV_D_E": Instruction8008("MOV D,E", "Move E to D", 0xDC, 5, 1, "transfer"),
    "MOV_D_H": Instruction8008("MOV D,H", "Move H to D", 0xDD, 5, 1, "transfer"),
    "MOV_D_L": Instruction8008("MOV D,L", "Move L to D", 0xDE, 5, 1, "transfer"),
    
    "MOV_E_A": Instruction8008("MOV E,A", "Move A to E", 0xE0, 5, 1, "transfer"),
    "MOV_E_B": Instruction8008("MOV E,B", "Move B to E", 0xE1, 5, 1, "transfer"),
    "MOV_E_C": Instruction8008("MOV E,C", "Move C to E", 0xE2, 5, 1, "transfer"),
    "MOV_E_D": Instruction8008("MOV E,D", "Move D to E", 0xE3, 5, 1, "transfer"),
    "MOV_E_E": Instruction8008("MOV E,E", "Move E to E", 0xE4, 5, 1, "transfer"),
    "MOV_E_H": Instruction8008("MOV E,H", "Move H to E", 0xE5, 5, 1, "transfer"),
    "MOV_E_L": Instruction8008("MOV E,L", "Move L to E", 0xE6, 5, 1, "transfer"),
    
    "MOV_H_A": Instruction8008("MOV H,A", "Move A to H", 0xE8, 5, 1, "transfer"),
    "MOV_H_B": Instruction8008("MOV H,B", "Move B to H", 0xE9, 5, 1, "transfer"),
    "MOV_H_C": Instruction8008("MOV H,C", "Move C to H", 0xEA, 5, 1, "transfer"),
    "MOV_H_D": Instruction8008("MOV H,D", "Move D to H", 0xEB, 5, 1, "transfer"),
    "MOV_H_E": Instruction8008("MOV H,E", "Move E to H", 0xEC, 5, 1, "transfer"),
    "MOV_H_H": Instruction8008("MOV H,H", "Move H to H", 0xED, 5, 1, "transfer"),
    "MOV_H_L": Instruction8008("MOV H,L", "Move L to H", 0xEE, 5, 1, "transfer"),
    
    "MOV_L_A": Instruction8008("MOV L,A", "Move A to L", 0xF0, 5, 1, "transfer"),
    "MOV_L_B": Instruction8008("MOV L,B", "Move B to L", 0xF1, 5, 1, "transfer"),
    "MOV_L_C": Instruction8008("MOV L,C", "Move C to L", 0xF2, 5, 1, "transfer"),
    "MOV_L_D": Instruction8008("MOV L,D", "Move D to L", 0xF3, 5, 1, "transfer"),
    "MOV_L_E": Instruction8008("MOV L,E", "Move E to L", 0xF4, 5, 1, "transfer"),
    "MOV_L_H": Instruction8008("MOV L,H", "Move H to L", 0xF5, 5, 1, "transfer"),
    "MOV_L_L": Instruction8008("MOV L,L", "Move L to L", 0xF6, 5, 1, "transfer"),
    
    # ========== MEMORY REFERENCE (8 T-states) ==========
    "MOV_A_M": Instruction8008("MOV A,M", "Load A from memory", 0xC7, 8, 1, "memory"),
    "MOV_B_M": Instruction8008("MOV B,M", "Load B from memory", 0xCF, 8, 1, "memory"),
    "MOV_C_M": Instruction8008("MOV C,M", "Load C from memory", 0xD7, 8, 1, "memory"),
    "MOV_D_M": Instruction8008("MOV D,M", "Load D from memory", 0xDF, 8, 1, "memory"),
    "MOV_E_M": Instruction8008("MOV E,M", "Load E from memory", 0xE7, 8, 1, "memory"),
    "MOV_H_M": Instruction8008("MOV H,M", "Load H from memory", 0xEF, 8, 1, "memory"),
    "MOV_L_M": Instruction8008("MOV L,M", "Load L from memory", 0xF7, 8, 1, "memory"),
    
    "MOV_M_A": Instruction8008("MOV M,A", "Store A to memory", 0xF8, 7, 1, "memory"),
    "MOV_M_B": Instruction8008("MOV M,B", "Store B to memory", 0xF9, 7, 1, "memory"),
    "MOV_M_C": Instruction8008("MOV M,C", "Store C to memory", 0xFA, 7, 1, "memory"),
    "MOV_M_D": Instruction8008("MOV M,D", "Store D to memory", 0xFB, 7, 1, "memory"),
    "MOV_M_E": Instruction8008("MOV M,E", "Store E to memory", 0xFC, 7, 1, "memory"),
    "MOV_M_H": Instruction8008("MOV M,H", "Store H to memory", 0xFD, 7, 1, "memory"),
    "MOV_M_L": Instruction8008("MOV M,L", "Store L to memory", 0xFE, 7, 1, "memory"),
    
    # ========== IMMEDIATE LOAD (8 T-states, 2 bytes) ==========
    "MVI_A": Instruction8008("MVI A", "Load A immediate", 0x06, 8, 2, "transfer"),
    "MVI_B": Instruction8008("MVI B", "Load B immediate", 0x0E, 8, 2, "transfer"),
    "MVI_C": Instruction8008("MVI C", "Load C immediate", 0x16, 8, 2, "transfer"),
    "MVI_D": Instruction8008("MVI D", "Load D immediate", 0x1E, 8, 2, "transfer"),
    "MVI_E": Instruction8008("MVI E", "Load E immediate", 0x26, 8, 2, "transfer"),
    "MVI_H": Instruction8008("MVI H", "Load H immediate", 0x2E, 8, 2, "transfer"),
    "MVI_L": Instruction8008("MVI L", "Load L immediate", 0x36, 8, 2, "transfer"),
    "MVI_M": Instruction8008("MVI M", "Load memory immediate", 0x3E, 9, 2, "memory"),
    
    # ========== ALU REGISTER OPERATIONS (5 T-states) ==========
    "ADD_A": Instruction8008("ADD A", "Add A to A", 0x80, 5, 1, "alu"),
    "ADD_B": Instruction8008("ADD B", "Add B to A", 0x81, 5, 1, "alu"),
    "ADD_C": Instruction8008("ADD C", "Add C to A", 0x82, 5, 1, "alu"),
    "ADD_D": Instruction8008("ADD D", "Add D to A", 0x83, 5, 1, "alu"),
    "ADD_E": Instruction8008("ADD E", "Add E to A", 0x84, 5, 1, "alu"),
    "ADD_H": Instruction8008("ADD H", "Add H to A", 0x85, 5, 1, "alu"),
    "ADD_L": Instruction8008("ADD L", "Add L to A", 0x86, 5, 1, "alu"),
    
    "ADC_A": Instruction8008("ADC A", "Add A+carry to A", 0x88, 5, 1, "alu"),
    "ADC_B": Instruction8008("ADC B", "Add B+carry to A", 0x89, 5, 1, "alu"),
    "ADC_C": Instruction8008("ADC C", "Add C+carry to A", 0x8A, 5, 1, "alu"),
    "ADC_D": Instruction8008("ADC D", "Add D+carry to A", 0x8B, 5, 1, "alu"),
    "ADC_E": Instruction8008("ADC E", "Add E+carry to A", 0x8C, 5, 1, "alu"),
    "ADC_H": Instruction8008("ADC H", "Add H+carry to A", 0x8D, 5, 1, "alu"),
    "ADC_L": Instruction8008("ADC L", "Add L+carry to A", 0x8E, 5, 1, "alu"),
    
    "SUB_A": Instruction8008("SUB A", "Subtract A from A", 0x90, 5, 1, "alu"),
    "SUB_B": Instruction8008("SUB B", "Subtract B from A", 0x91, 5, 1, "alu"),
    "SUB_C": Instruction8008("SUB C", "Subtract C from A", 0x92, 5, 1, "alu"),
    "SUB_D": Instruction8008("SUB D", "Subtract D from A", 0x93, 5, 1, "alu"),
    "SUB_E": Instruction8008("SUB E", "Subtract E from A", 0x94, 5, 1, "alu"),
    "SUB_H": Instruction8008("SUB H", "Subtract H from A", 0x95, 5, 1, "alu"),
    "SUB_L": Instruction8008("SUB L", "Subtract L from A", 0x96, 5, 1, "alu"),
    
    "SBB_A": Instruction8008("SBB A", "Subtract A+borrow", 0x98, 5, 1, "alu"),
    "SBB_B": Instruction8008("SBB B", "Subtract B+borrow", 0x99, 5, 1, "alu"),
    "SBB_C": Instruction8008("SBB C", "Subtract C+borrow", 0x9A, 5, 1, "alu"),
    "SBB_D": Instruction8008("SBB D", "Subtract D+borrow", 0x9B, 5, 1, "alu"),
    "SBB_E": Instruction8008("SBB E", "Subtract E+borrow", 0x9C, 5, 1, "alu"),
    "SBB_H": Instruction8008("SBB H", "Subtract H+borrow", 0x9D, 5, 1, "alu"),
    "SBB_L": Instruction8008("SBB L", "Subtract L+borrow", 0x9E, 5, 1, "alu"),
    
    "ANA_A": Instruction8008("ANA A", "AND A with A", 0xA0, 5, 1, "alu"),
    "ANA_B": Instruction8008("ANA B", "AND B with A", 0xA1, 5, 1, "alu"),
    "ANA_C": Instruction8008("ANA C", "AND C with A", 0xA2, 5, 1, "alu"),
    "ANA_D": Instruction8008("ANA D", "AND D with A", 0xA3, 5, 1, "alu"),
    "ANA_E": Instruction8008("ANA E", "AND E with A", 0xA4, 5, 1, "alu"),
    "ANA_H": Instruction8008("ANA H", "AND H with A", 0xA5, 5, 1, "alu"),
    "ANA_L": Instruction8008("ANA L", "AND L with A", 0xA6, 5, 1, "alu"),
    
    "XRA_A": Instruction8008("XRA A", "XOR A with A", 0xA8, 5, 1, "alu"),
    "XRA_B": Instruction8008("XRA B", "XOR B with A", 0xA9, 5, 1, "alu"),
    "XRA_C": Instruction8008("XRA C", "XOR C with A", 0xAA, 5, 1, "alu"),
    "XRA_D": Instruction8008("XRA D", "XOR D with A", 0xAB, 5, 1, "alu"),
    "XRA_E": Instruction8008("XRA E", "XOR E with A", 0xAC, 5, 1, "alu"),
    "XRA_H": Instruction8008("XRA H", "XOR H with A", 0xAD, 5, 1, "alu"),
    "XRA_L": Instruction8008("XRA L", "XOR L with A", 0xAE, 5, 1, "alu"),
    
    "ORA_A": Instruction8008("ORA A", "OR A with A", 0xB0, 5, 1, "alu"),
    "ORA_B": Instruction8008("ORA B", "OR B with A", 0xB1, 5, 1, "alu"),
    "ORA_C": Instruction8008("ORA C", "OR C with A", 0xB2, 5, 1, "alu"),
    "ORA_D": Instruction8008("ORA D", "OR D with A", 0xB3, 5, 1, "alu"),
    "ORA_E": Instruction8008("ORA E", "OR E with A", 0xB4, 5, 1, "alu"),
    "ORA_H": Instruction8008("ORA H", "OR H with A", 0xB5, 5, 1, "alu"),
    "ORA_L": Instruction8008("ORA L", "OR L with A", 0xB6, 5, 1, "alu"),
    
    "CMP_A": Instruction8008("CMP A", "Compare A with A", 0xB8, 5, 1, "alu"),
    "CMP_B": Instruction8008("CMP B", "Compare B with A", 0xB9, 5, 1, "alu"),
    "CMP_C": Instruction8008("CMP C", "Compare C with A", 0xBA, 5, 1, "alu"),
    "CMP_D": Instruction8008("CMP D", "Compare D with A", 0xBB, 5, 1, "alu"),
    "CMP_E": Instruction8008("CMP E", "Compare E with A", 0xBC, 5, 1, "alu"),
    "CMP_H": Instruction8008("CMP H", "Compare H with A", 0xBD, 5, 1, "alu"),
    "CMP_L": Instruction8008("CMP L", "Compare L with A", 0xBE, 5, 1, "alu"),
    
    # ========== ALU MEMORY OPERATIONS (8 T-states) ==========
    "ADD_M": Instruction8008("ADD M", "Add memory to A", 0x87, 8, 1, "alu"),
    "ADC_M": Instruction8008("ADC M", "Add memory+carry", 0x8F, 8, 1, "alu"),
    "SUB_M": Instruction8008("SUB M", "Subtract memory", 0x97, 8, 1, "alu"),
    "SBB_M": Instruction8008("SBB M", "Subtract memory+borrow", 0x9F, 8, 1, "alu"),
    "ANA_M": Instruction8008("ANA M", "AND memory with A", 0xA7, 8, 1, "alu"),
    "XRA_M": Instruction8008("XRA M", "XOR memory with A", 0xAF, 8, 1, "alu"),
    "ORA_M": Instruction8008("ORA M", "OR memory with A", 0xB7, 8, 1, "alu"),
    "CMP_M": Instruction8008("CMP M", "Compare memory", 0xBF, 8, 1, "alu"),
    
    # ========== ALU IMMEDIATE (8 T-states, 2 bytes) ==========
    "ADI": Instruction8008("ADI", "Add immediate", 0x04, 8, 2, "alu"),
    "ACI": Instruction8008("ACI", "Add immediate+carry", 0x0C, 8, 2, "alu"),
    "SUI": Instruction8008("SUI", "Subtract immediate", 0x14, 8, 2, "alu"),
    "SBI": Instruction8008("SBI", "Subtract immediate+borrow", 0x1C, 8, 2, "alu"),
    "ANI": Instruction8008("ANI", "AND immediate", 0x24, 8, 2, "alu"),
    "XRI": Instruction8008("XRI", "XOR immediate", 0x2C, 8, 2, "alu"),
    "ORI": Instruction8008("ORI", "OR immediate", 0x34, 8, 2, "alu"),
    "CPI": Instruction8008("CPI", "Compare immediate", 0x3C, 8, 2, "alu"),
    
    # ========== INCREMENT/DECREMENT (5 T-states) ==========
    "INR_A": Instruction8008("INR A", "Increment A", 0x00, 5, 1, "alu"),
    "INR_B": Instruction8008("INR B", "Increment B", 0x08, 5, 1, "alu"),
    "INR_C": Instruction8008("INR C", "Increment C", 0x10, 5, 1, "alu"),
    "INR_D": Instruction8008("INR D", "Increment D", 0x18, 5, 1, "alu"),
    "INR_E": Instruction8008("INR E", "Increment E", 0x20, 5, 1, "alu"),
    "INR_H": Instruction8008("INR H", "Increment H", 0x28, 5, 1, "alu"),
    "INR_L": Instruction8008("INR L", "Increment L", 0x30, 5, 1, "alu"),
    
    "DCR_A": Instruction8008("DCR A", "Decrement A", 0x01, 5, 1, "alu"),
    "DCR_B": Instruction8008("DCR B", "Decrement B", 0x09, 5, 1, "alu"),
    "DCR_C": Instruction8008("DCR C", "Decrement C", 0x11, 5, 1, "alu"),
    "DCR_D": Instruction8008("DCR D", "Decrement D", 0x19, 5, 1, "alu"),
    "DCR_E": Instruction8008("DCR E", "Decrement E", 0x21, 5, 1, "alu"),
    "DCR_H": Instruction8008("DCR H", "Decrement H", 0x29, 5, 1, "alu"),
    "DCR_L": Instruction8008("DCR L", "Decrement L", 0x31, 5, 1, "alu"),
    
    # ========== ROTATE (5 T-states) ==========
    "RLC": Instruction8008("RLC", "Rotate A left", 0x02, 5, 1, "alu"),
    "RRC": Instruction8008("RRC", "Rotate A right", 0x0A, 5, 1, "alu"),
    "RAL": Instruction8008("RAL", "Rotate A left thru carry", 0x12, 5, 1, "alu"),
    "RAR": Instruction8008("RAR", "Rotate A right thru carry", 0x1A, 5, 1, "alu"),
    
    # ========== JUMP (11 T-states, 3 bytes) ==========
    "JMP": Instruction8008("JMP", "Jump unconditional", 0x44, 11, 3, "control"),
    "JNC": Instruction8008("JNC", "Jump if no carry", 0x40, 11, 3, "control", "NC"),
    "JNZ": Instruction8008("JNZ", "Jump if not zero", 0x48, 11, 3, "control", "NZ"),
    "JP":  Instruction8008("JP", "Jump if positive", 0x50, 11, 3, "control", "P"),
    "JPO": Instruction8008("JPO", "Jump if parity odd", 0x58, 11, 3, "control", "PO"),
    "JC":  Instruction8008("JC", "Jump if carry", 0x60, 11, 3, "control", "C"),
    "JZ":  Instruction8008("JZ", "Jump if zero", 0x68, 11, 3, "control", "Z"),
    "JM":  Instruction8008("JM", "Jump if minus", 0x70, 11, 3, "control", "M"),
    "JPE": Instruction8008("JPE", "Jump if parity even", 0x78, 11, 3, "control", "PE"),
    
    # ========== CALL (11 T-states, 3 bytes) ==========
    "CALL": Instruction8008("CALL", "Call unconditional", 0x46, 11, 3, "control"),
    "CNC": Instruction8008("CNC", "Call if no carry", 0x42, 11, 3, "control", "NC"),
    "CNZ": Instruction8008("CNZ", "Call if not zero", 0x4A, 11, 3, "control", "NZ"),
    "CP":  Instruction8008("CP", "Call if positive", 0x52, 11, 3, "control", "P"),
    "CPO": Instruction8008("CPO", "Call if parity odd", 0x5A, 11, 3, "control", "PO"),
    "CC":  Instruction8008("CC", "Call if carry", 0x62, 11, 3, "control", "C"),
    "CZ":  Instruction8008("CZ", "Call if zero", 0x6A, 11, 3, "control", "Z"),
    "CM":  Instruction8008("CM", "Call if minus", 0x72, 11, 3, "control", "M"),
    "CPE": Instruction8008("CPE", "Call if parity even", 0x7A, 11, 3, "control", "PE"),
    
    # ========== RETURN (5 not taken, 11 taken) ==========
    "RET": Instruction8008("RET", "Return unconditional", 0x07, 5, 1, "control"),
    "RNC": Instruction8008("RNC", "Return if no carry", 0x03, 5, 1, "control", "NC"),
    "RNZ": Instruction8008("RNZ", "Return if not zero", 0x0B, 5, 1, "control", "NZ"),
    "RP":  Instruction8008("RP", "Return if positive", 0x13, 5, 1, "control", "P"),
    "RPO": Instruction8008("RPO", "Return if parity odd", 0x1B, 5, 1, "control", "PO"),
    "RC":  Instruction8008("RC", "Return if carry", 0x23, 5, 1, "control", "C"),
    "RZ":  Instruction8008("RZ", "Return if zero", 0x2B, 5, 1, "control", "Z"),
    "RM":  Instruction8008("RM", "Return if minus", 0x33, 5, 1, "control", "M"),
    "RPE": Instruction8008("RPE", "Return if parity even", 0x3B, 5, 1, "control", "PE"),
    
    # ========== RST (5 T-states) ==========
    "RST_0": Instruction8008("RST 0", "Restart 0", 0x05, 5, 1, "control"),
    "RST_1": Instruction8008("RST 1", "Restart 1", 0x0D, 5, 1, "control"),
    "RST_2": Instruction8008("RST 2", "Restart 2", 0x15, 5, 1, "control"),
    "RST_3": Instruction8008("RST 3", "Restart 3", 0x1D, 5, 1, "control"),
    "RST_4": Instruction8008("RST 4", "Restart 4", 0x25, 5, 1, "control"),
    "RST_5": Instruction8008("RST 5", "Restart 5", 0x2D, 5, 1, "control"),
    "RST_6": Instruction8008("RST 6", "Restart 6", 0x35, 5, 1, "control"),
    "RST_7": Instruction8008("RST 7", "Restart 7", 0x3D, 5, 1, "control"),
    
    # ========== I/O (8 T-states for IN, 6 for OUT) ==========
    "IN_0": Instruction8008("IN 0", "Input from port 0", 0x41, 8, 2, "io"),
    "IN_1": Instruction8008("IN 1", "Input from port 1", 0x43, 8, 2, "io"),
    "IN_2": Instruction8008("IN 2", "Input from port 2", 0x45, 8, 2, "io"),
    "IN_3": Instruction8008("IN 3", "Input from port 3", 0x47, 8, 2, "io"),
    "IN_4": Instruction8008("IN 4", "Input from port 4", 0x49, 8, 2, "io"),
    "IN_5": Instruction8008("IN 5", "Input from port 5", 0x4B, 8, 2, "io"),
    "IN_6": Instruction8008("IN 6", "Input from port 6", 0x4D, 8, 2, "io"),
    "IN_7": Instruction8008("IN 7", "Input from port 7", 0x4F, 8, 2, "io"),
    
    "OUT_8":  Instruction8008("OUT 8", "Output to port 8", 0x51, 6, 2, "io"),
    "OUT_9":  Instruction8008("OUT 9", "Output to port 9", 0x53, 6, 2, "io"),
    "OUT_10": Instruction8008("OUT 10", "Output to port 10", 0x55, 6, 2, "io"),
    "OUT_11": Instruction8008("OUT 11", "Output to port 11", 0x57, 6, 2, "io"),
    "OUT_12": Instruction8008("OUT 12", "Output to port 12", 0x59, 6, 2, "io"),
    "OUT_13": Instruction8008("OUT 13", "Output to port 13", 0x5B, 6, 2, "io"),
    "OUT_14": Instruction8008("OUT 14", "Output to port 14", 0x5D, 6, 2, "io"),
    "OUT_15": Instruction8008("OUT 15", "Output to port 15", 0x5F, 6, 2, "io"),
    "OUT_16": Instruction8008("OUT 16", "Output to port 16", 0x61, 6, 2, "io"),
    "OUT_17": Instruction8008("OUT 17", "Output to port 17", 0x63, 6, 2, "io"),
    "OUT_18": Instruction8008("OUT 18", "Output to port 18", 0x65, 6, 2, "io"),
    "OUT_19": Instruction8008("OUT 19", "Output to port 19", 0x67, 6, 2, "io"),
    "OUT_20": Instruction8008("OUT 20", "Output to port 20", 0x69, 6, 2, "io"),
    "OUT_21": Instruction8008("OUT 21", "Output to port 21", 0x6B, 6, 2, "io"),
    "OUT_22": Instruction8008("OUT 22", "Output to port 22", 0x6D, 6, 2, "io"),
    "OUT_23": Instruction8008("OUT 23", "Output to port 23", 0x6F, 6, 2, "io"),
    "OUT_24": Instruction8008("OUT 24", "Output to port 24", 0x71, 6, 2, "io"),
    "OUT_25": Instruction8008("OUT 25", "Output to port 25", 0x73, 6, 2, "io"),
    "OUT_26": Instruction8008("OUT 26", "Output to port 26", 0x75, 6, 2, "io"),
    "OUT_27": Instruction8008("OUT 27", "Output to port 27", 0x77, 6, 2, "io"),
    "OUT_28": Instruction8008("OUT 28", "Output to port 28", 0x79, 6, 2, "io"),
    "OUT_29": Instruction8008("OUT 29", "Output to port 29", 0x7B, 6, 2, "io"),
    "OUT_30": Instruction8008("OUT 30", "Output to port 30", 0x7D, 6, 2, "io"),
    "OUT_31": Instruction8008("OUT 31", "Output to port 31", 0x7F, 6, 2, "io"),
    
    # ========== HALT (4 T-states) ==========
    "HLT": Instruction8008("HLT", "Halt", 0x00, 4, 1, "control"),  # Note: Same as INR A!
    "HLT_FF": Instruction8008("HLT", "Halt (alt)", 0xFF, 4, 1, "control"),
}


@dataclass
class Intel8008Workload:
    """Workload profile for 8008."""
    name: str
    description: str
    instruction_mix: Dict[str, float]  # category -> fraction


WORKLOADS_8008 = {
    "typical": Intel8008Workload(
        "typical", "Typical program mix",
        {"transfer": 0.25, "alu": 0.35, "memory": 0.15, "control": 0.20, "io": 0.05}
    ),
    "compute": Intel8008Workload(
        "compute", "Compute-heavy (register ALU)",
        {"transfer": 0.20, "alu": 0.55, "memory": 0.10, "control": 0.12, "io": 0.03}
    ),
    "memory": Intel8008Workload(
        "memory", "Memory-intensive",
        {"transfer": 0.15, "alu": 0.20, "memory": 0.40, "control": 0.20, "io": 0.05}
    ),
    "control": Intel8008Workload(
        "control", "Control-flow heavy",
        {"transfer": 0.15, "alu": 0.20, "memory": 0.10, "control": 0.50, "io": 0.05}
    ),
    "scelbal": Intel8008Workload(
        "scelbal", "SCELBAL BASIC interpreter",
        {"transfer": 0.22, "alu": 0.30, "memory": 0.18, "control": 0.25, "io": 0.05}
    ),
}


@dataclass
class Intel8008Result:
    """Result from 8008 model."""
    system: str = ""
    clock_khz: float = 500
    
    avg_t_states: float = 0.0
    avg_clock_cycles: float = 0.0
    cpi: float = 0.0
    ipc: float = 0.0
    
    ips: float = 0.0
    mips: float = 0.0
    
    validation_status: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class Intel8008ModelV2:
    """Improved Intel 8008 Model with complete instruction timing."""
    
    CLOCKS_PER_T_STATE = 2  # CRITICAL: 8008 uses 2 clocks per T-state
    
    SYSTEMS = {
        "8008": {"name": "Intel 8008", "clock_khz": 500, "t_state_us": 4.0},
        "8008-1": {"name": "Intel 8008-1", "clock_khz": 800, "t_state_us": 2.5},
    }
    
    def __init__(self, system: str = "8008"):
        self.system = self.SYSTEMS.get(system, self.SYSTEMS["8008"])
        self.instructions = INSTRUCTIONS_8008_COMPLETE
    
    def _get_avg_t_states_by_category(self) -> Dict[str, float]:
        """Calculate average T-states per category."""
        by_cat = {}
        for instr in self.instructions.values():
            cat = instr.category
            if cat not in by_cat:
                by_cat[cat] = []
            by_cat[cat].append(instr.t_states)
        
        return {cat: sum(ts)/len(ts) for cat, ts in by_cat.items()}
    
    def analyze(self, workload: str = "typical") -> Intel8008Result:
        """Analyze performance for workload."""
        result = Intel8008Result()
        result.system = self.system["name"]
        result.clock_khz = self.system["clock_khz"]
        
        wl = WORKLOADS_8008.get(workload, WORKLOADS_8008["typical"])
        cat_avgs = self._get_avg_t_states_by_category()
        
        # Calculate weighted average T-states
        result.avg_t_states = sum(
            cat_avgs.get(cat, 7.0) * frac 
            for cat, frac in wl.instruction_mix.items()
        )
        
        result.avg_clock_cycles = result.avg_t_states * self.CLOCKS_PER_T_STATE
        result.cpi = result.avg_clock_cycles
        result.ipc = 1.0 / result.cpi
        
        # Calculate IPS
        instruction_time_us = result.avg_t_states * self.system["t_state_us"]
        result.ips = 1_000_000 / instruction_time_us
        result.mips = result.ips / 1_000_000
        
        # Validation
        if self.system["clock_khz"] == 500:
            expected = (22500, 50000)
        else:
            expected = (36000, 80000)
        
        if expected[0] <= result.ips <= expected[1]:
            result.validation_status = "PASS"
        else:
            result.validation_status = f"CHECK (expected {expected[0]:,}-{expected[1]:,})"
        
        return result
    
    def validate_timing(self) -> Dict[str, Tuple[bool, str]]:
        """Validate instruction timing against known values."""
        tests = {}
        
        # Check T-state range
        t_states = [i.t_states for i in self.instructions.values()]
        tests["min_t_states"] = (min(t_states) >= 4, f"min={min(t_states)}")
        tests["max_t_states"] = (max(t_states) == 11, f"max={max(t_states)}")
        
        # Check specific instructions
        tests["mov_r_r_is_5"] = (
            self.instructions["MOV_A_B"].t_states == 5,
            f"MOV r,r = {self.instructions['MOV_A_B'].t_states}T"
        )
        tests["mov_r_m_is_8"] = (
            self.instructions["MOV_A_M"].t_states == 8,
            f"MOV r,M = {self.instructions['MOV_A_M'].t_states}T"
        )
        tests["jmp_is_11"] = (
            self.instructions["JMP"].t_states == 11,
            f"JMP = {self.instructions['JMP'].t_states}T"
        )
        tests["hlt_is_4"] = (
            self.instructions["HLT"].t_states == 4,
            f"HLT = {self.instructions['HLT'].t_states}T"
        )
        
        # Instruction count
        tests["instruction_count"] = (
            len(self.instructions) >= 60,
            f"count={len(self.instructions)}"
        )
        
        return tests


def get_improved_8008_config() -> Dict:
    """Get improved 8008 config for unified interface."""
    model = Intel8008ModelV2("8008")
    result = model.analyze("typical")
    
    # Category averages
    cat_avgs = model._get_avg_t_states_by_category()
    
    return {
        "family": "INTEL",
        "category": "SIMPLE_8BIT",
        "year": 1972,
        "bits": 8,
        "clock_mhz": 0.5,
        "transistors": 3500,
        "process_um": 10,
        "description": "First 8-bit microprocessor",
        
        "base_cpi": result.cpi,
        "clocks_per_t_state": 2,
        
        "instruction_count": len(INSTRUCTIONS_8008_COMPLETE),
        "t_state_range": [4, 11],
        
        "category_timing": {
            cat: {"avg_t_states": avg, "avg_clocks": avg * 2}
            for cat, avg in cat_avgs.items()
        },
        
        "ips_range_500khz": [22500, 50000],
        "ips_range_800khz": [36000, 80000],
        "ips_typical": result.ips,
        "mips": result.mips,
        
        "validation": {
            "source": "Intel 8008 Users Manual, CPU-World",
            "t_state_note": "Each T-state = 2 clock cycles (unique to 8008)"
        }
    }


if __name__ == "__main__":
    print("="*70)
    print("INTEL 8008 IMPROVED MODEL v2.0")
    print("Complete instruction timing database")
    print("="*70)
    
    model = Intel8008ModelV2("8008")
    
    # Validation
    print("\n1. TIMING VALIDATION")
    print("-"*40)
    tests = model.validate_timing()
    passed = sum(1 for t, _ in tests.values() if t)
    print(f"   Passed: {passed}/{len(tests)}")
    for name, (ok, msg) in tests.items():
        print(f"   {'✓' if ok else '✗'} {name}: {msg}")
    
    # Instruction statistics
    print(f"\n2. INSTRUCTION SET ({len(INSTRUCTIONS_8008_COMPLETE)} instructions)")
    print("-"*40)
    cat_avgs = model._get_avg_t_states_by_category()
    for cat, avg in sorted(cat_avgs.items()):
        count = len([i for i in INSTRUCTIONS_8008_COMPLETE.values() if i.category == cat])
        print(f"   {cat:<12}: {count:>3} instructions, avg {avg:.1f} T-states")
    
    # System comparison
    print("\n3. SYSTEM PERFORMANCE")
    print("-"*40)
    for sys_name in ["8008", "8008-1"]:
        m = Intel8008ModelV2(sys_name)
        r = m.analyze("typical")
        print(f"   {r.system:<15}: {r.ips:>10,.0f} IPS, {r.mips:.4f} MIPS [{r.validation_status}]")
    
    # Workload analysis
    print("\n4. WORKLOAD ANALYSIS (8008 @ 500 kHz)")
    print("-"*40)
    for wl_name in WORKLOADS_8008:
        result = model.analyze(wl_name)
        print(f"   {wl_name:<12}: {result.ips:>8,.0f} IPS, {result.avg_t_states:.1f} avg T-states")
    
    # Export
    config = get_improved_8008_config()
    with open("/home/claude/8008_improved_v2.json", "w") as f:
        json.dump({
            "processor": "Intel 8008",
            "version": "2.0",
            "config": config,
            "instruction_count": len(INSTRUCTIONS_8008_COMPLETE),
            "workloads": {k: model.analyze(k).to_dict() for k in WORKLOADS_8008}
        }, f, indent=2)
    
    print("\n5. EXPORT")
    print("-"*40)
    print(f"   Total instructions: {config['instruction_count']}")
    print(f"   Exported to: 8008_improved_v2.json")
    print("="*70)
