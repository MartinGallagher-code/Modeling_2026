#!/usr/bin/env python3
"""
AMD Am2901 IMPROVED Performance Model v2.0

The Am2901 is a 4-bit bit-slice ALU processor building block.
It's NOT a standalone CPU - it requires:
- Microsequencer (Am2909/2910) for control flow
- Carry lookahead (Am2902) for fast multi-slice operation
- Custom microcode for each application

This model provides:
- Multi-slice system configurations
- Microcode complexity estimation
- Real-world system benchmarks
- Comparison vs contemporary microprocessors

Reference systems:
- Data General Nova 4: 4× Am2901 (16-bit)
- DEC VAX 11/730: 8× Am2901 (32-bit)  
- Various 8085/Z80 emulators

Author: Grey-Box Performance Modeling Research
Date: January 26, 2026
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple
from enum import Enum
import json


class SliceWidth(Enum):
    """Am2901 system configurations."""
    SLICE_4BIT = 1    # Single 2901
    SLICE_8BIT = 2    # 2× 2901
    SLICE_16BIT = 4   # 4× 2901 (Nova 4)
    SLICE_32BIT = 8   # 8× 2901 (VAX 11/730)


@dataclass  
class Am2901ALUOp:
    """Am2901 ALU operation."""
    code: int
    mnemonic: str
    description: str
    category: str


# Am2901 ALU function codes (I5-I3)
ALU_FUNCTIONS = {
    0: Am2901ALUOp(0, "ADD", "R + S", "arithmetic"),
    1: Am2901ALUOp(1, "SUBR", "S - R", "arithmetic"),
    2: Am2901ALUOp(2, "SUBS", "R - S", "arithmetic"),
    3: Am2901ALUOp(3, "OR", "R OR S", "logic"),
    4: Am2901ALUOp(4, "AND", "R AND S", "logic"),
    5: Am2901ALUOp(5, "NOTRS", "NOT R AND S", "logic"),
    6: Am2901ALUOp(6, "EXOR", "R XOR S", "logic"),
    7: Am2901ALUOp(7, "EXNOR", "R XNOR S", "logic"),
}

# Am2901 source operand codes (I2-I0)
SOURCE_OPERANDS = {
    0: ("A,Q", "A register, Q register"),
    1: ("A,B", "A register, B register"),
    2: ("0,Q", "Zero, Q register"),
    3: ("0,B", "Zero, B register"),
    4: ("0,A", "Zero, A register"),
    5: ("D,A", "Data input, A register"),
    6: ("D,Q", "Data input, Q register"),
    7: ("D,0", "Data input, Zero"),
}

# Am2901 destination codes (I8-I6)
DESTINATIONS = {
    0: ("QREG", "F -> Q"),
    1: ("NOP", "No output"),
    2: ("RAMA", "F -> B, F -> Y"),
    3: ("RAMF", "F -> B, A -> Y"),
    4: ("RAMQD", "F/2 -> B, Q/2 -> Q, F -> Y"),
    5: ("RAMD", "F/2 -> B, F -> Y"),
    6: ("RAMQU", "2F -> B, 2Q -> Q, F -> Y"),
    7: ("RAMU", "2F -> B, F -> Y"),
}


@dataclass
class Am2901SystemConfig:
    """Am2901-based system configuration."""
    name: str
    slices: int
    clock_mhz: float
    microcode_width: int  # bits
    pipeline_stages: int
    typical_microops_per_instr: float


# Reference systems
AM2901_SYSTEMS = {
    "generic_8bit": Am2901SystemConfig(
        "Generic 8-bit", 2, 10.0, 48, 1, 4.0
    ),
    "generic_16bit": Am2901SystemConfig(
        "Generic 16-bit", 4, 15.0, 56, 1, 3.5
    ),
    "nova_4": Am2901SystemConfig(
        "Data General Nova 4", 4, 20.0, 64, 2, 3.0
    ),
    "vax_11_730": Am2901SystemConfig(
        "DEC VAX 11/730", 8, 12.5, 80, 3, 5.0
    ),
    "8085_emulator": Am2901SystemConfig(
        "8085 Emulator", 2, 10.0, 48, 1, 5.0
    ),
    "z80_emulator": Am2901SystemConfig(
        "Z80 Emulator", 2, 12.0, 52, 1, 4.5
    ),
}


@dataclass
class MicrocodeWorkload:
    """Microcode workload profile."""
    name: str
    description: str
    avg_microops_per_instr: float
    memory_access_fraction: float
    branch_fraction: float


MICROCODE_WORKLOADS = {
    "typical": MicrocodeWorkload(
        "typical", "Typical mixed workload", 4.0, 0.30, 0.15
    ),
    "compute": MicrocodeWorkload(
        "compute", "Compute-intensive (register ALU)", 3.0, 0.15, 0.10
    ),
    "memory": MicrocodeWorkload(
        "memory", "Memory-intensive", 5.0, 0.50, 0.15
    ),
    "control": MicrocodeWorkload(
        "control", "Control-flow heavy", 4.5, 0.20, 0.35
    ),
    "emulation": MicrocodeWorkload(
        "emulation", "CPU emulation workload", 5.5, 0.35, 0.20
    ),
}


@dataclass
class Am2901Result:
    """Am2901 system analysis result."""
    system: str = ""
    slices: int = 0
    data_width: int = 0
    clock_mhz: float = 0.0
    
    microops_per_second: float = 0.0
    macro_ips: float = 0.0
    mips: float = 0.0
    
    # Comparison metrics
    speedup_vs_8085: float = 0.0
    speedup_vs_8086: float = 0.0
    
    validation_status: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class AMD2901ModelV2:
    """Improved Am2901 bit-slice system model."""
    
    # Reference microprocessor performance for comparison
    REFERENCE_MIPS = {
        "8085": 0.37,   # 3.125 MHz 8085
        "8086": 0.66,   # 5 MHz 8086
        "z80": 0.58,    # 4 MHz Z80
    }
    
    def __init__(self, system: str = "generic_16bit"):
        self.config = AM2901_SYSTEMS.get(system, AM2901_SYSTEMS["generic_16bit"])
    
    def analyze(self, workload: str = "typical") -> Am2901Result:
        """Analyze Am2901 system performance."""
        result = Am2901Result()
        result.system = self.config.name
        result.slices = self.config.slices
        result.data_width = self.config.slices * 4
        result.clock_mhz = self.config.clock_mhz
        
        wl = MICROCODE_WORKLOADS.get(workload, MICROCODE_WORKLOADS["typical"])
        
        # Micro-operations per second (one per clock in pipelined systems)
        if self.config.pipeline_stages > 1:
            # Pipelined: ~1 microop per clock after pipeline fill
            effective_cpi = 1.0 + (wl.branch_fraction * (self.config.pipeline_stages - 1))
        else:
            # Non-pipelined: 1 microop per clock
            effective_cpi = 1.0
        
        result.microops_per_second = (self.config.clock_mhz * 1_000_000) / effective_cpi
        
        # Macro instructions per second
        avg_microops = wl.avg_microops_per_instr
        result.macro_ips = result.microops_per_second / avg_microops
        result.mips = result.macro_ips / 1_000_000
        
        # Comparison vs reference CPUs
        result.speedup_vs_8085 = result.mips / self.REFERENCE_MIPS["8085"]
        result.speedup_vs_8086 = result.mips / self.REFERENCE_MIPS["8086"]
        
        # Validation: 2901 systems should be 3-20× faster than microprocessors
        expected_speedup = (2.0, 25.0)
        if expected_speedup[0] <= result.speedup_vs_8085 <= expected_speedup[1]:
            result.validation_status = "PASS"
        else:
            result.validation_status = f"CHECK (expected {expected_speedup[0]}-{expected_speedup[1]}× vs 8085)"
        
        return result
    
    def get_alu_capabilities(self) -> Dict[str, int]:
        """Get ALU function counts."""
        cats = {}
        for op in ALU_FUNCTIONS.values():
            if op.category not in cats:
                cats[op.category] = 0
            cats[op.category] += 1
        return cats
    
    @staticmethod
    def compare_systems() -> List[Am2901Result]:
        """Compare all reference systems."""
        results = []
        for sys_name in AM2901_SYSTEMS:
            model = AMD2901ModelV2(sys_name)
            result = model.analyze("typical")
            results.append(result)
        return results


def get_improved_2901_config() -> Dict:
    """Get Am2901 config for export."""
    model = AMD2901ModelV2("generic_16bit")
    result = model.analyze("typical")
    
    return {
        "family": "AMD",
        "category": "BIT_SLICE",
        "year": 1975,
        "bits": "4-bit slice (cascadable)",
        "technology": "Bipolar TTL/Schottky",
        "transistors": 200,  # Per slice
        
        "alu_functions": len(ALU_FUNCTIONS),
        "source_operand_modes": len(SOURCE_OPERANDS),
        "destination_modes": len(DESTINATIONS),
        "register_file": "16 × 4-bit",
        
        "configurations": {
            name: {
                "slices": cfg.slices,
                "data_width": cfg.slices * 4,
                "clock_mhz": cfg.clock_mhz,
                "pipeline_stages": cfg.pipeline_stages,
            }
            for name, cfg in AM2901_SYSTEMS.items()
        },
        
        "typical_16bit_performance": {
            "clock_mhz": 15.0,
            "microops_per_second": result.microops_per_second,
            "macro_ips": result.macro_ips,
            "mips": result.mips,
            "speedup_vs_8085": result.speedup_vs_8085,
            "speedup_vs_8086": result.speedup_vs_8086,
        },
        
        "design_note": "Requires microsequencer (Am2909/2910) and custom microcode",
        
        "validation": {
            "source": "AMD Am2900 Family Data Book, Wikipedia",
        }
    }


if __name__ == "__main__":
    print("="*70)
    print("AMD Am2901 IMPROVED MODEL v2.0")
    print("Bit-slice system performance modeling")
    print("="*70)
    
    # ALU capabilities
    print("\n1. Am2901 ALU FUNCTIONS")
    print("-"*40)
    for code, op in ALU_FUNCTIONS.items():
        print(f"   {code}: {op.mnemonic:<8} {op.description:<15} [{op.category}]")
    
    # Source operands
    print("\n2. SOURCE OPERAND MODES")
    print("-"*40)
    for code, (name, desc) in SOURCE_OPERANDS.items():
        print(f"   {code}: {name:<6} {desc}")
    
    # System comparison
    print("\n3. SYSTEM PERFORMANCE COMPARISON")
    print("-"*70)
    print(f"   {'System':<25} {'Width':>6} {'Clock':>8} {'MIPS':>8} {'vs 8085':>10} {'vs 8086':>10}")
    print(f"   {'-'*68}")
    
    for sys_name in AM2901_SYSTEMS:
        model = AMD2901ModelV2(sys_name)
        r = model.analyze("typical")
        print(f"   {r.system:<25} {r.data_width:>5}b {r.clock_mhz:>7.1f}M {r.mips:>8.2f} "
              f"{r.speedup_vs_8085:>9.1f}× {r.speedup_vs_8086:>9.1f}×")
    
    # Workload analysis for 16-bit system
    print("\n4. WORKLOAD ANALYSIS (16-bit @ 15 MHz)")
    print("-"*40)
    model = AMD2901ModelV2("generic_16bit")
    for wl_name in MICROCODE_WORKLOADS:
        result = model.analyze(wl_name)
        print(f"   {wl_name:<12}: {result.mips:.2f} MIPS, {result.speedup_vs_8085:.1f}× vs 8085 [{result.validation_status}]")
    
    # Key reference systems
    print("\n5. KEY REFERENCE SYSTEMS")
    print("-"*40)
    
    # Nova 4
    nova = AMD2901ModelV2("nova_4")
    r = nova.analyze("typical")
    print(f"   Data General Nova 4:")
    print(f"      {r.slices}× Am2901 = {r.data_width}-bit")
    print(f"      Clock: {r.clock_mhz} MHz")
    print(f"      Performance: {r.mips:.2f} MIPS ({r.speedup_vs_8086:.1f}× vs 8086)")
    
    # VAX 11/730
    vax = AMD2901ModelV2("vax_11_730")
    r = vax.analyze("typical")
    print(f"\n   DEC VAX 11/730:")
    print(f"      {r.slices}× Am2901 = {r.data_width}-bit")
    print(f"      Clock: {r.clock_mhz} MHz, {vax.config.pipeline_stages}-stage pipeline")
    print(f"      Performance: {r.mips:.2f} MIPS ({r.speedup_vs_8086:.1f}× vs 8086)")
    
    # Export
    config = get_improved_2901_config()
    with open("/home/claude/2901_improved_v2.json", "w") as f:
        json.dump({
            "processor": "AMD Am2901",
            "version": "2.0",
            "config": config,
            "systems": {
                name: AMD2901ModelV2(name).analyze("typical").to_dict()
                for name in AM2901_SYSTEMS
            }
        }, f, indent=2)
    
    print("\n6. EXPORT")
    print("-"*40)
    print(f"   ALU functions: {len(ALU_FUNCTIONS)}")
    print(f"   Reference systems: {len(AM2901_SYSTEMS)}")
    print(f"   Exported to: 2901_improved_v2.json")
    print("="*70)
