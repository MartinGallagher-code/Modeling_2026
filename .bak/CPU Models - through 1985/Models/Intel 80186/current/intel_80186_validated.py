#!/usr/bin/env python3
"""
Intel 80186/80188 IMPROVED Performance Model v2.0

Complete instruction timing based on:
- Intel 80186/80188 Datasheet
- Application Note AP-186
- stanislavs.org/helppc instruction reference

Key improvements over 8086:
- Dedicated address calculation unit
- MUL/DIV 4-5× faster  
- Multi-bit shifts ~4× faster
- 10 new instructions

Author: Grey-Box Performance Modeling Research
Date: January 26, 2026
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple
import json


@dataclass
class Instruction80186:
    """80186/80188 instruction with timing."""
    mnemonic: str
    description: str
    cycles_186: int       # 80186 clock cycles
    cycles_8086: int      # 8086 cycles for comparison
    is_new: bool = False  # New in 80186
    category: str = "misc"


# 80186 instruction timing compared to 8086
# Reference: Intel datasheet, AP-186
INSTRUCTIONS_80186 = {
    # ========== DATA TRANSFER ==========
    "MOV_reg_reg": Instruction80186("MOV reg,reg", "Move register to register", 2, 2, False, "transfer"),
    "MOV_reg_mem": Instruction80186("MOV reg,mem", "Move memory to register", 9, 10, False, "transfer"),
    "MOV_mem_reg": Instruction80186("MOV mem,reg", "Move register to memory", 9, 10, False, "transfer"),
    "MOV_reg_imm": Instruction80186("MOV reg,imm", "Move immediate to register", 3, 4, False, "transfer"),
    "MOV_mem_imm": Instruction80186("MOV mem,imm", "Move immediate to memory", 12, 14, False, "transfer"),
    "MOV_acc_mem": Instruction80186("MOV acc,mem", "Move memory to accumulator", 8, 10, False, "transfer"),
    "MOV_mem_acc": Instruction80186("MOV mem,acc", "Move accumulator to memory", 9, 10, False, "transfer"),
    
    "PUSH_reg": Instruction80186("PUSH reg", "Push register", 10, 11, False, "transfer"),
    "PUSH_mem": Instruction80186("PUSH mem", "Push memory", 16, 17, False, "transfer"),
    "PUSH_imm": Instruction80186("PUSH imm", "Push immediate", 10, 0, True, "transfer"),  # NEW
    "POP_reg": Instruction80186("POP reg", "Pop register", 10, 8, False, "transfer"),
    "POP_mem": Instruction80186("POP mem", "Pop memory", 17, 17, False, "transfer"),
    
    "XCHG_reg_reg": Instruction80186("XCHG reg,reg", "Exchange registers", 4, 4, False, "transfer"),
    "XCHG_reg_mem": Instruction80186("XCHG reg,mem", "Exchange with memory", 17, 17, False, "transfer"),
    
    "XLAT": Instruction80186("XLAT", "Translate", 11, 11, False, "transfer"),
    "LEA": Instruction80186("LEA", "Load effective address", 6, 2, False, "transfer"),
    "LDS": Instruction80186("LDS", "Load pointer using DS", 18, 16, False, "transfer"),
    "LES": Instruction80186("LES", "Load pointer using ES", 18, 16, False, "transfer"),
    "LAHF": Instruction80186("LAHF", "Load AH from flags", 2, 4, False, "transfer"),
    "SAHF": Instruction80186("SAHF", "Store AH to flags", 3, 4, False, "transfer"),
    "PUSHF": Instruction80186("PUSHF", "Push flags", 9, 10, False, "transfer"),
    "POPF": Instruction80186("POPF", "Pop flags", 8, 8, False, "transfer"),
    
    # NEW 80186 instructions
    "PUSHA": Instruction80186("PUSHA", "Push all registers", 36, 0, True, "transfer"),
    "POPA": Instruction80186("POPA", "Pop all registers", 51, 0, True, "transfer"),
    
    # ========== ARITHMETIC ==========
    "ADD_reg_reg": Instruction80186("ADD reg,reg", "Add register to register", 3, 3, False, "alu"),
    "ADD_reg_mem": Instruction80186("ADD reg,mem", "Add memory to register", 10, 10, False, "alu"),
    "ADD_mem_reg": Instruction80186("ADD mem,reg", "Add register to memory", 15, 16, False, "alu"),
    "ADD_reg_imm": Instruction80186("ADD reg,imm", "Add immediate to register", 4, 4, False, "alu"),
    "ADD_mem_imm": Instruction80186("ADD mem,imm", "Add immediate to memory", 15, 17, False, "alu"),
    "ADD_acc_imm": Instruction80186("ADD acc,imm", "Add immediate to accumulator", 3, 4, False, "alu"),
    
    "ADC_reg_reg": Instruction80186("ADC reg,reg", "Add with carry reg,reg", 3, 3, False, "alu"),
    "ADC_reg_mem": Instruction80186("ADC reg,mem", "Add with carry reg,mem", 10, 10, False, "alu"),
    
    "SUB_reg_reg": Instruction80186("SUB reg,reg", "Subtract reg from reg", 3, 3, False, "alu"),
    "SUB_reg_mem": Instruction80186("SUB reg,mem", "Subtract mem from reg", 10, 10, False, "alu"),
    "SUB_mem_reg": Instruction80186("SUB mem,reg", "Subtract reg from mem", 15, 16, False, "alu"),
    "SUB_reg_imm": Instruction80186("SUB reg,imm", "Subtract immediate", 4, 4, False, "alu"),
    
    "SBB_reg_reg": Instruction80186("SBB reg,reg", "Subtract with borrow", 3, 3, False, "alu"),
    
    "INC_reg": Instruction80186("INC reg", "Increment register", 3, 2, False, "alu"),
    "INC_mem": Instruction80186("INC mem", "Increment memory", 15, 15, False, "alu"),
    "DEC_reg": Instruction80186("DEC reg", "Decrement register", 3, 2, False, "alu"),
    "DEC_mem": Instruction80186("DEC mem", "Decrement memory", 15, 15, False, "alu"),
    
    "NEG_reg": Instruction80186("NEG reg", "Negate register", 3, 3, False, "alu"),
    "NEG_mem": Instruction80186("NEG mem", "Negate memory", 15, 16, False, "alu"),
    
    "CMP_reg_reg": Instruction80186("CMP reg,reg", "Compare registers", 3, 3, False, "alu"),
    "CMP_reg_mem": Instruction80186("CMP reg,mem", "Compare reg with mem", 10, 10, False, "alu"),
    "CMP_reg_imm": Instruction80186("CMP reg,imm", "Compare reg with immediate", 4, 4, False, "alu"),
    
    # MULTIPLY - MAJOR IMPROVEMENT!
    "MUL_reg8": Instruction80186("MUL reg8", "Unsigned multiply 8-bit", 26, 77, False, "alu"),
    "MUL_mem8": Instruction80186("MUL mem8", "Unsigned multiply 8-bit mem", 32, 83, False, "alu"),
    "MUL_reg16": Instruction80186("MUL reg16", "Unsigned multiply 16-bit", 35, 133, False, "alu"),
    "MUL_mem16": Instruction80186("MUL mem16", "Unsigned multiply 16-bit mem", 41, 139, False, "alu"),
    
    "IMUL_reg8": Instruction80186("IMUL reg8", "Signed multiply 8-bit", 25, 98, False, "alu"),
    "IMUL_mem8": Instruction80186("IMUL mem8", "Signed multiply 8-bit mem", 31, 104, False, "alu"),
    "IMUL_reg16": Instruction80186("IMUL reg16", "Signed multiply 16-bit", 34, 154, False, "alu"),
    "IMUL_mem16": Instruction80186("IMUL mem16", "Signed multiply 16-bit mem", 40, 160, False, "alu"),
    "IMUL_reg_imm": Instruction80186("IMUL reg,imm", "Signed multiply immediate", 22, 0, True, "alu"),  # NEW
    
    # DIVIDE - MAJOR IMPROVEMENT!
    "DIV_reg8": Instruction80186("DIV reg8", "Unsigned divide 8-bit", 29, 90, False, "alu"),
    "DIV_mem8": Instruction80186("DIV mem8", "Unsigned divide 8-bit mem", 35, 96, False, "alu"),
    "DIV_reg16": Instruction80186("DIV reg16", "Unsigned divide 16-bit", 38, 162, False, "alu"),
    "DIV_mem16": Instruction80186("DIV mem16", "Unsigned divide 16-bit mem", 44, 168, False, "alu"),
    
    "IDIV_reg8": Instruction80186("IDIV reg8", "Signed divide 8-bit", 44, 112, False, "alu"),
    "IDIV_mem8": Instruction80186("IDIV mem8", "Signed divide 8-bit mem", 50, 118, False, "alu"),
    "IDIV_reg16": Instruction80186("IDIV reg16", "Signed divide 16-bit", 57, 184, False, "alu"),
    "IDIV_mem16": Instruction80186("IDIV mem16", "Signed divide 16-bit mem", 63, 190, False, "alu"),
    
    "CBW": Instruction80186("CBW", "Convert byte to word", 2, 2, False, "alu"),
    "CWD": Instruction80186("CWD", "Convert word to double", 4, 5, False, "alu"),
    
    "AAA": Instruction80186("AAA", "ASCII adjust for add", 8, 4, False, "alu"),
    "AAS": Instruction80186("AAS", "ASCII adjust for sub", 7, 4, False, "alu"),
    "AAM": Instruction80186("AAM", "ASCII adjust for mul", 19, 83, False, "alu"),
    "AAD": Instruction80186("AAD", "ASCII adjust for div", 15, 60, False, "alu"),
    "DAA": Instruction80186("DAA", "Decimal adjust for add", 4, 4, False, "alu"),
    "DAS": Instruction80186("DAS", "Decimal adjust for sub", 4, 4, False, "alu"),
    
    # ========== LOGIC ==========
    "AND_reg_reg": Instruction80186("AND reg,reg", "AND registers", 3, 3, False, "logic"),
    "AND_reg_mem": Instruction80186("AND reg,mem", "AND with memory", 10, 10, False, "logic"),
    "AND_mem_reg": Instruction80186("AND mem,reg", "AND memory with reg", 15, 16, False, "logic"),
    "AND_reg_imm": Instruction80186("AND reg,imm", "AND with immediate", 4, 4, False, "logic"),
    
    "OR_reg_reg": Instruction80186("OR reg,reg", "OR registers", 3, 3, False, "logic"),
    "OR_reg_mem": Instruction80186("OR reg,mem", "OR with memory", 10, 10, False, "logic"),
    
    "XOR_reg_reg": Instruction80186("XOR reg,reg", "XOR registers", 3, 3, False, "logic"),
    "XOR_reg_mem": Instruction80186("XOR reg,mem", "XOR with memory", 10, 10, False, "logic"),
    
    "NOT_reg": Instruction80186("NOT reg", "NOT register", 3, 3, False, "logic"),
    "NOT_mem": Instruction80186("NOT mem", "NOT memory", 15, 16, False, "logic"),
    
    "TEST_reg_reg": Instruction80186("TEST reg,reg", "Test registers", 3, 3, False, "logic"),
    "TEST_reg_mem": Instruction80186("TEST reg,mem", "Test with memory", 10, 10, False, "logic"),
    "TEST_reg_imm": Instruction80186("TEST reg,imm", "Test with immediate", 4, 5, False, "logic"),
    
    # SHIFTS - MAJOR IMPROVEMENT!
    "SHL_reg_1": Instruction80186("SHL reg,1", "Shift left by 1", 2, 2, False, "shift"),
    "SHL_mem_1": Instruction80186("SHL mem,1", "Shift left mem by 1", 15, 15, False, "shift"),
    "SHL_reg_CL": Instruction80186("SHL reg,CL", "Shift left by CL", 5, 20, False, "shift"),  # Was 8+4n!
    "SHL_mem_CL": Instruction80186("SHL mem,CL", "Shift left mem by CL", 17, 28, False, "shift"),
    "SHL_reg_imm": Instruction80186("SHL reg,imm", "Shift left by immediate", 5, 0, True, "shift"),  # NEW
    "SHL_mem_imm": Instruction80186("SHL mem,imm", "Shift left mem by imm", 17, 0, True, "shift"),  # NEW
    
    "SHR_reg_1": Instruction80186("SHR reg,1", "Shift right by 1", 2, 2, False, "shift"),
    "SHR_mem_1": Instruction80186("SHR mem,1", "Shift right mem by 1", 15, 15, False, "shift"),
    "SHR_reg_CL": Instruction80186("SHR reg,CL", "Shift right by CL", 5, 20, False, "shift"),
    "SHR_mem_CL": Instruction80186("SHR mem,CL", "Shift right mem by CL", 17, 28, False, "shift"),
    "SHR_reg_imm": Instruction80186("SHR reg,imm", "Shift right by immediate", 5, 0, True, "shift"),  # NEW
    
    "SAR_reg_1": Instruction80186("SAR reg,1", "Arithmetic shift right 1", 2, 2, False, "shift"),
    "SAR_reg_CL": Instruction80186("SAR reg,CL", "Arithmetic shift right CL", 5, 20, False, "shift"),
    
    "ROL_reg_1": Instruction80186("ROL reg,1", "Rotate left by 1", 2, 2, False, "shift"),
    "ROL_reg_CL": Instruction80186("ROL reg,CL", "Rotate left by CL", 5, 20, False, "shift"),
    "ROR_reg_1": Instruction80186("ROR reg,1", "Rotate right by 1", 2, 2, False, "shift"),
    "ROR_reg_CL": Instruction80186("ROR reg,CL", "Rotate right by CL", 5, 20, False, "shift"),
    "RCL_reg_1": Instruction80186("RCL reg,1", "Rotate thru carry left 1", 2, 2, False, "shift"),
    "RCL_reg_CL": Instruction80186("RCL reg,CL", "Rotate thru carry left CL", 5, 20, False, "shift"),
    "RCR_reg_1": Instruction80186("RCR reg,1", "Rotate thru carry right 1", 2, 2, False, "shift"),
    "RCR_reg_CL": Instruction80186("RCR reg,CL", "Rotate thru carry right CL", 5, 20, False, "shift"),
    
    # ========== STRING OPERATIONS ==========
    "MOVSB": Instruction80186("MOVSB", "Move string byte", 14, 18, False, "string"),
    "MOVSW": Instruction80186("MOVSW", "Move string word", 14, 18, False, "string"),
    "CMPSB": Instruction80186("CMPSB", "Compare string byte", 22, 22, False, "string"),
    "CMPSW": Instruction80186("CMPSW", "Compare string word", 22, 22, False, "string"),
    "SCASB": Instruction80186("SCASB", "Scan string byte", 15, 15, False, "string"),
    "SCASW": Instruction80186("SCASW", "Scan string word", 15, 15, False, "string"),
    "LODSB": Instruction80186("LODSB", "Load string byte", 12, 12, False, "string"),
    "LODSW": Instruction80186("LODSW", "Load string word", 12, 12, False, "string"),
    "STOSB": Instruction80186("STOSB", "Store string byte", 10, 11, False, "string"),
    "STOSW": Instruction80186("STOSW", "Store string word", 10, 11, False, "string"),
    
    # NEW string I/O
    "INSB": Instruction80186("INSB", "Input string byte", 14, 0, True, "string"),
    "INSW": Instruction80186("INSW", "Input string word", 14, 0, True, "string"),
    "OUTSB": Instruction80186("OUTSB", "Output string byte", 14, 0, True, "string"),
    "OUTSW": Instruction80186("OUTSW", "Output string word", 14, 0, True, "string"),
    
    # ========== CONTROL TRANSFER ==========
    "JMP_short": Instruction80186("JMP short", "Jump short", 14, 15, False, "control"),
    "JMP_near": Instruction80186("JMP near", "Jump near", 14, 15, False, "control"),
    "JMP_far": Instruction80186("JMP far", "Jump far", 21, 15, False, "control"),
    "JMP_mem": Instruction80186("JMP mem", "Jump indirect", 18, 18, False, "control"),
    
    "Jcc_taken": Instruction80186("Jcc (taken)", "Conditional jump taken", 13, 16, False, "control"),
    "Jcc_not_taken": Instruction80186("Jcc (not taken)", "Conditional jump not taken", 4, 4, False, "control"),
    
    "LOOP": Instruction80186("LOOP", "Loop", 15, 17, False, "control"),
    "LOOPE": Instruction80186("LOOPE", "Loop if equal", 16, 18, False, "control"),
    "LOOPNE": Instruction80186("LOOPNE", "Loop if not equal", 16, 19, False, "control"),
    "JCXZ": Instruction80186("JCXZ", "Jump if CX zero", 8, 18, False, "control"),
    
    "CALL_near": Instruction80186("CALL near", "Call near", 15, 19, False, "control"),
    "CALL_far": Instruction80186("CALL far", "Call far", 23, 28, False, "control"),
    "CALL_mem": Instruction80186("CALL mem", "Call indirect", 21, 21, False, "control"),
    
    "RET_near": Instruction80186("RET near", "Return near", 16, 8, False, "control"),
    "RET_far": Instruction80186("RET far", "Return far", 22, 18, False, "control"),
    "RET_imm": Instruction80186("RET imm", "Return with stack adjust", 18, 12, False, "control"),
    
    "INT": Instruction80186("INT n", "Software interrupt", 47, 51, False, "control"),
    "INTO": Instruction80186("INTO", "Interrupt on overflow", 48, 53, False, "control"),
    "IRET": Instruction80186("IRET", "Interrupt return", 28, 24, False, "control"),
    
    # NEW stack frame
    "ENTER": Instruction80186("ENTER", "Make stack frame", 15, 0, True, "control"),  # +4 per level
    "LEAVE": Instruction80186("LEAVE", "Restore stack frame", 8, 0, True, "control"),
    "BOUND": Instruction80186("BOUND", "Check array bounds", 33, 0, True, "control"),
    
    # ========== I/O ==========
    "IN_fixed": Instruction80186("IN port", "Input from fixed port", 10, 10, False, "io"),
    "IN_dx": Instruction80186("IN DX", "Input from DX port", 8, 8, False, "io"),
    "OUT_fixed": Instruction80186("OUT port", "Output to fixed port", 9, 10, False, "io"),
    "OUT_dx": Instruction80186("OUT DX", "Output to DX port", 7, 8, False, "io"),
    
    # ========== PROCESSOR CONTROL ==========
    "CLC": Instruction80186("CLC", "Clear carry", 2, 2, False, "flag"),
    "STC": Instruction80186("STC", "Set carry", 2, 2, False, "flag"),
    "CMC": Instruction80186("CMC", "Complement carry", 2, 2, False, "flag"),
    "CLD": Instruction80186("CLD", "Clear direction", 2, 2, False, "flag"),
    "STD": Instruction80186("STD", "Set direction", 2, 2, False, "flag"),
    "CLI": Instruction80186("CLI", "Clear interrupt", 2, 2, False, "flag"),
    "STI": Instruction80186("STI", "Set interrupt", 2, 2, False, "flag"),
    "NOP": Instruction80186("NOP", "No operation", 3, 3, False, "control"),
    "HLT": Instruction80186("HLT", "Halt", 2, 2, False, "control"),
    "WAIT": Instruction80186("WAIT", "Wait for coprocessor", 6, 3, False, "control"),
    "LOCK": Instruction80186("LOCK", "Lock bus", 2, 2, False, "control"),
}


@dataclass
class Intel80186Workload:
    """Workload for 80186/80188."""
    name: str
    description: str
    instruction_mix: Dict[str, float]


WORKLOADS_80186 = {
    "typical": Intel80186Workload(
        "typical", "Typical embedded application",
        {"transfer": 0.25, "alu": 0.25, "logic": 0.10, "shift": 0.08, 
         "control": 0.20, "string": 0.05, "io": 0.05, "flag": 0.02}
    ),
    "compute": Intel80186Workload(
        "compute", "Compute-intensive (MUL/DIV heavy)",
        {"transfer": 0.15, "alu": 0.45, "logic": 0.10, "shift": 0.12,
         "control": 0.12, "string": 0.02, "io": 0.02, "flag": 0.02}
    ),
    "control": Intel80186Workload(
        "control", "Control-flow heavy",
        {"transfer": 0.20, "alu": 0.15, "logic": 0.08, "shift": 0.05,
         "control": 0.40, "string": 0.05, "io": 0.05, "flag": 0.02}
    ),
    "string": Intel80186Workload(
        "string", "String operations heavy",
        {"transfer": 0.15, "alu": 0.10, "logic": 0.05, "shift": 0.05,
         "control": 0.15, "string": 0.40, "io": 0.08, "flag": 0.02}
    ),
}


@dataclass
class Intel80186Result:
    """Result from 80186/80188 model."""
    variant: str = "80186"
    clock_mhz: float = 8.0
    
    avg_cycles_186: float = 0.0
    avg_cycles_8086: float = 0.0
    speedup_vs_8086: float = 0.0
    
    ips: float = 0.0
    mips: float = 0.0
    
    # 80188 penalty
    bus_penalty: float = 1.0
    ips_188: float = 0.0
    mips_188: float = 0.0
    
    validation_status: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class Intel80186ModelV2:
    """Improved 80186/80188 model with real instruction timing."""
    
    def __init__(self, clock_mhz: float = 8.0):
        self.clock_mhz = clock_mhz
        self.instructions = INSTRUCTIONS_80186
    
    def _get_avg_cycles_by_category(self, use_8086: bool = False) -> Dict[str, float]:
        """Calculate average cycles per category."""
        by_cat = {}
        for instr in self.instructions.values():
            cat = instr.category
            if cat not in by_cat:
                by_cat[cat] = []
            cycles = instr.cycles_8086 if use_8086 else instr.cycles_186
            if cycles > 0:  # Skip new instructions for 8086
                by_cat[cat].append(cycles)
        
        return {cat: sum(c)/len(c) for cat, c in by_cat.items() if c}
    
    def analyze(self, workload: str = "typical") -> Intel80186Result:
        """Analyze 80186/80188 performance."""
        result = Intel80186Result()
        result.variant = "80186"
        result.clock_mhz = self.clock_mhz
        
        wl = WORKLOADS_80186.get(workload, WORKLOADS_80186["typical"])
        
        cat_avgs_186 = self._get_avg_cycles_by_category(use_8086=False)
        cat_avgs_8086 = self._get_avg_cycles_by_category(use_8086=True)
        
        # Calculate weighted average cycles
        result.avg_cycles_186 = sum(
            cat_avgs_186.get(cat, 10.0) * frac
            for cat, frac in wl.instruction_mix.items()
        )
        
        result.avg_cycles_8086 = sum(
            cat_avgs_8086.get(cat, 12.0) * frac
            for cat, frac in wl.instruction_mix.items()
        )
        
        result.speedup_vs_8086 = result.avg_cycles_8086 / result.avg_cycles_186
        
        # IPS for 80186
        result.ips = (self.clock_mhz * 1_000_000) / result.avg_cycles_186
        result.mips = result.ips / 1_000_000
        
        # 80188: ~30% penalty for memory-heavy workloads
        memory_fraction = wl.instruction_mix.get("transfer", 0.25) + wl.instruction_mix.get("string", 0.05)
        result.bus_penalty = 1 + 0.35 * memory_fraction
        result.ips_188 = result.ips / result.bus_penalty
        result.mips_188 = result.mips / result.bus_penalty
        
        # Validation
        expected_mips = (0.8, 1.5) if self.clock_mhz >= 8 else (0.5, 1.0)
        if expected_mips[0] <= result.mips <= expected_mips[1]:
            result.validation_status = "PASS"
        else:
            result.validation_status = f"CHECK ({expected_mips[0]}-{expected_mips[1]} expected)"
        
        return result
    
    def get_speedup_analysis(self) -> Dict[str, float]:
        """Get speedup by instruction type."""
        speedups = {}
        for name, instr in self.instructions.items():
            if instr.cycles_8086 > 0 and instr.cycles_186 > 0:
                speedup = instr.cycles_8086 / instr.cycles_186
                if speedup > 1.5:  # Only show significant improvements
                    speedups[name] = speedup
        return dict(sorted(speedups.items(), key=lambda x: -x[1])[:20])


def get_improved_80186_config() -> Dict:
    """Get improved 80186 config."""
    model = Intel80186ModelV2(8.0)
    result = model.analyze("typical")
    
    new_instructions = [i for i in INSTRUCTIONS_80186.values() if i.is_new]
    
    return {
        "family": "INTEL",
        "category": "COMPLEX_16BIT",
        "year": 1982,
        "bits": 16,
        "clock_mhz": 8.0,
        "transistors": 55000,
        "process_um": 3,
        
        "instruction_count": len(INSTRUCTIONS_80186),
        "new_instructions": len(new_instructions),
        
        "avg_cpi_186": result.avg_cycles_186,
        "avg_cpi_8086": result.avg_cycles_8086,
        "speedup_vs_8086": result.speedup_vs_8086,
        
        "ips_186": result.ips,
        "mips_186": result.mips,
        "ips_188": result.ips_188,
        "mips_188": result.mips_188,
        
        "major_improvements": {
            "MUL_16bit": "133 -> 35 cycles (3.8×)",
            "DIV_16bit": "162 -> 38 cycles (4.3×)",
            "IMUL_16bit": "154 -> 34 cycles (4.5×)",
            "IDIV_16bit": "184 -> 57 cycles (3.2×)",
            "SHL_CL": "8+4n -> 5+n cycles (~4×)",
        },
        
        "validation": {
            "source": "Intel 80186 Datasheet, AP-186",
        }
    }


if __name__ == "__main__":
    print("="*70)
    print("INTEL 80186/80188 IMPROVED MODEL v2.0")
    print("Complete instruction timing with 8086 comparison")
    print("="*70)
    
    model = Intel80186ModelV2(8.0)
    
    # New instructions
    print(f"\n1. INSTRUCTION SET ({len(INSTRUCTIONS_80186)} instructions)")
    print("-"*40)
    new_instrs = [i for i in INSTRUCTIONS_80186.values() if i.is_new]
    print(f"   New 80186 instructions: {len(new_instrs)}")
    for instr in new_instrs:
        print(f"   • {instr.mnemonic}: {instr.description} ({instr.cycles_186} cycles)")
    
    # Major speedups
    print("\n2. MAJOR TIMING IMPROVEMENTS vs 8086")
    print("-"*40)
    speedups = model.get_speedup_analysis()
    print(f"   {'Instruction':<20} {'8086':>8} {'80186':>8} {'Speedup':>8}")
    print(f"   {'-'*44}")
    for name, speedup in list(speedups.items())[:10]:
        instr = INSTRUCTIONS_80186[name]
        print(f"   {instr.mnemonic:<20} {instr.cycles_8086:>8} {instr.cycles_186:>8} {speedup:>7.1f}×")
    
    # Performance by clock
    print("\n3. PERFORMANCE BY CLOCK SPEED")
    print("-"*40)
    print(f"   {'Clock':<8} {'80186 MIPS':>12} {'80188 MIPS':>12} {'vs 8086':>10}")
    print(f"   {'-'*44}")
    for clock in [6.0, 8.0, 10.0, 12.0, 16.0, 20.0]:
        m = Intel80186ModelV2(clock)
        r = m.analyze("typical")
        print(f"   {clock:>6.0f}M {r.mips:>12.2f} {r.mips_188:>12.2f} {r.speedup_vs_8086:>9.2f}×")
    
    # Workload analysis
    print("\n4. WORKLOAD ANALYSIS (8 MHz)")
    print("-"*40)
    for wl_name in WORKLOADS_80186:
        result = model.analyze(wl_name)
        print(f"   {wl_name:<12}: 186={result.mips:.2f} MIPS, 188={result.mips_188:.2f} MIPS, "
              f"vs 8086={result.speedup_vs_8086:.2f}×")
    
    # Export
    config = get_improved_80186_config()
    with open("/home/claude/80186_improved_v2.json", "w") as f:
        json.dump({
            "processor": "Intel 80186/80188",
            "version": "2.0",
            "config": config,
            "workloads": {k: model.analyze(k).to_dict() for k in WORKLOADS_80186}
        }, f, indent=2)
    
    print("\n5. EXPORT")
    print("-"*40)
    print(f"   Exported to: 80186_improved_v2.json")
    print(f"   80186 @ 8 MHz: {config['mips_186']:.2f} MIPS")
    print(f"   80188 @ 8 MHz: {config['mips_188']:.2f} MIPS")
    print("="*70)
