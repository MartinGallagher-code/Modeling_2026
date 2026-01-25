#!/usr/bin/env python3
"""
Intel 8086 CPI Stack Model (1978)

COMPLEMENTARY APPROACH TO QUEUEING THEORY

This model decomposes CPI (Cycles Per Instruction) into additive penalty
components, answering: "WHERE do the cycles go?"

While the queueing model (ibm_pc_8086_model.py) answers "What's the bottleneck?",
this CPI Stack model answers "What penalties are costing cycles?"

USE BOTH TOGETHER FOR COMPLETE INSIGHT:
- Queueing Model: Identifies resource saturation (BIU vs EU)
- CPI Stack Model: Identifies penalty sources (branches, EA calc, etc.)

Author: Grey-Box Performance Modeling Research
Date: January 25, 2026
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional


# =============================================================================
# WORKLOAD DEFINITION
# =============================================================================

@dataclass
class Workload:
    """Workload characteristics for CPI Stack analysis."""
    name: str = "default"
    
    # Instruction mix (must sum to 1.0)
    mix_alu: float = 0.35
    mix_mov_reg: float = 0.15
    mix_mov_mem: float = 0.20
    mix_branch: float = 0.15
    mix_mul_div: float = 0.05
    mix_string: float = 0.05
    mix_other: float = 0.05
    
    # Memory access patterns
    mem_operand_rate: float = 0.40
    avg_operand_size: float = 1.5
    
    # Effective address complexity
    ea_direct_rate: float = 0.30
    ea_register_rate: float = 0.25
    ea_base_disp_rate: float = 0.30
    ea_base_index_rate: float = 0.15
    
    # Branch behavior
    branch_taken_rate: float = 0.60
    
    # Code characteristics
    avg_instruction_bytes: float = 3.2
    
    def validate(self):
        total = (self.mix_alu + self.mix_mov_reg + self.mix_mov_mem + 
                 self.mix_branch + self.mix_mul_div + self.mix_string + 
                 self.mix_other)
        assert abs(total - 1.0) < 0.01, f"Mix sums to {total}, not 1.0"


# Predefined workloads
WORKLOADS = {
    "dos_typical": Workload(
        name="dos_typical",
        mix_alu=0.32, mix_mov_reg=0.18, mix_mov_mem=0.22,
        mix_branch=0.15, mix_mul_div=0.03, mix_string=0.05, mix_other=0.05,
        mem_operand_rate=0.40, branch_taken_rate=0.60
    ),
    "integer_compute": Workload(
        name="integer_compute",
        mix_alu=0.50, mix_mov_reg=0.20, mix_mov_mem=0.10,
        mix_branch=0.10, mix_mul_div=0.05, mix_string=0.02, mix_other=0.03,
        mem_operand_rate=0.25, branch_taken_rate=0.50
    ),
    "memory_intensive": Workload(
        name="memory_intensive",
        mix_alu=0.20, mix_mov_reg=0.10, mix_mov_mem=0.40,
        mix_branch=0.10, mix_mul_div=0.02, mix_string=0.10, mix_other=0.08,
        mem_operand_rate=0.60, branch_taken_rate=0.55
    ),
    "control_heavy": Workload(
        name="control_heavy",
        mix_alu=0.30, mix_mov_reg=0.15, mix_mov_mem=0.15,
        mix_branch=0.30, mix_mul_div=0.02, mix_string=0.03, mix_other=0.05,
        mem_operand_rate=0.30, branch_taken_rate=0.65
    ),
}


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass
class Intel8086Config:
    """8086 architectural parameters from Intel datasheets."""
    clock_mhz: float = 5.0
    bus_width_bits: int = 16
    memory_wait_states: int = 0
    prefetch_queue_bytes: int = 6
    prefetch_rate_bytes_per_4clocks: int = 2
    
    # Base instruction timings (cycles)
    timing_alu_reg_reg: int = 3
    timing_alu_reg_imm: int = 4
    timing_alu_mem_reg: int = 9
    timing_mov_reg_reg: int = 2
    timing_mov_reg_mem: int = 8
    timing_mov_mem_reg: int = 9
    timing_jmp_near: int = 15
    timing_jcc_taken: int = 16
    timing_jcc_not_taken: int = 4
    timing_call_near: int = 19
    timing_ret: int = 8
    timing_mul_16: int = 118
    timing_div_16: int = 165
    timing_movs: int = 18
    timing_push: int = 11
    timing_pop: int = 8
    
    # EA calculation times
    ea_direct: int = 6
    ea_register: int = 5
    ea_base_disp: int = 9
    ea_base_index: int = 11
    ea_base_index_disp: int = 12
    
    # Branch penalties
    branch_flush_penalty: int = 4


# =============================================================================
# CPI STACK RESULT
# =============================================================================

@dataclass
class CPIStackResult:
    """Complete CPI breakdown - the key output."""
    cpi_base: float = 0.0
    cpi_prefetch: float = 0.0
    cpi_bus: float = 0.0
    cpi_branch: float = 0.0
    cpi_memory: float = 0.0
    cpi_ea: float = 0.0
    
    cpi_total: float = 0.0
    ipc: float = 0.0
    mips: float = 0.0
    
    bottleneck: str = ""
    component_percentages: Dict[str, float] = field(default_factory=dict)
    
    def compute_totals(self, clock_mhz: float):
        self.cpi_total = (self.cpi_base + self.cpi_prefetch + self.cpi_bus +
                         self.cpi_branch + self.cpi_memory + self.cpi_ea)
        self.ipc = 1.0 / self.cpi_total if self.cpi_total > 0 else 0
        self.mips = (clock_mhz * self.ipc) if self.ipc > 0 else 0
        
        if self.cpi_total > 0:
            self.component_percentages = {
                'base': 100 * self.cpi_base / self.cpi_total,
                'prefetch': 100 * self.cpi_prefetch / self.cpi_total,
                'bus': 100 * self.cpi_bus / self.cpi_total,
                'branch': 100 * self.cpi_branch / self.cpi_total,
                'memory': 100 * self.cpi_memory / self.cpi_total,
                'ea_calc': 100 * self.cpi_ea / self.cpi_total,
            }
            penalties = {k: v for k, v in self.component_percentages.items() 
                        if k != 'base'}
            self.bottleneck = max(penalties, key=penalties.get)


# =============================================================================
# CPI STACK MODEL
# =============================================================================

class Intel8086CPIStackModel:
    """
    CPI Stack Model for Intel 8086.
    
    Decomposes CPI into: base + prefetch + bus + branch + memory + EA
    """
    
    def __init__(self, config: Intel8086Config = None):
        self.config = config or Intel8086Config()
    
    def _calc_cpi_base(self, workload: Workload) -> float:
        """Base CPI from instruction mix."""
        cfg = self.config
        cpi = 0.0
        
        cpi += workload.mix_alu * (0.6 * cfg.timing_alu_reg_reg + 
                                    0.4 * cfg.timing_alu_reg_imm)
        cpi += workload.mix_mov_reg * cfg.timing_mov_reg_reg
        cpi += workload.mix_mov_mem * (0.5 * cfg.timing_mov_reg_mem +
                                        0.5 * cfg.timing_mov_mem_reg)
        
        branch_cpi = (workload.branch_taken_rate * cfg.timing_jcc_taken +
                      (1 - workload.branch_taken_rate) * cfg.timing_jcc_not_taken)
        cpi += workload.mix_branch * branch_cpi
        
        cpi += workload.mix_mul_div * (0.8 * (cfg.timing_mul_16 * 0.7) +
                                        0.2 * (cfg.timing_div_16 * 0.7))
        cpi += workload.mix_string * cfg.timing_movs
        cpi += workload.mix_other * ((cfg.timing_push + cfg.timing_pop) / 2)
        
        return cpi
    
    def _calc_cpi_prefetch(self, workload: Workload, base_cpi: float) -> float:
        """Prefetch stall penalty."""
        cfg = self.config
        consumption_rate = workload.avg_instruction_bytes / base_cpi
        supply_rate = cfg.prefetch_rate_bytes_per_4clocks / 4.0
        
        if consumption_rate > supply_rate:
            deficit = consumption_rate - supply_rate
            stall_fraction = deficit / consumption_rate
            return base_cpi * stall_fraction * 0.5
        return 0.0
    
    def _calc_cpi_bus(self, workload: Workload) -> float:
        """Bus contention penalty."""
        mem_accesses = workload.mem_operand_rate * workload.avg_operand_size / 2
        bus_cycles = mem_accesses * 4
        return bus_cycles * 0.2
    
    def _calc_cpi_branch(self, workload: Workload) -> float:
        """Branch penalty (queue flush)."""
        cfg = self.config
        taken = workload.mix_branch * workload.branch_taken_rate
        return taken * cfg.branch_flush_penalty
    
    def _calc_cpi_memory(self, workload: Workload) -> float:
        """Memory wait state penalty."""
        cfg = self.config
        if cfg.memory_wait_states > 0:
            accesses = workload.mem_operand_rate * workload.avg_operand_size / 2
            return accesses * cfg.memory_wait_states * 4
        return 0.0
    
    def _calc_cpi_ea(self, workload: Workload) -> float:
        """EA calculation overhead."""
        cfg = self.config
        ea_instructions = workload.mix_mov_mem + workload.mix_alu * workload.mem_operand_rate
        
        avg_ea = (workload.ea_direct_rate * cfg.ea_direct +
                  workload.ea_register_rate * cfg.ea_register +
                  workload.ea_base_disp_rate * cfg.ea_base_disp +
                  workload.ea_base_index_rate * cfg.ea_base_index_disp)
        
        ea_overhead = avg_ea - cfg.ea_register
        return ea_instructions * ea_overhead * 0.5
    
    def predict(self, workload: Workload) -> CPIStackResult:
        """Main prediction - returns full CPI breakdown."""
        workload.validate()
        
        result = CPIStackResult()
        result.cpi_base = self._calc_cpi_base(workload)
        result.cpi_prefetch = self._calc_cpi_prefetch(workload, result.cpi_base)
        result.cpi_bus = self._calc_cpi_bus(workload)
        result.cpi_branch = self._calc_cpi_branch(workload)
        result.cpi_memory = self._calc_cpi_memory(workload)
        result.cpi_ea = self._calc_cpi_ea(workload)
        
        result.compute_totals(self.config.clock_mhz)
        return result
    
    def compare_workloads(self, workloads: List[Workload]) -> Dict[str, CPIStackResult]:
        """Compare multiple workloads."""
        return {w.name: self.predict(w) for w in workloads}
    
    def what_if(self, workload: Workload, param: str, 
                values: List[float]) -> List[Tuple[float, CPIStackResult]]:
        """What-if analysis on a parameter."""
        results = []
        for v in values:
            w = Workload(**{**workload.__dict__, param: v})
            try:
                w.validate()
                results.append((v, self.predict(w)))
            except:
                pass
        return results


# =============================================================================
# OUTPUT FORMATTING
# =============================================================================

def print_cpi_breakdown(result: CPIStackResult, name: str = ""):
    """Print visual CPI breakdown."""
    print(f"\n{'='*60}")
    print(f"CPI STACK: {name}" if name else "CPI STACK BREAKDOWN")
    print(f"{'='*60}")
    
    components = [
        ('Base (ideal)', 'base', result.cpi_base),
        ('Prefetch stalls', 'prefetch', result.cpi_prefetch),
        ('Bus contention', 'bus', result.cpi_bus),
        ('Branch penalty', 'branch', result.cpi_branch),
        ('Memory delay', 'memory', result.cpi_memory),
        ('EA calculation', 'ea_calc', result.cpi_ea),
    ]
    
    print(f"\n{'Component':<18} {'CPI':>7} {'%':>6}  Bar")
    print("-" * 60)
    
    max_pct = max(result.component_percentages.values())
    for label, key, cpi in components:
        pct = result.component_percentages.get(key, 0)
        bar = '█' * int(40 * pct / max_pct) if max_pct > 0 else ''
        marker = " ←" if key == result.bottleneck and key != 'base' else ""
        print(f"{label:<18} {cpi:>7.2f} {pct:>5.1f}%  {bar}{marker}")
    
    print("-" * 60)
    print(f"{'TOTAL':<18} {result.cpi_total:>7.2f} {'100.0':>5}%")
    print(f"\nIPC: {result.ipc:.4f}  |  MIPS: {result.mips:.3f}  |  Penalty: {result.bottleneck}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "="*60)
    print("INTEL 8086 CPI STACK MODEL")
    print("Complementary to queueing model (ibm_pc_8086_model.py)")
    print("="*60)
    
    model = Intel8086CPIStackModel()
    
    # Single workload
    result = model.predict(WORKLOADS["dos_typical"])
    print_cpi_breakdown(result, "DOS Typical")
    
    # Comparison
    print("\n\nWORKLOAD COMPARISON:")
    print("-" * 60)
    print(f"{'Workload':<20} {'CPI':>7} {'IPC':>7} {'MIPS':>7} {'Penalty':<12}")
    print("-" * 60)
    
    for name, workload in WORKLOADS.items():
        r = model.predict(workload)
        print(f"{name:<20} {r.cpi_total:>7.2f} {r.ipc:>7.4f} {r.mips:>7.3f} {r.bottleneck:<12}")


if __name__ == "__main__":
    main()
