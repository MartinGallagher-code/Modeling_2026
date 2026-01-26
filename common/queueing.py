"""M/M/1 Queueing Analysis for Microprocessor Performance Models.

This module provides queueing theory based analysis for CPU performance modeling.
It implements M/M/1 queue analysis for fetch, decode, execute, and memory stages.
"""

from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple, Union


@dataclass
class QueueingResult:
    """Results from queueing analysis."""
    ips: float                      # Instructions per second
    cpi: float                      # Cycles per instruction
    utilization: float              # Overall system utilization
    throughput: float               # Instructions per cycle
    avg_queue_length: float         # Average queue depth
    avg_response_time: float        # Average instruction latency
    bottleneck: str                 # Identified bottleneck
    bottleneck_utilization: float   # Utilization at bottleneck
    stage_utilizations: Dict[str, float]  # Per-stage utilizations


def mm1_utilization(arrival_rate: float, service_rate: float) -> float:
    """Calculate M/M/1 utilization (ρ = λ/μ)."""
    if service_rate <= 0:
        return 1.0
    return min(arrival_rate / service_rate, 0.999)


def mm1_response_time(arrival_rate: float, service_rate: float) -> float:
    """Calculate M/M/1 average response time (W = 1/(μ-λ))."""
    if service_rate <= arrival_rate:
        return float('inf')
    return 1.0 / (service_rate - arrival_rate)


def mm1_queue_length(arrival_rate: float, service_rate: float) -> float:
    """Calculate M/M/1 average queue length (L = ρ/(1-ρ))."""
    rho = mm1_utilization(arrival_rate, service_rate)
    if rho >= 0.999:
        return float('inf')
    return rho / (1.0 - rho)


def mm1_wait_time(arrival_rate: float, service_rate: float) -> float:
    """Calculate M/M/1 average wait time in queue (Wq = ρ/(μ-λ))."""
    if service_rate <= arrival_rate:
        return float('inf')
    rho = mm1_utilization(arrival_rate, service_rate)
    return rho / (service_rate - arrival_rate)


class QueueingModel:
    """M/M/1 queueing model for CPU performance analysis."""
    
    def __init__(
        self,
        clock_mhz: float,
        timing_categories: Dict[str, Dict],
        bus_width: int = 8,
        prefetch_depth: int = 0,
        cache_size: int = 0,
        pipeline_stages: int = 1,
        memory_wait_states: int = 0
    ):
        """Initialize queueing model.
        
        Args:
            clock_mhz: Clock frequency in MHz
            timing_categories: Dict of category -> {cycles, weight, description}
            bus_width: Data bus width in bits
            prefetch_depth: Prefetch queue depth in bytes (0 = no prefetch)
            cache_size: Instruction cache size in bytes (0 = no cache)
            pipeline_stages: Number of pipeline stages (1 = no pipelining)
            memory_wait_states: Additional memory wait states
        """
        self.clock_mhz = clock_mhz
        self.clock_hz = clock_mhz * 1_000_000
        self.timing_categories = timing_categories
        self.bus_width = bus_width
        self.prefetch_depth = prefetch_depth
        self.cache_size = cache_size
        self.pipeline_stages = pipeline_stages
        self.memory_wait_states = memory_wait_states
    
    def weighted_cpi(self, workload: Dict[str, float]) -> float:
        """Calculate weighted CPI for a workload.
        
        Args:
            workload: Dict of category -> weight (must sum to ~1.0)
            
        Returns:
            Weighted average cycles per instruction
        """
        total_cpi = 0.0
        total_weight = 0.0
        
        for category, weight in workload.items():
            if category in self.timing_categories:
                cycles = self.timing_categories[category].get('cycles', 4)
                total_cpi += cycles * weight
                total_weight += weight
        
        if total_weight > 0:
            return total_cpi / total_weight
        return sum(c.get('cycles', 4) for c in self.timing_categories.values()) / len(self.timing_categories)
    
    def calculate_ips(self, workload: Dict[str, float]) -> float:
        """Calculate instructions per second.
        
        Args:
            workload: Dict of category -> weight
            
        Returns:
            Instructions per second
        """
        cpi = self.weighted_cpi(workload)
        return self.clock_hz / cpi
    
    def _analyze_fetch_stage(self, cpi: float) -> Tuple[float, float]:
        """Analyze instruction fetch stage utilization."""
        # Average instruction size estimate
        avg_instr_size = 2.0  # bytes, typical for 8-bit CPUs
        if self.bus_width >= 16:
            avg_instr_size = 3.0
        if self.bus_width >= 32:
            avg_instr_size = 4.0
            
        # Fetch cycles needed
        bytes_per_fetch = self.bus_width / 8
        fetches_per_instr = avg_instr_size / bytes_per_fetch
        
        # With prefetch queue
        if self.prefetch_depth > 0:
            # Prefetch reduces effective fetch time
            prefetch_benefit = min(1.0, self.prefetch_depth / (avg_instr_size * 4))
            fetches_per_instr *= (1.0 - prefetch_benefit * 0.5)
        
        fetch_cycles = fetches_per_instr * (1 + self.memory_wait_states)
        fetch_utilization = fetch_cycles / max(cpi, 1)
        
        return fetch_utilization, fetch_cycles
    
    def _analyze_decode_stage(self, cpi: float, workload: Dict[str, float]) -> Tuple[float, float]:
        """Analyze instruction decode stage utilization."""
        # Estimate decode complexity from instruction mix
        complex_weight = 0.0
        for cat, weight in workload.items():
            if any(x in cat.lower() for x in ['call', 'return', 'mul', 'div', 'string']):
                complex_weight += weight * 2.0
            elif any(x in cat.lower() for x in ['branch', 'jump', 'memory']):
                complex_weight += weight * 1.2
            else:
                complex_weight += weight * 1.0
        
        # Decode typically takes 1-2 cycles for simple CPUs
        decode_cycles = 1.0 + complex_weight * 0.5
        decode_utilization = decode_cycles / max(cpi, 1)
        
        return decode_utilization, decode_cycles
    
    def _analyze_execute_stage(self, cpi: float, workload: Dict[str, float]) -> Tuple[float, float]:
        """Analyze execute stage utilization."""
        # Calculate execution cycles from timing categories
        exec_cycles = 0.0
        for cat, weight in workload.items():
            if cat in self.timing_categories:
                base_cycles = self.timing_categories[cat].get('cycles', 4)
                # Remove fetch overhead estimate
                exec_only = max(base_cycles - 2, 1)
                exec_cycles += exec_only * weight
        
        exec_utilization = exec_cycles / max(cpi, 1)
        return exec_utilization, exec_cycles
    
    def _analyze_memory_stage(self, cpi: float, workload: Dict[str, float]) -> Tuple[float, float]:
        """Analyze memory access stage utilization."""
        mem_cycles = 0.0
        for cat, weight in workload.items():
            if any(x in cat.lower() for x in ['memory', 'load', 'store', 'push', 'pop', 'stack']):
                # Memory operations include wait states
                mem_cycles += weight * (2 + self.memory_wait_states)
        
        mem_utilization = mem_cycles / max(cpi, 1)
        return mem_utilization, mem_cycles
    
    def _analyze_prefetch(self, cpi: float) -> Tuple[float, str]:
        """Analyze prefetch queue effectiveness."""
        if self.prefetch_depth == 0:
            return 0.0, "none"
        
        # Queue starvation likelihood
        avg_instr_size = 3.0 if self.bus_width >= 16 else 2.0
        queue_fullness = self.prefetch_depth / (avg_instr_size * cpi)
        
        if queue_fullness < 0.3:
            return 0.9, "prefetch_starvation"
        elif queue_fullness < 0.6:
            return 0.5, "prefetch_marginal"
        else:
            return 0.2, "prefetch_adequate"
    
    def _analyze_cache(self, cpi: float) -> Tuple[float, float]:
        """Analyze cache effectiveness."""
        if self.cache_size == 0:
            return 0.0, 0.0
        
        # Simple cache model
        hit_rate = min(0.95, 0.5 + self.cache_size / 1024 * 0.1)
        miss_penalty = 10 + self.memory_wait_states * 4
        
        cache_cpi_impact = (1.0 - hit_rate) * miss_penalty
        cache_utilization = cache_cpi_impact / max(cpi, 1)
        
        return cache_utilization, hit_rate
    
    def identify_bottleneck(self, utilizations: Dict[str, float]) -> Tuple[str, float]:
        """Identify the primary performance bottleneck.
        
        Args:
            utilizations: Dict of stage -> utilization
            
        Returns:
            Tuple of (bottleneck_name, utilization)
        """
        if not utilizations:
            return "unknown", 0.0
        
        max_util = 0.0
        bottleneck = "unknown"
        
        for stage, util in utilizations.items():
            if util > max_util:
                max_util = util
                bottleneck = stage
        
        return bottleneck, max_util
    
    def analyze(self, workload: Optional[Union[str, Dict[str, float]]] = None) -> QueueingResult:
        """Perform complete queueing analysis.
        
        Args:
            workload: Either a workload name ('typical', 'compute', 'memory', 'control')
                     or a dict of custom weights. If None, uses default weights.
                     
        Returns:
            QueueingResult with all analysis data
        """
        # Handle string workload names
        if workload is None or workload == 'typical':
            workload = {name: cat['weight'] for name, cat in self.timing_categories.items()}
        elif isinstance(workload, str):
            workload = self._get_named_workload(workload)
            
        cpi = self.weighted_cpi(workload)
        ips = self.clock_hz / cpi
        throughput = 1.0 / cpi
        
        # Analyze each stage
        utilizations = {}
        
        fetch_util, _ = self._analyze_fetch_stage(cpi)
        utilizations['fetch'] = fetch_util
        
        decode_util, _ = self._analyze_decode_stage(cpi, workload)
        utilizations['decode'] = decode_util
        
        exec_util, _ = self._analyze_execute_stage(cpi, workload)
        utilizations['execute'] = exec_util
        
        mem_util, _ = self._analyze_memory_stage(cpi, workload)
        utilizations['memory'] = mem_util
        
        # Prefetch analysis
        if self.prefetch_depth > 0:
            prefetch_util, prefetch_status = self._analyze_prefetch(cpi)
            utilizations['prefetch'] = prefetch_util
            if prefetch_status == "prefetch_starvation":
                utilizations['prefetch_starvation'] = prefetch_util
        
        # Cache analysis
        if self.cache_size > 0:
            cache_util, hit_rate = self._analyze_cache(cpi)
            utilizations['cache'] = cache_util
            utilizations['cache_miss'] = 1.0 - hit_rate
        
        # Identify bottleneck
        bottleneck, bottleneck_util = self.identify_bottleneck(utilizations)
        
        # Overall utilization (normalized)
        overall_util = min(sum(utilizations.values()) / max(len(utilizations), 1), 1.0)
        
        # Queue metrics
        service_rate = self.clock_hz / cpi
        arrival_rate = service_rate * overall_util
        avg_queue = mm1_queue_length(arrival_rate, service_rate)
        avg_response = cpi / self.clock_hz * 1e6  # microseconds
        
        return QueueingResult(
            ips=ips,
            cpi=cpi,
            utilization=overall_util,
            throughput=throughput,
            avg_queue_length=min(avg_queue, 100.0),
            avg_response_time=avg_response,
            bottleneck=bottleneck,
            bottleneck_utilization=bottleneck_util,
            stage_utilizations=utilizations
        )

    def _get_named_workload(self, name: str) -> Dict[str, float]:
        """Get weights for a named workload profile."""
        # Default: use category weights
        base_weights = {n: c['weight'] for n, c in self.timing_categories.items()}
        
        if name == 'typical':
            return base_weights
        
        # Adjust for specific workload types
        adjusted = base_weights.copy()
        
        if name == 'compute':
            # Increase ALU operations, decrease memory/branches
            for cat in adjusted:
                if 'alu' in cat.lower() or 'arith' in cat.lower():
                    adjusted[cat] *= 1.5
                elif 'mem' in cat.lower() or 'load' in cat.lower() or 'store' in cat.lower():
                    adjusted[cat] *= 0.7
                elif 'branch' in cat.lower():
                    adjusted[cat] *= 0.6
                    
        elif name == 'memory':
            # Increase memory operations
            for cat in adjusted:
                if 'mem' in cat.lower() or 'load' in cat.lower() or 'store' in cat.lower():
                    adjusted[cat] *= 1.8
                elif 'alu' in cat.lower():
                    adjusted[cat] *= 0.6
                    
        elif name == 'control':
            # Increase branches and calls
            for cat in adjusted:
                if 'branch' in cat.lower() or 'jump' in cat.lower() or 'call' in cat.lower():
                    adjusted[cat] *= 2.0
                elif 'alu' in cat.lower():
                    adjusted[cat] *= 0.5
        
        # Normalize to sum to 1.0
        total = sum(adjusted.values())
        if total > 0:
            adjusted = {k: v/total for k, v in adjusted.items()}
        
        return adjusted


def create_model(config: Dict) -> QueueingModel:
    """Create a QueueingModel from a configuration dict.
    
    Args:
        config: Dict with clock_mhz, timing_categories, etc.
        
    Returns:
        Configured QueueingModel instance
    """
    return QueueingModel(
        clock_mhz=config.get('clock_mhz', 1.0),
        timing_categories=config.get('timing_categories', {}),
        bus_width=config.get('bus_width', 8),
        prefetch_depth=config.get('prefetch_depth', 0),
        cache_size=config.get('cache_size', 0),
        pipeline_stages=config.get('pipeline_stages', 1),
        memory_wait_states=config.get('memory_wait_states', 0)
    )
