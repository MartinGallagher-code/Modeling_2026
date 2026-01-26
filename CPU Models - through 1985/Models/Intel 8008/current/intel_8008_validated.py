#!/usr/bin/env python3
"""
Intel 8008 Improved Performance Model

First 8-bit microprocessor (April 1972).
Architecture designed by CTC (Datapoint 2200).

Validation sources:
- Intel 8008 Datasheet
- CPU-World (corrected timing)
- Grokipedia
- willegal.net 8008 reference

Key characteristics:
- 8-bit data, 14-bit addresses (16 KB)
- Each T-state = 2 clock cycles (unlike 8080)
- Instructions: 5-11 T-states (10-22 clock cycles)
- 8008: 500 kHz, 8008-1: 800 kHz

Author: Grey-Box Performance Modeling Research
Date: January 25, 2026
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from enum import Enum
import json


@dataclass
class Instruction8008:
    """Intel 8008 instruction definition."""
    mnemonic: str
    description: str
    t_states: int        # Number of T-states (NOT clock cycles)
    bytes: int = 1
    category: str = "misc"
    
    @property
    def clock_cycles(self) -> int:
        # Each T-state = 2 clock cycles in the 8008
        return self.t_states * 2


# 8008 instruction set with T-state timing
# From datasheet and Grokipedia
INSTRUCTIONS_8008 = {
    # Register to Register - 5 T-states (1 machine cycle)
    "MOV_r_r": Instruction8008("MOV r,r", "Move register to register", 5, 1, "transfer"),
    
    # Register/Memory - 8 T-states for memory ops
    "MOV_r_M": Instruction8008("MOV r,M", "Load from memory", 8, 1, "memory"),
    "MOV_M_r": Instruction8008("MOV M,r", "Store to memory", 7, 1, "memory"),
    
    # Immediate - 8 T-states (2 bytes)
    "MVI_r": Instruction8008("MVI r", "Move immediate to register", 8, 2, "transfer"),
    "MVI_M": Instruction8008("MVI M", "Move immediate to memory", 9, 2, "memory"),
    
    # ALU Register - 5 T-states
    "ADD_r": Instruction8008("ADD r", "Add register", 5, 1, "alu"),
    "ADC_r": Instruction8008("ADC r", "Add with carry", 5, 1, "alu"),
    "SUB_r": Instruction8008("SUB r", "Subtract register", 5, 1, "alu"),
    "SBB_r": Instruction8008("SBB r", "Subtract with borrow", 5, 1, "alu"),
    "ANA_r": Instruction8008("ANA r", "AND register", 5, 1, "alu"),
    "XRA_r": Instruction8008("XRA r", "XOR register", 5, 1, "alu"),
    "ORA_r": Instruction8008("ORA r", "OR register", 5, 1, "alu"),
    "CMP_r": Instruction8008("CMP r", "Compare register", 5, 1, "alu"),
    
    # ALU Memory - 8 T-states
    "ADD_M": Instruction8008("ADD M", "Add memory", 8, 1, "alu"),
    "ADC_M": Instruction8008("ADC M", "Add memory with carry", 8, 1, "alu"),
    "SUB_M": Instruction8008("SUB M", "Subtract memory", 8, 1, "alu"),
    "SBB_M": Instruction8008("SBB M", "Subtract memory with borrow", 8, 1, "alu"),
    "ANA_M": Instruction8008("ANA M", "AND memory", 8, 1, "alu"),
    "XRA_M": Instruction8008("XRA M", "XOR memory", 8, 1, "alu"),
    "ORA_M": Instruction8008("ORA M", "OR memory", 8, 1, "alu"),
    "CMP_M": Instruction8008("CMP M", "Compare memory", 8, 1, "alu"),
    
    # ALU Immediate - 8 T-states
    "ADI": Instruction8008("ADI", "Add immediate", 8, 2, "alu"),
    "ACI": Instruction8008("ACI", "Add immediate with carry", 8, 2, "alu"),
    "SUI": Instruction8008("SUI", "Subtract immediate", 8, 2, "alu"),
    "SBI": Instruction8008("SBI", "Subtract immediate with borrow", 8, 2, "alu"),
    "ANI": Instruction8008("ANI", "AND immediate", 8, 2, "alu"),
    "XRI": Instruction8008("XRI", "XOR immediate", 8, 2, "alu"),
    "ORI": Instruction8008("ORI", "OR immediate", 8, 2, "alu"),
    "CPI": Instruction8008("CPI", "Compare immediate", 8, 2, "alu"),
    
    # Increment/Decrement - 5 T-states
    "INR_r": Instruction8008("INR r", "Increment register", 5, 1, "alu"),
    "DCR_r": Instruction8008("DCR r", "Decrement register", 5, 1, "alu"),
    
    # Rotate - 5 T-states
    "RLC": Instruction8008("RLC", "Rotate left", 5, 1, "alu"),
    "RRC": Instruction8008("RRC", "Rotate right", 5, 1, "alu"),
    "RAL": Instruction8008("RAL", "Rotate left through carry", 5, 1, "alu"),
    "RAR": Instruction8008("RAR", "Rotate right through carry", 5, 1, "alu"),
    
    # Jump - 11 T-states (3 bytes)
    "JMP": Instruction8008("JMP", "Jump unconditional", 11, 3, "control"),
    "JC": Instruction8008("JC", "Jump if carry", 11, 3, "control"),
    "JNC": Instruction8008("JNC", "Jump if no carry", 11, 3, "control"),
    "JZ": Instruction8008("JZ", "Jump if zero", 11, 3, "control"),
    "JNZ": Instruction8008("JNZ", "Jump if not zero", 11, 3, "control"),
    "JP": Instruction8008("JP", "Jump if positive", 11, 3, "control"),
    "JM": Instruction8008("JM", "Jump if minus", 11, 3, "control"),
    "JPE": Instruction8008("JPE", "Jump if parity even", 11, 3, "control"),
    "JPO": Instruction8008("JPO", "Jump if parity odd", 11, 3, "control"),
    
    # Call - 11 T-states (3 bytes)
    "CALL": Instruction8008("CALL", "Call subroutine", 11, 3, "control"),
    "CC": Instruction8008("CC", "Call if carry", 11, 3, "control"),
    "CNC": Instruction8008("CNC", "Call if no carry", 11, 3, "control"),
    "CZ": Instruction8008("CZ", "Call if zero", 11, 3, "control"),
    "CNZ": Instruction8008("CNZ", "Call if not zero", 11, 3, "control"),
    "CP": Instruction8008("CP", "Call if positive", 11, 3, "control"),
    "CM": Instruction8008("CM", "Call if minus", 11, 3, "control"),
    "CPE": Instruction8008("CPE", "Call if parity even", 11, 3, "control"),
    "CPO": Instruction8008("CPO", "Call if parity odd", 11, 3, "control"),
    
    # Return - 5 T-states (not taken) or 11 (taken)
    "RET": Instruction8008("RET", "Return", 5, 1, "control"),
    "RC": Instruction8008("RC", "Return if carry", 5, 1, "control"),  # 5 if not taken, 11 if taken
    "RNC": Instruction8008("RNC", "Return if no carry", 5, 1, "control"),
    "RZ": Instruction8008("RZ", "Return if zero", 5, 1, "control"),
    "RNZ": Instruction8008("RNZ", "Return if not zero", 5, 1, "control"),
    "RP": Instruction8008("RP", "Return if positive", 5, 1, "control"),
    "RM": Instruction8008("RM", "Return if minus", 5, 1, "control"),
    "RPE": Instruction8008("RPE", "Return if parity even", 5, 1, "control"),
    "RPO": Instruction8008("RPO", "Return if parity odd", 5, 1, "control"),
    
    # RST - 5 T-states
    "RST": Instruction8008("RST n", "Restart", 5, 1, "control"),
    
    # I/O - 8 T-states
    "IN": Instruction8008("IN", "Input", 8, 2, "io"),
    "OUT": Instruction8008("OUT", "Output", 6, 2, "io"),
    
    # Halt - 4 T-states
    "HLT": Instruction8008("HLT", "Halt", 4, 1, "control"),
}


@dataclass
class Intel8008Workload:
    """Workload profile for 8008."""
    name: str
    description: str
    avg_t_states: float = 7.0  # Average T-states per instruction


WORKLOADS_8008 = {
    "typical": Intel8008Workload("typical", "Typical program", 7.5),
    "compute": Intel8008Workload("compute", "Compute-heavy (register ops)", 6.0),
    "memory": Intel8008Workload("memory", "Memory-heavy", 8.5),
    "control": Intel8008Workload("control", "Control-heavy (jumps/calls)", 9.0),
    "basic": Intel8008Workload("basic", "BASIC interpreter (SCELBAL)", 7.8),
}


@dataclass
class Intel8008SystemConfig:
    """8008 system configuration."""
    name: str
    clock_khz: float
    t_state_us: float  # Microseconds per T-state


SYSTEMS_8008 = {
    "8008_500khz": Intel8008SystemConfig("Intel 8008 @ 500 kHz", 500, 4.0),
    "8008-1_800khz": Intel8008SystemConfig("Intel 8008-1 @ 800 kHz", 800, 2.5),
}


@dataclass
class Intel8008Result:
    """Result from 8008 model."""
    avg_t_states: float = 0.0
    avg_clock_cycles: float = 0.0
    cpi: float = 0.0       # Cycles per instruction (clock cycles)
    ipc: float = 0.0
    ips: float = 0.0
    mips: float = 0.0
    avg_instruction_time_us: float = 0.0
    validation_status: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class Intel8008Model:
    """
    Intel 8008 Performance Model
    
    Key timing note:
    - Each T-state = 2 clock cycles (unlike 8080 where T-state = 1 clock)
    - Instructions take 5-11 T-states = 10-22 clock cycles
    """
    
    # T-state to clock cycle ratio (unique to 8008)
    CLOCKS_PER_T_STATE = 2
    
    def __init__(self, system: str = "8008_500khz"):
        """Initialize 8008 model."""
        self.system = SYSTEMS_8008.get(system, SYSTEMS_8008["8008_500khz"])
        self.instructions = INSTRUCTIONS_8008
    
    def analyze(self, workload: str = "typical") -> Intel8008Result:
        """Analyze 8008 performance."""
        result = Intel8008Result()
        
        wl = WORKLOADS_8008.get(workload, WORKLOADS_8008["typical"])
        
        result.avg_t_states = wl.avg_t_states
        result.avg_clock_cycles = wl.avg_t_states * self.CLOCKS_PER_T_STATE
        result.cpi = result.avg_clock_cycles
        result.ipc = 1.0 / result.cpi
        
        # Time per instruction
        result.avg_instruction_time_us = wl.avg_t_states * self.system.t_state_us
        result.ips = 1_000_000 / result.avg_instruction_time_us
        result.mips = result.ips / 1_000_000
        
        # Validation against CPU-World corrected values
        if self.system.clock_khz == 500:
            expected_min, expected_max = 22500, 50000
        else:  # 800 kHz
            expected_min, expected_max = 36000, 80000
        
        if expected_min <= result.ips <= expected_max:
            result.validation_status = "PASS"
        else:
            result.validation_status = f"CHECK (expected {expected_min:,}-{expected_max:,})"
        
        return result
    
    def run_validation_suite(self) -> Dict[str, bool]:
        """Validate timing."""
        tests = {}
        
        t_states = [i.t_states for i in self.instructions.values()]
        
        tests["min_t_states_is_4_or_5"] = min(t_states) in [4, 5]
        tests["max_t_states_is_11"] = max(t_states) == 11
        tests["clocks_per_t_state_is_2"] = self.CLOCKS_PER_T_STATE == 2
        tests["total_instructions"] = len(self.instructions) >= 45
        
        return tests
    
    def print_result(self, result: Intel8008Result):
        """Print formatted result."""
        print(f"\n{'='*70}")
        print(f"  Intel 8008 Performance Analysis")
        print(f"  System: {self.system.name}")
        print(f"  T-state: {self.system.t_state_us} µs")
        print(f"{'='*70}")
        
        print(f"\n  ┌─ PERFORMANCE METRICS {'─'*44}┐")
        print(f"  │  IPS: {result.ips:,.0f}  |  MIPS: {result.mips:.4f}                  │")
        print(f"  │  Avg T-states: {result.avg_t_states:.1f}  |  Clock cycles: {result.avg_clock_cycles:.1f}       │")
        print(f"  │  Avg instruction time: {result.avg_instruction_time_us:.1f} µs                 │")
        print(f"  │  Validation: {result.validation_status:<45}   │")
        print(f"  └{'─'*66}┘")


def get_improved_8008_config() -> Dict:
    """Get improved 8008 configuration."""
    model = Intel8008Model("8008_500khz")
    result = model.analyze("typical")
    
    return {
        "family": "INTEL",
        "category": "SIMPLE_8BIT",
        "year": 1972,
        "bits": 8,
        "clock_mhz": 0.5,
        "transistors": 3500,
        "process_um": 10,
        "description": "First 8-bit microprocessor (CTC/Datapoint architecture)",
        
        "base_cpi": result.cpi,  # Clock cycles
        
        "has_prefetch": False,
        "has_cache": False,
        "pipeline_stages": 1,
        "branch_penalty": 6,  # Extra T-states for jumps
        
        "timings": {
            "alu": 10,      # 5 T-states × 2
            "mov": 10,      # 5 T-states × 2
            "branch": 22,   # 11 T-states × 2
            "memory": 16,   # 8 T-states × 2
        },
        
        # 8008 unique characteristics
        "clocks_per_t_state": 2,
        "min_t_states": 5,
        "max_t_states": 11,
        "address_bits": 14,
        "address_space_kb": 16,
        
        "ips_typical": result.ips,
        "mips": result.mips,
        
        "validation": {
            "source": "Intel 8008 Datasheet, CPU-World (corrected)",
            "note": "T-state = 2 clock cycles (unlike 8080)",
            "ips_range_500khz": "22,500-50,000",
            "ips_range_800khz": "36,000-80,000",
        }
    }


if __name__ == "__main__":
    print("="*70)
    print("INTEL 8008 IMPROVED PERFORMANCE MODEL")
    print("First 8-bit microprocessor (April 1972)")
    print("="*70)
    
    model = Intel8008Model("8008_500khz")
    
    # Validation
    print("\n1. TIMING VALIDATION")
    print("-"*40)
    validation = model.run_validation_suite()
    passed = sum(1 for v in validation.values() if v)
    print(f"   Passed: {passed}/{len(validation)} tests")
    
    # Instruction timing stats
    t_states = [i.t_states for i in INSTRUCTIONS_8008.values()]
    print(f"\n   T-state range: {min(t_states)}-{max(t_states)}")
    print(f"   Clock cycle range: {min(t_states)*2}-{max(t_states)*2}")
    print(f"   Total instructions: {len(INSTRUCTIONS_8008)}")
    
    # System comparison
    print("\n2. SYSTEM COMPARISON")
    print("-"*40)
    print(f"{'System':<25} {'Clock':>10} {'T-state':>10} {'IPS':>12} {'MIPS':>8}")
    print("-"*70)
    
    for sys_name, sys_config in SYSTEMS_8008.items():
        m = Intel8008Model(sys_name)
        r = m.analyze("typical")
        print(f"{sys_config.name:<25} {sys_config.clock_khz:>9.0f}kHz {sys_config.t_state_us:>9.1f}µs "
              f"{r.ips:>11,.0f} {r.mips:>8.4f}")
    
    # Comparison with 6502
    print("\n   Note: 6502 @ 1 MHz achieves ~300,000 IPS")
    print("   The 8008 is ~10× slower than 6502 for typical programs")
    
    # Workload analysis
    print("\n3. WORKLOAD ANALYSIS (8008 @ 500 kHz)")
    print("-"*40)
    for wl_name in WORKLOADS_8008:
        result = model.analyze(wl_name)
        print(f"   {wl_name:<12}: {result.ips:>10,.0f} IPS, {result.mips:.4f} MIPS")
    
    # Export
    config = get_improved_8008_config()
    with open("/home/claude/8008_validated_model.json", "w") as f:
        json.dump({
            "processor": "Intel 8008",
            "config": config,
            "workloads": {k: model.analyze(k).to_dict() for k in WORKLOADS_8008}
        }, f, indent=2)
    
    print("\n4. EXPORT")
    print("-"*40)
    print("   Exported to: 8008_validated_model.json")
    print(f"   base_cpi: {config['base_cpi']:.1f} clock cycles")
    print(f"   ips_typical: {config['ips_typical']:,.0f}")
    print("="*70)
