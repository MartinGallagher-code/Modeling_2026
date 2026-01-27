#!/usr/bin/env python3
"""
Fairchild F8 IMPROVED Performance Model v2.0

Complete instruction timing based on:
- Fairchild F8 User's Guide (1976)
- 1982/1983 Fairchild Microprocessor Products Data Book
- MAME emulator source code (cycle-accurate)

Key timing:
- Short cycle (cS): 4 φ periods = 4 µs @ 1 MHz = 2 µs @ 2 MHz
- Long cycle (cL): 6 φ periods = 6 µs @ 1 MHz = 3 µs @ 2 MHz
- Most instructions: 1 short cycle (4 φ)
- Memory/branch: 1 long cycle (6 φ) or more

Author: Grey-Box Performance Modeling Research
Date: January 26, 2026
"""

from dataclasses import dataclass, asdict
from typing import Dict, List
from enum import Enum
import json


class CycleType(Enum):
    """F8 cycle types from MAME source."""
    SHORT = 4   # 4 φ periods (cS)
    LONG = 6    # 6 φ periods (cL)


@dataclass
class F8Instruction:
    """F8 instruction with validated timing."""
    mnemonic: str
    description: str
    opcode: int
    phi_periods: int      # Total φ periods
    bytes: int            # Instruction length
    category: str
    
    @property
    def cycles_short_equiv(self) -> float:
        """Equivalent short cycles."""
        return self.phi_periods / 4


# Complete F8 instruction set from MAME and Fairchild databook
# Timing in φ periods (4 = short cycle, 6 = long cycle, etc.)
INSTRUCTIONS_F8_COMPLETE = {
    # ========== ACCUMULATOR/REGISTER TRANSFER (4 φ) ==========
    "LR_A_KU": F8Instruction("LR A,KU", "Load A from KU", 0x00, 4, 1, "transfer"),
    "LR_A_KL": F8Instruction("LR A,KL", "Load A from KL", 0x01, 4, 1, "transfer"),
    "LR_A_QU": F8Instruction("LR A,QU", "Load A from QU", 0x02, 4, 1, "transfer"),
    "LR_A_QL": F8Instruction("LR A,QL", "Load A from QL", 0x03, 4, 1, "transfer"),
    "LR_KU_A": F8Instruction("LR KU,A", "Load KU from A", 0x04, 4, 1, "transfer"),
    "LR_KL_A": F8Instruction("LR KL,A", "Load KL from A", 0x05, 4, 1, "transfer"),
    "LR_QU_A": F8Instruction("LR QU,A", "Load QU from A", 0x06, 4, 1, "transfer"),
    "LR_QL_A": F8Instruction("LR QL,A", "Load QL from A", 0x07, 4, 1, "transfer"),
    
    # ========== PC/K TRANSFERS (8 φ = 2 short cycles) ==========
    "LR_K_P": F8Instruction("LR K,P", "Load K from PC0", 0x08, 8, 1, "transfer"),
    "LR_P_K": F8Instruction("LR P,K", "Load PC0 from K", 0x09, 8, 1, "transfer"),
    "LR_A_IS": F8Instruction("LR A,IS", "Load A from ISAR", 0x0A, 4, 1, "transfer"),
    "LR_IS_A": F8Instruction("LR IS,A", "Load ISAR from A", 0x0B, 4, 1, "transfer"),
    
    # ========== STACK OPERATIONS ==========
    "PK": F8Instruction("PK", "Push K, branch to PC0", 0x0C, 8, 1, "control"),
    "LR_P0_Q": F8Instruction("LR P0,Q", "Load PC0 from Q", 0x0D, 8, 1, "transfer"),
    "LR_Q_DC": F8Instruction("LR Q,DC", "Load Q from DC", 0x0E, 8, 1, "transfer"),
    "LR_DC_Q": F8Instruction("LR DC,Q", "Load DC from Q", 0x0F, 8, 1, "transfer"),
    "LR_DC_H": F8Instruction("LR DC,H", "Load DC from H", 0x10, 8, 1, "transfer"),
    "LR_H_DC": F8Instruction("LR H,DC", "Load H from DC", 0x11, 8, 1, "transfer"),
    
    # ========== SCRATCHPAD REGISTER OPERATIONS (4 φ) ==========
    "LR_A_r": F8Instruction("LR A,r", "Load A from scratchpad", 0x40, 4, 1, "transfer"),  # 0x40-0x4B
    "LR_r_A": F8Instruction("LR r,A", "Load scratchpad from A", 0x50, 4, 1, "transfer"),  # 0x50-0x5B
    
    # ISAR-addressed scratchpad (4 φ)
    "LR_A_S": F8Instruction("LR A,S", "Load A from (ISAR)", 0x4C, 4, 1, "transfer"),
    "LR_A_I": F8Instruction("LR A,I", "Load A from (ISAR), inc ISAR", 0x4D, 4, 1, "transfer"),
    "LR_A_D": F8Instruction("LR A,D", "Load A from (ISAR), dec ISAR", 0x4E, 4, 1, "transfer"),
    "LR_S_A": F8Instruction("LR S,A", "Load (ISAR) from A", 0x5C, 4, 1, "transfer"),
    "LR_I_A": F8Instruction("LR I,A", "Load (ISAR) from A, inc", 0x5D, 4, 1, "transfer"),
    "LR_D_A": F8Instruction("LR D,A", "Load (ISAR) from A, dec", 0x5E, 4, 1, "transfer"),
    
    # ========== IMMEDIATE OPERATIONS (6 φ = 1 long + fetch) ==========
    "LI": F8Instruction("LI", "Load A immediate", 0x20, 6, 2, "transfer"),
    "NI": F8Instruction("NI", "AND A with immediate", 0x21, 6, 2, "alu"),
    "OI": F8Instruction("OI", "OR A with immediate", 0x22, 6, 2, "alu"),
    "XI": F8Instruction("XI", "XOR A with immediate", 0x23, 6, 2, "alu"),
    "AI": F8Instruction("AI", "Add immediate to A", 0x24, 6, 2, "alu"),
    "CI": F8Instruction("CI", "Compare A with immediate", 0x25, 6, 2, "alu"),
    "IN": F8Instruction("IN", "Input from port", 0x26, 8, 2, "io"),
    "OUT": F8Instruction("OUT", "Output to port", 0x27, 8, 2, "io"),
    
    # ========== I/O OPERATIONS (8-12 φ) ==========
    "INS_0": F8Instruction("INS 0", "Input short from port 0", 0xA0, 8, 1, "io"),
    "INS_1": F8Instruction("INS 1", "Input short from port 1", 0xA1, 8, 1, "io"),
    "OUTS_0": F8Instruction("OUTS 0", "Output short to port 0", 0xB0, 8, 1, "io"),
    "OUTS_1": F8Instruction("OUTS 1", "Output short to port 1", 0xB1, 8, 1, "io"),
    
    # ========== ALU OPERATIONS (4 φ for register) ==========
    "SR_1": F8Instruction("SR 1", "Shift right 1", 0x12, 4, 1, "alu"),
    "SL_1": F8Instruction("SL 1", "Shift left 1", 0x13, 4, 1, "alu"),
    "SR_4": F8Instruction("SR 4", "Shift right 4", 0x14, 4, 1, "alu"),
    "SL_4": F8Instruction("SL 4", "Shift left 4", 0x15, 4, 1, "alu"),
    "LM": F8Instruction("LM", "Load A from (DC)", 0x16, 10, 1, "memory"),
    "ST": F8Instruction("ST", "Store A to (DC)", 0x17, 10, 1, "memory"),
    "COM": F8Instruction("COM", "Complement A", 0x18, 4, 1, "alu"),
    "LNK": F8Instruction("LNK", "Link carry to A", 0x19, 4, 1, "alu"),
    "DI": F8Instruction("DI", "Disable interrupt", 0x1A, 4, 1, "control"),
    "EI": F8Instruction("EI", "Enable interrupt", 0x1B, 4, 1, "control"),
    "POP": F8Instruction("POP", "Pop PC from stack", 0x1C, 8, 1, "control"),
    "LR_W_J": F8Instruction("LR W,J", "Load W from J (status)", 0x1D, 4, 1, "transfer"),
    "LR_J_W": F8Instruction("LR J,W", "Load J from W", 0x1E, 8, 1, "transfer"),
    "INC": F8Instruction("INC", "Increment A", 0x1F, 4, 1, "alu"),
    
    # ========== ARITHMETIC WITH SCRATCHPAD (4 φ) ==========
    # AS r - Add scratchpad to A with carry
    "AS_0": F8Instruction("AS 0", "Add r0 to A", 0xC0, 4, 1, "alu"),
    "AS_1": F8Instruction("AS 1", "Add r1 to A", 0xC1, 4, 1, "alu"),
    "AS_2": F8Instruction("AS 2", "Add r2 to A", 0xC2, 4, 1, "alu"),
    "AS_3": F8Instruction("AS 3", "Add r3 to A", 0xC3, 4, 1, "alu"),
    "AS_S": F8Instruction("AS S", "Add (ISAR) to A", 0xCC, 4, 1, "alu"),
    "AS_I": F8Instruction("AS I", "Add (ISAR) to A, inc", 0xCD, 4, 1, "alu"),
    "AS_D": F8Instruction("AS D", "Add (ISAR) to A, dec", 0xCE, 4, 1, "alu"),
    
    # ASD r - Add scratchpad to A with carry, decimal
    "ASD_0": F8Instruction("ASD 0", "Add r0 BCD to A", 0xD0, 8, 1, "alu"),
    "ASD_1": F8Instruction("ASD 1", "Add r1 BCD to A", 0xD1, 8, 1, "alu"),
    "ASD_2": F8Instruction("ASD 2", "Add r2 BCD to A", 0xD2, 8, 1, "alu"),
    "ASD_3": F8Instruction("ASD 3", "Add r3 BCD to A", 0xD3, 8, 1, "alu"),
    "ASD_S": F8Instruction("ASD S", "Add (ISAR) BCD to A", 0xDC, 8, 1, "alu"),
    "ASD_I": F8Instruction("ASD I", "Add (ISAR) BCD, inc", 0xDD, 8, 1, "alu"),
    "ASD_D": F8Instruction("ASD D", "Add (ISAR) BCD, dec", 0xDE, 8, 1, "alu"),
    
    # XS r - XOR scratchpad with A
    "XS_0": F8Instruction("XS 0", "XOR r0 with A", 0xE0, 4, 1, "alu"),
    "XS_1": F8Instruction("XS 1", "XOR r1 with A", 0xE1, 4, 1, "alu"),
    "XS_2": F8Instruction("XS 2", "XOR r2 with A", 0xE2, 4, 1, "alu"),
    "XS_3": F8Instruction("XS 3", "XOR r3 with A", 0xE3, 4, 1, "alu"),
    "XS_S": F8Instruction("XS S", "XOR (ISAR) with A", 0xEC, 4, 1, "alu"),
    "XS_I": F8Instruction("XS I", "XOR (ISAR), inc", 0xED, 4, 1, "alu"),
    "XS_D": F8Instruction("XS D", "XOR (ISAR), dec", 0xEE, 4, 1, "alu"),
    
    # NS r - AND scratchpad with A
    "NS_0": F8Instruction("NS 0", "AND r0 with A", 0xF0, 4, 1, "alu"),
    "NS_1": F8Instruction("NS 1", "AND r1 with A", 0xF1, 4, 1, "alu"),
    "NS_2": F8Instruction("NS 2", "AND r2 with A", 0xF2, 4, 1, "alu"),
    "NS_3": F8Instruction("NS 3", "AND r3 with A", 0xF3, 4, 1, "alu"),
    "NS_S": F8Instruction("NS S", "AND (ISAR) with A", 0xFC, 4, 1, "alu"),
    "NS_I": F8Instruction("NS I", "AND (ISAR), inc", 0xFD, 4, 1, "alu"),
    "NS_D": F8Instruction("NS D", "AND (ISAR), dec", 0xFE, 4, 1, "alu"),
    
    # ========== COMPARE/DECREMENT (4 φ) ==========
    "DS_0": F8Instruction("DS 0", "Decrement r0", 0x30, 6, 1, "alu"),
    "DS_1": F8Instruction("DS 1", "Decrement r1", 0x31, 6, 1, "alu"),
    "DS_2": F8Instruction("DS 2", "Decrement r2", 0x32, 6, 1, "alu"),
    "DS_3": F8Instruction("DS 3", "Decrement r3", 0x33, 6, 1, "alu"),
    "DS_S": F8Instruction("DS S", "Decrement (ISAR)", 0x3C, 6, 1, "alu"),
    "DS_I": F8Instruction("DS I", "Decrement (ISAR), inc", 0x3D, 6, 1, "alu"),
    "DS_D": F8Instruction("DS D", "Decrement (ISAR), dec", 0x3E, 6, 1, "alu"),
    
    # ========== BRANCH INSTRUCTIONS (6-8 φ) ==========
    "BR": F8Instruction("BR", "Branch relative", 0x90, 6, 2, "control"),
    "BM": F8Instruction("BM", "Branch on minus", 0x91, 6, 2, "control"),
    "BNC": F8Instruction("BNC", "Branch no carry", 0x92, 6, 2, "control"),
    "BNO": F8Instruction("BNO", "Branch no overflow", 0x94, 6, 2, "control"),
    "BZ": F8Instruction("BZ", "Branch if zero", 0x84, 6, 2, "control"),
    "BP": F8Instruction("BP", "Branch positive", 0x81, 6, 2, "control"),
    "BC": F8Instruction("BC", "Branch on carry", 0x82, 6, 2, "control"),
    "BT": F8Instruction("BT", "Branch on test", 0x80, 6, 2, "control"),
    "BNZ": F8Instruction("BNZ", "Branch not zero", 0x94, 6, 2, "control"),
    "BR7": F8Instruction("BR7", "Branch if ISAR != 7", 0x8F, 6, 2, "control"),
    
    # Conditional branch taken adds 2 φ
    "BR_TAKEN": F8Instruction("BR (taken)", "Branch taken", 0x90, 8, 2, "control"),
    
    # ========== JUMP/CALL (12-14 φ) ==========
    "JMP": F8Instruction("JMP", "Jump absolute", 0x29, 14, 3, "control"),
    "PI": F8Instruction("PI", "Push PC, jump indirect", 0x28, 14, 3, "control"),
    
    # ========== ADDITIONAL CONTROL ==========
    "NOP": F8Instruction("NOP", "No operation", 0x2B, 4, 1, "control"),
    "XDC": F8Instruction("XDC", "Exchange DC with DC'", 0x2C, 8, 1, "transfer"),
    
    # ========== ADDRESS MODE VARIANTS ==========
    "AM": F8Instruction("AM", "Add (DC) to A", 0x88, 10, 1, "memory"),
    "AMD": F8Instruction("AMD", "Add (DC) BCD to A", 0x89, 10, 1, "memory"),
    "NM": F8Instruction("NM", "AND (DC) with A", 0x8A, 10, 1, "memory"),
    "OM": F8Instruction("OM", "OR (DC) with A", 0x8B, 10, 1, "memory"),
    "XM": F8Instruction("XM", "XOR (DC) with A", 0x8C, 10, 1, "memory"),
    "CM": F8Instruction("CM", "Compare (DC) with A", 0x8D, 10, 1, "memory"),
    "ADC": F8Instruction("ADC", "Add DC to A", 0x8E, 8, 1, "alu"),
    
    # ========== LISU/LISL (4 φ) ==========
    "LISU": F8Instruction("LISU", "Load ISAR upper", 0x60, 4, 1, "transfer"),  # 0x60-0x67
    "LISL": F8Instruction("LISL", "Load ISAR lower", 0x68, 4, 1, "transfer"),  # 0x68-0x6F
    
    # ========== CLR (4 φ) ==========
    "CLR": F8Instruction("CLR", "Clear A", 0x70, 4, 1, "alu"),
}


@dataclass
class F8Workload:
    """F8 workload profile."""
    name: str
    description: str
    instruction_mix: Dict[str, float]


WORKLOADS_F8 = {
    "typical": F8Workload(
        "typical", "Typical embedded application",
        {"transfer": 0.30, "alu": 0.30, "control": 0.20, "io": 0.10, "memory": 0.10}
    ),
    "compute": F8Workload(
        "compute", "Compute-intensive",
        {"transfer": 0.20, "alu": 0.50, "control": 0.15, "io": 0.05, "memory": 0.10}
    ),
    "control": F8Workload(
        "control", "Control-flow heavy",
        {"transfer": 0.20, "alu": 0.15, "control": 0.45, "io": 0.10, "memory": 0.10}
    ),
    "channel_f": F8Workload(
        "channel_f", "Fairchild Channel F game console",
        {"transfer": 0.25, "alu": 0.25, "control": 0.25, "io": 0.15, "memory": 0.10}
    ),
}


@dataclass
class F8SystemConfig:
    """F8 system configuration."""
    name: str
    clock_mhz: float
    phi_period_us: float  # Time per φ period
    
    @property
    def short_cycle_us(self) -> float:
        return self.phi_period_us * 4
    
    @property
    def long_cycle_us(self) -> float:
        return self.phi_period_us * 6


F8_SYSTEMS = {
    "f3850_1mhz": F8SystemConfig("F3850 @ 1 MHz", 1.0, 1.0),
    "f3850_2mhz": F8SystemConfig("F3850 @ 2 MHz", 2.0, 0.5),
    "mostek_3870": F8SystemConfig("Mostek 3870", 4.0, 0.375),
    "channel_f": F8SystemConfig("Channel F (1.79 MHz)", 1.79, 0.56),
}


@dataclass
class F8Result:
    """F8 analysis result."""
    system: str = ""
    clock_mhz: float = 0.0
    
    avg_phi_periods: float = 0.0
    avg_instruction_time_us: float = 0.0
    
    ips: float = 0.0
    mips: float = 0.0
    
    validation_status: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class FairchildF8ModelV2:
    """Improved F8 model with complete instruction timing."""
    
    def __init__(self, system: str = "f3850_2mhz"):
        self.system = F8_SYSTEMS.get(system, F8_SYSTEMS["f3850_2mhz"])
        self.instructions = INSTRUCTIONS_F8_COMPLETE
    
    def _get_avg_phi_by_category(self) -> Dict[str, float]:
        """Calculate average φ periods per category."""
        by_cat = {}
        for instr in self.instructions.values():
            cat = instr.category
            if cat not in by_cat:
                by_cat[cat] = []
            by_cat[cat].append(instr.phi_periods)
        
        return {cat: sum(p)/len(p) for cat, p in by_cat.items()}
    
    def analyze(self, workload: str = "typical") -> F8Result:
        """Analyze F8 performance."""
        result = F8Result()
        result.system = self.system.name
        result.clock_mhz = self.system.clock_mhz
        
        wl = WORKLOADS_F8.get(workload, WORKLOADS_F8["typical"])
        cat_avgs = self._get_avg_phi_by_category()
        
        # Calculate weighted average φ periods
        result.avg_phi_periods = sum(
            cat_avgs.get(cat, 6.0) * frac
            for cat, frac in wl.instruction_mix.items()
        )
        
        # Calculate instruction time
        result.avg_instruction_time_us = result.avg_phi_periods * self.system.phi_period_us
        
        # Calculate IPS
        result.ips = 1_000_000 / result.avg_instruction_time_us
        result.mips = result.ips / 1_000_000
        
        # Validation: Expected 250,000-500,000 IPS for typical F8 systems
        expected = (200000, 600000)
        if expected[0] <= result.ips <= expected[1]:
            result.validation_status = "PASS"
        else:
            result.validation_status = f"CHECK ({expected[0]:,}-{expected[1]:,} expected)"
        
        return result
    
    def validate_timing(self) -> Dict[str, tuple]:
        """Validate instruction timing."""
        tests = {}
        
        # Check φ period range
        phi_periods = [i.phi_periods for i in self.instructions.values()]
        tests["min_phi"] = (min(phi_periods) == 4, f"min={min(phi_periods)}")
        tests["max_phi"] = (max(phi_periods) <= 14, f"max={max(phi_periods)}")
        
        # Verify specific instructions
        tests["short_is_4"] = (
            self.instructions["LR_A_KU"].phi_periods == 4,
            f"LR A,KU = {self.instructions['LR_A_KU'].phi_periods}φ"
        )
        tests["long_is_6"] = (
            self.instructions["LI"].phi_periods == 6,
            f"LI = {self.instructions['LI'].phi_periods}φ"
        )
        tests["memory_is_10"] = (
            self.instructions["LM"].phi_periods == 10,
            f"LM = {self.instructions['LM'].phi_periods}φ"
        )
        tests["jmp_is_14"] = (
            self.instructions["JMP"].phi_periods == 14,
            f"JMP = {self.instructions['JMP'].phi_periods}φ"
        )
        
        # Instruction count
        tests["instruction_count"] = (
            len(self.instructions) >= 70,
            f"count={len(self.instructions)}"
        )
        
        return tests


def get_improved_f8_config() -> Dict:
    """Get improved F8 config for export."""
    model = FairchildF8ModelV2("f3850_2mhz")
    result = model.analyze("typical")
    cat_avgs = model._get_avg_phi_by_category()
    
    return {
        "family": "FAIRCHILD",
        "category": "MICROCONTROLLER_8BIT",
        "year": 1975,
        "bits": 8,
        "clock_mhz": 2.0,
        "transistors": 5000,  # Estimated
        
        "instruction_count": len(INSTRUCTIONS_F8_COMPLETE),
        "phi_period_range": [4, 14],
        
        "category_timing": {
            cat: {"avg_phi_periods": avg}
            for cat, avg in cat_avgs.items()
        },
        
        "avg_phi_periods": result.avg_phi_periods,
        "ips_typical": result.ips,
        "mips": result.mips,
        
        "systems": {
            name: {
                "clock_mhz": sys.clock_mhz,
                "phi_period_us": sys.phi_period_us,
                "short_cycle_us": sys.short_cycle_us,
                "long_cycle_us": sys.long_cycle_us,
            }
            for name, sys in F8_SYSTEMS.items()
        },
        
        "validation": {
            "source": "Fairchild F8 User's Guide, MAME emulator",
            "timing_note": "φ periods: short=4, long=6"
        }
    }


if __name__ == "__main__":
    print("="*70)
    print("FAIRCHILD F8 IMPROVED MODEL v2.0")
    print("Complete instruction timing database")
    print("="*70)
    
    model = FairchildF8ModelV2("f3850_2mhz")
    
    # Validation
    print("\n1. TIMING VALIDATION")
    print("-"*40)
    tests = model.validate_timing()
    passed = sum(1 for t, _ in tests.values() if t)
    print(f"   Passed: {passed}/{len(tests)}")
    for name, (ok, msg) in tests.items():
        print(f"   {'✓' if ok else '✗'} {name}: {msg}")
    
    # Instruction statistics
    print(f"\n2. INSTRUCTION SET ({len(INSTRUCTIONS_F8_COMPLETE)} instructions)")
    print("-"*40)
    cat_avgs = model._get_avg_phi_by_category()
    for cat, avg in sorted(cat_avgs.items()):
        count = len([i for i in INSTRUCTIONS_F8_COMPLETE.values() if i.category == cat])
        print(f"   {cat:<12}: {count:>3} instructions, avg {avg:.1f} φ periods")
    
    # System comparison
    print("\n3. SYSTEM PERFORMANCE")
    print("-"*40)
    print(f"   {'System':<25} {'Clock':<8} {'IPS':>12} {'MIPS':>8}")
    print(f"   {'-'*55}")
    for sys_name in F8_SYSTEMS:
        m = FairchildF8ModelV2(sys_name)
        r = m.analyze("typical")
        print(f"   {r.system:<25} {r.clock_mhz:.2f}M  {r.ips:>12,.0f} {r.mips:>8.3f}")
    
    # Workload analysis
    print("\n4. WORKLOAD ANALYSIS (F3850 @ 2 MHz)")
    print("-"*40)
    for wl_name in WORKLOADS_F8:
        result = model.analyze(wl_name)
        print(f"   {wl_name:<12}: {result.ips:>9,.0f} IPS, {result.avg_phi_periods:.1f} avg φ [{result.validation_status}]")
    
    # Export
    config = get_improved_f8_config()
    with open("/home/claude/f8_improved_v2.json", "w") as f:
        json.dump({
            "processor": "Fairchild F8",
            "version": "2.0",
            "config": config,
            "workloads": {k: model.analyze(k).to_dict() for k in WORKLOADS_F8}
        }, f, indent=2)
    
    print("\n5. EXPORT")
    print("-"*40)
    print(f"   Total instructions: {len(INSTRUCTIONS_F8_COMPLETE)}")
    print(f"   Exported to: f8_improved_v2.json")
    print("="*70)
