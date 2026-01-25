#!/usr/bin/env python3
"""
Intel 80386 CPU Queueing Model

This model extends the 80286 to include the 80386's architectural advances:
- 16-byte instruction prefetch queue (vs 6 bytes on 80286)
- 32-bit data bus and registers
- On-chip cache (optional, varies by implementation)
- Paging unit (in addition to segmentation)
- Improved pipeline (6 stages vs 4 on 80286)

Author: Grey-Box Performance Modeling Research
Date: January 23, 2026
Target CPU: Intel 80386 (1985-2007)
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class MemoryMode(Enum):
    """80386 Memory Management Modes"""
    REAL = 0           # 8086 compatibility
    PROTECTED = 1      # Segmentation with protection
    VIRTUAL_8086 = 2   # Virtual 8086 mode
    PAGED = 3          # Paging enabled


@dataclass
class CacheMetrics:
    """Metrics for cache hierarchy"""
    hit_rate: float
    miss_rate: float
    hit_latency: float      # cycles
    miss_latency: float     # cycles
    effective_latency: float  # weighted average


@dataclass
class QueueMetrics:
    """Metrics for a single queue/stage"""
    name: str
    arrival_rate: float      # λ (instructions/cycle)
    service_time: float      # S (cycles/instruction)
    utilization: float       # ρ = λ × S
    queue_length: float      # L = ρ / (1 - ρ)
    wait_time: float         # W = S / (1 - ρ)
    response_time: float     # R = W + S


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
    cache_metrics: Optional[CacheMetrics]


class Intel80386QueueModel:
    """
    Queueing network model for Intel 80386 CPU.
    
    Architecture Evolution:
    ======================
    
    80286:
    - 16-bit registers
    - 6-byte prefetch queue
    - No cache
    - Segmentation only
    
    80386:
    - 32-bit registers ✓
    - 16-byte prefetch queue ✓
    - Optional on-chip cache ✓
    - Segmentation + Paging ✓
    - 6-stage pipeline ✓
    
    Pipeline Structure:
    ==================
    
    BIU (Bus Interface Unit) - Parallel:
    ┌─────────────────────────────────────┐
    │  Prefetch Queue (16 bytes)          │
    │  - Larger than 80286 (6 bytes)      │
    │  - M/M/1/16 bounded queue           │
    │  - Fetches from cache or memory     │
    └─────────────────┬───────────────────┘
                      │ Instructions
                      ↓
    EU (Execution Unit) - Series Pipeline:
    ┌─────────────────────────────────────┐
    │  Stage 1: Fetch (from prefetch)     │
    │  - Get instruction bytes            │
    └─────────────────┬───────────────────┘
                      ↓
    ┌─────────────────────────────────────┐
    │  Stage 2: Decode                    │
    │  - Decode 32-bit instructions       │
    │  - More complex than 80286          │
    └─────────────────┬───────────────────┘
                      ↓
    ┌─────────────────────────────────────┐
    │  Stage 3: Address Calculation       │
    │  - Segmentation                     │
    │  - Paging (if enabled)              │
    │  - TLB lookup                       │
    └─────────────────┬───────────────────┘
                      ↓
    ┌─────────────────────────────────────┐
    │  Stage 4: Execute                   │
    │  - ALU (32-bit)                     │
    │  - Multiply (faster than 80286)     │
    │  - Divide (faster than 80286)       │
    └─────────────────┬───────────────────┘
                      ↓
    ┌─────────────────────────────────────┐
    │  Stage 5: Memory Access             │
    │  - Cache lookup (if present)        │
    │  - Load/Store                       │
    └─────────────────┬───────────────────┘
                      ↓
    ┌─────────────────────────────────────┐
    │  Stage 6: Writeback                 │
    │  - Update 32-bit registers          │
    │  - Update flags                     │
    └─────────────────────────────────────┘
    
    Cache Hierarchy (Optional):
    ===========================
    
    Some 80386 implementations (386DX-25+) had on-chip cache:
    - Unified cache (instructions + data)
    - Typically 8-16 KB
    - Direct-mapped or 2-way set associative
    - Hit: 0 wait states
    - Miss: Go to external memory
    """
    
    def __init__(self, config_file: str):
        """Initialize model from JSON configuration file."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Extract architecture parameters
        arch = self.config['architecture']
        self.clock_freq_mhz = arch['clock_frequency_mhz']
        self.prefetch_queue_size = arch['prefetch_queue_size']
        self.data_bus_width = arch['data_bus_width']
        
        # Pipeline stages
        stages = self.config['pipeline_stages']
        self.fetch_cycles = stages['fetch']['base_cycles']
        self.decode_cycles = stages['decode']['base_cycles']
        self.address_calc_cycles = stages['address_calculation']['base_cycles']
        self.execute_cycles = stages['execute']['base_cycles']
        self.memory_cycles = stages['memory_access']['base_cycles']
        self.writeback_cycles = stages['writeback']['base_cycles']
        
        # Instruction mix
        mix = self.config['instruction_mix']
        self.p_alu = mix['alu']
        self.p_mul = mix['multiply']
        self.p_div = mix['divide']
        self.p_load = mix['load']
        self.p_store = mix['store']
        self.p_branch = mix['branch']
        
        # Cache system
        cache_cfg = self.config['cache_system']
        self.has_cache = cache_cfg['enabled']
        self.cache_size_kb = cache_cfg['size_kb']
        self.cache_hit_rate = cache_cfg['instruction_hit_rate']
        self.cache_data_hit_rate = cache_cfg['data_hit_rate']
        self.cache_hit_cycles = cache_cfg['hit_latency_cycles']
        self.cache_miss_cycles = cache_cfg['miss_latency_cycles']
        
        # Memory system
        mem = self.config['memory_system']
        self.external_memory_cycles = mem['external_memory_access_cycles']
        
        # Paging system
        paging = self.config['paging_system']
        self.paging_enabled = paging['enabled']
        self.tlb_hit_rate = paging['tlb_hit_rate']
        self.tlb_hit_cycles = paging['tlb_hit_cycles']
        self.tlb_miss_cycles = paging['tlb_miss_cycles']
        self.page_table_walk_cycles = paging['page_table_walk_cycles']
        
        # Segmentation (carried over from 80286)
        seg = self.config['segmentation']
        self.segment_translation_cycles = seg['segment_translation_cycles']
        self.p_segment_ops = seg['segment_operation_probability']
        
    def compute_cache_effective_latency(self, is_instruction: bool = True) -> CacheMetrics:
        """
        Compute effective memory access latency with cache.
        
        Args:
            is_instruction: True for instruction fetch, False for data access
        
        Returns:
            CacheMetrics with hit/miss rates and effective latency
        """
        if not self.has_cache:
            # No cache - always go to external memory
            return CacheMetrics(
                hit_rate=0.0,
                miss_rate=1.0,
                hit_latency=0.0,
                miss_latency=self.external_memory_cycles,
                effective_latency=self.external_memory_cycles
            )
        
        # With cache
        hit_rate = self.cache_hit_rate if is_instruction else self.cache_data_hit_rate
        miss_rate = 1.0 - hit_rate
        
        # Effective latency = hit_rate × hit_latency + miss_rate × miss_latency
        effective_latency = (
            hit_rate * self.cache_hit_cycles +
            miss_rate * self.cache_miss_cycles
        )
        
        return CacheMetrics(
            hit_rate=hit_rate,
            miss_rate=miss_rate,
            hit_latency=self.cache_hit_cycles,
            miss_latency=self.cache_miss_cycles,
            effective_latency=effective_latency
        )
    
    def compute_paging_overhead(self) -> float:
        """
        Compute paging overhead (TLB + page table walks).
        
        Returns:
            Average cycles added by paging
        """
        if not self.paging_enabled:
            return 0.0
        
        # TLB hit: fast
        # TLB miss: page table walk required
        overhead = (
            self.tlb_hit_rate * self.tlb_hit_cycles +
            (1 - self.tlb_hit_rate) * (self.tlb_miss_cycles + self.page_table_walk_cycles)
        )
        
        return overhead
    
    def compute_prefetch_metrics(self, arrival_rate: float) -> QueueMetrics:
        """
        Compute metrics for the prefetch queue (BIU).
        
        80386 has 16-byte prefetch queue (vs 6 bytes on 80286).
        Modeled as M/M/1/K with K=16.
        """
        # Service time = time to fetch instruction bytes from cache/memory
        cache_metrics = self.compute_cache_effective_latency(is_instruction=True)
        
        # Average instruction is ~3 bytes on 80386 (32-bit instructions are longer)
        # Fetch in chunks of 4 bytes (32-bit bus)
        service_time = cache_metrics.effective_latency / 4.0
        
        # M/M/1/K formulas with K=16
        K = self.prefetch_queue_size
        rho = arrival_rate * service_time
        
        if rho >= 1.0:
            utilization = 1.0
            queue_length = K / 2.0
            wait_time = queue_length / arrival_rate if arrival_rate > 0 else 0
        else:
            utilization = rho
            if abs(rho - 1.0) < 1e-6:
                queue_length = K / 2.0
            else:
                numerator = rho * (1 - (K+1) * (rho**K) + K * (rho**(K+1)))
                denominator = (1 - rho) * (1 - rho**(K+1))
                queue_length = numerator / denominator if abs(denominator) > 1e-10 else K/2.0
            
            wait_time = queue_length / arrival_rate if arrival_rate > 0 else 0
        
        response_time = wait_time + service_time
        
        return QueueMetrics(
            name="Prefetch_Queue_BIU",
            arrival_rate=arrival_rate,
            service_time=service_time,
            utilization=utilization,
            queue_length=queue_length,
            wait_time=wait_time,
            response_time=response_time
        )
    
    def compute_fetch_service_time(self) -> float:
        """
        Fetch stage: Get instruction from prefetch queue.
        Simple passthrough - already fetched by BIU.
        """
        return self.fetch_cycles
    
    def compute_decode_service_time(self) -> float:
        """
        Decode stage: Decode 32-bit instructions.
        
        80386 has more complex instructions than 80286:
        - Variable length (1-15 bytes)
        - 32-bit operands
        - More addressing modes
        """
        base_decode = self.decode_cycles
        
        # Longer instructions take longer to decode (on average)
        # Model as 10% overhead for 32-bit vs 16-bit (reduced from 20%)
        complexity_factor = 1.05
        
        return base_decode * complexity_factor
    
    def compute_address_calc_service_time(self) -> float:
        """
        Address calculation: Segmentation + Paging + TLB.
        
        80386 adds paging on top of segmentation.
        """
        base_address_calc = self.address_calc_cycles
        
        # Segmentation overhead (carried over from 80286)
        segment_overhead = self.p_segment_ops * self.segment_translation_cycles
        
        # Paging overhead (new in 80386)
        paging_overhead = self.compute_paging_overhead()
        
        total = base_address_calc + segment_overhead + paging_overhead
        return total
    
    def compute_execute_service_time(self) -> float:
        """
        Execute stage: 32-bit ALU, multiply, divide.
        
        80386 improvements over 80286:
        - 32-bit operations (not just 16-bit)
        - Faster multiply: 9-22 cycles (vs 13 cycles on 80286)
        - Faster divide: 14-43 cycles (vs 17 cycles on 80286)
        """
        # Instruction latencies (80386 is faster than 80286)
        alu_cycles = self.execute_cycles  # 2 cycles typical
        mul_cycles = 9   # 32-bit multiply (best case)
        div_cycles = 14  # 32-bit divide (best case)
        
        # Weighted average
        weighted_cycles = (
            self.p_alu * alu_cycles +
            self.p_mul * mul_cycles +
            self.p_div * div_cycles +
            (1 - self.p_alu - self.p_mul - self.p_div) * alu_cycles
        )
        
        return weighted_cycles
    
    def compute_memory_service_time(self) -> float:
        """
        Memory access stage: Load/store with cache.
        
        80386 adds cache, dramatically improving memory performance.
        """
        p_memory = self.p_load + self.p_store
        
        if p_memory == 0:
            return 0.1  # Minimal passthrough
        
        # Get effective memory latency (including cache)
        cache_metrics = self.compute_cache_effective_latency(is_instruction=False)
        
        # Memory operations use effective latency
        service_time = p_memory * cache_metrics.effective_latency
        
        return max(service_time, 0.1)
    
    def compute_writeback_service_time(self) -> float:
        """Writeback stage: Update 32-bit registers."""
        return self.writeback_cycles
    
    def compute_stage_metrics(self, arrival_rate: float) -> List[QueueMetrics]:
        """
        Compute metrics for all pipeline stages.
        
        Returns list of QueueMetrics for each stage.
        """
        metrics = []
        
        # Stage 0: Prefetch Queue (parallel, bounded)
        prefetch = self.compute_prefetch_metrics(arrival_rate)
        metrics.append(prefetch)
        
        # Stages 1-6: Series pipeline
        stage_configs = [
            ("Fetch", self.compute_fetch_service_time()),
            ("Decode", self.compute_decode_service_time()),
            ("Address_Calc", self.compute_address_calc_service_time()),
            ("Execute", self.compute_execute_service_time()),
            ("Memory_Access", self.compute_memory_service_time()),
            ("Writeback", self.compute_writeback_service_time())
        ]
        
        for name, service_time in stage_configs:
            utilization = arrival_rate * service_time
            
            if utilization >= 1.0:
                queue_length = float('inf')
                wait_time = float('inf')
            else:
                queue_length = utilization / (1 - utilization)
                wait_time = service_time / (1 - utilization)
            
            response_time = wait_time + service_time
            
            metrics.append(QueueMetrics(
                name=name,
                arrival_rate=arrival_rate,
                service_time=service_time,
                utilization=utilization,
                queue_length=queue_length,
                wait_time=wait_time,
                response_time=response_time
            ))
        
        return metrics
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        """
        Predict IPC for given arrival rate.
        
        Returns:
            (predicted_ipc, stage_metrics)
        """
        metrics = self.compute_stage_metrics(arrival_rate)
        
        # Check for instability
        max_util = max(m.utilization for m in metrics)
        if max_util >= 1.0:
            return 0.0, metrics
        
        # Get execution unit stages (exclude prefetch which is parallel)
        eu_stages = [m for m in metrics if m.name != "Prefetch_Queue_BIU"]
        
        # For a pipeline, steady-state throughput = arrival_rate (if stable)
        # IPC is essentially the arrival rate that the system can sustain
        # The bottleneck limits the maximum throughput
        
        # Find bottleneck utilization
        bottleneck = max(eu_stages, key=lambda m: m.utilization)
        
        # If bottleneck utilization is ρ, then max throughput is approximately:
        # throughput ≈ (1 - ρ) × (1 / S_bottleneck)
        # But for our model, we're given arrival rate and predict what IPC results
        
        # Simplified approach: IPC ≈ throughput ≈ arrival_rate × efficiency
        # where efficiency accounts for pipeline stalls
        
        # Calculate efficiency based on utilizations
        avg_utilization = np.mean([m.utilization for m in eu_stages])
        
        # Pipeline efficiency factor (1.0 = perfect, 0 = completely stalled)
        # As utilization increases, efficiency decreases due to queueing
        efficiency = 1.0 / (1.0 + avg_utilization)
        
        # Predicted IPC = arrival_rate × efficiency
        predicted_ipc = arrival_rate * efficiency
        
        # Cap at theoretical maximum (1.0 for in-order single-issue)
        predicted_ipc = min(predicted_ipc, 1.0)
        
        return predicted_ipc, metrics
    
    def find_bottleneck(self, metrics: List[QueueMetrics]) -> str:
        """Identify bottleneck stage (highest utilization)."""
        bottleneck = max(metrics, key=lambda m: m.utilization)
        return bottleneck.name
    
    def calibrate(self,
                  measured_ipc: float,
                  initial_arrival_rate: float = 0.5,
                  tolerance_percent: float = 2.0,
                  max_iterations: int = 50) -> CalibrationResult:
        """
        Calibrate model to match measured IPC.
        
        Uses binary search on arrival rate.
        """
        low = 0.01
        high = 0.95
        arrival_rate = initial_arrival_rate
        
        best_error = float('inf')
        best_rate = arrival_rate
        best_metrics = None
        
        for iteration in range(max_iterations):
            predicted_ipc, metrics = self.predict_ipc(arrival_rate)
            
            error_percent = abs(predicted_ipc - measured_ipc) / measured_ipc * 100
            
            if error_percent < best_error:
                best_error = error_percent
                best_rate = arrival_rate
                best_metrics = metrics
            
            if error_percent <= tolerance_percent:
                cache_metrics = self.compute_cache_effective_latency(is_instruction=True)
                return CalibrationResult(
                    predicted_ipc=predicted_ipc,
                    measured_ipc=measured_ipc,
                    error_percent=error_percent,
                    iterations=iteration + 1,
                    converged=True,
                    bottleneck_stage=self.find_bottleneck(metrics),
                    stage_metrics=metrics,
                    cache_metrics=cache_metrics
                )
            
            # Binary search
            if predicted_ipc < measured_ipc:
                low = arrival_rate
            else:
                high = arrival_rate
            
            arrival_rate = (low + high) / 2.0
            
            if abs(high - low) < 1e-6:
                break
        
        cache_metrics = self.compute_cache_effective_latency(is_instruction=True)
        
        # Calculate IPC for best metrics
        if best_metrics:
            eu_stages = [m for m in best_metrics if m.name != "Prefetch_Queue_BIU"]
            avg_util = np.mean([m.utilization for m in eu_stages])
            efficiency = 1.0 / (1.0 + avg_util)
            best_ipc = min(best_rate * efficiency, 1.0)
        else:
            best_ipc = 0.0
        
        return CalibrationResult(
            predicted_ipc=best_ipc,
            measured_ipc=measured_ipc,
            error_percent=best_error,
            iterations=max_iterations,
            converged=False,
            bottleneck_stage=best_metrics and self.find_bottleneck(best_metrics),
            stage_metrics=best_metrics or [],
            cache_metrics=cache_metrics
        )
    
    def print_metrics(self, metrics: List[QueueMetrics]):
        """Pretty print stage metrics."""
        print("\n" + "="*80)
        print("Intel 80386 CPU Pipeline Metrics")
        print("="*80)
        print(f"{'Stage':<25} {'λ':>8} {'S':>8} {'ρ':>8} {'L':>8} {'W':>8} {'R':>8}")
        print(f"{'':25} {'(ins/c)':>8} {'(cyc)':>8} {'':>8} {'(ins)':>8} {'(cyc)':>8} {'(cyc)':>8}")
        print("-"*80)
        
        for m in metrics:
            l_str = f"{m.queue_length:.2f}" if m.queue_length != float('inf') else "inf"
            w_str = f"{m.wait_time:.2f}" if m.wait_time != float('inf') else "inf"
            r_str = f"{m.response_time:.2f}" if m.response_time != float('inf') else "inf"
            
            print(f"{m.name:<25} {m.arrival_rate:>8.4f} {m.service_time:>8.2f} "
                  f"{m.utilization:>8.4f} {l_str:>8} {w_str:>8} {r_str:>8}")
        
        print("="*80)
        
        # Print bottleneck
        bottleneck = max(metrics, key=lambda m: m.utilization)
        print(f"\nBottleneck: {bottleneck.name} (ρ = {bottleneck.utilization:.4f})")
        
        # Print cache stats if enabled
        if self.has_cache:
            cache_i = self.compute_cache_effective_latency(is_instruction=True)
            cache_d = self.compute_cache_effective_latency(is_instruction=False)
            print(f"\nCache Performance:")
            print(f"  Instruction Cache: {cache_i.hit_rate*100:.1f}% hit rate, "
                  f"{cache_i.effective_latency:.2f} cycles effective latency")
            print(f"  Data Cache:        {cache_d.hit_rate*100:.1f}% hit rate, "
                  f"{cache_d.effective_latency:.2f} cycles effective latency")
        
        # Print paging stats if enabled
        if self.paging_enabled:
            paging_overhead = self.compute_paging_overhead()
            print(f"\nPaging Performance:")
            print(f"  TLB Hit Rate:      {self.tlb_hit_rate*100:.1f}%")
            print(f"  Paging Overhead:   {paging_overhead:.2f} cycles average")
        
        # Print total metrics
        eu_stages = [m for m in metrics if m.name != "Prefetch_Queue_BIU"]
        avg_utilization = np.mean([m.utilization for m in eu_stages])
        efficiency = 1.0 / (1.0 + avg_utilization)
        
        # Get arrival rate from first metric
        arrival_rate = metrics[0].arrival_rate
        predicted_ipc = arrival_rate * efficiency
        predicted_ipc = min(predicted_ipc, 1.0)
        
        print(f"\nAverage Utilization: {avg_utilization:.4f}")
        print(f"Pipeline Efficiency: {efficiency:.4f}")
        print(f"Predicted IPC:       {predicted_ipc:.4f}")
        print()


def main():
    """Example usage of the 80386 model."""
    print("Intel 80386 CPU Queueing Model")
    print("="*80)
    
    # Load model
    model = Intel80386QueueModel('80386_cpu_model.json')
    
    # Example 1: Predict IPC at different arrival rates
    print("\nExample 1: IPC Prediction at Different Load Levels")
    print("-"*80)
    
    for arrival_rate in [0.3, 0.5, 0.7, 0.9]:
        ipc, metrics = model.predict_ipc(arrival_rate)
        bottleneck = model.find_bottleneck(metrics)
        print(f"Arrival Rate: {arrival_rate:.2f} → IPC: {ipc:.4f}, "
              f"Bottleneck: {bottleneck}")
    
    # Example 2: Full metrics at moderate load
    print("\nExample 2: Detailed Metrics at 50% Load")
    ipc, metrics = model.predict_ipc(0.5)
    model.print_metrics(metrics)
    
    # Example 3: Cache impact analysis
    print("\nExample 3: Cache Impact Analysis")
    print("-"*80)
    
    # Without cache
    model.has_cache = False
    ipc_no_cache, _ = model.predict_ipc(0.5)
    
    # With cache
    model.has_cache = True
    ipc_with_cache, _ = model.predict_ipc(0.5)
    
    speedup = ipc_with_cache / ipc_no_cache if ipc_no_cache > 0 else 0
    print(f"IPC without cache: {ipc_no_cache:.4f}")
    print(f"IPC with cache:    {ipc_with_cache:.4f}")
    print(f"Cache speedup:     {speedup:.2f}x")
    
    # Example 4: Paging overhead analysis
    print("\nExample 4: Paging Overhead Analysis")
    print("-"*80)
    
    # Without paging
    model.paging_enabled = False
    ipc_no_paging, _ = model.predict_ipc(0.5)
    
    # With paging
    model.paging_enabled = True
    ipc_with_paging, _ = model.predict_ipc(0.5)
    
    overhead_percent = (1 - ipc_with_paging / ipc_no_paging) * 100 if ipc_no_paging > 0 else 0
    print(f"IPC without paging: {ipc_no_paging:.4f}")
    print(f"IPC with paging:    {ipc_with_paging:.4f}")
    print(f"Paging overhead:    {overhead_percent:.1f}%")
    
    # Example 5: Calibration
    print("\nExample 5: Model Calibration")
    print("-"*80)
    
    measured_ipc = 0.85  # Example measured IPC
    result = model.calibrate(measured_ipc, tolerance_percent=2.0)
    
    print(f"Target IPC:     {result.measured_ipc:.4f}")
    print(f"Predicted IPC:  {result.predicted_ipc:.4f}")
    print(f"Error:          {result.error_percent:.2f}%")
    print(f"Iterations:     {result.iterations}")
    print(f"Converged:      {result.converged}")
    print(f"Bottleneck:     {result.bottleneck_stage}")


if __name__ == "__main__":
    main()
