#!/usr/bin/env python3
"""
Universal CPI Stack Framework for Pre-1986 Microprocessors

This module provides CPI Stack analysis for ALL processors in the collection,
complementing the existing queueing theory models.

SUPPORTED PROCESSORS (65 total):
- Intel: 4004, 4040, 8008, 8035, 8039, 8048, 8051, 8080, 8085, 8085a,
         8086, 8088, 8096, 80186, 80188, 80286, 80386, iAPX 432
- Motorola: 6800, 6801, 6802, 6803, 6805, 6809, 68000, 68008, 68010, 68020
- MOS/WDC: 6502, 65c02, 65802, 65816
- Zilog: Z80, Z180, Z280, Z8, Z8000, Z80 Peripherals
- RCA: 1802, CDP1804, CDP1805, CDP1806
- TI: TMS1000, TMS7000, TMS9900, TMS9995
- National: NSC800, NS32016, NS32032
- NEC: V20, V30
- Others: AMD 2901, ARM1, Fairchild F8, Ferranti F100-L, 
         GI CP1600, GI PIC1650, Hitachi 6309, Intersil 6100,
         MIPS R2000, Rockwell R6511, Signetics 2650

Author: Grey-Box Performance Modeling Research
Date: January 25, 2026
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum


# =============================================================================
# PROCESSOR CATEGORIES
# =============================================================================

class ProcessorCategory(Enum):
    """Processor architectural categories affecting CPI breakdown."""
    SIMPLE_4BIT = "4bit"           # 4004, 4040, TMS1000
    SIMPLE_8BIT = "simple_8bit"    # 8008, 8080, 6800, 6502
    ENHANCED_8BIT = "enhanced_8bit"  # Z80, 6809, 6309
    MCU_8BIT = "mcu_8bit"          # 8048, 8051, PIC, etc.
    PREFETCH_16BIT = "prefetch_16"  # 8086, 8088, 80186, 80188
    PROTECTED_16BIT = "protected_16"  # 80286
    EARLY_32BIT = "early_32bit"    # 68000, 68010, Z8000
    FULL_32BIT = "full_32bit"      # 80386, 68020, NS32032
    RISC = "risc"                  # ARM1, MIPS R2000
    SPECIAL = "special"            # 1802, iAPX 432, AMD 2901


# =============================================================================
# PROCESSOR SPECIFICATIONS DATABASE
# =============================================================================

PROCESSOR_SPECS = {
    # Intel 4-bit
    "Intel 4004": {
        "category": ProcessorCategory.SIMPLE_4BIT,
        "year": 1971, "bits": 4, "clock_mhz": 0.74,
        "base_cpi": 10.8, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 8, "mov": 8, "branch": 12, "io": 8}
    },
    "Intel 4040": {
        "category": ProcessorCategory.SIMPLE_4BIT,
        "year": 1974, "bits": 4, "clock_mhz": 0.74,
        "base_cpi": 10.5, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 8, "mov": 8, "branch": 12, "io": 8}
    },
    
    # Intel 8-bit CPUs
    "Intel 8008": {
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1972, "bits": 8, "clock_mhz": 0.5,
        "base_cpi": 20.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 8, "mov": 7, "branch": 11, "memory": 16}
    },
    "Intel 8080": {
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1974, "bits": 8, "clock_mhz": 2.0,
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 5, "branch": 10, "memory": 7}
    },
    "Intel 8085": {
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1976, "bits": 8, "clock_mhz": 3.0,
        "base_cpi": 9.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 7}
    },
    "Intel 8085a": {
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1976, "bits": 8, "clock_mhz": 5.0,
        "base_cpi": 9.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 7}
    },
    
    # Intel 8-bit MCUs
    "Intel 8035": {
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1976, "bits": 8, "clock_mhz": 6.0,
        "base_cpi": 15.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 1, "mov": 1, "branch": 2, "memory": 2}
    },
    "Intel 8039": {
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1976, "bits": 8, "clock_mhz": 6.0,
        "base_cpi": 15.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 1, "mov": 1, "branch": 2, "memory": 2}
    },
    "Intel 8048": {
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1976, "bits": 8, "clock_mhz": 6.0,
        "base_cpi": 15.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 1, "mov": 1, "branch": 2, "memory": 2}
    },
    "Intel 8051": {
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1980, "bits": 8, "clock_mhz": 12.0,
        "base_cpi": 12.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 1, "mov": 1, "branch": 2, "memory": 2}
    },
    "Intel 8096": {
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1982, "bits": 16, "clock_mhz": 12.0,
        "base_cpi": 8.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 2,
        "timings": {"alu": 4, "mov": 4, "branch": 8, "memory": 6}
    },
    
    # Intel 16-bit
    "Intel 8086": {
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1978, "bits": 16, "clock_mhz": 5.0,
        "base_cpi": 9.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 6,
        "timings": {"alu": 3, "mov": 2, "branch": 15, "memory": 9, "mul": 118}
    },
    "Intel 8088": {
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1979, "bits": 16, "clock_mhz": 5.0,
        "base_cpi": 12.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 4,
        "bus_width": 8,
        "timings": {"alu": 3, "mov": 2, "branch": 15, "memory": 13, "mul": 118}
    },
    "Intel 80186": {
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1982, "bits": 16, "clock_mhz": 8.0,
        "base_cpi": 8.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 6,
        "timings": {"alu": 3, "mov": 2, "branch": 14, "memory": 8, "mul": 36}
    },
    "Intel 80188": {
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1982, "bits": 16, "clock_mhz": 8.0,
        "base_cpi": 10.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 4,
        "bus_width": 8,
        "timings": {"alu": 3, "mov": 2, "branch": 14, "memory": 12, "mul": 36}
    },
    "Intel 80286": {
        "category": ProcessorCategory.PROTECTED_16BIT,
        "year": 1982, "bits": 16, "clock_mhz": 6.0,
        "base_cpi": 6.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 3, "branch_penalty": 3, "prefetch_bytes": 6,
        "timings": {"alu": 2, "mov": 2, "branch": 7, "memory": 5, "mul": 21}
    },
    "Intel 80386": {
        "category": ProcessorCategory.FULL_32BIT,
        "year": 1985, "bits": 32, "clock_mhz": 16.0,
        "base_cpi": 5.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 4, "branch_penalty": 4, "prefetch_bytes": 16,
        "timings": {"alu": 2, "mov": 2, "branch": 7, "memory": 4, "mul": 12}
    },
    "Intel iapx 432": {
        "category": ProcessorCategory.SPECIAL,
        "year": 1981, "bits": 32, "clock_mhz": 5.0,
        "base_cpi": 20.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 8,
        "timings": {"alu": 6, "mov": 8, "branch": 20, "memory": 15}
    },
    
    # Motorola 6800 family
    "Motorola 6800": {
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1974, "bits": 8, "clock_mhz": 1.0,
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 4, "memory": 5}
    },
    "Motorola 6801": {
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1978, "bits": 8, "clock_mhz": 1.0,
        "base_cpi": 9.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 4, "memory": 4}
    },
    "Motorola 6802": {
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1977, "bits": 8, "clock_mhz": 1.0,
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 4, "memory": 5}
    },
    "Motorola 6803": {
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1983, "bits": 8, "clock_mhz": 1.0,
        "base_cpi": 9.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 4, "memory": 4}
    },
    "Motorola 6805": {
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1979, "bits": 8, "clock_mhz": 4.0,
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 3, "mov": 4, "branch": 5, "memory": 5}
    },
    "Motorola 6809": {
        "category": ProcessorCategory.ENHANCED_8BIT,
        "year": 1979, "bits": 8, "clock_mhz": 1.0,
        "base_cpi": 7.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 3, "memory": 4}
    },
    
    # Motorola 68000 family
    "Motorola 68000": {
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1979, "bits": 32, "clock_mhz": 8.0,
        "base_cpi": 7.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 4,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 8, "mul": 70}
    },
    "Motorola 68008": {
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1982, "bits": 32, "clock_mhz": 8.0,
        "base_cpi": 10.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 2,
        "bus_width": 8,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 12, "mul": 70}
    },
    "Motorola 68010": {
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1982, "bits": 32, "clock_mhz": 10.0,
        "base_cpi": 6.5, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 4,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 7, "mul": 70}
    },
    "Motorola 68020": {
        "category": ProcessorCategory.FULL_32BIT,
        "year": 1984, "bits": 32, "clock_mhz": 16.0,
        "base_cpi": 4.5, "has_prefetch": True, "has_cache": True,
        "pipeline_stages": 3, "branch_penalty": 3, "prefetch_bytes": 256,
        "cache_size": 256, "cache_hit_rate": 0.90,
        "timings": {"alu": 2, "mov": 2, "branch": 6, "memory": 3, "mul": 28}
    },
    
    # MOS/WDC 6502 family
    "MOS 6502": {
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1975, "bits": 8, "clock_mhz": 1.0,
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 3, "memory": 4}
    },
    "WDC 65c02": {
        "category": ProcessorCategory.ENHANCED_8BIT,
        "year": 1983, "bits": 8, "clock_mhz": 4.0,
        "base_cpi": 9.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 3, "memory": 4}
    },
    "WDC 65802": {
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1984, "bits": 16, "clock_mhz": 4.0,
        "base_cpi": 8.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 1,
        "timings": {"alu": 2, "mov": 3, "branch": 3, "memory": 4}
    },
    "WDC 65816": {
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1984, "bits": 16, "clock_mhz": 2.8,
        "base_cpi": 8.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 1,
        "timings": {"alu": 2, "mov": 3, "branch": 3, "memory": 5}
    },
    
    # Zilog
    "Zilog Z80": {
        "category": ProcessorCategory.ENHANCED_8BIT,
        "year": 1976, "bits": 8, "clock_mhz": 2.5,
        "base_cpi": 8.5, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 7}
    },
    "Zilog Z180": {
        "category": ProcessorCategory.ENHANCED_8BIT,
        "year": 1985, "bits": 8, "clock_mhz": 6.0,
        "base_cpi": 6.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 3, "mov": 3, "branch": 8, "memory": 5}
    },
    "Zilog Z280": {
        "category": ProcessorCategory.PROTECTED_16BIT,
        "year": 1985, "bits": 16, "clock_mhz": 12.0,
        "base_cpi": 5.0, "has_prefetch": True, "has_cache": True,
        "pipeline_stages": 2, "branch_penalty": 3,
        "timings": {"alu": 2, "mov": 2, "branch": 6, "memory": 4}
    },
    "Zilog Z8": {
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1979, "bits": 8, "clock_mhz": 8.0,
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 6, "mov": 6, "branch": 12, "memory": 8}
    },
    "Zilog Z8000": {
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1979, "bits": 16, "clock_mhz": 4.0,
        "base_cpi": 9.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 2,
        "timings": {"alu": 4, "mov": 3, "branch": 7, "memory": 7}
    },
    "Zilog Z80 Peripherals": {
        "category": ProcessorCategory.SPECIAL,
        "year": 1976, "bits": 8, "clock_mhz": 2.5,
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 7}
    },
    
    # RCA COSMAC
    "RCA 1802": {
        "category": ProcessorCategory.SPECIAL,
        "year": 1976, "bits": 8, "clock_mhz": 2.0,
        "base_cpi": 20.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 16, "mov": 16, "branch": 16, "memory": 16}
    },
    "RCA CDP1804": {
        "category": ProcessorCategory.SPECIAL,
        "year": 1980, "bits": 8, "clock_mhz": 2.0,
        "base_cpi": 18.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 14, "mov": 14, "branch": 14, "memory": 14}
    },
    "RCA CDP1805": {
        "category": ProcessorCategory.SPECIAL,
        "year": 1984, "bits": 8, "clock_mhz": 4.0,
        "base_cpi": 16.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 12, "mov": 12, "branch": 12, "memory": 12}
    },
    "RCA CDP1806": {
        "category": ProcessorCategory.SPECIAL,
        "year": 1985, "bits": 8, "clock_mhz": 4.0,
        "base_cpi": 14.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 10, "mov": 10, "branch": 10, "memory": 10}
    },
    
    # Texas Instruments
    "TI tms1000": {
        "category": ProcessorCategory.SIMPLE_4BIT,
        "year": 1974, "bits": 4, "clock_mhz": 0.4,
        "base_cpi": 25.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 1, "mov": 1, "branch": 2, "memory": 2}
    },
    "TI tms7000": {
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1981, "bits": 8, "clock_mhz": 10.0,
        "base_cpi": 11.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 5, "mov": 5, "branch": 7, "memory": 7}
    },
    "TI TMS9900": {
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1976, "bits": 16, "clock_mhz": 3.0,
        "base_cpi": 12.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 8, "mov": 8, "branch": 12, "memory": 10}
    },
    "TI TMS9995": {
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1981, "bits": 16, "clock_mhz": 12.0,
        "base_cpi": 8.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 8, "memory": 6}
    },
    
    # National Semiconductor
    "NSC NSC800": {
        "category": ProcessorCategory.ENHANCED_8BIT,
        "year": 1979, "bits": 8, "clock_mhz": 4.0,
        "base_cpi": 8.5, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 10, "memory": 7}
    },
    "National Semiconductor NS32016": {
        "category": ProcessorCategory.FULL_32BIT,
        "year": 1982, "bits": 32, "clock_mhz": 10.0,
        "base_cpi": 10.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4,
        "timings": {"alu": 4, "mov": 3, "branch": 8, "memory": 6}
    },
    "National Semiconductor NA32032": {
        "category": ProcessorCategory.FULL_32BIT,
        "year": 1984, "bits": 32, "clock_mhz": 10.0,
        "base_cpi": 8.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4,
        "timings": {"alu": 3, "mov": 3, "branch": 7, "memory": 5}
    },
    
    # NEC
    "NEC V20": {
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1984, "bits": 16, "clock_mhz": 8.0,
        "base_cpi": 8.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 6,
        "timings": {"alu": 2, "mov": 2, "branch": 12, "memory": 8, "mul": 100}
    },
    "NEC V30": {
        "category": ProcessorCategory.PREFETCH_16BIT,
        "year": 1984, "bits": 16, "clock_mhz": 10.0,
        "base_cpi": 7.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 2, "branch_penalty": 4, "prefetch_bytes": 6,
        "timings": {"alu": 2, "mov": 2, "branch": 12, "memory": 7, "mul": 100}
    },
    
    # Others
    "AMD 2901": {
        "category": ProcessorCategory.SPECIAL,
        "year": 1975, "bits": 4, "clock_mhz": 10.0,
        "base_cpi": 1.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 1, "mov": 1, "branch": 1, "memory": 1}
    },
    "ARM1": {
        "category": ProcessorCategory.RISC,
        "year": 1985, "bits": 32, "clock_mhz": 6.0,
        "base_cpi": 2.0, "has_prefetch": True, "has_cache": False,
        "pipeline_stages": 3, "branch_penalty": 2,
        "timings": {"alu": 1, "mov": 1, "branch": 3, "memory": 2}
    },
    "Fairchild F8": {
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1975, "bits": 8, "clock_mhz": 2.0,
        "base_cpi": 12.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 6, "memory": 6}
    },
    "Ferranti f1001": {
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1976, "bits": 16, "clock_mhz": 8.0,
        "base_cpi": 6.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 2,
        "timings": {"alu": 2, "mov": 2, "branch": 4, "memory": 4}
    },
    "General Instrument Pic1600": {
        "category": ProcessorCategory.EARLY_32BIT,
        "year": 1975, "bits": 16, "clock_mhz": 1.0,
        "base_cpi": 12.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 6, "mov": 6, "branch": 10, "memory": 8}
    },
    "General Instrument Pic1650": {
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1977, "bits": 8, "clock_mhz": 4.0,
        "base_cpi": 4.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 1, "mov": 1, "branch": 2, "memory": 1}
    },
    "Hitachi 6309": {
        "category": ProcessorCategory.ENHANCED_8BIT,
        "year": 1982, "bits": 8, "clock_mhz": 2.0,
        "base_cpi": 5.5, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 2, "branch": 3, "memory": 4}
    },
    "Intersil 6100": {
        "category": ProcessorCategory.SPECIAL,
        "year": 1975, "bits": 12, "clock_mhz": 4.0,
        "base_cpi": 8.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 3, "mov": 3, "branch": 4, "memory": 5}
    },
    "MIPS R2000": {
        "category": ProcessorCategory.RISC,
        "year": 1985, "bits": 32, "clock_mhz": 8.0,
        "base_cpi": 1.7, "has_prefetch": True, "has_cache": True,
        "pipeline_stages": 5, "branch_penalty": 1,
        "cache_hit_rate": 0.95,
        "timings": {"alu": 1, "mov": 1, "branch": 1, "memory": 1}
    },
    "Rockwell r6511": {
        "category": ProcessorCategory.MCU_8BIT,
        "year": 1980, "bits": 8, "clock_mhz": 2.0,
        "base_cpi": 10.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 2, "mov": 3, "branch": 3, "memory": 4}
    },
    "Signetics 2650": {
        "category": ProcessorCategory.SIMPLE_8BIT,
        "year": 1975, "bits": 8, "clock_mhz": 1.25,
        "base_cpi": 11.0, "has_prefetch": False, "has_cache": False,
        "pipeline_stages": 1, "branch_penalty": 0,
        "timings": {"alu": 4, "mov": 4, "branch": 6, "memory": 6}
    },
}


# =============================================================================
# WORKLOAD DEFINITION
# =============================================================================

@dataclass
class Workload:
    """Universal workload for CPI Stack analysis."""
    name: str = "default"
    mix_alu: float = 0.35
    mix_mov: float = 0.25
    mix_branch: float = 0.15
    mix_memory: float = 0.20
    mix_other: float = 0.05
    
    branch_taken_rate: float = 0.60
    memory_operand_rate: float = 0.40
    cache_hit_rate: float = 0.90
    
    def validate(self):
        total = self.mix_alu + self.mix_mov + self.mix_branch + self.mix_memory + self.mix_other
        assert abs(total - 1.0) < 0.01, f"Mix sums to {total}, not 1.0"


STANDARD_WORKLOADS = {
    "typical": Workload(name="typical"),
    "compute": Workload(name="compute", mix_alu=0.50, mix_mov=0.20, mix_branch=0.10, mix_memory=0.15, mix_other=0.05),
    "memory": Workload(name="memory", mix_alu=0.20, mix_mov=0.15, mix_branch=0.10, mix_memory=0.50, mix_other=0.05),
    "control": Workload(name="control", mix_alu=0.25, mix_mov=0.20, mix_branch=0.35, mix_memory=0.15, mix_other=0.05),
}


# =============================================================================
# CPI STACK RESULT
# =============================================================================

@dataclass
class CPIStackResult:
    """CPI breakdown result."""
    processor: str = ""
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


# =============================================================================
# UNIVERSAL CPI STACK MODEL
# =============================================================================

class UniversalCPIStackModel:
    """
    Universal CPI Stack Model for all pre-1986 processors.
    
    Adapts CPI breakdown based on processor category and features.
    """
    
    def __init__(self):
        self.specs = PROCESSOR_SPECS
    
    def get_processor_list(self) -> List[str]:
        """Get list of all supported processors."""
        return list(self.specs.keys())
    
    def get_processor_info(self, processor: str) -> Dict:
        """Get specs for a processor."""
        return self.specs.get(processor, {})
    
    def predict(self, processor: str, workload: Workload = None) -> CPIStackResult:
        """
        Predict CPI breakdown for a processor.
        
        Args:
            processor: Processor name (e.g., "Intel 8086")
            workload: Workload characteristics (defaults to typical)
        
        Returns:
            CPIStackResult with full breakdown
        """
        if processor not in self.specs:
            raise ValueError(f"Unknown processor: {processor}")
        
        spec = self.specs[processor]
        workload = workload or STANDARD_WORKLOADS["typical"]
        workload.validate()
        
        result = CPIStackResult(processor=processor)
        
        # Base CPI from instruction mix
        result.cpi_base = self._calc_base_cpi(spec, workload)
        
        # Prefetch penalty (if applicable)
        if spec.get("has_prefetch", False):
            result.cpi_prefetch = self._calc_prefetch_penalty(spec, workload)
        
        # Branch penalty (for pipelined processors)
        if spec.get("pipeline_stages", 1) > 1:
            result.cpi_branch = self._calc_branch_penalty(spec, workload)
        
        # Memory penalty
        result.cpi_memory = self._calc_memory_penalty(spec, workload)
        
        # Cache miss penalty (if applicable)
        if spec.get("has_cache", False):
            result.cpi_cache = self._calc_cache_penalty(spec, workload)
        
        # Pipeline hazard penalty (for deep pipelines)
        if spec.get("pipeline_stages", 1) >= 3:
            result.cpi_pipeline = self._calc_pipeline_penalty(spec, workload)
        
        result.compute_totals(spec["clock_mhz"])
        return result
    
    def _calc_base_cpi(self, spec: Dict, workload: Workload) -> float:
        """Calculate base CPI from instruction mix."""
        timings = spec.get("timings", {})
        
        cpi = (workload.mix_alu * timings.get("alu", 4) +
               workload.mix_mov * timings.get("mov", 4) +
               workload.mix_branch * timings.get("branch", 8) +
               workload.mix_memory * timings.get("memory", 8) +
               workload.mix_other * 5)
        
        return cpi
    
    def _calc_prefetch_penalty(self, spec: Dict, workload: Workload) -> float:
        """Calculate prefetch stall penalty."""
        prefetch_bytes = spec.get("prefetch_bytes", 4)
        bus_width = spec.get("bus_width", spec["bits"] // 8)
        
        # Simplified: smaller queue = more stalls
        stall_factor = max(0, (6 - prefetch_bytes) * 0.05)
        
        # Narrower bus = more stalls
        if bus_width < spec["bits"] // 8:
            stall_factor *= 1.5
        
        return spec.get("base_cpi", 10) * stall_factor
    
    def _calc_branch_penalty(self, spec: Dict, workload: Workload) -> float:
        """Calculate branch misprediction/flush penalty."""
        branch_penalty = spec.get("branch_penalty", 0)
        
        # Only taken branches cause penalty in simple predictors
        taken_branches = workload.mix_branch * workload.branch_taken_rate
        
        return taken_branches * branch_penalty
    
    def _calc_memory_penalty(self, spec: Dict, workload: Workload) -> float:
        """Calculate memory operand penalty."""
        memory_cycles = spec.get("timings", {}).get("memory", 8)
        base_cycles = spec.get("timings", {}).get("alu", 4)
        
        # Extra cycles for memory operands beyond base
        extra = max(0, memory_cycles - base_cycles)
        
        return workload.memory_operand_rate * extra * 0.3
    
    def _calc_cache_penalty(self, spec: Dict, workload: Workload) -> float:
        """Calculate cache miss penalty."""
        hit_rate = spec.get("cache_hit_rate", 0.90)
        miss_penalty = 10  # Simplified: ~10 cycles per miss
        
        miss_rate = 1 - hit_rate
        memory_accesses = workload.mix_memory + workload.memory_operand_rate * 0.3
        
        return memory_accesses * miss_rate * miss_penalty
    
    def _calc_pipeline_penalty(self, spec: Dict, workload: Workload) -> float:
        """Calculate pipeline hazard penalty."""
        stages = spec.get("pipeline_stages", 1)
        
        # More stages = more hazards
        hazard_factor = (stages - 2) * 0.02
        
        return spec.get("base_cpi", 10) * hazard_factor
    
    def compare_processors(self, processors: List[str], 
                          workload: Workload = None) -> Dict[str, CPIStackResult]:
        """Compare CPI breakdown across processors."""
        return {p: self.predict(p, workload) for p in processors if p in self.specs}
    
    def print_result(self, result: CPIStackResult):
        """Print formatted CPI breakdown."""
        print(f"\n{'='*60}")
        print(f"CPI STACK: {result.processor}")
        print(f"{'='*60}")
        
        components = [
            ('Base (ideal)', 'base', result.cpi_base),
            ('Prefetch', 'prefetch', result.cpi_prefetch),
            ('Branch', 'branch', result.cpi_branch),
            ('Memory', 'memory', result.cpi_memory),
            ('Cache miss', 'cache', result.cpi_cache),
            ('Pipeline', 'pipeline', result.cpi_pipeline),
        ]
        
        print(f"\n{'Component':<16} {'CPI':>7} {'%':>6}  Bar")
        print("-" * 55)
        
        max_pct = max(result.breakdown.values()) if result.breakdown else 1
        for label, key, cpi in components:
            if cpi > 0:
                pct = result.breakdown.get(key, 0)
                bar = '█' * int(30 * pct / max_pct) if max_pct > 0 else ''
                marker = " ←" if key == result.bottleneck and key != 'base' else ""
                print(f"{label:<16} {cpi:>7.2f} {pct:>5.1f}%  {bar}{marker}")
        
        print("-" * 55)
        print(f"{'TOTAL':<16} {result.cpi_total:>7.2f} {'100.0':>5}%")
        print(f"\nIPC: {result.ipc:.4f}  |  MIPS: {result.mips:.3f}")
        if result.bottleneck != "none":
            print(f"Primary penalty: {result.bottleneck}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("="*70)
    print("UNIVERSAL CPI STACK FRAMEWORK - PRE-1986 PROCESSORS")
    print("="*70)
    
    model = UniversalCPIStackModel()
    
    print(f"\nSupported processors: {len(model.get_processor_list())}")
    
    # Show a few examples
    examples = ["Intel 8080", "Intel 8086", "Motorola 68000", "Zilog Z80", 
                "MOS 6502", "ARM1", "Intel 80386"]
    
    for proc in examples:
        result = model.predict(proc)
        model.print_result(result)
    
    # Comparison table
    print("\n\n" + "="*70)
    print("PROCESSOR COMPARISON")
    print("="*70)
    print(f"\n{'Processor':<28} {'CPI':>7} {'IPC':>7} {'MIPS':>8} {'Bottleneck':<12}")
    print("-" * 70)
    
    all_results = model.compare_processors(model.get_processor_list())
    for proc, result in sorted(all_results.items(), key=lambda x: -x[1].mips):
        print(f"{proc:<28} {result.cpi_total:>7.2f} {result.ipc:>7.4f} {result.mips:>8.3f} {result.bottleneck:<12}")


if __name__ == "__main__":
    main()
