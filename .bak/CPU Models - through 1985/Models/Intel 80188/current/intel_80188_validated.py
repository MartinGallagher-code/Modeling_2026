#!/usr/bin/env python3
"""
Intel 80186/80188 Improved Performance Model

The 80186 is an enhanced 8086 with integrated peripherals.
The 80188 is identical but with 8-bit external data bus.

Validation sources:
- Intel 80186/80188 Datasheet
- Wikipedia Intel 80186
- Application Note AP-186

Key improvements over 8086:
- Faster address calculation (dedicated hardware)
- Much faster MUL/DIV (4-5× improvement)
- Faster multi-bit shifts (~4× improvement)
- 10 new instructions

Author: Grey-Box Performance Modeling Research
Date: January 25, 2026
"""

from dataclasses import dataclass, asdict
from typing import Dict
import json


@dataclass
class Intel80186Workload:
    """Workload profile for 80186/80188."""
    name: str
    description: str
    memory_fraction: float = 0.35    # Fraction of memory operations
    mul_div_fraction: float = 0.05   # Fraction of multiply/divide
    shift_fraction: float = 0.08     # Fraction of multi-bit shifts


WORKLOADS_80186 = {
    "typical": Intel80186Workload("typical", "Typical embedded application", 0.35, 0.05, 0.08),
    "compute": Intel80186Workload("compute", "Compute-intensive", 0.25, 0.12, 0.15),
    "memory": Intel80186Workload("memory", "Memory-intensive", 0.50, 0.03, 0.05),
    "control": Intel80186Workload("control", "Control-intensive", 0.30, 0.02, 0.04),
    "embedded": Intel80186Workload("embedded", "Embedded controller", 0.40, 0.04, 0.06),
}


@dataclass
class Intel80186Result:
    """Result from 80186/80188 model."""
    variant: str = "80186"
    clock_mhz: float = 8.0
    bus_width: int = 16
    
    # Performance
    avg_cpi: float = 0.0
    ipc: float = 0.0
    ips: float = 0.0
    mips: float = 0.0
    
    # Speedup vs 8086
    speedup_vs_8086: float = 0.0
    
    # Bus bandwidth
    bus_bandwidth_mb_s: float = 0.0
    
    validation_status: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class Intel80186Model:
    """
    Intel 80186/80188 Performance Model
    
    Key timing improvements over 8086:
    - Address calculation: Dedicated hardware (saves 4-8 cycles)
    - MUL 16-bit: 26-28 cycles (vs 118-133 on 8086) = ~4.5× faster
    - DIV 16-bit: 29 cycles (vs 144-162 on 8086) = ~5× faster
    - Multi-bit shifts: 5+n cycles (vs 8+4n on 8086) = ~4× faster
    """
    
    # 8086 baseline CPI for comparison
    BASELINE_8086_CPI = 12.0  # Typical 8086 CPI
    
    # 80186 improvement factors
    ADDRESS_CALC_SPEEDUP = 1.25  # ~25% faster addressing
    MUL_DIV_SPEEDUP = 4.5        # 4-5× faster
    SHIFT_SPEEDUP = 3.5          # ~4× faster
    
    def __init__(self, variant: str = "80186", clock_mhz: float = 8.0):
        """Initialize 80186/80188 model."""
        self.variant = variant
        self.clock_mhz = clock_mhz
        self.bus_width = 16 if variant == "80186" else 8
    
    def analyze(self, workload: str = "typical") -> Intel80186Result:
        """Analyze 80186/80188 performance."""
        result = Intel80186Result()
        result.variant = self.variant
        result.clock_mhz = self.clock_mhz
        result.bus_width = self.bus_width
        
        wl = WORKLOADS_80186.get(workload, WORKLOADS_80186["typical"])
        
        # Calculate effective CPI with improvements
        # Start with 8086 baseline
        base_cpi = self.BASELINE_8086_CPI
        
        # Apply speedup for address calculation (affects memory ops)
        cpi_after_addr = base_cpi / (1 + (self.ADDRESS_CALC_SPEEDUP - 1) * wl.memory_fraction)
        
        # Apply speedup for MUL/DIV
        cpi_after_muldiv = cpi_after_addr / (1 + (self.MUL_DIV_SPEEDUP - 1) * wl.mul_div_fraction)
        
        # Apply speedup for shifts
        cpi_after_shift = cpi_after_muldiv / (1 + (self.SHIFT_SPEEDUP - 1) * wl.shift_fraction)
        
        # 80188 penalty: 8-bit bus adds ~30-40% for memory operations
        if self.variant == "80188":
            bus_penalty = 1 + 0.35 * wl.memory_fraction
            result.avg_cpi = cpi_after_shift * bus_penalty
        else:
            result.avg_cpi = cpi_after_shift
        
        # Performance metrics
        result.ipc = 1.0 / result.avg_cpi
        result.ips = self.clock_mhz * 1_000_000 * result.ipc
        result.mips = result.ips / 1_000_000
        
        # Speedup vs 8086 at same clock
        result.speedup_vs_8086 = self.BASELINE_8086_CPI / result.avg_cpi
        
        # Bus bandwidth
        if self.variant == "80186":
            result.bus_bandwidth_mb_s = self.clock_mhz / 2  # 16-bit @ 2 cycles
        else:
            result.bus_bandwidth_mb_s = self.clock_mhz / 4  # 8-bit @ 4 cycles per word
        
        # Validation
        if self.variant == "80186":
            expected_mips_min = 0.8
            expected_mips_max = 1.5
        else:  # 80188
            expected_mips_min = 0.5
            expected_mips_max = 1.0
        
        if expected_mips_min <= result.mips <= expected_mips_max:
            result.validation_status = "PASS"
        else:
            result.validation_status = f"CHECK (expected {expected_mips_min}-{expected_mips_max})"
        
        return result
    
    def print_result(self, result: Intel80186Result):
        """Print formatted result."""
        print(f"\n{'='*70}")
        print(f"  Intel {result.variant} Performance Analysis")
        print(f"  Clock: {result.clock_mhz} MHz, Bus: {result.bus_width}-bit")
        print(f"{'='*70}")
        
        print(f"\n  ┌─ PERFORMANCE METRICS {'─'*44}┐")
        print(f"  │  IPS: {result.ips:,.0f}  |  MIPS: {result.mips:.2f}                    │")
        print(f"  │  Avg CPI: {result.avg_cpi:.2f}  |  IPC: {result.ipc:.3f}                       │")
        print(f"  │  Speedup vs 8086: {result.speedup_vs_8086:.2f}×                          │")
        print(f"  │  Bus bandwidth: {result.bus_bandwidth_mb_s:.1f} MB/sec                      │")
        print(f"  │  Validation: {result.validation_status:<45}   │")
        print(f"  └{'─'*66}┘")


def get_improved_80186_config() -> Dict:
    """Get improved 80186 configuration."""
    model = Intel80186Model("80186", 8.0)
    result = model.analyze("typical")
    
    return {
        "family": "INTEL",
        "category": "COMPLEX_16BIT",
        "year": 1982,
        "bits": 16,
        "clock_mhz": 8.0,
        "transistors": 55000,
        "process_um": 3,
        "description": "Enhanced 8086 with integrated peripherals",
        
        "base_cpi": result.avg_cpi,
        
        "has_prefetch": True,
        "prefetch_size": 6,
        "has_cache": False,
        "pipeline_stages": 2,
        "branch_penalty": 4,
        
        "timings": {
            "alu": 3,
            "mov": 2,
            "branch": 15,
            "memory": 4,
            "mul_16": 27,
            "div_16": 29,
        },
        
        # Integrated peripherals
        "integrated_clock": True,
        "dma_channels": 2,
        "timers": 3,
        "interrupt_controller": True,
        
        "ips_typical": result.ips,
        "mips": result.mips,
        "bus_bandwidth_mb_s": result.bus_bandwidth_mb_s,
        
        "validation": {
            "source": "Intel 80186 Datasheet, AP-186",
            "speedup_vs_8086": f"{result.speedup_vs_8086:.2f}×",
        }
    }


def get_improved_80188_config() -> Dict:
    """Get improved 80188 configuration."""
    model = Intel80186Model("80188", 8.0)
    result = model.analyze("typical")
    
    return {
        "family": "INTEL",
        "category": "COMPLEX_16BIT",
        "year": 1982,
        "bits": 16,  # Internal
        "external_bus": 8,  # External
        "clock_mhz": 8.0,
        "transistors": 55000,
        "process_um": 3,
        "description": "80186 with 8-bit external bus",
        
        "base_cpi": result.avg_cpi,
        
        "has_prefetch": True,
        "prefetch_size": 4,
        "has_cache": False,
        "pipeline_stages": 2,
        "branch_penalty": 4,
        
        "timings": {
            "alu": 3,
            "mov": 2,
            "branch": 15,
            "memory": 8,  # Extra cycle for 8-bit bus
            "mul_16": 27,
            "div_16": 29,
        },
        
        # Same integrated peripherals as 80186
        "integrated_clock": True,
        "dma_channels": 2,
        "timers": 3,
        "interrupt_controller": True,
        
        "ips_typical": result.ips,
        "mips": result.mips,
        "bus_bandwidth_mb_s": result.bus_bandwidth_mb_s,
        
        "validation": {
            "source": "Intel 80188 Datasheet",
            "note": "~30-40% slower than 80186 for memory-heavy code",
        }
    }


if __name__ == "__main__":
    print("="*70)
    print("INTEL 80186/80188 IMPROVED PERFORMANCE MODEL")
    print("Enhanced 8086 with integrated peripherals (1982)")
    print("="*70)
    
    # New instructions
    print("\n1. NEW INSTRUCTIONS (10)")
    print("-"*40)
    new_instructions = [
        "ENTER", "LEAVE",     # Stack frame
        "PUSHA", "POPA",      # Push/pop all
        "BOUND",              # Array bounds check
        "INS", "OUTS",        # String I/O
        "PUSH imm",           # Push immediate
        "IMUL imm",           # Multiply immediate
        "SHL/SHR/etc imm",    # Immediate shifts
    ]
    for instr in new_instructions:
        print(f"   • {instr}")
    
    # Timing improvements
    print("\n2. TIMING IMPROVEMENTS vs 8086")
    print("-"*40)
    print(f"   {'Operation':<25} {'8086':>10} {'80186':>10} {'Speedup':>10}")
    print(f"   {'-'*55}")
    print(f"   {'MUL 16-bit':<25} {'118-133':>10} {'26-28':>10} {'~4.5×':>10}")
    print(f"   {'DIV 16-bit':<25} {'144-162':>10} {'29':>10} {'~5×':>10}")
    print(f"   {'Shift by n':<25} {'8+4n':>10} {'5+n':>10} {'~4×':>10}")
    print(f"   {'Address calc':<25} {'EA cycles':>10} {'dedicated':>10} {'~25%':>10}")
    
    # Variant comparison
    print("\n3. 80186 vs 80188 COMPARISON")
    print("-"*40)
    
    configs = [
        ("80186", 6.0),
        ("80186", 8.0),
        ("80186", 10.0),
        ("80188", 6.0),
        ("80188", 8.0),
        ("80188", 10.0),
    ]
    
    print(f"{'Variant':<10} {'Clock':>8} {'MIPS':>8} {'Bus BW':>10} {'vs 8086':>10}")
    print("-"*50)
    
    for variant, clock in configs:
        m = Intel80186Model(variant, clock)
        r = m.analyze("typical")
        print(f"{variant:<10} {clock:>7.0f}M {r.mips:>8.2f} {r.bus_bandwidth_mb_s:>9.1f}MB {r.speedup_vs_8086:>9.2f}×")
    
    # Workload analysis
    print("\n4. WORKLOAD ANALYSIS (80186 @ 8 MHz)")
    print("-"*40)
    model = Intel80186Model("80186", 8.0)
    for wl_name in WORKLOADS_80186:
        result = model.analyze(wl_name)
        print(f"   {wl_name:<12}: {result.mips:.2f} MIPS, {result.speedup_vs_8086:.2f}× vs 8086")
    
    # Export both configs
    config_80186 = get_improved_80186_config()
    config_80188 = get_improved_80188_config()
    
    with open("/home/claude/80186_validated_model.json", "w") as f:
        json.dump({
            "processor": "Intel 80186",
            "config": config_80186,
            "workloads": {k: Intel80186Model("80186", 8.0).analyze(k).to_dict() 
                         for k in WORKLOADS_80186}
        }, f, indent=2)
    
    with open("/home/claude/80188_validated_model.json", "w") as f:
        json.dump({
            "processor": "Intel 80188",
            "config": config_80188,
            "workloads": {k: Intel80186Model("80188", 8.0).analyze(k).to_dict() 
                         for k in WORKLOADS_80186}
        }, f, indent=2)
    
    print("\n5. EXPORT")
    print("-"*40)
    print("   Exported: 80186_validated_model.json")
    print("   Exported: 80188_validated_model.json")
    print(f"   80186 @ 8 MHz: {config_80186['mips']:.2f} MIPS")
    print(f"   80188 @ 8 MHz: {config_80188['mips']:.2f} MIPS")
    print("="*70)
