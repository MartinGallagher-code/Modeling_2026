#!/usr/bin/env python3
"""
Era-Specific Architectural Patterns for Modeling_2026
=====================================================

This module defines the correct queueing network architectures for each
processor era (1971-1988). Each era requires different modeling approaches
based on the underlying microarchitecture.

Eras:
1. Sequential (1971-1976): Simple serial execution, no parallelism
2. Prefetch Queue (1976-1982): Parallel fetch/execute units
3. Pipelined (1979-1985): Multi-stage instruction pipelines
4. Cache/RISC (1983-1988): Cache hierarchies + deep pipelines

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum, auto


# =============================================================================
# ERA DEFINITIONS
# =============================================================================

class ProcessorEra(Enum):
    """Processor architectural eras"""
    SEQUENTIAL = auto()      # 1971-1976: Serial execution
    PREFETCH_QUEUE = auto()  # 1976-1982: BIU/EU parallelism
    PIPELINED = auto()       # 1979-1985: Multi-stage pipeline
    CACHE_RISC = auto()      # 1983-1988: Cache + RISC features


@dataclass
class EraDefinition:
    """Definition of a processor era"""
    era: ProcessorEra
    name: str
    year_start: int
    year_end: int
    description: str
    architectural_features: List[str]
    queueing_model: str
    example_processors: List[str]


# Era definitions with characteristics
ERA_DEFINITIONS: Dict[ProcessorEra, EraDefinition] = {
    ProcessorEra.SEQUENTIAL: EraDefinition(
        era=ProcessorEra.SEQUENTIAL,
        name="Sequential Execution",
        year_start=1971,
        year_end=1976,
        description="Simple serial instruction execution with no overlap",
        architectural_features=[
            "Single instruction at a time",
            "No instruction prefetch",
            "No pipeline",
            "Direct memory access on every instruction",
            "Variable-length instruction fetch",
        ],
        queueing_model="Serial M/M/1 chain",
        example_processors=["4004", "4040", "8008", "6800", "6502", "SC/MP", "1802", "F8", "2650"]
    ),
    
    ProcessorEra.PREFETCH_QUEUE: EraDefinition(
        era=ProcessorEra.PREFETCH_QUEUE,
        name="Prefetch Queue",
        year_start=1976,
        year_end=1982,
        description="Parallel Bus Interface Unit (BIU) and Execution Unit (EU)",
        architectural_features=[
            "Instruction prefetch queue (4-6 bytes)",
            "BIU fetches while EU executes",
            "Queue can stall on branches/jumps",
            "Bus contention between fetch and memory ops",
            "Some instruction overlap possible",
        ],
        queueing_model="Parallel M/M/1 queues with synchronization",
        example_processors=["8086", "8088", "80186", "80188", "Z80", "Z8000", "6809"]
    ),
    
    ProcessorEra.PIPELINED: EraDefinition(
        era=ProcessorEra.PIPELINED,
        name="Pipelined Execution",
        year_start=1979,
        year_end=1985,
        description="Multi-stage instruction pipeline with parallel stages",
        architectural_features=[
            "3-5 stage pipeline",
            "Instruction prefetch buffer",
            "Pipeline stalls on hazards",
            "Some have instruction cache",
            "Microcoded execution",
        ],
        queueing_model="Pipeline queueing network",
        example_processors=["68000", "68010", "68020", "80286", "Z80000", "32016", "32032"]
    ),
    
    ProcessorEra.CACHE_RISC: EraDefinition(
        era=ProcessorEra.CACHE_RISC,
        name="Cache/RISC Architecture",
        year_start=1983,
        year_end=1988,
        description="Cache hierarchies with RISC-style execution",
        architectural_features=[
            "On-chip instruction cache",
            "Deep pipeline (5+ stages)",
            "Load/store architecture",
            "Register windows or large register files",
            "Single-cycle execution goal",
            "Delayed branches",
        ],
        queueing_model="Cache hierarchy + pipeline network",
        example_processors=["ARM1", "SPARC", "MIPS R2000", "Am29000", "T414", "80386"]
    ),
}


# =============================================================================
# PROCESSOR TO ERA MAPPING
# =============================================================================

# Directories to skip (not actual processors)
SKIP_DIRECTORIES = {
    'documentation', 'docs', 'common', 'scripts', 'tests', 'tools',
    'archive', 'templates', 'examples', 'data', 'resources', 'assets',
    '__pycache__', '.git', '.github', 'node_modules', 'venv', 'env',
}

# Comprehensive mapping of all 61+ processors to their correct era
PROCESSOR_ERA_MAP: Dict[str, ProcessorEra] = {
    # Intel Family
    "i4004": ProcessorEra.SEQUENTIAL,
    "i4040": ProcessorEra.SEQUENTIAL,
    "i8008": ProcessorEra.SEQUENTIAL,
    "i8048": ProcessorEra.SEQUENTIAL,
    "i8051": ProcessorEra.SEQUENTIAL,
    "i8080": ProcessorEra.SEQUENTIAL,
    "i8085": ProcessorEra.SEQUENTIAL,  # Enhanced 8080, still sequential
    "i8748": ProcessorEra.SEQUENTIAL,
    "i8751": ProcessorEra.SEQUENTIAL,
    "i8086": ProcessorEra.PREFETCH_QUEUE,
    "i8088": ProcessorEra.PREFETCH_QUEUE,
    "i80186": ProcessorEra.PREFETCH_QUEUE,
    "i80188": ProcessorEra.PREFETCH_QUEUE,
    "i80286": ProcessorEra.PIPELINED,
    "i80386": ProcessorEra.CACHE_RISC,
    "i80486": ProcessorEra.CACHE_RISC,
    "i860": ProcessorEra.CACHE_RISC,     # Intel RISC processor (1989)
    "pentium": ProcessorEra.CACHE_RISC,  # Superscalar (1993) - extends RISC model
    "iapx432": ProcessorEra.PIPELINED,   # Unique capability architecture
    "i80287": ProcessorEra.PREFETCH_QUEUE,  # FPU, matches 286 era
    "i80387": ProcessorEra.CACHE_RISC,   # FPU, matches 386 era
    "i960": ProcessorEra.CACHE_RISC,     # Intel RISC
    
    # Motorola Family
    "m6800": ProcessorEra.SEQUENTIAL,
    "m6801": ProcessorEra.SEQUENTIAL,
    "m6802": ProcessorEra.SEQUENTIAL,
    "m6805": ProcessorEra.SEQUENTIAL,
    "m6809": ProcessorEra.PREFETCH_QUEUE,  # Has instruction queue
    "m68hc11": ProcessorEra.PREFETCH_QUEUE,
    "m68000": ProcessorEra.PIPELINED,
    "m68008": ProcessorEra.PIPELINED,
    "m68010": ProcessorEra.PIPELINED,
    "m68020": ProcessorEra.PIPELINED,    # Has instruction cache
    "m68030": ProcessorEra.CACHE_RISC,   # On-chip caches (1987)
    "m68040": ProcessorEra.CACHE_RISC,   # On-chip caches + FPU (1990)
    "m68060": ProcessorEra.CACHE_RISC,   # Superscalar (1994)
    "m68881": ProcessorEra.PIPELINED,    # FPU
    "m68882": ProcessorEra.PIPELINED,    # FPU
    
    # MOS/WDC Family
    "mos6502": ProcessorEra.SEQUENTIAL,
    "mos6510": ProcessorEra.SEQUENTIAL,
    "wdc65c02": ProcessorEra.SEQUENTIAL,  # Enhanced but still sequential
    "wdc65816": ProcessorEra.PREFETCH_QUEUE,  # 16-bit with prefetch
    
    # Zilog Family
    "z8": ProcessorEra.SEQUENTIAL,
    "z80": ProcessorEra.PREFETCH_QUEUE,  # Technically has limited prefetch
    "z80a": ProcessorEra.PREFETCH_QUEUE,
    "z80b": ProcessorEra.PREFETCH_QUEUE,
    "z180": ProcessorEra.PREFETCH_QUEUE,
    "z8000": ProcessorEra.PREFETCH_QUEUE,
    "z80000": ProcessorEra.PIPELINED,
    
    # Other Family - AMD
    "am2901": ProcessorEra.SEQUENTIAL,   # Bit-slice, simple
    "am2903": ProcessorEra.SEQUENTIAL,
    "am29000": ProcessorEra.CACHE_RISC,
    
    # Other Family - ARM (Acorn)
    "arm1": ProcessorEra.CACHE_RISC,     # 1985
    "arm2": ProcessorEra.CACHE_RISC,     # 1986
    "arm3": ProcessorEra.CACHE_RISC,     # 1989
    "arm6": ProcessorEra.CACHE_RISC,     # 1991
    "arm7": ProcessorEra.CACHE_RISC,     # 1993
    "arm610": ProcessorEra.CACHE_RISC,
    
    # Other Family - MIPS
    "mips_r2000": ProcessorEra.CACHE_RISC,
    "mips_r3000": ProcessorEra.CACHE_RISC,
    "mips_r4000": ProcessorEra.CACHE_RISC,
    
    # Other Family - SPARC
    "sparc": ProcessorEra.CACHE_RISC,
    "sun_sparc": ProcessorEra.CACHE_RISC,
    "sun_spark": ProcessorEra.CACHE_RISC,  # Common typo
    
    # Other Family - Transputer (INMOS)
    "t414": ProcessorEra.CACHE_RISC,
    "t800": ProcessorEra.CACHE_RISC,
    
    # Other Family - DEC Alpha
    "alpha": ProcessorEra.CACHE_RISC,
    "alpha21064": ProcessorEra.CACHE_RISC,  # First Alpha (1992)
    "alpha21164": ProcessorEra.CACHE_RISC,
    
    # Other Family - HP PA-RISC
    "pa_risc": ProcessorEra.CACHE_RISC,
    "hp_pa_risc": ProcessorEra.CACHE_RISC,
    "parisc": ProcessorEra.CACHE_RISC,
    
    # Other Family - PowerPC (AIM alliance)
    "powerpc": ProcessorEra.CACHE_RISC,
    "ppc601": ProcessorEra.CACHE_RISC,
    "aim_ppc_601": ProcessorEra.CACHE_RISC,
    "aim__ppc_601": ProcessorEra.CACHE_RISC,  # Double underscore variant
    
    # Other Family - Fairchild/Various
    "f8": ProcessorEra.SEQUENTIAL,
    "clipper": ProcessorEra.CACHE_RISC,  # Fairchild/Intergraph
    
    # Other Family - RCA
    "rca1802": ProcessorEra.SEQUENTIAL,
    "rca1805": ProcessorEra.SEQUENTIAL,
    
    # Other Family - National Semiconductor
    "scmp": ProcessorEra.SEQUENTIAL,     # SC/MP
    "ns32016": ProcessorEra.PIPELINED,
    "ns32032": ProcessorEra.PIPELINED,
    "ns32332": ProcessorEra.PIPELINED,
    
    # Other Family - Signetics
    "signetics2650": ProcessorEra.SEQUENTIAL,
    
    # Other Family - Texas Instruments
    "tms9900": ProcessorEra.SEQUENTIAL,
    "tms9995": ProcessorEra.SEQUENTIAL,
    "tms320c10": ProcessorEra.PIPELINED,  # DSP with pipeline
    "tms320c25": ProcessorEra.PIPELINED,
    
    # Other Family - Western Electric
    "we32000": ProcessorEra.PIPELINED,
    "we32100": ProcessorEra.PIPELINED,
    
    # Other Family - Stack machines
    "novix_nc4016": ProcessorEra.SEQUENTIAL,
    "harris_rtx2000": ProcessorEra.PIPELINED,
}

# Alternate name mappings (handle variations in naming)
PROCESSOR_ALIASES: Dict[str, str] = {
    # Intel
    "4004": "i4004", "intel_4004": "i4004", "intel4004": "i4004",
    "4040": "i4040", "intel_4040": "i4040",
    "8008": "i8008", "intel_8008": "i8008",
    "8048": "i8048", "intel_8048": "i8048",
    "8051": "i8051", "intel_8051": "i8051",
    "8080": "i8080", "intel_8080": "i8080",
    "8085": "i8085", "intel_8085": "i8085",
    "8086": "i8086", "intel_8086": "i8086",
    "8088": "i8088", "intel_8088": "i8088",
    "80186": "i80186", "intel_80186": "i80186",
    "80188": "i80188", "intel_80188": "i80188",
    "80286": "i80286", "intel_80286": "i80286", "286": "i80286",
    "80386": "i80386", "intel_80386": "i80386", "386": "i80386",
    "80486": "i80486", "intel_80486": "i80486", "486": "i80486",
    "860": "i860", "intel_860": "i860", "intel_i860": "i860",
    "iapx_432": "iapx432",
    "intel_pentium": "pentium",
    
    # Motorola
    "6800": "m6800", "mc6800": "m6800", "motorola_6800": "m6800",
    "6801": "m6801", "mc6801": "m6801",
    "6802": "m6802", "mc6802": "m6802",
    "6805": "m6805", "mc6805": "m6805",
    "6809": "m6809", "mc6809": "m6809",
    "68hc11": "m68hc11", "mc68hc11": "m68hc11",
    "68000": "m68000", "mc68000": "m68000", "motorola_68000": "m68000",
    "68008": "m68008", "mc68008": "m68008",
    "68010": "m68010", "mc68010": "m68010",
    "68020": "m68020", "mc68020": "m68020",
    "68030": "m68030", "mc68030": "m68030",
    "68040": "m68040", "mc68040": "m68040",
    "68060": "m68060", "mc68060": "m68060",
    "68881": "m68881", "mc68881": "m68881",
    "68882": "m68882", "mc68882": "m68882",
    
    # MOS/WDC
    "6502": "mos6502", "mos_6502": "mos6502",
    "6510": "mos6510", "mos_6510": "mos6510",
    "65c02": "wdc65c02", "wdc_65c02": "wdc65c02",
    "65816": "wdc65816", "wdc_65816": "wdc65816", "65c816": "wdc65816",
    
    # Zilog
    "z_80": "z80", "zilog_z80": "z80",
    "z_8000": "z8000", "zilog_z8000": "z8000",
    "z_80000": "z80000",
    
    # AMD
    "2901": "am2901", "amd_2901": "am2901",
    "2903": "am2903", "amd_2903": "am2903",
    "29000": "am29000", "amd29000": "am29000", "amd_29000": "am29000",
    
    # MIPS
    "r2000": "mips_r2000", "mipsr2000": "mips_r2000",
    "r3000": "mips_r3000", "mipsr3000": "mips_r3000",
    "r4000": "mips_r4000", "mipsr4000": "mips_r4000",
    
    # ARM
    "arm_1": "arm1", "acorn_arm1": "arm1",
    "arm_2": "arm2", "acorn_arm2": "arm2",
    "arm_3": "arm3", "acorn_arm3": "arm3",
    "arm_6": "arm6", "acorn_arm6": "arm6",
    "arm_7": "arm7",
    
    # SPARC
    "sun_sparc": "sparc", "sun_spark": "sparc", "sparc_v7": "sparc",
    
    # DEC Alpha
    "dec_alpha": "alpha", "alpha_21064": "alpha21064", 
    "alpha_21164": "alpha21164", "dec_alpha21064": "alpha21064",
    
    # HP PA-RISC
    "hp_parisc": "pa_risc", "hppa": "pa_risc", "hp_pa": "pa_risc",
    
    # PowerPC / AIM
    "ppc_601": "ppc601", "ppc601": "ppc601", 
    "aim_ppc601": "ppc601", "aim_ppc_601": "ppc601",
    "aim__ppc_601": "aim__ppc_601",  # Exact match for double underscore
    "powerpc_601": "ppc601",
    
    # RCA
    "1802": "rca1802", "cdp1802": "rca1802",
    "1805": "rca1805", "cdp1805": "rca1805",
    
    # National Semiconductor
    "sc_mp": "scmp", "sc-mp": "scmp",
    "32016": "ns32016", "ns_32016": "ns32016",
    "32032": "ns32032", "ns_32032": "ns32032",
    "32332": "ns32332", "ns_32332": "ns32332",
    
    # Signetics
    "2650": "signetics2650", "signetics_2650": "signetics2650",
    
    # Texas Instruments
    "9900": "tms9900", "tms_9900": "tms9900",
    "9995": "tms9995", "tms_9995": "tms9995",
    "320c10": "tms320c10", "tms320": "tms320c10",
    
    # Western Electric
    "32000": "we32000", "we_32000": "we32000",
    "32100": "we32100", "we_32100": "we32100",
    
    # Stack machines
    "nc4016": "novix_nc4016",
    "rtx2000": "harris_rtx2000",
    
    # Transputer
    "inmos_t414": "t414", "transputer": "t414",
    "inmos_t800": "t800",
}


def get_processor_era(processor_name: str) -> Optional[ProcessorEra]:
    """Get the era for a processor by name"""
    # Normalize name
    normalized = processor_name.lower().replace('-', '_').replace(' ', '_')
    
    # Check direct mapping
    if normalized in PROCESSOR_ERA_MAP:
        return PROCESSOR_ERA_MAP[normalized]
    
    # Check aliases
    if normalized in PROCESSOR_ALIASES:
        canonical = PROCESSOR_ALIASES[normalized]
        if canonical in PROCESSOR_ERA_MAP:
            return PROCESSOR_ERA_MAP[canonical]
    
    # Try partial matching
    for key in PROCESSOR_ERA_MAP:
        if key in normalized or normalized in key:
            return PROCESSOR_ERA_MAP[key]
    
    return None


def get_era_definition(era: ProcessorEra) -> EraDefinition:
    """Get the definition for an era"""
    return ERA_DEFINITIONS[era]


def should_skip_directory(dir_name: str) -> bool:
    """Check if a directory should be skipped (not a processor)"""
    normalized = dir_name.lower()
    return normalized in SKIP_DIRECTORIES or normalized.startswith('.')


def is_valid_processor(processor_name: str) -> bool:
    """Check if a name corresponds to a known processor"""
    if should_skip_directory(processor_name):
        return False
    era = get_processor_era(processor_name)
    return era is not None


# =============================================================================
# QUEUEING MODEL BASE CLASSES
# =============================================================================

@dataclass
class QueueMetrics:
    """Metrics for a single queue"""
    arrival_rate: float  # λ (lambda)
    service_rate: float  # μ (mu)
    utilization: float   # ρ = λ/μ
    avg_queue_length: float  # L
    avg_wait_time: float     # W
    avg_system_time: float   # W + service time


@dataclass
class StageResult:
    """Result for a pipeline/queue stage"""
    name: str
    service_time_cycles: float
    utilization: float
    queue_length: float
    contribution_to_cpi: float


@dataclass 
class ArchitecturalAnalysis:
    """Complete architectural analysis result"""
    processor: str
    era: ProcessorEra
    workload: str
    cpi: float
    ipc: float
    ips: float
    bottleneck_stage: str
    stage_results: List[StageResult]
    utilizations: Dict[str, float]
    warnings: List[str] = field(default_factory=list)


class BaseQueueingModel(ABC):
    """Abstract base for all queueing models"""
    
    @abstractmethod
    def compute_metrics(self, arrival_rate: float) -> QueueMetrics:
        """Compute queue metrics for given arrival rate"""
        pass


class MM1Queue(BaseQueueingModel):
    """
    M/M/1 Queue Model
    
    - Markovian (Poisson) arrivals
    - Markovian (Exponential) service times
    - Single server
    
    Used for: Simple sequential stages
    """
    
    def __init__(self, service_rate: float, name: str = "MM1"):
        """
        Args:
            service_rate: μ (mu) - average service rate (1/avg_service_time)
            name: Identifier for this queue
        """
        self.service_rate = service_rate
        self.name = name
    
    def compute_metrics(self, arrival_rate: float) -> QueueMetrics:
        """
        Compute M/M/1 queue metrics.
        
        Formulas:
            ρ = λ/μ (utilization, must be < 1 for stability)
            L = ρ/(1-ρ) (average queue length)
            W = 1/(μ-λ) (average time in system)
        """
        if arrival_rate >= self.service_rate:
            # Queue is unstable - return saturated values
            return QueueMetrics(
                arrival_rate=arrival_rate,
                service_rate=self.service_rate,
                utilization=1.0,
                avg_queue_length=float('inf'),
                avg_wait_time=float('inf'),
                avg_system_time=float('inf')
            )
        
        utilization = arrival_rate / self.service_rate
        avg_queue_length = utilization / (1 - utilization)
        avg_system_time = 1 / (self.service_rate - arrival_rate)
        avg_wait_time = avg_system_time - (1 / self.service_rate)
        
        return QueueMetrics(
            arrival_rate=arrival_rate,
            service_rate=self.service_rate,
            utilization=utilization,
            avg_queue_length=avg_queue_length,
            avg_wait_time=avg_wait_time,
            avg_system_time=avg_system_time
        )


class MMkQueue(BaseQueueingModel):
    """
    M/M/k Queue Model
    
    - Markovian arrivals
    - Markovian service times
    - k parallel servers
    
    Used for: Superscalar execution units
    """
    
    def __init__(self, service_rate: float, num_servers: int, name: str = "MMk"):
        self.service_rate = service_rate
        self.num_servers = num_servers
        self.name = name
    
    def compute_metrics(self, arrival_rate: float) -> QueueMetrics:
        """Compute M/M/k queue metrics using Erlang-C formula"""
        k = self.num_servers
        mu = self.service_rate
        rho = arrival_rate / (k * mu)
        
        if rho >= 1:
            return QueueMetrics(
                arrival_rate=arrival_rate,
                service_rate=self.service_rate,
                utilization=1.0,
                avg_queue_length=float('inf'),
                avg_wait_time=float('inf'),
                avg_system_time=float('inf')
            )
        
        # Erlang-C probability (simplified)
        # P(wait) = (k*rho)^k / (k! * (1-rho)) * P0
        # This is a simplified approximation
        avg_queue_length = (rho ** (k + 1)) / (1 - rho) 
        avg_wait_time = avg_queue_length / arrival_rate
        avg_system_time = avg_wait_time + 1/mu
        
        return QueueMetrics(
            arrival_rate=arrival_rate,
            service_rate=self.service_rate,
            utilization=rho,
            avg_queue_length=avg_queue_length,
            avg_wait_time=avg_wait_time,
            avg_system_time=avg_system_time
        )


# =============================================================================
# ERA-SPECIFIC ARCHITECTURAL MODELS
# =============================================================================

class SequentialArchitecture:
    """
    Sequential Execution Architecture (1971-1976)
    
    Models processors with no instruction overlap:
    - 4004, 4040, 8008, 8080, 6800, 6502, SC/MP, 1802, F8
    
    Architecture:
        FETCH → DECODE → EXECUTE → MEMORY → WRITEBACK
        (All stages are serial, no overlap)
    
    Queueing Model:
        Series of M/M/1 queues (Jackson Network)
        CPI = sum of stage service times
    """
    
    def __init__(self, 
                 fetch_cycles: float,
                 decode_cycles: float,
                 execute_cycles: float,
                 memory_cycles: float,
                 writeback_cycles: float = 0,
                 clock_mhz: float = 1.0,
                 name: str = "Sequential"):
        """
        Args:
            fetch_cycles: Average cycles for instruction fetch
            decode_cycles: Average cycles for decode
            execute_cycles: Average cycles for execution (weighted by instruction mix)
            memory_cycles: Average cycles for memory operations (weighted by mem ops fraction)
            writeback_cycles: Average cycles for writeback (often 0 for simple CPUs)
            clock_mhz: Clock frequency in MHz
            name: Processor name
        """
        self.name = name
        self.clock_mhz = clock_mhz
        self.stages = {
            'fetch': fetch_cycles,
            'decode': decode_cycles,
            'execute': execute_cycles,
            'memory': memory_cycles,
            'writeback': writeback_cycles,
        }
    
    def analyze(self, workload_weights: Optional[Dict[str, float]] = None) -> ArchitecturalAnalysis:
        """
        Analyze performance for sequential architecture.
        
        For sequential execution:
            CPI = sum of all stage times
            No queueing effects (stages don't overlap)
        """
        # Calculate total CPI
        total_cpi = sum(self.stages.values())
        
        # All stages have utilization = 1/CPI for their contribution
        stage_results = []
        bottleneck_stage = max(self.stages, key=self.stages.get)
        
        for stage_name, cycles in self.stages.items():
            if cycles > 0:
                stage_results.append(StageResult(
                    name=stage_name,
                    service_time_cycles=cycles,
                    utilization=cycles / total_cpi,  # Fraction of CPI
                    queue_length=0,  # No queueing in sequential
                    contribution_to_cpi=cycles
                ))
        
        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc
        
        return ArchitecturalAnalysis(
            processor=self.name,
            era=ProcessorEra.SEQUENTIAL,
            workload='default',
            cpi=total_cpi,
            ipc=ipc,
            ips=ips,
            bottleneck_stage=bottleneck_stage,
            stage_results=stage_results,
            utilizations={s.name: s.utilization for s in stage_results}
        )
    
    @staticmethod
    def get_template() -> str:
        """Return Python code template for sequential architecture"""
        return '''
class {ClassName}Model(BaseProcessorModel):
    """
    {ProcessorName} Grey-Box Queueing Model
    
    Architecture: Sequential Execution (Era: 1971-1976)
    - No instruction overlap
    - Serial stage execution
    - CPI = sum of stage times
    """
    
    # Processor specifications
    name = "{ProcessorName}"
    manufacturer = "{Manufacturer}"
    year = {Year}
    clock_mhz = {ClockMHz}
    transistor_count = {Transistors}
    data_width = {DataWidth}
    address_width = {AddressWidth}
    
    def __init__(self):
        # Stage timing (cycles)
        self.stage_timing = {
            'fetch': {FetchCycles},      # Instruction fetch
            'decode': {DecodeCycles},     # Decode
            'execute': {ExecuteCycles},   # Execute (weighted average)
            'memory': {MemoryCycles},     # Memory access (for load/store)
            'writeback': {WritebackCycles}, # Register writeback
        }
        
        # Instruction categories (5-15 recommended)
        self.instruction_categories = {
            'register_ops': InstructionCategory('register_ops', {RegOpsCycles}, 0, "Register-to-register"),
            'immediate': InstructionCategory('immediate', {ImmediateCycles}, 0, "Immediate operand"),
            'memory_read': InstructionCategory('memory_read', {MemReadCycles}, {MemReadMem}, "Load from memory"),
            'memory_write': InstructionCategory('memory_write', {MemWriteCycles}, {MemWriteMem}, "Store to memory"),
            'branch': InstructionCategory('branch', {BranchCycles}, 0, "Branch/jump"),
            'call_return': InstructionCategory('call_return', {CallRetCycles}, {CallRetMem}, "Subroutine call/return"),
        }
        
        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'register_ops': 0.30,
                'immediate': 0.15,
                'memory_read': 0.25,
                'memory_write': 0.15,
                'branch': 0.10,
                'call_return': 0.05,
            }, "Typical mixed workload"),
            'compute': WorkloadProfile('compute', {
                'register_ops': 0.50,
                'immediate': 0.25,
                'memory_read': 0.10,
                'memory_write': 0.05,
                'branch': 0.08,
                'call_return': 0.02,
            }, "Compute-intensive workload"),
            'memory': WorkloadProfile('memory', {
                'register_ops': 0.15,
                'immediate': 0.10,
                'memory_read': 0.40,
                'memory_write': 0.25,
                'branch': 0.05,
                'call_return': 0.05,
            }, "Memory-intensive workload"),
            'control': WorkloadProfile('control', {
                'register_ops': 0.20,
                'immediate': 0.10,
                'memory_read': 0.15,
                'memory_write': 0.10,
                'branch': 0.30,
                'call_return': 0.15,
            }, "Control-flow intensive workload"),
        }
    
    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using sequential execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        
        # Calculate weighted average CPI
        total_cpi = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            total_cpi += weight * cat.total_cycles
        
        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc
        
        # Identify bottleneck (highest contribution)
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            contributions[cat_name] = weight * cat.total_cycles
        bottleneck = max(contributions, key=contributions.get)
        
        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=total_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=contributions
        )
    
    def validate(self) -> Dict[str, Any]:
        """Run validation tests"""
        # TODO: Implement validation against known timing data
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}
    
    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories
    
    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles
'''


class PrefetchQueueArchitecture:
    """
    Prefetch Queue Architecture (1976-1982)
    
    Models processors with parallel BIU/EU:
    - 8086, 8088, 80186, 80188, Z80, Z8000, 6809
    
    Architecture:
        ┌──────────┐     ┌─────────────┐
        │   BIU    │────►│   Prefetch  │
        │ (fetch)  │     │   Queue     │
        └──────────┘     └──────┬──────┘
                               │
                         ┌─────▼─────┐
                         │    EU     │
                         │ (execute) │
                         └───────────┘
    
    Queueing Model:
        - BIU: M/M/1 queue feeding prefetch buffer
        - EU: M/M/1 queue consuming from buffer
        - Contention when EU needs memory access
    """
    
    def __init__(self,
                 bus_width: int,  # 8 or 16 bits
                 prefetch_queue_size: int,  # bytes
                 bus_cycle_time: float,  # cycles per bus access
                 avg_instruction_length: float,  # bytes
                 eu_cycles: float,  # average EU execution time
                 memory_op_fraction: float,  # fraction of instructions needing memory
                 clock_mhz: float = 5.0,
                 name: str = "PrefetchQueue"):
        
        self.name = name
        self.clock_mhz = clock_mhz
        self.bus_width = bus_width
        self.prefetch_queue_size = prefetch_queue_size
        self.bus_cycle_time = bus_cycle_time
        self.avg_instruction_length = avg_instruction_length
        self.eu_cycles = eu_cycles
        self.memory_op_fraction = memory_op_fraction
        
        # Calculate derived parameters
        self.bytes_per_bus_cycle = bus_width // 8
        self.fetch_cycles_per_instruction = (
            avg_instruction_length / self.bytes_per_bus_cycle * bus_cycle_time
        )
    
    def analyze(self, workload_weights: Optional[Dict[str, float]] = None) -> ArchitecturalAnalysis:
        """
        Analyze performance for prefetch queue architecture.
        
        Key insight: BIU and EU operate in parallel, but:
        1. EU stalls if prefetch queue is empty
        2. BIU stalls during EU memory operations (bus contention)
        """
        # BIU queue model
        biu_service_time = self.fetch_cycles_per_instruction
        
        # EU queue model  
        eu_service_time = self.eu_cycles
        
        # Effective CPI considering parallelism and contention
        # Simplified model: CPI = max(fetch_time, eu_time) + contention_penalty
        
        base_cpi = max(biu_service_time, eu_service_time)
        
        # Contention: when EU does memory op, BIU must wait
        contention_penalty = self.memory_op_fraction * self.bus_cycle_time
        
        # Queue stall: if EU is faster than BIU, queue empties
        if eu_service_time < biu_service_time:
            queue_stall = (biu_service_time - eu_service_time) * 0.5  # Amortized
        else:
            queue_stall = 0
        
        total_cpi = base_cpi + contention_penalty + queue_stall
        
        # Determine bottleneck
        if biu_service_time > eu_service_time:
            bottleneck = "BIU (fetch-bound)"
        elif contention_penalty > queue_stall:
            bottleneck = "Bus Contention"
        else:
            bottleneck = "EU (execution-bound)"
        
        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc
        
        stage_results = [
            StageResult("BIU", biu_service_time, biu_service_time/total_cpi, 0, biu_service_time),
            StageResult("EU", eu_service_time, eu_service_time/total_cpi, 0, eu_service_time),
            StageResult("Contention", contention_penalty, contention_penalty/total_cpi, 0, contention_penalty),
        ]
        
        return ArchitecturalAnalysis(
            processor=self.name,
            era=ProcessorEra.PREFETCH_QUEUE,
            workload='default',
            cpi=total_cpi,
            ipc=ipc,
            ips=ips,
            bottleneck_stage=bottleneck,
            stage_results=stage_results,
            utilizations={s.name: s.utilization for s in stage_results}
        )
    
    @staticmethod
    def get_template() -> str:
        """Return Python code template for prefetch queue architecture"""
        return '''
class {ClassName}Model(BaseProcessorModel):
    """
    {ProcessorName} Grey-Box Queueing Model
    
    Architecture: Prefetch Queue (Era: 1976-1982)
    - Parallel BIU (Bus Interface Unit) and EU (Execution Unit)
    - Instruction prefetch queue ({QueueSize} bytes)
    - Bus contention during memory operations
    """
    
    # Processor specifications
    name = "{ProcessorName}"
    manufacturer = "{Manufacturer}"
    year = {Year}
    clock_mhz = {ClockMHz}
    transistor_count = {Transistors}
    data_width = {DataWidth}
    address_width = {AddressWidth}
    
    # Architecture parameters
    bus_width = {BusWidth}  # bits
    prefetch_queue_size = {QueueSize}  # bytes
    
    def __init__(self):
        # BIU timing
        self.bus_cycle_time = {BusCycleTime}  # cycles per bus access
        self.bytes_per_access = self.bus_width // 8
        
        # EU timing by instruction category
        self.instruction_categories = {
            'register_ops': InstructionCategory('register_ops', {RegOpsCycles}, 0, "Register operations"),
            'immediate': InstructionCategory('immediate', {ImmediateCycles}, 0, "Immediate operand"),
            'memory_read': InstructionCategory('memory_read', {MemReadCycles}, {MemReadBus}, "Load from memory"),
            'memory_write': InstructionCategory('memory_write', {MemWriteCycles}, {MemWriteBus}, "Store to memory"),
            'branch': InstructionCategory('branch', {BranchCycles}, 0, "Branch (flushes queue)"),
            'string_ops': InstructionCategory('string_ops', {StringCycles}, {StringBus}, "String operations"),
        }
        
        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'register_ops': 0.25,
                'immediate': 0.20,
                'memory_read': 0.20,
                'memory_write': 0.15,
                'branch': 0.15,
                'string_ops': 0.05,
            }, "Typical mixed workload"),
            'compute': WorkloadProfile('compute', {
                'register_ops': 0.40,
                'immediate': 0.30,
                'memory_read': 0.10,
                'memory_write': 0.05,
                'branch': 0.12,
                'string_ops': 0.03,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'register_ops': 0.10,
                'immediate': 0.10,
                'memory_read': 0.35,
                'memory_write': 0.25,
                'branch': 0.10,
                'string_ops': 0.10,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'register_ops': 0.15,
                'immediate': 0.15,
                'memory_read': 0.15,
                'memory_write': 0.10,
                'branch': 0.35,
                'string_ops': 0.10,
            }, "Control-flow intensive"),
        }
    
    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using prefetch queue model with BIU/EU parallelism"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        
        # Calculate EU cycles
        eu_cycles = 0
        memory_ops_fraction = 0
        for cat_name, weight in profile.category_weights.items():
            cat = self.instruction_categories[cat_name]
            eu_cycles += weight * cat.base_cycles
            memory_ops_fraction += weight * (cat.memory_cycles / max(cat.total_cycles, 1))
        
        # Calculate BIU cycles (instruction fetch)
        avg_inst_length = {AvgInstLength}  # bytes
        biu_cycles = (avg_inst_length / self.bytes_per_access) * self.bus_cycle_time
        
        # Effective CPI with parallelism
        base_cpi = max(biu_cycles, eu_cycles)
        
        # Bus contention penalty
        contention = memory_ops_fraction * self.bus_cycle_time
        
        # Branch penalty (queue flush)
        branch_weight = profile.category_weights.get('branch', 0.15)
        branch_penalty = branch_weight * (self.prefetch_queue_size / self.bytes_per_access) * 0.5
        
        total_cpi = base_cpi + contention + branch_penalty
        
        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc
        
        # Bottleneck analysis
        if biu_cycles > eu_cycles:
            bottleneck = "BIU_fetch"
        elif contention > branch_penalty:
            bottleneck = "bus_contention"
        else:
            bottleneck = "EU_execute"
        
        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=total_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations={'biu': biu_cycles/total_cpi, 'eu': eu_cycles/total_cpi, 'contention': contention/total_cpi}
        )
    
    def validate(self) -> Dict[str, Any]:
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}
    
    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories
    
    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles
'''


class PipelinedArchitecture:
    """
    Pipelined Execution Architecture (1979-1985)
    
    Models processors with multi-stage pipelines:
    - 68000, 68010, 68020, 80286, Z80000, NS32016/32032
    
    Architecture:
        IF → ID → OF → EX → WB
        (Stages operate in parallel on different instructions)
    
    Queueing Model:
        - Each stage is M/M/1 queue
        - Pipeline hazards cause stalls
        - Instruction cache (if present) affects IF
    """
    
    def __init__(self,
                 pipeline_stages: Dict[str, float],  # stage_name -> cycles
                 has_icache: bool = False,
                 icache_hit_rate: float = 0.95,
                 icache_miss_penalty: float = 10,
                 hazard_stall_fraction: float = 0.1,
                 clock_mhz: float = 8.0,
                 name: str = "Pipelined"):
        
        self.name = name
        self.clock_mhz = clock_mhz
        self.pipeline_stages = pipeline_stages
        self.has_icache = has_icache
        self.icache_hit_rate = icache_hit_rate
        self.icache_miss_penalty = icache_miss_penalty
        self.hazard_stall_fraction = hazard_stall_fraction
        
        self.num_stages = len(pipeline_stages)
    
    def analyze(self, workload_weights: Optional[Dict[str, float]] = None) -> ArchitecturalAnalysis:
        """
        Analyze performance for pipelined architecture.
        
        Ideal CPI = 1.0 (one instruction per cycle)
        Actual CPI = 1.0 + stalls + hazards + cache_misses
        """
        # Find bottleneck stage
        bottleneck_stage = max(self.pipeline_stages, key=self.pipeline_stages.get)
        bottleneck_cycles = self.pipeline_stages[bottleneck_stage]
        
        # Base CPI limited by slowest stage
        base_cpi = bottleneck_cycles
        
        # Cache miss penalty
        if self.has_icache:
            cache_penalty = (1 - self.icache_hit_rate) * self.icache_miss_penalty
        else:
            cache_penalty = 0
        
        # Hazard stalls
        hazard_penalty = self.hazard_stall_fraction * self.num_stages
        
        total_cpi = base_cpi + cache_penalty + hazard_penalty
        
        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc
        
        stage_results = []
        for stage_name, cycles in self.pipeline_stages.items():
            stage_results.append(StageResult(
                name=stage_name,
                service_time_cycles=cycles,
                utilization=cycles / bottleneck_cycles,
                queue_length=0,  # Simplified
                contribution_to_cpi=cycles / total_cpi
            ))
        
        return ArchitecturalAnalysis(
            processor=self.name,
            era=ProcessorEra.PIPELINED,
            workload='default',
            cpi=total_cpi,
            ipc=ipc,
            ips=ips,
            bottleneck_stage=bottleneck_stage,
            stage_results=stage_results,
            utilizations={s.name: s.utilization for s in stage_results}
        )
    
    @staticmethod
    def get_template() -> str:
        """Return Python code template for pipelined architecture"""
        return '''
class {ClassName}Model(BaseProcessorModel):
    """
    {ProcessorName} Grey-Box Queueing Model
    
    Architecture: Pipelined Execution (Era: 1979-1985)
    - {NumStages}-stage instruction pipeline
    - Pipeline hazards cause stalls
    - {CacheInfo}
    """
    
    # Processor specifications
    name = "{ProcessorName}"
    manufacturer = "{Manufacturer}"
    year = {Year}
    clock_mhz = {ClockMHz}
    transistor_count = {Transistors}
    data_width = {DataWidth}
    address_width = {AddressWidth}
    
    def __init__(self):
        # Pipeline stages and timing
        self.pipeline_stages = {
            'IF': {IFCycles},   # Instruction Fetch
            'ID': {IDCycles},   # Instruction Decode
            'OF': {OFCycles},   # Operand Fetch
            'EX': {EXCycles},   # Execute
            'WB': {WBCycles},   # Write Back
        }
        
        # Cache parameters
        self.has_icache = {HasICache}
        self.icache_hit_rate = {ICacheHitRate}
        self.icache_miss_penalty = {ICacheMissPenalty}
        
        # Instruction categories
        self.instruction_categories = {
            'alu_reg': InstructionCategory('alu_reg', {ALURegCycles}, 0, "ALU register operations"),
            'alu_mem': InstructionCategory('alu_mem', {ALUMemCycles}, {ALUMemMem}, "ALU with memory operand"),
            'load': InstructionCategory('load', {LoadCycles}, {LoadMem}, "Load from memory"),
            'store': InstructionCategory('store', {StoreCycles}, {StoreMem}, "Store to memory"),
            'branch': InstructionCategory('branch', {BranchCycles}, 0, "Branch/jump"),
            'multiply': InstructionCategory('multiply', {MultiplyCycles}, 0, "Multiply operations"),
            'divide': InstructionCategory('divide', {DivideCycles}, 0, "Divide operations"),
        }
        
        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu_reg': 0.30, 'alu_mem': 0.15, 'load': 0.20,
                'store': 0.12, 'branch': 0.15, 'multiply': 0.05, 'divide': 0.03,
            }, "Typical workload"),
            'compute': WorkloadProfile('compute', {
                'alu_reg': 0.45, 'alu_mem': 0.15, 'load': 0.10,
                'store': 0.05, 'branch': 0.10, 'multiply': 0.10, 'divide': 0.05,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu_reg': 0.15, 'alu_mem': 0.20, 'load': 0.30,
                'store': 0.20, 'branch': 0.10, 'multiply': 0.03, 'divide': 0.02,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu_reg': 0.20, 'alu_mem': 0.10, 'load': 0.15,
                'store': 0.10, 'branch': 0.35, 'multiply': 0.05, 'divide': 0.05,
            }, "Control-flow intensive"),
        }
    
    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using pipelined execution model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        
        # Find pipeline bottleneck
        bottleneck_stage = max(self.pipeline_stages, key=self.pipeline_stages.get)
        base_cpi = self.pipeline_stages[bottleneck_stage]
        
        # Calculate hazard stalls from instruction mix
        hazard_rate = 0.1  # Base structural hazards
        branch_weight = profile.category_weights.get('branch', 0.15)
        hazard_rate += branch_weight * 0.3  # Branch misprediction
        
        # Memory stalls
        mem_weight = sum(profile.category_weights.get(c, 0) for c in ['load', 'store', 'alu_mem'])
        mem_stalls = mem_weight * 0.2  # Memory latency
        
        # Cache effects
        if self.has_icache:
            cache_stalls = (1 - self.icache_hit_rate) * self.icache_miss_penalty
        else:
            cache_stalls = 0
        
        total_cpi = base_cpi + hazard_rate + mem_stalls + cache_stalls
        
        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc
        
        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=total_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck_stage,
            utilizations={s: c/total_cpi for s, c in self.pipeline_stages.items()}
        )
    
    def validate(self) -> Dict[str, Any]:
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}
    
    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories
    
    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles
'''


class CacheRISCArchitecture:
    """
    Cache/RISC Architecture (1983-1988)
    
    Models processors with cache hierarchies and RISC features:
    - ARM1, SPARC, MIPS R2000, Am29000, 80386, Transputer
    
    Architecture:
        ┌───────────┐
        │  I-Cache  │──► IF → ID → EX → MEM → WB
        └───────────┘                    │
                                   ┌─────▼─────┐
                                   │  D-Cache  │
                                   └───────────┘
    
    Features:
        - On-chip instruction cache
        - Load/store architecture
        - Single-cycle execution goal
        - Delayed branches (some)
        - Register windows (SPARC)
    """
    
    def __init__(self,
                 pipeline_depth: int = 5,
                 icache_size_kb: float = 4,
                 icache_hit_rate: float = 0.95,
                 dcache_size_kb: float = 0,  # 0 if no D-cache
                 dcache_hit_rate: float = 0.90,
                 memory_latency_cycles: int = 10,
                 has_delayed_branch: bool = False,
                 register_windows: int = 0,  # SPARC
                 clock_mhz: float = 16.0,
                 name: str = "CacheRISC"):
        
        self.name = name
        self.clock_mhz = clock_mhz
        self.pipeline_depth = pipeline_depth
        self.icache_size_kb = icache_size_kb
        self.icache_hit_rate = icache_hit_rate
        self.dcache_size_kb = dcache_size_kb
        self.dcache_hit_rate = dcache_hit_rate
        self.memory_latency_cycles = memory_latency_cycles
        self.has_delayed_branch = has_delayed_branch
        self.register_windows = register_windows
    
    def analyze(self, workload_weights: Optional[Dict[str, float]] = None) -> ArchitecturalAnalysis:
        """
        Analyze performance for Cache/RISC architecture.
        
        RISC goal: CPI ≈ 1.0
        Actual: CPI = 1.0 + cache_misses + hazards + branch_penalties
        """
        # Base CPI (RISC target)
        base_cpi = 1.0
        
        # I-cache miss penalty
        icache_miss_cpi = (1 - self.icache_hit_rate) * self.memory_latency_cycles
        
        # D-cache miss penalty (assume 30% load/store)
        load_store_fraction = 0.30
        if self.dcache_size_kb > 0:
            dcache_miss_cpi = load_store_fraction * (1 - self.dcache_hit_rate) * self.memory_latency_cycles
        else:
            dcache_miss_cpi = load_store_fraction * self.memory_latency_cycles * 0.3  # Some loads miss
        
        # Branch penalty
        branch_fraction = 0.15
        if self.has_delayed_branch:
            branch_penalty = branch_fraction * 0.1  # Mostly filled delay slots
        else:
            branch_penalty = branch_fraction * (self.pipeline_depth / 2)  # Flush penalty
        
        # Data hazards
        hazard_cpi = 0.1  # Load-use hazards
        
        total_cpi = base_cpi + icache_miss_cpi + dcache_miss_cpi + branch_penalty + hazard_cpi
        
        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc
        
        # Determine bottleneck
        penalties = {
            'icache': icache_miss_cpi,
            'dcache': dcache_miss_cpi,
            'branch': branch_penalty,
            'hazard': hazard_cpi,
        }
        bottleneck = max(penalties, key=penalties.get)
        
        stage_results = [
            StageResult("Base", base_cpi, base_cpi/total_cpi, 0, base_cpi),
            StageResult("I-Cache", icache_miss_cpi, icache_miss_cpi/total_cpi, 0, icache_miss_cpi),
            StageResult("D-Cache", dcache_miss_cpi, dcache_miss_cpi/total_cpi, 0, dcache_miss_cpi),
            StageResult("Branch", branch_penalty, branch_penalty/total_cpi, 0, branch_penalty),
        ]
        
        return ArchitecturalAnalysis(
            processor=self.name,
            era=ProcessorEra.CACHE_RISC,
            workload='default',
            cpi=total_cpi,
            ipc=ipc,
            ips=ips,
            bottleneck_stage=bottleneck,
            stage_results=stage_results,
            utilizations={s.name: s.utilization for s in stage_results}
        )
    
    @staticmethod
    def get_template() -> str:
        """Return Python code template for Cache/RISC architecture"""
        return '''
class {ClassName}Model(BaseProcessorModel):
    """
    {ProcessorName} Grey-Box Queueing Model
    
    Architecture: Cache/RISC (Era: 1983-1988)
    - {PipelineDepth}-stage pipeline
    - {ICacheSize}KB instruction cache
    - {DCacheInfo}
    - {BranchInfo}
    """
    
    # Processor specifications
    name = "{ProcessorName}"
    manufacturer = "{Manufacturer}"
    year = {Year}
    clock_mhz = {ClockMHz}
    transistor_count = {Transistors}
    data_width = {DataWidth}
    address_width = {AddressWidth}
    
    def __init__(self):
        # Pipeline configuration
        self.pipeline_depth = {PipelineDepth}
        
        # Cache configuration
        self.icache_size_kb = {ICacheSize}
        self.icache_hit_rate = {ICacheHitRate}
        self.dcache_size_kb = {DCacheSize}
        self.dcache_hit_rate = {DCacheHitRate}
        self.memory_latency = {MemoryLatency}
        
        # Branch handling
        self.has_delayed_branch = {HasDelayedBranch}
        self.branch_penalty = {BranchPenalty}
        
        # Instruction categories (RISC: most are single-cycle)
        self.instruction_categories = {
            'alu': InstructionCategory('alu', 1, 0, "ALU operations (single-cycle)"),
            'load': InstructionCategory('load', 1, {LoadLatency}, "Load from memory"),
            'store': InstructionCategory('store', 1, 0, "Store to memory"),
            'branch': InstructionCategory('branch', 1, 0, "Branch (+ penalty if taken)"),
            'multiply': InstructionCategory('multiply', {MultiplyCycles}, 0, "Multiply"),
            'divide': InstructionCategory('divide', {DivideCycles}, 0, "Divide"),
            'fp_single': InstructionCategory('fp_single', {FPSingleCycles}, 0, "FP single precision"),
            'fp_double': InstructionCategory('fp_double', {FPDoubleCycles}, 0, "FP double precision"),
        }
        
        # Workload profiles
        self.workload_profiles = {
            'typical': WorkloadProfile('typical', {
                'alu': 0.40, 'load': 0.20, 'store': 0.10,
                'branch': 0.15, 'multiply': 0.05, 'divide': 0.02,
                'fp_single': 0.05, 'fp_double': 0.03,
            }, "Typical RISC workload"),
            'compute': WorkloadProfile('compute', {
                'alu': 0.55, 'load': 0.10, 'store': 0.05,
                'branch': 0.10, 'multiply': 0.10, 'divide': 0.05,
                'fp_single': 0.03, 'fp_double': 0.02,
            }, "Compute-intensive"),
            'memory': WorkloadProfile('memory', {
                'alu': 0.20, 'load': 0.35, 'store': 0.20,
                'branch': 0.15, 'multiply': 0.03, 'divide': 0.02,
                'fp_single': 0.03, 'fp_double': 0.02,
            }, "Memory-intensive"),
            'control': WorkloadProfile('control', {
                'alu': 0.30, 'load': 0.15, 'store': 0.10,
                'branch': 0.35, 'multiply': 0.03, 'divide': 0.02,
                'fp_single': 0.03, 'fp_double': 0.02,
            }, "Control-flow intensive"),
        }
    
    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """Analyze using Cache/RISC model"""
        profile = self.workload_profiles.get(workload, self.workload_profiles['typical'])
        
        # Base CPI (RISC goal: 1.0)
        base_cpi = 1.0
        
        # I-cache miss penalty
        icache_miss_cpi = (1 - self.icache_hit_rate) * self.memory_latency
        
        # D-cache miss penalty
        load_weight = profile.category_weights.get('load', 0.20)
        store_weight = profile.category_weights.get('store', 0.10)
        mem_fraction = load_weight + store_weight
        
        if self.dcache_size_kb > 0:
            dcache_miss_cpi = mem_fraction * (1 - self.dcache_hit_rate) * self.memory_latency
        else:
            dcache_miss_cpi = load_weight * self.memory_latency * 0.3
        
        # Branch penalty
        branch_weight = profile.category_weights.get('branch', 0.15)
        taken_rate = 0.6  # Fraction of branches taken
        if self.has_delayed_branch:
            branch_cpi = branch_weight * taken_rate * 0.2  # Some unfilled delay slots
        else:
            branch_cpi = branch_weight * taken_rate * self.branch_penalty
        
        # Multi-cycle instructions
        mult_cpi = profile.category_weights.get('multiply', 0) * ({MultiplyCycles} - 1)
        div_cpi = profile.category_weights.get('divide', 0) * ({DivideCycles} - 1)
        
        total_cpi = base_cpi + icache_miss_cpi + dcache_miss_cpi + branch_cpi + mult_cpi + div_cpi
        
        ipc = 1.0 / total_cpi
        ips = self.clock_mhz * 1e6 * ipc
        
        # Bottleneck
        penalties = {'icache': icache_miss_cpi, 'dcache': dcache_miss_cpi, 'branch': branch_cpi}
        bottleneck = max(penalties, key=penalties.get) if max(penalties.values()) > 0.1 else 'balanced'
        
        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=total_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=penalties
        )
    
    def validate(self) -> Dict[str, Any]:
        return {"tests": [], "passed": 0, "total": 0, "accuracy_percent": None}
    
    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        return self.instruction_categories
    
    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        return self.workload_profiles
'''


# =============================================================================
# TEMPLATE REGISTRY
# =============================================================================

ERA_TEMPLATES = {
    ProcessorEra.SEQUENTIAL: SequentialArchitecture.get_template(),
    ProcessorEra.PREFETCH_QUEUE: PrefetchQueueArchitecture.get_template(),
    ProcessorEra.PIPELINED: PipelinedArchitecture.get_template(),
    ProcessorEra.CACHE_RISC: CacheRISCArchitecture.get_template(),
}


def get_template_for_processor(processor_name: str) -> Optional[str]:
    """Get the appropriate template for a processor"""
    era = get_processor_era(processor_name)
    if era:
        return ERA_TEMPLATES.get(era)
    return None


def get_architecture_class(era: ProcessorEra):
    """Get the architecture class for an era"""
    classes = {
        ProcessorEra.SEQUENTIAL: SequentialArchitecture,
        ProcessorEra.PREFETCH_QUEUE: PrefetchQueueArchitecture,
        ProcessorEra.PIPELINED: PipelinedArchitecture,
        ProcessorEra.CACHE_RISC: CacheRISCArchitecture,
    }
    return classes.get(era)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def print_era_summary():
    """Print summary of all eras and their processors"""
    print("=" * 70)
    print("ERA-SPECIFIC ARCHITECTURAL PATTERNS")
    print("=" * 70)
    
    for era, definition in ERA_DEFINITIONS.items():
        print(f"\n{definition.name} ({definition.year_start}-{definition.year_end})")
        print("-" * 50)
        print(f"Queueing Model: {definition.queueing_model}")
        print(f"Features:")
        for feature in definition.architectural_features[:3]:
            print(f"  • {feature}")
        print(f"Examples: {', '.join(definition.example_processors[:5])}")
    
    print("\n" + "=" * 70)


def get_processors_by_era(era: ProcessorEra) -> List[str]:
    """Get list of processors for an era"""
    return [p for p, e in PROCESSOR_ERA_MAP.items() if e == era]


if __name__ == '__main__':
    print_era_summary()
    
    print("\nProcessor count by era:")
    for era in ProcessorEra:
        processors = get_processors_by_era(era)
        print(f"  {era.name}: {len(processors)} processors")
