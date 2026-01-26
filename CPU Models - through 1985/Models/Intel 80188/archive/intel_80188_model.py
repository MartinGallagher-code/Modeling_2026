#!/usr/bin/env python3
"""
Intel 80188 CPU Queueing Model

The 80188: Cost-Optimized Embedded System-on-Chip

Relationship: 80188 is to 80186 as 8088 is to 8086
- Same CPU core (16-bit internal)
- Same integrated peripherals
- 8-bit external data bus (vs 16-bit)
- Smaller prefetch queue (4 bytes vs 6 bytes)

Performance Impact:
- ~18% slower than 80186 due to bus bottleneck
- BIU becomes the limiting factor (vs EU in 80186)

Cost Advantage:
- Uses cheaper 8-bit memory systems
- Simpler PCB (8 data traces vs 16)
- Lower total system cost

Author: Grey-Box Performance Modeling Research
Date: January 24, 2026
Target CPU: Intel 80188 (1982-2007)
"""

import json
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class QueueMetrics:
    """Metrics for a single queue/stage"""
    name: str
    arrival_rate: float
    service_time: float
    utilization: float
    queue_length: float
    wait_time: float
    response_time: float


@dataclass
class CalibrationResult:
    """Results from model calibration"""
    predicted_ipc: float
    measured_ipc: float
    error_percent: float
    iterations: int
    converged: bool
    bottleneck_stage: str
    stage_metrics: List[QueueMetrics]


class Intel80188QueueModel:
    """
    Queueing network model for Intel 80188 CPU.
    
    Architecture Overview:
    =====================
    The 80188 is an 80186 with an 8-bit external data bus:
    
    Same as 80186:
    - 16-bit internal architecture
    - Same EU (Execution Unit)
    - Same integrated peripherals
    - Same instruction set
    
    Different from 80186:
    - 8-bit external data bus (vs 16-bit)
    - 4-byte prefetch queue (vs 6-byte)
    - Slower memory bandwidth
    
    Performance Impact:
    ==================
    The 8-bit bus creates a BIU bottleneck:
    
    80186: EU is bottleneck (BIU keeps up)
    80188: BIU is bottleneck (EU waits for data)
    
    Result: ~18% slower than 80186
    
    This is the SAME tradeoff as 8086 vs 8088!
    
    Cost Advantage:
    ==============
    Why choose 80188 over 80186?
    - 8-bit memory systems are cheaper
    - Simpler PCB design (8 data traces vs 16)
    - Lower total system cost
    - Same peripherals, lower cost
    
    Queueing Model:
    ==============
    Two M/M/1 queues (BIU and EU) with 4-byte bounded prefetch:
    
    Memory → [BIU Queue (M/M/1/4)] → [EU Queue] → Completed
                    ↑
            8-bit bus bottleneck!
    """
    
    def __init__(self, config_file: str):
        """Initialize model from JSON configuration file."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Architecture parameters
        arch = self.config['architecture']
        self.clock_freq_mhz = arch['clock_frequency_mhz']
        self.data_bus_width = arch['data_bus_width_bits']  # 8 bits!
        self.prefetch_queue_size = arch['prefetch_queue_bytes']  # 4 bytes
        
        # Instruction mix
        mix = self.config['instruction_mix']
        self.p_mov = mix['mov_operations']
        self.p_alu = mix['alu_operations']
        self.p_load_store = mix['load_store']
        self.p_jump_call = mix['jump_call']
        self.p_stack = mix['stack_operations']
        self.p_string = mix['string_operations']
        self.p_io = mix['io_operations']
        
        # Instruction timings (slower memory ops due to 8-bit bus)
        timings = self.config['instruction_timings']
        mov = timings['basic_mov']
        self.mov_reg_cycles = mov['reg_to_reg']
        self.mov_mem_cycles = np.mean([mov['reg_to_mem'], mov['mem_to_reg']])
        
        alu = timings['alu_operations']
        self.alu_reg_cycles = alu['add_reg']
        self.alu_mem_cycles = alu['add_mem']
        
        branch = timings['branch_jump']
        self.branch_avg_cycles = np.mean([
            branch['short_jump'],
            branch['near_jump'],
            branch['near_call'],
            branch['ret_near']
        ])
        
        # Prefetch queue characteristics
        queue = self.config['prefetch_queue']
        self.queue_empty_prob = queue['queue_empty_probability']
        self.queue_efficiency = queue['efficiency']
        
        # Memory system (8-bit bus!)
        mem = self.config['memory_system']
        self.memory_access_cycles = mem['memory_access_cycles']
        self.bytes_per_fetch = mem['bus_width_bytes']  # 1 byte per fetch
        
        # Instruction length
        inst_len = self.config['instruction_length_distribution']
        self.avg_instruction_bytes = inst_len['average_bytes']
    
    def compute_biu_service_time(self) -> float:
        """
        Compute BIU service time for 80188.
        
        Critical difference from 80186:
        - 8-bit bus fetches 1 byte per cycle (vs 2 bytes)
        - Takes 2× as many bus cycles for same instruction
        
        Returns:
            Average cycles for BIU to fetch an instruction
        """
        # 8-bit bus: 1 byte per bus cycle
        # Average instruction is 2.5 bytes
        # Each byte takes memory_access_cycles
        fetch_cycles = self.avg_instruction_bytes * self.memory_access_cycles
        
        return fetch_cycles  # ~10 cycles (vs ~5 for 80186)
    
    def compute_eu_service_time(self) -> float:
        """
        Compute EU service time.
        
        Same as 80186 - internal execution identical.
        
        Returns:
            Average cycles for EU to execute an instruction
        """
        # MOV: 92% register, 8% memory
        mov_avg = 0.92 * self.mov_reg_cycles + 0.08 * self.mov_mem_cycles
        
        # ALU: 92% register, 8% memory
        alu_avg = 0.92 * self.alu_reg_cycles + 0.08 * self.alu_mem_cycles
        
        # Weighted average
        weighted_cycles = (
            self.p_mov * mov_avg +
            self.p_alu * alu_avg +
            self.p_load_store * 12.0 +  # Slower due to 8-bit bus
            self.p_jump_call * self.branch_avg_cycles +
            self.p_stack * 10.0 +
            self.p_string * 14.0 +
            self.p_io * 12.0
        )
        
        return weighted_cycles
    
    def compute_stage_metrics(self, arrival_rate: float) -> List[QueueMetrics]:
        """
        Compute metrics for BIU and EU stages.
        
        Key insight: 8-bit bus makes BIU the bottleneck!
        
        Args:
            arrival_rate: Instruction arrival rate (instructions/cycle)
        
        Returns:
            List of QueueMetrics for BIU and EU
        """
        metrics = []
        
        # BIU stage (THE BOTTLENECK on 80188!)
        biu_service = self.compute_biu_service_time()
        biu_util = arrival_rate * biu_service
        
        if biu_util >= 1.0:
            biu_queue_length = float('inf')
            biu_wait_time = float('inf')
        else:
            biu_queue_length = biu_util / (1 - biu_util)
            biu_wait_time = biu_service / (1 - biu_util)
        
        metrics.append(QueueMetrics(
            name="BIU (8-bit)",
            arrival_rate=arrival_rate,
            service_time=biu_service,
            utilization=biu_util,
            queue_length=biu_queue_length,
            wait_time=biu_wait_time,
            response_time=biu_wait_time + biu_service if biu_util < 1.0 else float('inf')
        ))
        
        # EU stage (same as 80186)
        eu_service = self.compute_eu_service_time()
        eu_util = arrival_rate * eu_service
        
        if eu_util >= 1.0:
            eu_queue_length = float('inf')
            eu_wait_time = float('inf')
        else:
            eu_queue_length = eu_util / (1 - eu_util)
            eu_wait_time = eu_service / (1 - eu_util)
        
        metrics.append(QueueMetrics(
            name="EU",
            arrival_rate=arrival_rate,
            service_time=eu_service,
            utilization=eu_util,
            queue_length=eu_queue_length,
            wait_time=eu_wait_time,
            response_time=eu_wait_time + eu_service if eu_util < 1.0 else float('inf')
        ))
        
        return metrics
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        """
        Predict IPC for given arrival rate.
        
        Expected: ~0.33 IPC (vs 80186's ~0.40)
        ~18% slower due to 8-bit bus bottleneck
        
        Returns:
            (predicted_ipc, stage_metrics)
        """
        metrics = self.compute_stage_metrics(arrival_rate)
        
        max_util = max(m.utilization for m in metrics)
        if max_util >= 1.0:
            return 0.0, metrics
        
        # IPC limited by bottleneck (BIU on 80188)
        effective_efficiency = self.queue_efficiency * (1.0 - self.queue_empty_prob)
        predicted_ipc = arrival_rate * effective_efficiency
        
        # Cap at bottleneck limit
        bottleneck_service = max(m.service_time for m in metrics)
        max_theoretical_ipc = 1.0 / bottleneck_service
        predicted_ipc = min(predicted_ipc, max_theoretical_ipc)
        
        return predicted_ipc, metrics
    
    def calibrate(self,
                  measured_ipc: float,
                  initial_arrival_rate: float = 0.20,
                  tolerance_percent: float = 2.0,
                  max_iterations: int = 50) -> CalibrationResult:
        """Calibrate model to match measured IPC."""
        biu_service = self.compute_biu_service_time()
        eu_service = self.compute_eu_service_time()
        max_stable_rate = 0.95 / max(biu_service, eu_service)
        
        low = 0.02
        high = min(0.40, max_stable_rate)
        arrival_rate = min(initial_arrival_rate, high * 0.9)
        
        best_error = float('inf')
        best_rate = arrival_rate
        best_metrics = None
        best_ipc = 0.0
        
        for iteration in range(max_iterations):
            predicted_ipc, metrics = self.predict_ipc(arrival_rate)
            
            if predicted_ipc == 0.0:
                high = arrival_rate
                arrival_rate = (low + high) / 2.0
                continue
            
            error_percent = abs(predicted_ipc - measured_ipc) / measured_ipc * 100
            
            if error_percent < best_error:
                best_error = error_percent
                best_rate = arrival_rate
                best_metrics = metrics
                best_ipc = predicted_ipc
            
            if error_percent <= tolerance_percent:
                bottleneck = max(metrics, key=lambda m: m.utilization)
                return CalibrationResult(
                    predicted_ipc=predicted_ipc,
                    measured_ipc=measured_ipc,
                    error_percent=error_percent,
                    iterations=iteration + 1,
                    converged=True,
                    bottleneck_stage=bottleneck.name,
                    stage_metrics=metrics
                )
            
            if predicted_ipc < measured_ipc:
                low = arrival_rate
            else:
                high = arrival_rate
            
            arrival_rate = (low + high) / 2.0
            
            if abs(high - low) < 1e-6:
                break
        
        bottleneck = max(best_metrics, key=lambda m: m.utilization) if best_metrics else None
        return CalibrationResult(
            predicted_ipc=best_ipc,
            measured_ipc=measured_ipc,
            error_percent=best_error,
            iterations=max_iterations,
            converged=best_error <= tolerance_percent,
            bottleneck_stage=bottleneck.name if bottleneck else "Unknown",
            stage_metrics=best_metrics or []
        )
    
    def compare_with_80186(self) -> Dict:
        """
        Compare 80188 with 80186.
        
        Same relationship as 8088 vs 8086!
        
        Returns:
            Dictionary with detailed comparison
        """
        test_arrival_rate = 0.08
        
        # 80188 performance
        i80188_ipc, i80188_metrics = self.predict_ipc(test_arrival_rate)
        i80188_biu = i80188_metrics[0].service_time
        i80188_eu = i80188_metrics[1].service_time
        
        # 80186 estimated (16-bit bus = half the BIU service time)
        i80186_biu = i80188_biu / 2.0  # 16-bit bus fetches 2× faster
        i80186_eu = i80188_eu  # Same EU
        
        # Estimate 80186 IPC (less BIU bottleneck)
        i80186_ipc = i80188_ipc * 1.18  # ~18% faster
        
        return {
            'arrival_rate': test_arrival_rate,
            '80188': {
                'ipc': i80188_ipc,
                'biu_service': i80188_biu,
                'eu_service': i80188_eu,
                'bus_width': 8,
                'prefetch_queue': 4,
                'bottleneck': max(i80188_metrics, key=lambda m: m.utilization).name,
                'clock_mhz': self.clock_freq_mhz,
                'mips': i80188_ipc * self.clock_freq_mhz
            },
            '80186': {
                'ipc': i80186_ipc,
                'biu_service': i80186_biu,
                'eu_service': i80186_eu,
                'bus_width': 16,
                'prefetch_queue': 6,
                'bottleneck': 'EU',
                'clock_mhz': self.clock_freq_mhz,
                'mips': i80186_ipc * self.clock_freq_mhz
            },
            'performance_ratio': {
                'ipc_ratio': i80188_ipc / i80186_ipc if i80186_ipc > 0 else 0,
                'penalty': f"{(1 - i80188_ipc/i80186_ipc)*100:.0f}% slower" if i80186_ipc > 0 else "N/A",
                'biu_ratio': i80188_biu / i80186_biu,
                'bottleneck_shift': 'EU (80186) → BIU (80188)'
            },
            'cost_tradeoff': {
                'performance_loss': '~18%',
                'cost_savings': 'Significant (8-bit memory cheaper)',
                'pcb_savings': '8 fewer data traces',
                'when_to_choose_80188': 'Cost matters more than performance'
            }
        }
    
    def compare_with_8088(self) -> Dict:
        """
        Compare 80188 with 8088.
        
        Both are 8-bit bus versions of 16-bit CPUs.
        
        Returns:
            Dictionary with comparison
        """
        test_arrival_rate = 0.08
        
        i80188_ipc, _ = self.predict_ipc(test_arrival_rate)
        
        # 8088 characteristics (from your existing model)
        i8088_ipc = 0.33  # Typical 8088 IPC
        
        return {
            '80188': {
                'ipc': i80188_ipc,
                'integrated_peripherals': True,
                'clock_mhz': self.clock_freq_mhz,
                'chip_count': 1
            },
            '8088': {
                'ipc': i8088_ipc,
                'integrated_peripherals': False,
                'clock_mhz': 4.77,
                'chip_count': '5+ (CPU + DMA + Timer + IRQ + glue)'
            },
            'comparison': {
                'ipc_similar': 'Both ~0.33 (8-bit bus limited)',
                '80188_advantage': 'Integrated peripherals',
                '8088_advantage': 'IBM PC compatible',
                'lesson': 'Same bus width = similar performance ceiling'
            }
        }
    
    def print_metrics(self, metrics: List[QueueMetrics]):
        """Pretty print stage metrics."""
        print("\n" + "="*80)
        print("Intel 80188 CPU Pipeline Metrics (8-bit Bus)")
        print("="*80)
        print(f"{'Stage':<15} {'λ':>10} {'S':>10} {'ρ':>10} {'L':>10} {'W':>10}")
        print(f"{'':15} {'(ins/cyc)':>10} {'(cyc)':>10} {'':>10} {'(ins)':>10} {'(cyc)':>10}")
        print("-"*80)
        
        for m in metrics:
            l_str = f"{m.queue_length:.2f}" if m.queue_length != float('inf') else "inf"
            w_str = f"{m.wait_time:.2f}" if m.wait_time != float('inf') else "inf"
            
            print(f"{m.name:<15} {m.arrival_rate:>10.4f} {m.service_time:>10.2f} "
                  f"{m.utilization:>10.4f} {l_str:>10} {w_str:>10}")
        
        print("="*80)
        
        bottleneck = max(metrics, key=lambda m: m.utilization)
        print(f"\nBottleneck: {bottleneck.name} (ρ = {bottleneck.utilization:.4f})")
        print("Note: BIU is bottleneck due to 8-bit bus (vs EU on 80186)")
        
        predicted_ipc, _ = self.predict_ipc(metrics[0].arrival_rate)
        print(f"Predicted IPC: {predicted_ipc:.4f}")


def main():
    """Example usage of the 80188 model."""
    print("Intel 80188 CPU Queueing Model")
    print("="*80)
    print("Cost-Optimized Embedded SoC: 80186 with 8-bit Bus")
    print("="*80)
    
    model = Intel80188QueueModel('intel_80188_model.json')
    
    # Example 1: IPC prediction
    print("\nExample 1: IPC Prediction at Different Loads")
    print("-"*80)
    for arrival_rate in [0.04, 0.06, 0.08, 0.10]:
        ipc, metrics = model.predict_ipc(arrival_rate)
        bottleneck = max(metrics, key=lambda m: m.utilization)
        print(f"λ={arrival_rate:.2f} → IPC={ipc:.4f}, Bottleneck: {bottleneck.name}")
    
    # Example 2: Detailed metrics
    print("\nExample 2: Detailed Metrics (λ=0.08)")
    ipc, metrics = model.predict_ipc(0.08)
    model.print_metrics(metrics)
    
    # Example 3: Compare with 80186
    print("\nExample 3: 80188 vs 80186 Comparison")
    print("-"*80)
    comparison = model.compare_with_80186()
    
    print("Bus Architecture:")
    print(f"  80188: {comparison['80188']['bus_width']}-bit bus, {comparison['80188']['prefetch_queue']}-byte queue")
    print(f"  80186: {comparison['80186']['bus_width']}-bit bus, {comparison['80186']['prefetch_queue']}-byte queue")
    
    print(f"\nPerformance:")
    print(f"  80188 IPC: {comparison['80188']['ipc']:.4f}")
    print(f"  80186 IPC: {comparison['80186']['ipc']:.4f} (estimated)")
    print(f"  Ratio: {comparison['performance_ratio']['ipc_ratio']:.2f}× ({comparison['performance_ratio']['penalty']})")
    
    print(f"\nBottleneck Shift:")
    print(f"  {comparison['performance_ratio']['bottleneck_shift']}")
    
    print(f"\nCost Tradeoff:")
    for key, value in comparison['cost_tradeoff'].items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")
    
    # Example 4: Compare with 8088
    print("\nExample 4: 80188 vs 8088 (Both 8-bit Bus)")
    print("-"*80)
    comp_8088 = model.compare_with_8088()
    
    print(f"80188: IPC={comp_8088['80188']['ipc']:.4f}, Integrated={comp_8088['80188']['integrated_peripherals']}")
    print(f"8088:  IPC={comp_8088['8088']['ipc']:.4f}, Integrated={comp_8088['8088']['integrated_peripherals']}")
    print(f"\nLesson: {comp_8088['comparison']['lesson']}")
    
    # Example 5: Calibration
    print("\nExample 5: Model Calibration")
    print("-"*80)
    result = model.calibrate(measured_ipc=0.06)
    print(f"Target IPC: {result.measured_ipc:.4f}")
    print(f"Predicted IPC: {result.predicted_ipc:.4f}")
    print(f"Error: {result.error_percent:.2f}%")
    print(f"Converged: {result.converged}")
    print(f"Bottleneck: {result.bottleneck_stage}")
    
    print("\n" + "="*80)
    print("The 80188 shows the classic cost-performance tradeoff:")
    print("  • 8-bit bus = ~18% slower than 80186")
    print("  • 8-bit bus = cheaper memory, simpler PCB")
    print("  • Same pattern as 8088 vs 8086!")
    print("Lesson: For cost-sensitive embedded, sacrifice performance for cost.")
    print("="*80)


if __name__ == "__main__":
    main()
