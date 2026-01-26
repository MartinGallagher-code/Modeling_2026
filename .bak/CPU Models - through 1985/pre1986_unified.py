#!/usr/bin/env python3
"""
Pre-1986 Microprocessor Unified Modeling Interface

A single interface to access ALL modeling capabilities for the complete
collection of 65 pre-1986 microprocessors.

FEATURES:
- Run queueing theory models
- Run CPI Stack analysis
- Compare processors side-by-side
- What-if analysis
- Export results to various formats
- Interactive CLI mode

SUPPORTED MODELS:
- 65 processors from 1971-1985
- Intel, Motorola, MOS/WDC, Zilog, RCA, TI, National, NEC, and others

Usage:
    # Python API
    from pre1986_unified import ModelingInterface
    interface = ModelingInterface()
    result = interface.analyze("Intel 8086")
    
    # Command line
    python pre1986_unified.py --processor "Intel 8086" --model both
    python pre1986_unified.py --compare "Intel 8080,Zilog Z80,MOS 6502"
    python pre1986_unified.py --interactive

Author: Grey-Box Performance Modeling Research
Date: January 25, 2026
"""

import json
import argparse
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from abc import ABC, abstractmethod


# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class ModelType(Enum):
    """Available model types."""
    QUEUEING = "queueing"
    CPI_STACK = "cpi_stack"
    BOTH = "both"


class ProcessorFamily(Enum):
    """Processor manufacturer families."""
    INTEL = "Intel"
    MOTOROLA = "Motorola"
    MOS_WDC = "MOS/WDC"
    ZILOG = "Zilog"
    RCA = "RCA"
    TI = "Texas Instruments"
    NATIONAL = "National Semiconductor"
    NEC = "NEC"
    OTHER = "Other"


class ProcessorCategory(Enum):
    """Architectural categories."""
    SIMPLE_4BIT = "4-bit"
    SIMPLE_8BIT = "Simple 8-bit"
    ENHANCED_8BIT = "Enhanced 8-bit"
    MCU_8BIT = "8-bit MCU"
    PREFETCH_16BIT = "16-bit with Prefetch"
    PROTECTED_16BIT = "16-bit Protected Mode"
    EARLY_32BIT = "Early 32-bit"
    FULL_32BIT = "Full 32-bit"
    RISC = "RISC"
    SPECIAL = "Special Architecture"


# =============================================================================
# PROCESSOR DATABASE
# =============================================================================

PROCESSORS = {
    # Intel 4-bit
    "Intel 4004": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.SIMPLE_4BIT,
        "year": 1971, "bits": 4, "clock_mhz": 0.74,
        "transistors": 2300, "process_um": 10,
        "description": "First commercial microprocessor",
        "base_cpi": 10.8, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 8, "mov": 8, "branch": 12, "memory": 8}
    },
    "Intel 4040": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.SIMPLE_4BIT,
        "year": 1974, "bits": 4, "clock_mhz": 0.74,
        "transistors": 3000, "process_um": 10,
        "description": "Enhanced 4004 with interrupts",
        "base_cpi": 10.5, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 8, "mov": 8, "branch": 12, "memory": 8}
    },
    
    # Intel 8-bit CPUs
    "Intel 8008": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1972, "bits": 8, "clock_mhz": 0.5,
        "transistors": 3500, "process_um": 10,
        "description": "First 8-bit microprocessor",
        "base_cpi": 20.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 8, "mov": 7, "branch": 11, "memory": 16}
    },
    "Intel 8080": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1974, "bits": 8, "clock_mhz": 2.0,
        "transistors": 4500, "process_um": 6,
        "description": "Foundation of personal computing",
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 5, "branch": 10, "memory": 7}
    },
    "Intel 8085": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1976, "bits": 8, "clock_mhz": 3.0,
        "transistors": 6500, "process_um": 3,
        "description": "Enhanced 8080 with single supply",
        "base_cpi": 9.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 7}
    },
    "Intel 8085a": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1976, "bits": 8, "clock_mhz": 5.0,
        "transistors": 6500, "process_um": 3,
        "description": "High-speed 8085 variant",
        "base_cpi": 9.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 7}
    },
    
    # Intel 8-bit MCUs
    "Intel 8035": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1976, "bits": 8, "clock_mhz": 6.0,
        "transistors": 5000, "process_um": 5,
        "description": "MCS-48 family, no internal ROM",
        "base_cpi": 15.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 1, "mov": 1, "branch": 2, "memory": 2}
    },
    "Intel 8039": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1976, "bits": 8, "clock_mhz": 6.0,
        "transistors": 5000, "process_um": 5,
        "description": "MCS-48 with 128 bytes RAM",
        "base_cpi": 15.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 1, "mov": 1, "branch": 2, "memory": 2}
    },
    "Intel 8048": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1976, "bits": 8, "clock_mhz": 6.0,
        "transistors": 6000, "process_um": 5,
        "description": "MCS-48 with 1KB ROM, 64B RAM",
        "base_cpi": 15.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 1, "mov": 1, "branch": 2, "memory": 2}
    },
    "Intel 8051": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1980, "bits": 8, "clock_mhz": 12.0,
        "transistors": 60000, "process_um": 3,
        "description": "MCS-51, most popular MCU ever",
        "base_cpi": 12.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 1, "mov": 1, "branch": 2, "memory": 2}
    },
    "Intel 8096": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1982, "bits": 16, "clock_mhz": 12.0,
        "transistors": 120000, "process_um": 1.5,
        "description": "16-bit MCU for automotive",
        "base_cpi": 8.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 2,
        "timings": {"alu": 4, "mov": 4, "branch": 8, "memory": 6}
    },
    
    # Intel 16-bit
    "Intel 8086": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1978, "bits": 16, "clock_mhz": 5.0,
        "transistors": 29000, "process_um": 3,
        "description": "Foundation of x86 architecture",
        "base_cpi": 9.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 6,
        "timings": {"alu": 3, "mov": 2, "branch": 15, "memory": 9, "mul": 118}
    },
    "Intel 8088": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1979, "bits": 16, "clock_mhz": 5.0,
        "transistors": 29000, "process_um": 3,
        "description": "8086 with 8-bit bus (IBM PC)",
        "base_cpi": 12.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 4,
        "bus_width": 8,
        "timings": {"alu": 3, "mov": 2, "branch": 15, "memory": 13, "mul": 118}
    },
    "Intel 80186": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1982, "bits": 16, "clock_mhz": 8.0,
        "transistors": 55000, "process_um": 3,
        "description": "8086 with integrated peripherals",
        "base_cpi": 8.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 6,
        "timings": {"alu": 3, "mov": 2, "branch": 14, "memory": 8, "mul": 36}
    },
    "Intel 80188": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1982, "bits": 16, "clock_mhz": 8.0,
        "transistors": 55000, "process_um": 3,
        "description": "80186 with 8-bit bus",
        "base_cpi": 10.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 4,
        "bus_width": 8,
        "timings": {"alu": 3, "mov": 2, "branch": 14, "memory": 12, "mul": 36}
    },
    "Intel 80286": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.PROTECTED_16BIT,
        "year": 1982, "bits": 16, "clock_mhz": 6.0,
        "transistors": 134000, "process_um": 1.5,
        "description": "First x86 with protected mode",
        "base_cpi": 6.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 3, "branch_penalty": 3, "prefetch_bytes": 6,
        "timings": {"alu": 2, "mov": 2, "branch": 7, "memory": 5, "mul": 21}
    },
    "Intel 80386": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.FULL_32BIT,
        "year": 1985, "bits": 32, "clock_mhz": 16.0,
        "transistors": 275000, "process_um": 1.5,
        "description": "First 32-bit x86, virtual memory",
        "base_cpi": 5.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 4, "branch_penalty": 4, "prefetch_bytes": 16,
        "timings": {"alu": 2, "mov": 2, "branch": 7, "memory": 4, "mul": 12}
    },
    "Intel iapx 432": {
        "family": ProcessorFamily.INTEL,
        "category": ProcessorCategory.SPECIAL,
        "year": 1981, "bits": 32, "clock_mhz": 5.0,
        "transistors": 200000, "process_um": 2,
        "description": "Object-oriented CPU, commercial failure",
        "base_cpi": 20.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 8,
        "timings": {"alu": 6, "mov": 8, "branch": 20, "memory": 15}
    },
    
    # Motorola 6800 family
    "Motorola 6800": {
        "family": ProcessorFamily.MOTOROLA,
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1974, "bits": 8, "clock_mhz": 1.0,
        "transistors": 4100, "process_um": 6,
        "description": "Motorola's first microprocessor",
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 4, "memory": 5}
    },
    "Motorola 6801": {
        "family": ProcessorFamily.MOTOROLA,
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1978, "bits": 8, "clock_mhz": 1.0,
        "transistors": 10000, "process_um": 5,
        "description": "6800-based MCU with RAM/ROM",
        "base_cpi": 9.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 4, "memory": 4}
    },
    "Motorola 6802": {
        "family": ProcessorFamily.MOTOROLA,
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1977, "bits": 8, "clock_mhz": 1.0,
        "transistors": 5000, "process_um": 5,
        "description": "6800 with internal clock and RAM",
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 4, "memory": 5}
    },
    "Motorola 6803": {
        "family": ProcessorFamily.MOTOROLA,
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1983, "bits": 8, "clock_mhz": 1.0,
        "transistors": 12000, "process_um": 3,
        "description": "Enhanced 6801 MCU",
        "base_cpi": 9.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 4, "memory": 4}
    },
    "Motorola 6805": {
        "family": ProcessorFamily.MOTOROLA,
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1979, "bits": 8, "clock_mhz": 4.0,
        "transistors": 8000, "process_um": 4,
        "description": "Low-cost MCU family",
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 3, "mov": 4, "branch": 5, "memory": 5}
    },
    "Motorola 6809": {
        "family": ProcessorFamily.MOTOROLA,
        "category": ProcessorCategory.ENHANCED_8BIT,
        "year": 1979, "bits": 8, "clock_mhz": 1.0,
        "transistors": 9000, "process_um": 5,
        "description": "Advanced 8-bit, position-independent code",
        "base_cpi": 7.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 3, "memory": 4}
    },
    
    # Motorola 68000 family
    "Motorola 68000": {
        "family": ProcessorFamily.MOTOROLA,
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1979, "bits": 32, "clock_mhz": 8.0,
        "transistors": 68000, "process_um": 3.5,
        "description": "Revolutionary 32-bit architecture",
        "base_cpi": 7.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 4,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 8, "mul": 70}
    },
    "Motorola 68008": {
        "family": ProcessorFamily.MOTOROLA,
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1982, "bits": 32, "clock_mhz": 8.0,
        "transistors": 70000, "process_um": 3,
        "description": "68000 with 8-bit bus",
        "base_cpi": 10.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 2,
        "bus_width": 8,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 12, "mul": 70}
    },
    "Motorola 68010": {
        "family": ProcessorFamily.MOTOROLA,
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1982, "bits": 32, "clock_mhz": 10.0,
        "transistors": 84000, "process_um": 2.5,
        "description": "68000 with virtual memory support",
        "base_cpi": 6.5, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 4,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 7, "mul": 70}
    },
    "Motorola 68020": {
        "family": ProcessorFamily.MOTOROLA,
        "category": ProcessorCategory.FULL_32BIT,
        "year": 1984, "bits": 32, "clock_mhz": 16.0,
        "transistors": 190000, "process_um": 2,
        "description": "Full 32-bit with instruction cache",
        "base_cpi": 4.5, "has_prefetch": True, "has_cache": True,
        "pipeline_stages": 3, "branch_penalty": 3, "prefetch_bytes": 256,
        "cache_size": 256, "cache_hit_rate": 0.90,
        "timings": {"alu": 2, "mov": 2, "branch": 6, "memory": 3, "mul": 28}
    },
    
    # MOS/WDC 6502 family
    "MOS 6502": {
        "family": ProcessorFamily.MOS_WDC,
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1975, "bits": 8, "clock_mhz": 1.0,
        "transistors": 3510, "process_um": 8,
        "description": "$25 CPU that enabled home computers",
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 3, "memory": 4}
    },
    "WDC 65c02": {
        "family": ProcessorFamily.MOS_WDC,
        "category": ProcessorCategory.ENHANCED_8BIT,
        "year": 1983, "bits": 8, "clock_mhz": 4.0,
        "transistors": 5000, "process_um": 3,
        "description": "CMOS 6502 with extra instructions",
        "base_cpi": 9.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 3, "memory": 4}
    },
    "WDC 65802": {
        "family": ProcessorFamily.MOS_WDC,
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1984, "bits": 16, "clock_mhz": 4.0,
        "transistors": 8000, "process_um": 2,
        "description": "65816 in 6502-compatible package",
        "base_cpi": 8.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 1,
        "timings": {"alu": 2, "mov": 3, "branch": 3, "memory": 4}
    },
    "WDC 65816": {
        "family": ProcessorFamily.MOS_WDC,
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1984, "bits": 16, "clock_mhz": 2.8,
        "transistors": 22000, "process_um": 2,
        "description": "16-bit 6502, used in Apple IIGS/SNES",
        "base_cpi": 8.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 1,
        "timings": {"alu": 2, "mov": 3, "branch": 3, "memory": 5}
    },
    
    # Zilog
    "Zilog Z80": {
        "family": ProcessorFamily.ZILOG,
        "category": ProcessorCategory.ENHANCED_8BIT,
        "year": 1976, "bits": 8, "clock_mhz": 2.5,
        "transistors": 8500, "process_um": 4,
        "description": "Most popular 8-bit CPU ever",
        "base_cpi": 8.5, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 7}
    },
    "Zilog Z180": {
        "family": ProcessorFamily.ZILOG,
        "category": ProcessorCategory.ENHANCED_8BIT,
        "year": 1985, "bits": 8, "clock_mhz": 6.0,
        "transistors": 20000, "process_um": 2,
        "description": "Enhanced Z80 with MMU",
        "base_cpi": 6.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 3, "mov": 3, "branch": 8, "memory": 5}
    },
    "Zilog Z280": {
        "family": ProcessorFamily.ZILOG,
        "category": ProcessorCategory.PROTECTED_16BIT,
        "year": 1985, "bits": 16, "clock_mhz": 12.0,
        "transistors": 75000, "process_um": 1.5,
        "description": "16-bit Z80 with cache and MMU",
        "base_cpi": 5.0, "has_prefetch": True, "has_cache": True,
        "pipeline_stages": 2, "branch_penalty": 3,
        "timings": {"alu": 2, "mov": 2, "branch": 6, "memory": 4}
    },
    "Zilog Z8": {
        "family": ProcessorFamily.ZILOG,
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1979, "bits": 8, "clock_mhz": 8.0,
        "transistors": 10000, "process_um": 4,
        "description": "8-bit MCU with 124 registers",
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 6, "mov": 6, "branch": 12, "memory": 8}
    },
    "Zilog Z8000": {
        "family": ProcessorFamily.ZILOG,
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1979, "bits": 16, "clock_mhz": 4.0,
        "transistors": 17500, "process_um": 4,
        "description": "16-bit CPU, segmented/non-segmented",
        "base_cpi": 9.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 2,
        "timings": {"alu": 4, "mov": 3, "branch": 7, "memory": 7}
    },
    "Zilog Z80 Peripherals": {
        "family": ProcessorFamily.ZILOG,
        "category": ProcessorCategory.SPECIAL,
        "year": 1976, "bits": 8, "clock_mhz": 2.5,
        "transistors": 8500, "process_um": 4,
        "description": "Z80 peripheral chip modeling",
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 7}
    },
    
    # RCA COSMAC
    "RCA 1802": {
        "family": ProcessorFamily.RCA,
        "category": ProcessorCategory.SPECIAL,
        "year": 1976, "bits": 8, "clock_mhz": 2.0,
        "transistors": 5000, "process_um": 5,
        "description": "Radiation-hardened, still on Voyager",
        "base_cpi": 20.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 16, "mov": 16, "branch": 16, "memory": 16}
    },
    "RCA CDP1804": {
        "family": ProcessorFamily.RCA,
        "category": ProcessorCategory.SPECIAL,
        "year": 1980, "bits": 8, "clock_mhz": 2.0,
        "transistors": 6000, "process_um": 4,
        "description": "Enhanced 1802 with timer",
        "base_cpi": 18.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 14, "mov": 14, "branch": 14, "memory": 14}
    },
    "RCA CDP1805": {
        "family": ProcessorFamily.RCA,
        "category": ProcessorCategory.SPECIAL,
        "year": 1984, "bits": 8, "clock_mhz": 4.0,
        "transistors": 8000, "process_um": 3,
        "description": "Faster COSMAC with more instructions",
        "base_cpi": 16.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 12, "mov": 12, "branch": 12, "memory": 12}
    },
    "RCA CDP1806": {
        "family": ProcessorFamily.RCA,
        "category": ProcessorCategory.SPECIAL,
        "year": 1985, "bits": 8, "clock_mhz": 4.0,
        "transistors": 9000, "process_um": 2,
        "description": "Latest COSMAC variant",
        "base_cpi": 14.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 10, "mov": 10, "branch": 10, "memory": 10}
    },
    
    # Texas Instruments
    "TI TMS1000": {
        "family": ProcessorFamily.TI,
        "category": ProcessorCategory.SIMPLE_4BIT,
        "year": 1974, "bits": 4, "clock_mhz": 0.4,
        "transistors": 8000, "process_um": 8,
        "description": "First single-chip microcontroller",
        "base_cpi": 25.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 1, "mov": 1, "branch": 2, "memory": 2}
    },
    "TI TMS7000": {
        "family": ProcessorFamily.TI,
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1981, "bits": 8, "clock_mhz": 10.0,
        "transistors": 20000, "process_um": 3,
        "description": "8-bit MCU family",
        "base_cpi": 11.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 5, "mov": 5, "branch": 7, "memory": 7}
    },
    "TI TMS9900": {
        "family": ProcessorFamily.TI,
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1976, "bits": 16, "clock_mhz": 3.0,
        "transistors": 8000, "process_um": 6,
        "description": "First 16-bit single-chip CPU",
        "base_cpi": 12.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 8, "mov": 8, "branch": 12, "memory": 10}
    },
    "TI TMS9995": {
        "family": ProcessorFamily.TI,
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1981, "bits": 16, "clock_mhz": 12.0,
        "transistors": 20000, "process_um": 3,
        "description": "Enhanced TMS9900",
        "base_cpi": 8.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 8, "memory": 6}
    },
    
    # National Semiconductor
    "NSC NSC800": {
        "family": ProcessorFamily.NATIONAL,
        "category": ProcessorCategory.ENHANCED_8BIT,
        "year": 1979, "bits": 8, "clock_mhz": 4.0,
        "transistors": 10000, "process_um": 4,
        "description": "Z80-compatible with CMOS",
        "base_cpi": 8.5, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 7}
    },
    "National Semiconductor NS32016": {
        "family": ProcessorFamily.NATIONAL,
        "category": ProcessorCategory.FULL_32BIT,
        "year": 1982, "bits": 32, "clock_mhz": 10.0,
        "transistors": 60000, "process_um": 3,
        "description": "32-bit CPU with orthogonal design",
        "base_cpi": 10.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4,
        "timings": {"alu": 4, "mov": 3, "branch": 8, "memory": 6}
    },
    "National Semiconductor NS32032": {
        "family": ProcessorFamily.NATIONAL,
        "category": ProcessorCategory.FULL_32BIT,
        "year": 1984, "bits": 32, "clock_mhz": 10.0,
        "transistors": 80000, "process_um": 2,
        "description": "Enhanced NS32016",
        "base_cpi": 8.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4,
        "timings": {"alu": 3, "mov": 3, "branch": 7, "memory": 5}
    },
    
    # NEC
    "NEC V20": {
        "family": ProcessorFamily.NEC,
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1984, "bits": 16, "clock_mhz": 8.0,
        "transistors": 63000, "process_um": 2,
        "description": "8086-compatible, faster execution",
        "base_cpi": 8.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 6,
        "timings": {"alu": 2, "mov": 2, "branch": 12, "memory": 8, "mul": 100}
    },
    "NEC V30": {
        "family": ProcessorFamily.NEC,
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1984, "bits": 16, "clock_mhz": 10.0,
        "transistors": 63000, "process_um": 2,
        "description": "8088-compatible, faster than original",
        "base_cpi": 7.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 6,
        "timings": {"alu": 2, "mov": 2, "branch": 12, "memory": 7, "mul": 100}
    },
    
    # Others
    "AMD 2901": {
        "family": ProcessorFamily.OTHER,
        "category": ProcessorCategory.SPECIAL,
        "year": 1975, "bits": 4, "clock_mhz": 10.0,
        "transistors": 1000, "process_um": 7,
        "description": "4-bit slice ALU, build any width",
        "base_cpi": 1.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 1, "mov": 1, "branch": 1, "memory": 1}
    },
    "ARM1": {
        "family": ProcessorFamily.OTHER,
        "category": ProcessorCategory.RISC,
        "year": 1985, "bits": 32, "clock_mhz": 6.0,
        "transistors": 25000, "process_um": 3,
        "description": "First ARM, RISC pioneer",
        "base_cpi": 2.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 3, "branch_penalty": 2,
        "timings": {"alu": 1, "mov": 1, "branch": 3, "memory": 2}
    },
    "MIPS R2000": {
        "family": ProcessorFamily.OTHER,
        "category": ProcessorCategory.RISC,
        "year": 1985, "bits": 32, "clock_mhz": 8.0,
        "transistors": 110000, "process_um": 2,
        "description": "Classic RISC, 5-stage pipeline",
        "base_cpi": 1.7, "has_prefetch": True, "has_cache": True,
        "pipeline_stages": 5, "branch_penalty": 1,
        "cache_hit_rate": 0.95,
        "timings": {"alu": 1, "mov": 1, "branch": 1, "memory": 1}
    },
    "Fairchild F8": {
        "family": ProcessorFamily.OTHER,
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1975, "bits": 8, "clock_mhz": 2.0,
        "transistors": 5000, "process_um": 8,
        "description": "Multi-chip CPU architecture",
        "base_cpi": 12.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 6, "memory": 6}
    },
    "Ferranti F100-L": {
        "family": ProcessorFamily.OTHER,
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1976, "bits": 16, "clock_mhz": 8.0,
        "transistors": 12000, "process_um": 5,
        "description": "UK military processor",
        "base_cpi": 6.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 2,
        "timings": {"alu": 2, "mov": 2, "branch": 4, "memory": 4}
    },
    "GI CP1600": {
        "family": ProcessorFamily.OTHER,
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1975, "bits": 16, "clock_mhz": 1.0,
        "transistors": 8000, "process_um": 6,
        "description": "Intellivision game console CPU",
        "base_cpi": 12.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 6, "mov": 6, "branch": 10, "memory": 8}
    },
    "GI PIC1650": {
        "family": ProcessorFamily.OTHER,
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1977, "bits": 8, "clock_mhz": 4.0,
        "transistors": 2000, "process_um": 6,
        "description": "First PIC microcontroller",
        "base_cpi": 4.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 1, "mov": 1, "branch": 2, "memory": 1}
    },
    "Hitachi 6309": {
        "family": ProcessorFamily.OTHER,
        "category": ProcessorCategory.ENHANCED_8BIT,
        "year": 1982, "bits": 8, "clock_mhz": 2.0,
        "transistors": 12000, "process_um": 3,
        "description": "Enhanced 6809 with extra features",
        "base_cpi": 5.5, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 2, "branch": 3, "memory": 4}
    },
    "Intersil 6100": {
        "family": ProcessorFamily.OTHER,
        "category": ProcessorCategory.SPECIAL,
        "year": 1975, "bits": 12, "clock_mhz": 4.0,
        "transistors": 4000, "process_um": 6,
        "description": "PDP-8 compatible on a chip",
        "base_cpi": 8.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 3, "mov": 3, "branch": 4, "memory": 5}
    },
    "Rockwell R6511": {
        "family": ProcessorFamily.OTHER,
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1980, "bits": 8, "clock_mhz": 2.0,
        "transistors": 6000, "process_um": 4,
        "description": "6502-based MCU",
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 3, "memory": 4}
    },
    "Signetics 2650": {
        "family": ProcessorFamily.OTHER,
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1975, "bits": 8, "clock_mhz": 1.25,
        "transistors": 5000, "process_um": 7,
        "description": "Unique architecture, used in gaming",
        "base_cpi": 11.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 6, "memory": 6}
    },
}


# =============================================================================
# WORKLOAD DEFINITIONS
# =============================================================================

@dataclass
class Workload:
    """Workload characteristics for performance analysis."""
    name: str = "typical"
    description: str = "Typical mixed workload"
    
    # Instruction mix
    mix_alu: float = 0.35
    mix_mov: float = 0.25
    mix_branch: float = 0.15
    mix_memory: float = 0.20
    mix_other: float = 0.05
    
    # Behavior characteristics
    branch_taken_rate: float = 0.60
    memory_operand_rate: float = 0.40
    cache_hit_rate: float = 0.90
    
    def validate(self):
        total = self.mix_alu + self.mix_mov + self.mix_branch + self.mix_memory + self.mix_other
        assert abs(total - 1.0) < 0.01, f"Mix sums to {total}, not 1.0"
    
    def to_dict(self) -> Dict:
        return asdict(self)


WORKLOADS = {
    "typical": Workload(
        name="typical",
        description="Typical mixed workload"
    ),
    "compute": Workload(
        name="compute",
        description="Compute-intensive (high ALU)",
        mix_alu=0.50, mix_mov=0.20, mix_branch=0.10, 
        mix_memory=0.15, mix_other=0.05,
        branch_taken_rate=0.50
    ),
    "memory": Workload(
        name="memory",
        description="Memory-intensive (high load/store)",
        mix_alu=0.20, mix_mov=0.15, mix_branch=0.10, 
        mix_memory=0.50, mix_other=0.05,
        memory_operand_rate=0.60
    ),
    "control": Workload(
        name="control",
        description="Control-heavy (high branch)",
        mix_alu=0.25, mix_mov=0.20, mix_branch=0.35, 
        mix_memory=0.15, mix_other=0.05,
        branch_taken_rate=0.70
    ),
    "string": Workload(
        name="string",
        description="String processing",
        mix_alu=0.15, mix_mov=0.30, mix_branch=0.15, 
        mix_memory=0.35, mix_other=0.05,
        memory_operand_rate=0.55
    ),
}


# =============================================================================
# RESULT CLASSES
# =============================================================================

@dataclass
class QueueingResult:
    """Result from queueing theory model."""
    ipc: float = 0.0
    mips: float = 0.0
    bottleneck: str = ""
    utilizations: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CPIStackResult:
    """Result from CPI Stack analysis."""
    cpi_base: float = 0.0
    cpi_prefetch: float = 0.0
    cpi_branch: float = 0.0
    cpi_memory: float = 0.0
    cpi_cache: float = 0.0
    cpi_pipeline: float = 0.0
    
    cpi_total: float = 0.0
    ipc: float = 0.0
    mips: float = 0.0
    
    bottleneck: str = ""
    breakdown: Dict[str, float] = field(default_factory=dict)
    
    def compute_totals(self, clock_mhz: float):
        self.cpi_total = (self.cpi_base + self.cpi_prefetch + self.cpi_branch +
                          self.cpi_memory + self.cpi_cache + self.cpi_pipeline)
        self.ipc = 1.0 / self.cpi_total if self.cpi_total > 0 else 0
        self.mips = clock_mhz * self.ipc
        
        if self.cpi_total > 0:
            self.breakdown = {
                'base': 100 * self.cpi_base / self.cpi_total,
                'prefetch': 100 * self.cpi_prefetch / self.cpi_total,
                'branch': 100 * self.cpi_branch / self.cpi_total,
                'memory': 100 * self.cpi_memory / self.cpi_total,
                'cache': 100 * self.cpi_cache / self.cpi_total,
                'pipeline': 100 * self.cpi_pipeline / self.cpi_total,
            }
            penalties = {k: v for k, v in self.breakdown.items() if k != 'base' and v > 0}
            self.bottleneck = max(penalties, key=penalties.get) if penalties else "none"
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class UnifiedResult:
    """Combined result from both models."""
    processor: str
    workload: str
    
    # Processor info
    year: int = 0
    bits: int = 0
    clock_mhz: float = 0.0
    family: str = ""
    category: str = ""
    description: str = ""
    
    # Queueing results
    queueing: Optional[QueueingResult] = None
    
    # CPI Stack results
    cpi_stack: Optional[CPIStackResult] = None
    
    # Summary
    best_ipc: float = 0.0
    best_mips: float = 0.0
    
    def to_dict(self) -> Dict:
        result = {
            'processor': self.processor,
            'workload': self.workload,
            'year': self.year,
            'bits': self.bits,
            'clock_mhz': self.clock_mhz,
            'family': self.family,
            'category': self.category,
            'description': self.description,
            'best_ipc': self.best_ipc,
            'best_mips': self.best_mips,
        }
        if self.queueing:
            result['queueing'] = self.queueing.to_dict()
        if self.cpi_stack:
            result['cpi_stack'] = self.cpi_stack.to_dict()
        return result


# =============================================================================
# UNIFIED MODELING INTERFACE
# =============================================================================

class ModelingInterface:
    """
    Unified interface for all pre-1986 microprocessor models.
    
    Provides access to:
    - Queueing theory models
    - CPI Stack analysis
    - Processor comparison
    - What-if analysis
    - Result export
    
    Usage:
        interface = ModelingInterface()
        
        # List available processors
        processors = interface.list_processors()
        
        # Analyze a processor
        result = interface.analyze("Intel 8086")
        
        # Compare processors
        comparison = interface.compare(["Intel 8080", "Zilog Z80", "MOS 6502"])
        
        # What-if analysis
        whatif = interface.what_if("Intel 8086", "clock_mhz", [5, 8, 10])
    """
    
    def __init__(self):
        self.processors = PROCESSORS
        self.workloads = WORKLOADS
    
    # -------------------------------------------------------------------------
    # LISTING AND INFO
    # -------------------------------------------------------------------------
    
    def list_processors(self, 
                        family: ProcessorFamily = None,
                        category: ProcessorCategory = None,
                        year_range: Tuple[int, int] = None,
                        bits: int = None) -> List[str]:
        """
        List available processors with optional filters.
        
        Args:
            family: Filter by manufacturer family
            category: Filter by architectural category
            year_range: Filter by year range (min, max)
            bits: Filter by data width
        
        Returns:
            List of processor names
        """
        result = []
        for name, spec in self.processors.items():
            if family and spec.get("family") != family:
                continue
            if category and spec.get("category") != category:
                continue
            if year_range:
                year = spec.get("year", 0)
                if year < year_range[0] or year > year_range[1]:
                    continue
            if bits and spec.get("bits") != bits:
                continue
            result.append(name)
        return sorted(result)
    
    def list_families(self) -> List[str]:
        """List all processor families."""
        return [f.value for f in ProcessorFamily]
    
    def list_categories(self) -> List[str]:
        """List all architectural categories."""
        return [c.value for c in ProcessorCategory]
    
    def list_workloads(self) -> List[str]:
        """List available workload types."""
        return list(self.workloads.keys())
    
    def get_processor_info(self, processor: str) -> Dict:
        """Get detailed information about a processor."""
        if processor not in self.processors:
            raise ValueError(f"Unknown processor: {processor}")
        
        spec = self.processors[processor].copy()
        spec['family'] = spec['family'].value
        spec['category'] = spec['category'].value
        return spec
    
    def get_workload(self, name: str) -> Workload:
        """Get a workload by name."""
        if name not in self.workloads:
            raise ValueError(f"Unknown workload: {name}")
        return self.workloads[name]
    
    # -------------------------------------------------------------------------
    # MODEL EXECUTION
    # -------------------------------------------------------------------------
    
    def _run_queueing_model(self, processor: str, 
                            spec: Dict, 
                            workload: Workload) -> QueueingResult:
        """Run queueing theory model."""
        result = QueueingResult()
        
        # Simplified queueing calculation
        timings = spec.get("timings", {})
        
        # Calculate weighted service time
        service_time = (
            workload.mix_alu * timings.get("alu", 4) +
            workload.mix_mov * timings.get("mov", 4) +
            workload.mix_branch * timings.get("branch", 8) +
            workload.mix_memory * timings.get("memory", 8) +
            workload.mix_other * 5
        )
        
        # Add prefetch effects
        if spec.get("has_prefetch", False):
            prefetch_bytes = spec.get("prefetch_bytes", 4)
            if prefetch_bytes < 6:
                service_time *= 1.05  # Small queue penalty
        
        # Calculate utilization and throughput
        arrival_rate = 0.1  # Normalized
        util = arrival_rate * service_time
        
        if util >= 1.0:
            result.ipc = 0.01
            result.bottleneck = "saturated"
        else:
            result.ipc = 1.0 / service_time
            
            # Determine bottleneck
            if spec.get("has_prefetch", False) and spec.get("bus_width", 16) < spec.get("bits", 8):
                result.bottleneck = "bus_interface"
            else:
                result.bottleneck = "execution_unit"
        
        result.mips = spec.get("clock_mhz", 1.0) * result.ipc
        result.utilizations = {
            "EU": min(util, 0.95),
            "BIU": min(util * 0.7, 0.95) if spec.get("has_prefetch") else 0
        }
        
        return result
    
    def _run_cpi_stack_model(self, processor: str, 
                              spec: Dict, 
                              workload: Workload) -> CPIStackResult:
        """Run CPI Stack analysis."""
        result = CPIStackResult()
        timings = spec.get("timings", {})
        
        # Base CPI from instruction mix
        result.cpi_base = (
            workload.mix_alu * timings.get("alu", 4) +
            workload.mix_mov * timings.get("mov", 4) +
            workload.mix_branch * timings.get("branch", 8) +
            workload.mix_memory * timings.get("memory", 8) +
            workload.mix_other * 5
        )
        
        # Prefetch penalty
        if spec.get("has_prefetch", False):
            prefetch_bytes = spec.get("prefetch_bytes", 4)
            bus_width = spec.get("bus_width", spec["bits"] // 8)
            stall_factor = max(0, (6 - prefetch_bytes) * 0.05)
            if bus_width < spec["bits"] // 8:
                stall_factor *= 1.5
            result.cpi_prefetch = result.cpi_base * stall_factor
        
        # Branch penalty
        if spec.get("pipeline_stages", 1) > 1:
            branch_penalty = spec.get("branch_penalty", 0)
            taken = workload.mix_branch * workload.branch_taken_rate
            result.cpi_branch = taken * branch_penalty
        
        # Memory penalty
        memory_cycles = timings.get("memory", 8)
        base_cycles = timings.get("alu", 4)
        extra = max(0, memory_cycles - base_cycles)
        result.cpi_memory = workload.memory_operand_rate * extra * 0.3
        
        # Cache miss penalty
        if spec.get("has_cache", False):
            hit_rate = spec.get("cache_hit_rate", 0.90)
            miss_rate = 1 - hit_rate
            memory_accesses = workload.mix_memory + workload.memory_operand_rate * 0.3
            result.cpi_cache = memory_accesses * miss_rate * 10
        
        # Pipeline hazard penalty
        if spec.get("pipeline_stages", 1) >= 3:
            stages = spec["pipeline_stages"]
            result.cpi_pipeline = result.cpi_base * 0.02 * (stages - 2)
        
        result.compute_totals(spec.get("clock_mhz", 1.0))
        return result
    
    def analyze(self, processor: str, 
                workload: str = "typical",
                model: ModelType = ModelType.BOTH) -> UnifiedResult:
        """
        Analyze a processor with specified model(s).
        
        Args:
            processor: Processor name
            workload: Workload name or Workload object
            model: Which model(s) to run
        
        Returns:
            UnifiedResult with all analysis results
        """
        if processor not in self.processors:
            raise ValueError(f"Unknown processor: {processor}")
        
        spec = self.processors[processor]
        
        if isinstance(workload, str):
            if workload not in self.workloads:
                raise ValueError(f"Unknown workload: {workload}")
            wl = self.workloads[workload]
        else:
            wl = workload
        
        wl.validate()
        
        result = UnifiedResult(
            processor=processor,
            workload=wl.name,
            year=spec.get("year", 0),
            bits=spec.get("bits", 0),
            clock_mhz=spec.get("clock_mhz", 0),
            family=spec.get("family", ProcessorFamily.OTHER).value,
            category=spec.get("category", ProcessorCategory.SIMPLE_8BIT).value,
            description=spec.get("description", "")
        )
        
        # Run queueing model
        if model in (ModelType.QUEUEING, ModelType.BOTH):
            result.queueing = self._run_queueing_model(processor, spec, wl)
        
        # Run CPI Stack model
        if model in (ModelType.CPI_STACK, ModelType.BOTH):
            result.cpi_stack = self._run_cpi_stack_model(processor, spec, wl)
        
        # Calculate best IPC/MIPS
        ipcs = []
        if result.queueing:
            ipcs.append(result.queueing.ipc)
        if result.cpi_stack:
            ipcs.append(result.cpi_stack.ipc)
        
        if ipcs:
            result.best_ipc = sum(ipcs) / len(ipcs)
            result.best_mips = result.best_ipc * result.clock_mhz
        
        return result
    
    def compare(self, processors: List[str],
                workload: str = "typical",
                model: ModelType = ModelType.BOTH) -> Dict[str, UnifiedResult]:
        """
        Compare multiple processors.
        
        Args:
            processors: List of processor names
            workload: Workload name
            model: Which model(s) to run
        
        Returns:
            Dict mapping processor names to results
        """
        results = {}
        for proc in processors:
            if proc in self.processors:
                results[proc] = self.analyze(proc, workload, model)
        return results
    
    def compare_all(self, workload: str = "typical",
                    model: ModelType = ModelType.BOTH) -> Dict[str, UnifiedResult]:
        """Compare all processors."""
        return self.compare(list(self.processors.keys()), workload, model)
    
    def what_if(self, processor: str,
                parameter: str,
                values: List[Any],
                workload: str = "typical") -> List[Tuple[Any, UnifiedResult]]:
        """
        What-if analysis: vary a parameter and see effects.
        
        Args:
            processor: Processor name
            parameter: Parameter to vary (e.g., "clock_mhz", "branch_taken_rate")
            values: List of values to try
            workload: Workload name
        
        Returns:
            List of (value, result) tuples
        """
        results = []
        
        # Get base specs
        if processor not in self.processors:
            raise ValueError(f"Unknown processor: {processor}")
        
        base_spec = self.processors[processor].copy()
        base_workload = self.workloads.get(workload, WORKLOADS["typical"])
        
        for value in values:
            # Modify parameter
            if parameter in base_spec:
                # Processor parameter
                modified_spec = base_spec.copy()
                modified_spec[parameter] = value
                self.processors[processor] = modified_spec
                result = self.analyze(processor, workload)
                self.processors[processor] = base_spec  # Restore
            elif hasattr(base_workload, parameter):
                # Workload parameter
                modified_wl = Workload(**{**asdict(base_workload), parameter: value})
                try:
                    modified_wl.validate()
                    result = self.analyze(processor, modified_wl)
                except AssertionError:
                    continue
            else:
                raise ValueError(f"Unknown parameter: {parameter}")
            
            results.append((value, result))
        
        return results
    
    # -------------------------------------------------------------------------
    # OUTPUT FORMATTING
    # -------------------------------------------------------------------------
    
    def print_result(self, result: UnifiedResult, detailed: bool = True):
        """Print formatted analysis result."""
        print(f"\n{'='*70}")
        print(f"  {result.processor}")
        print(f"  {result.description}")
        print(f"{'='*70}")
        
        print(f"\n  Year: {result.year}  |  {result.bits}-bit  |  "
              f"{result.clock_mhz} MHz  |  {result.family}")
        
        if result.queueing and detailed:
            q = result.queueing
            print(f"\n  ┌─ QUEUEING MODEL {'─'*48}┐")
            print(f"  │  IPC: {q.ipc:.4f}  |  MIPS: {q.mips:.3f}  |  "
                  f"Bottleneck: {q.bottleneck:<18} │")
            print(f"  └{'─'*66}┘")
        
        if result.cpi_stack and detailed:
            c = result.cpi_stack
            print(f"\n  ┌─ CPI STACK {'─'*53}┐")
            print(f"  │  IPC: {c.ipc:.4f}  |  MIPS: {c.mips:.3f}  |  "
                  f"CPI: {c.cpi_total:.2f}  |  Penalty: {c.bottleneck:<8} │")
            
            if c.breakdown:
                print(f"  │{' '*66}│")
                print(f"  │  {'Component':<14} {'CPI':>7} {'%':>6}  {'Bar':<32} │")
                print(f"  │  {'-'*62} │")
                
                max_pct = max(c.breakdown.values()) if c.breakdown else 1
                for comp in ['base', 'prefetch', 'branch', 'memory', 'cache', 'pipeline']:
                    pct = c.breakdown.get(comp, 0)
                    if pct > 0:
                        cpi_val = getattr(c, f'cpi_{comp}', 0)
                        bar = '█' * int(25 * pct / max_pct)
                        marker = "←" if comp == c.bottleneck and comp != 'base' else " "
                        print(f"  │  {comp:<14} {cpi_val:>7.2f} {pct:>5.1f}%  {bar:<25}{marker}    │")
            
            print(f"  └{'─'*66}┘")
        
        print(f"\n  SUMMARY: IPC={result.best_ipc:.4f}, MIPS={result.best_mips:.3f}")
    
    def print_comparison(self, results: Dict[str, UnifiedResult], 
                         sort_by: str = "mips"):
        """Print comparison table."""
        print(f"\n{'='*90}")
        print("PROCESSOR COMPARISON")
        print(f"{'='*90}")
        
        print(f"\n{'Processor':<28} {'Year':>5} {'Bits':>5} {'MHz':>6} "
              f"{'IPC':>7} {'MIPS':>8} {'Bottleneck':<12}")
        print("-" * 90)
        
        # Sort results
        sorted_items = sorted(
            results.items(),
            key=lambda x: getattr(x[1], f'best_{sort_by}', 0) if sort_by in ['ipc', 'mips'] 
                         else x[1].year,
            reverse=(sort_by in ['ipc', 'mips'])
        )
        
        for proc, result in sorted_items:
            bottleneck = ""
            if result.cpi_stack:
                bottleneck = result.cpi_stack.bottleneck
            elif result.queueing:
                bottleneck = result.queueing.bottleneck
            
            print(f"{proc:<28} {result.year:>5} {result.bits:>5} "
                  f"{result.clock_mhz:>6.1f} {result.best_ipc:>7.4f} "
                  f"{result.best_mips:>8.3f} {bottleneck:<12}")
        
        print("-" * 90)
    
    def export_json(self, results: Dict[str, UnifiedResult], 
                    filename: str):
        """Export results to JSON file."""
        data = {name: result.to_dict() for name, result in results.items()}
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Exported to {filename}")
    
    def export_csv(self, results: Dict[str, UnifiedResult], 
                   filename: str):
        """Export results to CSV file."""
        import csv
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Processor', 'Year', 'Bits', 'Clock_MHz', 'Family', 'Category',
                'IPC', 'MIPS', 'CPI', 'Bottleneck'
            ])
            
            for proc, result in results.items():
                cpi = result.cpi_stack.cpi_total if result.cpi_stack else 0
                bottleneck = result.cpi_stack.bottleneck if result.cpi_stack else ""
                
                writer.writerow([
                    proc, result.year, result.bits, result.clock_mhz,
                    result.family, result.category,
                    f"{result.best_ipc:.4f}", f"{result.best_mips:.3f}",
                    f"{cpi:.2f}", bottleneck
                ])
        
        print(f"Exported to {filename}")


# =============================================================================
# INTERACTIVE CLI
# =============================================================================

def interactive_mode(interface: ModelingInterface):
    """Run interactive command-line interface."""
    print("\n" + "="*70)
    print("  PRE-1986 MICROPROCESSOR MODELING INTERFACE")
    print("  Interactive Mode")
    print("="*70)
    
    print(f"\n  {len(interface.processors)} processors available")
    print("\n  Commands:")
    print("    list [family|category]  - List processors")
    print("    info <processor>        - Show processor info")
    print("    analyze <processor>     - Analyze processor")
    print("    compare <p1,p2,...>     - Compare processors")
    print("    workloads               - List workloads")
    print("    help                    - Show help")
    print("    quit                    - Exit")
    
    while True:
        try:
            cmd = input("\n> ").strip()
            
            if not cmd:
                continue
            
            parts = cmd.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            if command == "quit" or command == "exit":
                print("Goodbye!")
                break
            
            elif command == "list":
                if args == "family" or args == "families":
                    print("\nFamilies:", ", ".join(interface.list_families()))
                elif args == "category" or args == "categories":
                    print("\nCategories:", ", ".join(interface.list_categories()))
                else:
                    procs = interface.list_processors()
                    print(f"\nProcessors ({len(procs)}):")
                    for i, p in enumerate(procs):
                        print(f"  {p}")
                        if i > 20:
                            print(f"  ... and {len(procs) - 21} more")
                            break
            
            elif command == "info":
                if args:
                    try:
                        info = interface.get_processor_info(args)
                        print(f"\n{args}:")
                        for k, v in info.items():
                            print(f"  {k}: {v}")
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print("Usage: info <processor>")
            
            elif command == "analyze":
                if args:
                    try:
                        result = interface.analyze(args)
                        interface.print_result(result)
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print("Usage: analyze <processor>")
            
            elif command == "compare":
                if args:
                    procs = [p.strip() for p in args.split(",")]
                    results = interface.compare(procs)
                    interface.print_comparison(results)
                else:
                    print("Usage: compare <processor1,processor2,...>")
            
            elif command == "workloads":
                print("\nWorkloads:")
                for name, wl in interface.workloads.items():
                    print(f"  {name}: {wl.description}")
            
            elif command == "help":
                print("\nCommands:")
                print("  list              - List all processors")
                print("  list families     - List processor families")
                print("  list categories   - List architectural categories")
                print("  info <processor>  - Show processor details")
                print("  analyze <processor> - Run full analysis")
                print("  compare <p1,p2>   - Compare processors")
                print("  workloads         - List workload types")
                print("  quit              - Exit")
            
            else:
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Pre-1986 Microprocessor Unified Modeling Interface"
    )
    
    parser.add_argument(
        "--processor", "-p",
        help="Processor to analyze"
    )
    parser.add_argument(
        "--compare", "-c",
        help="Comma-separated list of processors to compare"
    )
    parser.add_argument(
        "--workload", "-w",
        default="typical",
        help="Workload type (typical, compute, memory, control, string)"
    )
    parser.add_argument(
        "--model", "-m",
        choices=["queueing", "cpi_stack", "both"],
        default="both",
        help="Model type to run"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all processors"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--export",
        help="Export results to file (JSON or CSV)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Analyze all processors"
    )
    
    args = parser.parse_args()
    
    interface = ModelingInterface()
    
    # Convert model type
    model_type = {
        "queueing": ModelType.QUEUEING,
        "cpi_stack": ModelType.CPI_STACK,
        "both": ModelType.BOTH
    }.get(args.model, ModelType.BOTH)
    
    if args.interactive:
        interactive_mode(interface)
    
    elif args.list:
        procs = interface.list_processors()
        print(f"\nAvailable processors ({len(procs)}):")
        for p in procs:
            info = interface.processors[p]
            print(f"  {p:<30} {info['year']}  {info['bits']:>2}-bit  {info['family'].value}")
    
    elif args.processor:
        result = interface.analyze(args.processor, args.workload, model_type)
        interface.print_result(result)
        
        if args.export:
            results = {args.processor: result}
            if args.export.endswith('.json'):
                interface.export_json(results, args.export)
            else:
                interface.export_csv(results, args.export)
    
    elif args.compare:
        procs = [p.strip() for p in args.compare.split(",")]
        results = interface.compare(procs, args.workload, model_type)
        interface.print_comparison(results)
        
        if args.export:
            if args.export.endswith('.json'):
                interface.export_json(results, args.export)
            else:
                interface.export_csv(results, args.export)
    
    elif args.all:
        results = interface.compare_all(args.workload, model_type)
        interface.print_comparison(results)
        
        if args.export:
            if args.export.endswith('.json'):
                interface.export_json(results, args.export)
            else:
                interface.export_csv(results, args.export)
    
    else:
        # Default: show summary and enter interactive mode
        print("\n" + "="*70)
        print("  PRE-1986 MICROPROCESSOR UNIFIED MODELING INTERFACE")
        print("="*70)
        print(f"\n  Processors: {len(interface.processors)}")
        print(f"  Families: {len(interface.list_families())}")
        print(f"  Categories: {len(interface.list_categories())}")
        print(f"  Workloads: {len(interface.workloads)}")
        
        print("\n  Usage:")
        print("    python pre1986_unified.py --processor 'Intel 8086'")
        print("    python pre1986_unified.py --compare 'Intel 8080,Zilog Z80,MOS 6502'")
        print("    python pre1986_unified.py --all --export results.csv")
        print("    python pre1986_unified.py --interactive")
        
        print("\n  Quick comparison of key processors:")
        key_procs = ["Intel 8080", "Intel 8086", "Motorola 68000", "Zilog Z80", 
                     "MOS 6502", "ARM1", "MIPS R2000"]
        results = interface.compare(key_procs)
        interface.print_comparison(results)


if __name__ == "__main__":
    main()
