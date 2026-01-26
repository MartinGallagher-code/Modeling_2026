#!/usr/bin/env python3
"""
Intel 8086 Unified Performance Model

COMBINES QUEUEING THEORY AND CPI STACK APPROACHES

This module provides a unified interface to both modeling approaches,
allowing users to:
1. Run either model independently
2. Compare results from both approaches
3. Get combined insights

Usage:
    from ibm_pc_8086_unified import Intel8086UnifiedModel
    
    model = Intel8086UnifiedModel()
    results = model.analyze(workload)
    model.print_combined_analysis(results)

Author: Grey-Box Performance Modeling Research
Date: January 25, 2026
"""

import json
from dataclasses import dataclass
from typing import Dict, Optional

# Import both models
from ibm_pc_8086_cpi_stack import (
    Intel8086CPIStackModel, 
    CPIStackResult, 
    Workload, 
    WORKLOADS,
    Intel8086Config
)


# =============================================================================
# UNIFIED RESULT
# =============================================================================

@dataclass
class UnifiedResult:
    """Combined results from both modeling approaches."""
    
    # CPI Stack results
    cpi_stack_ipc: float
    cpi_stack_cpi: float
    cpi_stack_mips: float
    cpi_stack_bottleneck: str
    cpi_stack_breakdown: Dict[str, float]
    
    # Queueing results (if available)
    queueing_ipc: Optional[float] = None
    queueing_bottleneck: Optional[str] = None
    queueing_utilizations: Optional[Dict[str, float]] = None
    
    # Combined analysis
    ipc_agreement: float = 0.0  # How close the two models agree
    combined_insight: str = ""


# =============================================================================
# UNIFIED MODEL
# =============================================================================

class Intel8086UnifiedModel:
    """
    Unified model combining Queueing Theory and CPI Stack.
    
    Provides:
    - Independent access to each model
    - Combined analysis
    - Cross-validation between approaches
    """
    
    def __init__(self, config: Intel8086Config = None):
        self.config = config or Intel8086Config()
        self.cpi_model = Intel8086CPIStackModel(self.config)
        
        # Try to load queueing model config
        self.queueing_config = self._load_queueing_config()
    
    def _load_queueing_config(self) -> Optional[Dict]:
        """Try to load the queueing model configuration."""
        try:
            with open('ibm_pc_8086_model.json', 'r') as f:
                return json.load(f)
        except:
            return None
    
    def _run_queueing_model(self, workload: Workload) -> Dict:
        """
        Run queueing model prediction.
        
        This is a simplified version - in practice, you'd import
        the actual queueing model class.
        """
        if self.queueing_config is None:
            return None
        
        # Simplified queueing calculation based on config
        # (Real implementation would use full ibm_pc_8086_model.py)
        
        try:
            arch = self.queueing_config.get('architecture', {})
            clock = arch.get('clock_frequency_mhz', 5.0)
            
            # Simplified EU service time
            timings = self.queueing_config.get('instruction_timings', {})
            base_timing = timings.get('one_word_instruction', 8)
            
            # Simplified BIU model
            prefetch = self.queueing_config.get('bus_interface_unit', {})
            prefetch_depth = prefetch.get('prefetch_queue_bytes', 6)
            
            # Basic queueing estimate
            service_time = base_timing + workload.mem_operand_rate * 4
            arrival_rate = 0.10  # Simplified
            
            util = arrival_rate * service_time
            if util >= 1.0:
                ipc = 0.0
                bottleneck = "saturated"
            else:
                ipc = 1.0 / service_time
                bottleneck = "execution_unit" if util > 0.5 else "bus_interface"
            
            return {
                'ipc': ipc,
                'bottleneck': bottleneck,
                'utilizations': {
                    'EU': util,
                    'BIU': util * 0.7,
                    'prefetch': util * 0.6
                }
            }
        except:
            return None
    
    def analyze_cpi_stack(self, workload: Workload) -> CPIStackResult:
        """Run CPI Stack analysis only."""
        return self.cpi_model.predict(workload)
    
    def analyze_queueing(self, workload: Workload) -> Optional[Dict]:
        """Run Queueing analysis only."""
        return self._run_queueing_model(workload)
    
    def analyze(self, workload: Workload) -> UnifiedResult:
        """
        Run both models and combine results.
        
        This is the main entry point for unified analysis.
        """
        # Run CPI Stack
        cpi_result = self.analyze_cpi_stack(workload)
        
        # Run Queueing (if available)
        q_result = self.analyze_queueing(workload)
        
        # Build unified result
        result = UnifiedResult(
            cpi_stack_ipc=cpi_result.ipc,
            cpi_stack_cpi=cpi_result.cpi_total,
            cpi_stack_mips=cpi_result.mips,
            cpi_stack_bottleneck=cpi_result.bottleneck,
            cpi_stack_breakdown=cpi_result.component_percentages
        )
        
        if q_result:
            result.queueing_ipc = q_result['ipc']
            result.queueing_bottleneck = q_result['bottleneck']
            result.queueing_utilizations = q_result['utilizations']
            
            # Calculate agreement
            if result.queueing_ipc > 0:
                diff = abs(result.cpi_stack_ipc - result.queueing_ipc)
                avg = (result.cpi_stack_ipc + result.queueing_ipc) / 2
                result.ipc_agreement = 100 * (1 - diff / avg)
        
        # Generate combined insight
        result.combined_insight = self._generate_insight(result)
        
        return result
    
    def _generate_insight(self, result: UnifiedResult) -> str:
        """Generate combined insight from both models."""
        insights = []
        
        # CPI Stack insight
        penalty = result.cpi_stack_bottleneck
        pct = result.cpi_stack_breakdown.get(penalty, 0)
        insights.append(f"CPI Stack: Largest penalty is {penalty} ({pct:.1f}%)")
        
        # Queueing insight
        if result.queueing_bottleneck:
            insights.append(f"Queueing: Bottleneck is {result.queueing_bottleneck}")
        
        # Combined recommendation
        if penalty == 'branch':
            insights.append("→ Optimize: Reduce branch frequency or improve prediction")
        elif penalty == 'ea_calc':
            insights.append("→ Optimize: Use simpler addressing modes")
        elif penalty == 'memory':
            insights.append("→ Optimize: Reduce memory operands, use registers")
        elif penalty == 'bus':
            insights.append("→ Optimize: Reduce memory traffic")
        
        return "\n".join(insights)
    
    def print_combined_analysis(self, result: UnifiedResult, name: str = ""):
        """Print formatted combined analysis."""
        
        print(f"\n{'='*70}")
        print(f"UNIFIED ANALYSIS: {name}" if name else "UNIFIED 8086 ANALYSIS")
        print(f"{'='*70}")
        
        # CPI Stack section
        print(f"\n┌{'─'*68}┐")
        print(f"│ {'CPI STACK MODEL':<66} │")
        print(f"├{'─'*68}┤")
        print(f"│ IPC: {result.cpi_stack_ipc:.4f}  |  "
              f"MIPS: {result.cpi_stack_mips:.3f}  |  "
              f"CPI: {result.cpi_stack_cpi:.2f}{' '*19} │")
        print(f"│ Largest penalty: {result.cpi_stack_bottleneck:<48} │")
        print(f"│{' '*68}│")
        
        # Breakdown
        print(f"│ {'Component':<15} {'Percent':>8}  {'Bar':<42} │")
        for comp, pct in sorted(result.cpi_stack_breakdown.items(), 
                                 key=lambda x: -x[1]):
            bar = '█' * int(35 * pct / 100)
            marker = " ←" if comp == result.cpi_stack_bottleneck and comp != 'base' else ""
            print(f"│ {comp:<15} {pct:>7.1f}%  {bar:<40}{marker:>2} │")
        
        print(f"└{'─'*68}┘")
        
        # Queueing section (if available)
        if result.queueing_ipc is not None:
            print(f"\n┌{'─'*68}┐")
            print(f"│ {'QUEUEING MODEL':<66} │")
            print(f"├{'─'*68}┤")
            print(f"│ IPC: {result.queueing_ipc:.4f}  |  "
                  f"Bottleneck: {result.queueing_bottleneck:<30} │")
            
            if result.queueing_utilizations:
                print(f"│{' '*68}│")
                print(f"│ {'Resource':<15} {'Utilization':>12}{' '*39} │")
                for res, util in result.queueing_utilizations.items():
                    bar = '█' * int(30 * util)
                    print(f"│ {res:<15} {util*100:>10.1f}%  {bar:<38} │")
            
            print(f"└{'─'*68}┘")
            
            # Agreement
            print(f"\n Model Agreement: {result.ipc_agreement:.1f}%")
        
        # Combined insight
        print(f"\n┌{'─'*68}┐")
        print(f"│ {'COMBINED INSIGHT':<66} │")
        print(f"├{'─'*68}┤")
        for line in result.combined_insight.split('\n'):
            print(f"│ {line:<66} │")
        print(f"└{'─'*68}┘")


# =============================================================================
# MAIN DEMONSTRATION
# =============================================================================

def main():
    print("\n" + "="*70)
    print("  INTEL 8086 UNIFIED PERFORMANCE MODEL")
    print("  Combining Queueing Theory + CPI Stack")
    print("="*70)
    
    model = Intel8086UnifiedModel()
    
    # Analyze typical workload
    workload = WORKLOADS["dos_typical"]
    result = model.analyze(workload)
    model.print_combined_analysis(result, "DOS Typical Workload")
    
    # Compare workloads
    print("\n\n" + "="*70)
    print("WORKLOAD COMPARISON (CPI Stack)")
    print("="*70)
    print(f"\n{'Workload':<20} {'IPC':>8} {'CPI':>8} {'Penalty':<15}")
    print("-"*55)
    
    for name, wl in WORKLOADS.items():
        r = model.analyze(wl)
        print(f"{name:<20} {r.cpi_stack_ipc:>8.4f} {r.cpi_stack_cpi:>8.2f} "
              f"{r.cpi_stack_bottleneck:<15}")
    
    print("\n" + "="*70)
    print("KEY INSIGHT:")
    print("="*70)
    print("""
    Queueing Model tells you: WHAT is the bottleneck resource?
    CPI Stack Model tells you: WHERE do the cycles go?
    
    USE BOTH for complete understanding:
    1. Queueing → Identify saturated resources (EU vs BIU)
    2. CPI Stack → Identify specific penalties (branch, EA, memory)
    3. Combined → Actionable optimization recommendations
    """)


if __name__ == "__main__":
    main()
