#!/usr/bin/env python3
"""
Intel 8088 CPU Queueing Model - Python Implementation

This module implements a grey-box queueing model for the Intel 8088 microprocessor,
the CPU used in the original IBM PC. The model captures:

- 4-byte prefetch queue
- 8-bit external data bus bottleneck
- Bus Interface Unit (BIU) and Execution Unit (EU) interaction
- Instruction fetch/execute pipelining
- Queue flush penalties on branches

Author: Grey-Box Performance Modeling Research
Date: January 23, 2026
Version: 1.0
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class QueueState(Enum):
    """Prefetch queue state"""
    EMPTY = 0
    PARTIAL = 1
    FULL = 2


@dataclass
class InstructionTiming:
    """Timing information for one instruction type"""
    mnemonic: str
    base_cycles: float
    frequency: float
    instruction_bytes: int
    queue_flush: bool = False
    memory_access: bool = False
    effective_address_cycles: int = 0


@dataclass
class SimulationResult:
    """Results from model simulation"""
    total_cycles: int
    total_instructions: int
    ipc: float
    cpi: float
    fetch_cycles: int
    execute_cycles: int
    stall_cycles: int
    branch_penalty_cycles: int
    memory_cycles: int
    queue_utilization_avg: float
    biu_utilization: float
    eu_utilization: float
    bottleneck: str


class PrefetchQueue:
    """
    Models the Intel 8088's 4-byte prefetch queue.
    
    The queue operates as a FIFO buffer between the BIU (fetch) and EU (execute).
    The BIU fills the queue opportunistically when the bus is available.
    The EU drains the queue as it decodes and executes instructions.
    """
    
    def __init__(self, size: int = 4):
        """
        Initialize prefetch queue.
        
        Args:
            size: Queue capacity in bytes (4 for 8088, 6 for 8086)
        """
        self.size = size
        self.occupancy = 0
        self.total_bytes_fetched = 0
        self.total_bytes_drained = 0
        self.flush_count = 0
        
    def can_fetch(self) -> bool:
        """Check if BIU can fetch into queue"""
        return self.occupancy < self.size
    
    def fetch_byte(self):
        """Add one byte to queue (called by BIU)"""
        if self.can_fetch():
            self.occupancy += 1
            self.total_bytes_fetched += 1
    
    def drain_bytes(self, count: int) -> int:
        """
        Remove bytes from queue (called by EU).
        
        Args:
            count: Number of bytes to drain
            
        Returns:
            Number of bytes actually drained
        """
        actual = min(count, self.occupancy)
        self.occupancy -= actual
        self.total_bytes_drained += actual
        return actual
    
    def flush(self):
        """Flush queue (called on branch/interrupt)"""
        self.occupancy = 0
        self.flush_count += 1
    
    def get_state(self) -> QueueState:
        """Get current queue state"""
        if self.occupancy == 0:
            return QueueState.EMPTY
        elif self.occupancy == self.size:
            return QueueState.FULL
        else:
            return QueueState.PARTIAL
    
    def utilization(self) -> float:
        """Calculate average queue utilization"""
        return self.occupancy / self.size


class BusInterfaceUnit:
    """
    Models the 8088's Bus Interface Unit (BIU).
    
    The BIU is responsible for:
    - Fetching instruction bytes from memory
    - Filling the prefetch queue
    - Handling memory reads/writes for the EU
    - Managing bus cycles (4 clocks per byte)
    """
    
    def __init__(self, clock_mhz: float, cycles_per_fetch: int = 4, 
                 wait_states: int = 0):
        """
        Initialize BIU.
        
        Args:
            clock_mhz: CPU clock frequency in MHz
            cycles_per_fetch: Clock cycles per byte fetch (4 for 8088)
            wait_states: Additional wait states per bus cycle
        """
        self.clock_mhz = clock_mhz
        self.cycles_per_fetch = cycles_per_fetch + wait_states
        self.total_fetch_cycles = 0
        self.total_fetches = 0
        self.bus_blocked = False  # True when EU is using bus
        
    def fetch_cycle(self, queue: PrefetchQueue) -> int:
        """
        Perform one fetch cycle if possible.
        
        Args:
            queue: The prefetch queue to fill
            
        Returns:
            Number of cycles consumed (0 if fetch blocked)
        """
        if self.bus_blocked or not queue.can_fetch():
            return 0
        
        queue.fetch_byte()
        self.total_fetch_cycles += self.cycles_per_fetch
        self.total_fetches += 1
        return self.cycles_per_fetch
    
    def memory_access(self, num_bytes: int) -> int:
        """
        Perform EU-requested memory access.
        
        Args:
            num_bytes: Number of bytes to transfer
            
        Returns:
            Number of cycles consumed
        """
        cycles = num_bytes * self.cycles_per_fetch
        self.total_fetch_cycles += cycles
        return cycles
    
    def utilization(self, total_cycles: int) -> float:
        """Calculate BIU utilization"""
        return self.total_fetch_cycles / total_cycles if total_cycles > 0 else 0.0


class ExecutionUnit:
    """
    Models the 8088's Execution Unit (EU).
    
    The EU is responsible for:
    - Reading instruction bytes from prefetch queue
    - Decoding instructions
    - Executing operations (ALU, memory access, etc.)
    - Updating registers and flags
    """
    
    def __init__(self, instruction_mix: Dict[str, InstructionTiming]):
        """
        Initialize EU.
        
        Args:
            instruction_mix: Dictionary of instruction types and their timings
        """
        self.instruction_mix = instruction_mix
        self.total_execute_cycles = 0
        self.total_instructions = 0
        self.total_memory_ops = 0
        
    def execute_instruction(self, instr_type: str, queue: PrefetchQueue, 
                           biu: BusInterfaceUnit) -> Dict[str, int]:
        """
        Execute one instruction.
        
        Args:
            instr_type: Type of instruction to execute
            queue: Prefetch queue to drain bytes from
            biu: BIU for memory operations
            
        Returns:
            Dictionary with cycle breakdown:
                - fetch: Cycles waiting for instruction bytes
                - execute: Base execution cycles
                - memory: Memory access cycles
                - stall: Queue underflow stall cycles
                - branch: Branch penalty cycles
        """
        instr = self.instruction_mix[instr_type]
        
        result = {
            'fetch': 0,
            'execute': 0,
            'memory': 0,
            'stall': 0,
            'branch': 0
        }
        
        # Step 1: Drain instruction bytes from queue
        bytes_needed = instr.instruction_bytes
        stall_cycles = 0
        
        while bytes_needed > 0:
            drained = queue.drain_bytes(bytes_needed)
            bytes_needed -= drained
            
            if bytes_needed > 0:
                # Queue empty, must wait for BIU fetch
                # In real 8088, EU stalls 1 cycle at a time
                stall_cycles += 1
                # BIU will fetch in parallel (handled in main simulation loop)
        
        result['stall'] = stall_cycles
        
        # Step 2: Execute instruction base cycles
        result['execute'] = int(instr.base_cycles)
        
        # Step 3: Memory operand access (if applicable)
        if instr.memory_access:
            biu.bus_blocked = True
            # Memory operations: EA calculation + memory access
            result['memory'] = (instr.effective_address_cycles + 
                               biu.memory_access(2))  # Assume 16-bit operand
            biu.bus_blocked = False
            self.total_memory_ops += 1
        
        # Step 4: Branch penalty (queue flush)
        if instr.queue_flush:
            queue.flush()
            # Must refill queue before next instruction can start
            # Minimum 2 bytes needed (typical shortest instruction)
            result['branch'] = biu.cycles_per_fetch * 2
        
        self.total_execute_cycles += (result['execute'] + result['memory'] + 
                                     result['stall'] + result['branch'])
        self.total_instructions += 1
        
        return result
    
    def utilization(self, total_cycles: int) -> float:
        """Calculate EU utilization"""
        return self.total_execute_cycles / total_cycles if total_cycles > 0 else 0.0


class Intel8088Model:
    """
    Complete Intel 8088 queueing model.
    
    This class orchestrates the BIU, EU, and prefetch queue to simulate
    instruction execution and predict performance (IPC/CPI).
    """
    
    def __init__(self, config_file: str):
        """
        Initialize model from configuration file.
        
        Args:
            config_file: Path to JSON configuration file
        """
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Extract parameters
        arch = self.config['architecture']
        self.clock_mhz = arch['clock_frequency_mhz']
        
        bus = self.config['bus_timing']
        self.cycles_per_bus = bus['cycles_per_bus_cycle']
        self.wait_states = bus['wait_states']['ram_typical']
        
        queue_cfg = self.config['pipeline_structure']['prefetch_queue']
        self.queue_size = queue_cfg['size_bytes']
        
        # Build instruction mix
        self.instruction_mix = self._build_instruction_mix()
        
        # Initialize components
        self.queue = PrefetchQueue(self.queue_size)
        self.biu = BusInterfaceUnit(self.clock_mhz, self.cycles_per_bus, 
                                     self.wait_states)
        self.eu = ExecutionUnit(self.instruction_mix)
        
        # Statistics
        self.cycle_history = []
        self.queue_occupancy_history = []
    
    def _build_instruction_mix(self) -> Dict[str, InstructionTiming]:
        """Build instruction mix from configuration"""
        mix = {}
        
        for instr_type, details in self.config['instruction_mix'].items():
            if instr_type == 'description' or instr_type == 'source':
                continue
            
            # Handle instructions with variable timing (min/max/avg)
            if 'base_cycles_avg' in details:
                base_cycles = details['base_cycles_avg']
            else:
                base_cycles = details['base_cycles']
            
            # Check for queue flush (branches)
            queue_flush = details.get('queue_flush_penalty', 0) > 0
            
            # Check for memory access
            memory_access = 'memory' in instr_type or 'effective_address_cycles' in details
            ea_cycles = details.get('effective_address_cycles', 0)
            
            mix[instr_type] = InstructionTiming(
                mnemonic=details.get('mnemonic', instr_type),
                base_cycles=base_cycles,
                frequency=details['frequency'],
                instruction_bytes=details['instruction_bytes'],
                queue_flush=queue_flush,
                memory_access=memory_access,
                effective_address_cycles=ea_cycles
            )
        
        return mix
    
    def simulate(self, num_instructions: int, verbose: bool = False) -> SimulationResult:
        """
        Simulate execution of instructions.
        
        Args:
            num_instructions: Number of instructions to simulate
            verbose: Print detailed cycle-by-cycle information
            
        Returns:
            SimulationResult with performance metrics
        """
        # Reset statistics
        total_cycles = 0
        fetch_cycles = 0
        execute_cycles = 0
        stall_cycles = 0
        branch_penalty_cycles = 0
        memory_cycles = 0
        
        self.queue = PrefetchQueue(self.queue_size)
        self.biu = BusInterfaceUnit(self.clock_mhz, self.cycles_per_bus, 
                                     self.wait_states)
        self.eu = ExecutionUnit(self.instruction_mix)
        
        # Generate instruction stream based on mix
        instruction_stream = self._generate_instruction_stream(num_instructions)
        
        for i, instr_type in enumerate(instruction_stream):
            if verbose and i < 10:
                print(f"\n--- Instruction {i}: {instr_type} ---")
                print(f"Queue occupancy: {self.queue.occupancy}/{self.queue.size}")
            
            # Execute instruction
            breakdown = self.eu.execute_instruction(instr_type, self.queue, self.biu)
            
            # During instruction execution, BIU can fetch in parallel
            # Simulate opportunistic prefetching
            parallel_cycles = breakdown['execute']
            while parallel_cycles > 0 and self.queue.can_fetch():
                if not self.biu.bus_blocked:
                    fetch_time = self.biu.fetch_cycle(self.queue)
                    if fetch_time > 0:
                        parallel_cycles -= fetch_time
                        fetch_cycles += fetch_time
                    else:
                        break
                else:
                    break
            
            # Accumulate statistics
            execute_cycles += breakdown['execute']
            stall_cycles += breakdown['stall']
            branch_penalty_cycles += breakdown['branch']
            memory_cycles += breakdown['memory']
            
            instr_total = sum(breakdown.values())
            total_cycles += instr_total
            
            # Record history
            self.queue_occupancy_history.append(self.queue.occupancy)
            
            if verbose and i < 10:
                print(f"Breakdown: {breakdown}")
                print(f"Total cycles: {instr_total}")
        
        # Calculate metrics
        ipc = num_instructions / total_cycles if total_cycles > 0 else 0.0
        cpi = total_cycles / num_instructions if num_instructions > 0 else 0.0
        
        queue_util = np.mean(self.queue_occupancy_history) / self.queue_size
        biu_util = self.biu.utilization(total_cycles)
        eu_util = self.eu.utilization(total_cycles)
        
        # Identify bottleneck
        bottleneck = self._identify_bottleneck(biu_util, eu_util, queue_util)
        
        return SimulationResult(
            total_cycles=total_cycles,
            total_instructions=num_instructions,
            ipc=ipc,
            cpi=cpi,
            fetch_cycles=fetch_cycles,
            execute_cycles=execute_cycles,
            stall_cycles=stall_cycles,
            branch_penalty_cycles=branch_penalty_cycles,
            memory_cycles=memory_cycles,
            queue_utilization_avg=queue_util,
            biu_utilization=biu_util,
            eu_utilization=eu_util,
            bottleneck=bottleneck
        )
    
    def _generate_instruction_stream(self, count: int) -> List[str]:
        """Generate random instruction stream based on frequency distribution"""
        types = list(self.instruction_mix.keys())
        freqs = [instr.frequency for instr in self.instruction_mix.values()]
        
        # Normalize frequencies
        total_freq = sum(freqs)
        probs = [f / total_freq for f in freqs]
        
        return np.random.choice(types, size=count, p=probs).tolist()
    
    def _identify_bottleneck(self, biu_util: float, eu_util: float, 
                            queue_util: float) -> str:
        """Identify primary performance bottleneck"""
        if eu_util > 0.85:
            return "Execution Unit (EU)"
        elif biu_util > 0.85:
            return "Bus Interface Unit (BIU) - Memory Bandwidth"
        elif queue_util < 0.3:
            return "Prefetch Queue Underflow"
        elif biu_util > eu_util:
            return "BIU (8-bit bus bottleneck)"
        else:
            return "Balanced (no clear bottleneck)"
    
    def calibrate(self, measured_ipc: float, tolerance: float = 0.05, 
                  max_iterations: int = 20) -> Dict:
        """
        Calibrate model to match measured IPC.
        
        Args:
            measured_ipc: IPC measured from real system or emulator
            tolerance: Acceptable error as fraction (0.05 = 5%)
            max_iterations: Maximum calibration iterations
            
        Returns:
            Dictionary with calibration results
        """
        best_error = float('inf')
        best_wait_states = self.wait_states
        
        for iteration in range(max_iterations):
            # Run simulation
            result = self.simulate(num_instructions=10000)
            predicted_ipc = result.ipc
            
            error = abs(predicted_ipc - measured_ipc) / measured_ipc
            
            print(f"Iteration {iteration + 1}: "
                  f"Predicted IPC={predicted_ipc:.4f}, "
                  f"Error={error*100:.2f}%")
            
            if error < tolerance:
                print(f"✓ Calibration converged in {iteration + 1} iterations")
                return {
                    'converged': True,
                    'iterations': iteration + 1,
                    'final_error_percent': error * 100,
                    'predicted_ipc': predicted_ipc,
                    'measured_ipc': measured_ipc,
                    'calibrated_wait_states': self.wait_states
                }
            
            if error < best_error:
                best_error = error
                best_wait_states = self.wait_states
            
            # Adjust wait states (simple gradient descent)
            if predicted_ipc > measured_ipc:
                # Model too fast, add wait states
                self.wait_states += 0.1
            else:
                # Model too slow, reduce wait states
                self.wait_states = max(0, self.wait_states - 0.1)
            
            # Reinitialize BIU with new wait states
            self.biu = BusInterfaceUnit(self.clock_mhz, self.cycles_per_bus, 
                                        self.wait_states)
        
        print(f"✗ Calibration did not converge in {max_iterations} iterations")
        print(f"Best error: {best_error*100:.2f}%")
        
        return {
            'converged': False,
            'iterations': max_iterations,
            'final_error_percent': best_error * 100,
            'predicted_ipc': result.ipc,
            'measured_ipc': measured_ipc,
            'calibrated_wait_states': best_wait_states
        }
    
    def print_report(self, result: SimulationResult):
        """Print detailed simulation report"""
        print("\n" + "=" * 70)
        print("Intel 8088 CPU Queueing Model - Simulation Report")
        print("=" * 70)
        
        print(f"\nArchitecture: {self.config['architecture']['cpu_model']}")
        print(f"Clock Frequency: {self.clock_mhz} MHz")
        print(f"Queue Size: {self.queue_size} bytes")
        print(f"Bus Width: {self.config['architecture']['data_bus_width_bits']} bits")
        
        print(f"\n--- Performance Metrics ---")
        print(f"Instructions Executed: {result.total_instructions:,}")
        print(f"Total Cycles: {result.total_cycles:,}")
        print(f"IPC (Instructions Per Cycle): {result.ipc:.4f}")
        print(f"CPI (Cycles Per Instruction): {result.cpi:.2f}")
        print(f"MIPS: {result.ipc * self.clock_mhz:.3f}")
        
        print(f"\n--- Cycle Breakdown ---")
        print(f"Fetch Cycles: {result.fetch_cycles:,} "
              f"({result.fetch_cycles/result.total_cycles*100:.1f}%)")
        print(f"Execute Cycles: {result.execute_cycles:,} "
              f"({result.execute_cycles/result.total_cycles*100:.1f}%)")
        print(f"Memory Access Cycles: {result.memory_cycles:,} "
              f"({result.memory_cycles/result.total_cycles*100:.1f}%)")
        print(f"Stall Cycles (Queue Empty): {result.stall_cycles:,} "
              f"({result.stall_cycles/result.total_cycles*100:.1f}%)")
        print(f"Branch Penalty Cycles: {result.branch_penalty_cycles:,} "
              f"({result.branch_penalty_cycles/result.total_cycles*100:.1f}%)")
        
        print(f"\n--- Component Utilization ---")
        print(f"Prefetch Queue: {result.queue_utilization_avg*100:.1f}%")
        print(f"Bus Interface Unit (BIU): {result.biu_utilization*100:.1f}%")
        print(f"Execution Unit (EU): {result.eu_utilization*100:.1f}%")
        
        print(f"\n--- Bottleneck Analysis ---")
        print(f"Primary Bottleneck: {result.bottleneck}")
        
        print("\n" + "=" * 70 + "\n")


def main():
    """Example usage of Intel 8088 model"""
    
    print("Intel 8088 CPU Queueing Model - Example")
    print("-" * 50)
    
    # Load model
    model = Intel8088Model('intel_8088_model.json')
    
    # Run simulation
    print("\nRunning simulation with 100,000 instructions...")
    result = model.simulate(num_instructions=100000, verbose=False)
    
    # Print report
    model.print_report(result)
    
    # Example calibration
    print("\n" + "=" * 70)
    print("Calibration Example")
    print("=" * 70)
    print("\nSimulating calibration to Dhrystone benchmark...")
    print("Target IPC: 0.318 (measured from real IBM PC)")
    
    calibration = model.calibrate(measured_ipc=0.318, tolerance=0.02, 
                                  max_iterations=15)
    
    if calibration['converged']:
        print(f"\n✓ Model calibrated successfully!")
        print(f"Final error: {calibration['final_error_percent']:.2f}%")
        print(f"Calibrated wait states: {calibration['calibrated_wait_states']:.2f}")
    else:
        print(f"\n✗ Calibration incomplete")
        print(f"Best error: {calibration['final_error_percent']:.2f}%")


if __name__ == '__main__':
    main()
