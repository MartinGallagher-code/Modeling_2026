#!/usr/bin/env python3
"""
Populate Validation Data for Modeling_2026
============================================

Auto-populates validation JSON files with:
1. Timing tests from datasheet values
2. Validation dates
3. Source URLs
4. Runs models to calculate actual accuracy

Usage:
    python populate_validation_data.py [repo_path] [--dry-run] [--run-accuracy]

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import json
import argparse
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple


# =============================================================================
# TIMING DATABASE - Known cycle counts from datasheets
# =============================================================================

TIMING_DATABASE = {
    # Intel 4004 (1971) - Sequential
    'i4004': {
        'clock_mhz': 0.74,
        'typical_cpi': 10.8,
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'ADD', 'category': 'alu', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'SUB', 'category': 'alu', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'LD', 'category': 'memory', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'JMP', 'category': 'control', 'expected_cycles': 16, 'source': 'datasheet'},
            {'name': 'JCN', 'category': 'control', 'expected_cycles': 16, 'source': 'datasheet'},
        ],
    },
    
    # Intel 8008 (1972) - Sequential
    'i8008': {
        'clock_mhz': 0.5,
        'typical_cpi': 11.0,
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'MOV_r_r', 'category': 'data_transfer', 'expected_cycles': 5, 'source': 'datasheet'},
            {'name': 'MOV_r_M', 'category': 'memory', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'ADD_r', 'category': 'alu', 'expected_cycles': 5, 'source': 'datasheet'},
            {'name': 'ADD_M', 'category': 'alu', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'JMP', 'category': 'control', 'expected_cycles': 11, 'source': 'datasheet'},
            {'name': 'CALL', 'category': 'control', 'expected_cycles': 11, 'source': 'datasheet'},
            {'name': 'RET', 'category': 'control', 'expected_cycles': 5, 'source': 'datasheet'},
        ],
    },
    
    # Intel 8080 (1974) - Sequential
    'i8080': {
        'clock_mhz': 2.0,
        'typical_cpi': 9.2,
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'MOV_r_r', 'category': 'data_transfer', 'expected_cycles': 5, 'source': 'datasheet'},
            {'name': 'MOV_r_M', 'category': 'memory', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'MOV_M_r', 'category': 'memory', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'ADD_r', 'category': 'alu', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADD_M', 'category': 'alu', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'JMP', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'JZ', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'CALL', 'category': 'control', 'expected_cycles': 17, 'source': 'datasheet'},
            {'name': 'RET', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'PUSH', 'category': 'stack', 'expected_cycles': 11, 'source': 'datasheet'},
            {'name': 'POP', 'category': 'stack', 'expected_cycles': 10, 'source': 'datasheet'},
        ],
    },
    
    # Intel 8085 (1976) - Sequential
    'i8085': {
        'clock_mhz': 3.0,
        'typical_cpi': 5.5,
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'MOV_r_r', 'category': 'data_transfer', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'MOV_r_M', 'category': 'memory', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'ADD_r', 'category': 'alu', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADD_M', 'category': 'alu', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'JMP', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'CALL', 'category': 'control', 'expected_cycles': 18, 'source': 'datasheet'},
            {'name': 'RET', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
        ],
    },
    
    # Intel 8086 (1978) - Prefetch Queue
    'i8086': {
        'clock_mhz': 5.0,
        'typical_cpi': 4.5,
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'MOV_r_r', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MOV_r_m', 'category': 'memory', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'MOV_m_r', 'category': 'memory', 'expected_cycles': 9, 'source': 'datasheet'},
            {'name': 'ADD_r_r', 'category': 'alu', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'ADD_r_m', 'category': 'alu', 'expected_cycles': 9, 'source': 'datasheet'},
            {'name': 'MUL_r8', 'category': 'mul_div', 'expected_cycles': 77, 'source': 'datasheet'},
            {'name': 'DIV_r8', 'category': 'mul_div', 'expected_cycles': 90, 'source': 'datasheet'},
            {'name': 'JMP_near', 'category': 'control', 'expected_cycles': 15, 'source': 'datasheet'},
            {'name': 'JZ_taken', 'category': 'control', 'expected_cycles': 16, 'source': 'datasheet'},
            {'name': 'JZ_not_taken', 'category': 'control', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'CALL_near', 'category': 'control', 'expected_cycles': 19, 'source': 'datasheet'},
            {'name': 'RET_near', 'category': 'control', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'PUSH', 'category': 'stack', 'expected_cycles': 11, 'source': 'datasheet'},
            {'name': 'POP', 'category': 'stack', 'expected_cycles': 8, 'source': 'datasheet'},
        ],
    },
    
    # Intel 8088 (1979) - Prefetch Queue (8-bit bus)
    'i8088': {
        'clock_mhz': 5.0,
        'typical_cpi': 5.2,
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'MOV_r_r', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MOV_r_m', 'category': 'memory', 'expected_cycles': 12, 'source': 'datasheet'},
            {'name': 'ADD_r_r', 'category': 'alu', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'JMP_near', 'category': 'control', 'expected_cycles': 15, 'source': 'datasheet'},
            {'name': 'CALL_near', 'category': 'control', 'expected_cycles': 23, 'source': 'datasheet'},
        ],
    },
    
    # Intel 80286 (1982) - Pipelined
    'i80286': {
        'clock_mhz': 6.0,
        'typical_cpi': 4.0,
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'MOV_r_r', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MOV_r_m', 'category': 'memory', 'expected_cycles': 5, 'source': 'datasheet'},
            {'name': 'ADD_r_r', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MUL_r16', 'category': 'mul_div', 'expected_cycles': 21, 'source': 'datasheet'},
            {'name': 'JMP_near', 'category': 'control', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'CALL_near', 'category': 'control', 'expected_cycles': 7, 'source': 'datasheet'},
        ],
    },
    
    # Intel 80386 (1985) - Cache/RISC era
    'i80386': {
        'clock_mhz': 16.0,
        'typical_cpi': 4.5,
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'MOV_r_r', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MOV_r_m', 'category': 'memory', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADD_r_r', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MUL_r32', 'category': 'mul_div', 'expected_cycles': 14, 'source': 'datasheet'},
            {'name': 'DIV_r32', 'category': 'mul_div', 'expected_cycles': 40, 'source': 'datasheet'},
            {'name': 'JMP_near', 'category': 'control', 'expected_cycles': 7, 'source': 'datasheet'},
        ],
    },
    
    # MOS 6502 (1975) - Sequential
    'mos6502': {
        'clock_mhz': 1.0,
        'typical_cpi': 3.5,
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'LDA_imm', 'category': 'memory', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'LDA_zp', 'category': 'memory', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'LDA_abs', 'category': 'memory', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'STA_zp', 'category': 'memory', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'STA_abs', 'category': 'memory', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADC_imm', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'ADC_zp', 'category': 'alu', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'INX', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'DEX', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'JMP_abs', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'JSR', 'category': 'control', 'expected_cycles': 6, 'source': 'datasheet'},
            {'name': 'RTS', 'category': 'control', 'expected_cycles': 6, 'source': 'datasheet'},
            {'name': 'BEQ_taken', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'BEQ_not_taken', 'category': 'control', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'PHA', 'category': 'stack', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'PLA', 'category': 'stack', 'expected_cycles': 4, 'source': 'datasheet'},
        ],
    },
    
    # Zilog Z80 (1976) - Prefetch Queue
    'z80': {
        'clock_mhz': 2.5,
        'typical_cpi': 5.5,
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'LD_r_r', 'category': 'data_transfer', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'LD_r_n', 'category': 'data_transfer', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'LD_r_HL', 'category': 'memory', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'LD_HL_r', 'category': 'memory', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'ADD_A_r', 'category': 'alu', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADD_A_HL', 'category': 'alu', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'INC_r', 'category': 'alu', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'JP_nn', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'JP_cc_nn', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'JR_e', 'category': 'control', 'expected_cycles': 12, 'source': 'datasheet'},
            {'name': 'CALL_nn', 'category': 'control', 'expected_cycles': 17, 'source': 'datasheet'},
            {'name': 'RET', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'PUSH_qq', 'category': 'stack', 'expected_cycles': 11, 'source': 'datasheet'},
            {'name': 'POP_qq', 'category': 'stack', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'LDIR', 'category': 'block', 'expected_cycles': 21, 'source': 'datasheet'},
        ],
    },
    
    # Motorola 6800 (1974) - Sequential
    'm6800': {
        'clock_mhz': 1.0,
        'typical_cpi': 4.0,
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'LDAA_imm', 'category': 'memory', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'LDAA_dir', 'category': 'memory', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'LDAA_ext', 'category': 'memory', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'STAA_dir', 'category': 'memory', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADDA_imm', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'INCA', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'JMP_ext', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'JSR_ext', 'category': 'control', 'expected_cycles': 9, 'source': 'datasheet'},
            {'name': 'RTS', 'category': 'control', 'expected_cycles': 5, 'source': 'datasheet'},
            {'name': 'BEQ', 'category': 'control', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'PSHA', 'category': 'stack', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'PULA', 'category': 'stack', 'expected_cycles': 4, 'source': 'datasheet'},
        ],
    },
    
    # Motorola 6809 (1978) - Prefetch Queue
    'm6809': {
        'clock_mhz': 1.0,
        'typical_cpi': 3.5,
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'LDA_imm', 'category': 'memory', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'LDA_dir', 'category': 'memory', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'STA_dir', 'category': 'memory', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADDA_imm', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MUL', 'category': 'mul_div', 'expected_cycles': 11, 'source': 'datasheet'},
            {'name': 'JMP_ext', 'category': 'control', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'JSR_ext', 'category': 'control', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'RTS', 'category': 'control', 'expected_cycles': 5, 'source': 'datasheet'},
            {'name': 'BEQ', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'PSHS', 'category': 'stack', 'expected_cycles': 5, 'source': 'datasheet'},
            {'name': 'PULS', 'category': 'stack', 'expected_cycles': 5, 'source': 'datasheet'},
        ],
    },
    
    # Motorola 68000 (1979) - Pipelined
    'm68000': {
        'clock_mhz': 8.0,
        'typical_cpi': 6.5,
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'MOVE_Dn_Dn', 'category': 'data_transfer', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'MOVE_An_Dn', 'category': 'data_transfer', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'MOVE_mem_Dn', 'category': 'memory', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'MOVE_Dn_mem', 'category': 'memory', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'ADD_Dn_Dn', 'category': 'alu', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADD_mem_Dn', 'category': 'alu', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'MULU', 'category': 'mul_div', 'expected_cycles': 70, 'source': 'datasheet'},
            {'name': 'DIVU', 'category': 'mul_div', 'expected_cycles': 140, 'source': 'datasheet'},
            {'name': 'JMP', 'category': 'control', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'JSR', 'category': 'control', 'expected_cycles': 16, 'source': 'datasheet'},
            {'name': 'RTS', 'category': 'control', 'expected_cycles': 16, 'source': 'datasheet'},
            {'name': 'Bcc_taken', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'Bcc_not_taken', 'category': 'control', 'expected_cycles': 8, 'source': 'datasheet'},
        ],
    },
    
    # ARM1 (1985) - Cache/RISC
    'arm1': {
        'clock_mhz': 6.0,
        'typical_cpi': 1.8,
        'timing_tests': [
            {'name': 'MOV_r_r', 'category': 'data_transfer', 'expected_cycles': 1, 'source': 'datasheet'},
            {'name': 'MOV_r_imm', 'category': 'data_transfer', 'expected_cycles': 1, 'source': 'datasheet'},
            {'name': 'LDR', 'category': 'memory', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'STR', 'category': 'memory', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'ADD_r_r', 'category': 'alu', 'expected_cycles': 1, 'source': 'datasheet'},
            {'name': 'MUL', 'category': 'mul_div', 'expected_cycles': 16, 'source': 'datasheet'},
            {'name': 'B', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'BL', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
        ],
    },
    
    # SPARC (1987) - Cache/RISC
    'sparc': {
        'clock_mhz': 14.0,
        'typical_cpi': 1.5,
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 1, 'source': 'datasheet'},
            {'name': 'MOV_r_r', 'category': 'data_transfer', 'expected_cycles': 1, 'source': 'datasheet'},
            {'name': 'LD', 'category': 'memory', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'ST', 'category': 'memory', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'ADD', 'category': 'alu', 'expected_cycles': 1, 'source': 'datasheet'},
            {'name': 'SMUL', 'category': 'mul_div', 'expected_cycles': 19, 'source': 'datasheet'},
            {'name': 'BA', 'category': 'control', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'CALL', 'category': 'control', 'expected_cycles': 2, 'source': 'datasheet'},
        ],
    },
}

# Aliases for processor names
PROCESSOR_ALIASES = {
    'i4040': 'i4004',  # Similar timing
    'mos6510': 'mos6502',  # Same core
    'wdc65c02': 'mos6502',  # Similar timing
    'z80a': 'z80',
    'z80b': 'z80',
    'm6801': 'm6800',
    'm6802': 'm6800',
    'm6805': 'm6800',
    'm68008': 'm68000',
    'm68010': 'm68000',
    'sun_spark': 'sparc',
}


# =============================================================================
# SOURCE URL DATABASE
# =============================================================================

SOURCE_URLS = {
    'i4004': {
        'datasheet': 'http://datasheets.chipdb.org/Intel/MCS-4/datashts/intel-4004.pdf',
        'wikichip': 'https://en.wikichip.org/wiki/intel/mcs-4/4004',
        'wikipedia': 'https://en.wikipedia.org/wiki/Intel_4004',
    },
    'i8008': {
        'datasheet': 'http://datasheets.chipdb.org/Intel/MCS-8/intel-8008.pdf',
        'wikichip': 'https://en.wikichip.org/wiki/intel/mcs-8/8008',
        'wikipedia': 'https://en.wikipedia.org/wiki/Intel_8008',
    },
    'i8080': {
        'datasheet': 'http://datasheets.chipdb.org/Intel/MCS-80/intel-8080.pdf',
        'wikichip': 'https://en.wikichip.org/wiki/intel/mcs-80/8080',
        'wikipedia': 'https://en.wikipedia.org/wiki/Intel_8080',
        'mame': 'https://github.com/mamedev/mame/blob/master/src/devices/cpu/i8085/i8085.cpp',
    },
    'i8085': {
        'datasheet': 'http://datasheets.chipdb.org/Intel/MCS-85/intel-8085.pdf',
        'wikichip': 'https://en.wikichip.org/wiki/intel/mcs-85/8085',
        'wikipedia': 'https://en.wikipedia.org/wiki/Intel_8085',
    },
    'i8086': {
        'datasheet': 'http://datasheets.chipdb.org/Intel/x86/808x/datashts/8086.pdf',
        'wikichip': 'https://en.wikichip.org/wiki/intel/8086',
        'wikipedia': 'https://en.wikipedia.org/wiki/Intel_8086',
    },
    'i8088': {
        'datasheet': 'http://datasheets.chipdb.org/Intel/x86/808x/datashts/8088.pdf',
        'wikichip': 'https://en.wikichip.org/wiki/intel/8088',
        'wikipedia': 'https://en.wikipedia.org/wiki/Intel_8088',
    },
    'i80286': {
        'datasheet': 'http://datasheets.chipdb.org/Intel/x86/286/datashts/intel-80286.pdf',
        'wikichip': 'https://en.wikichip.org/wiki/intel/80286',
        'wikipedia': 'https://en.wikipedia.org/wiki/Intel_80286',
    },
    'i80386': {
        'datasheet': 'http://datasheets.chipdb.org/Intel/x86/386/datashts/intel-80386.pdf',
        'wikichip': 'https://en.wikichip.org/wiki/intel/80386',
        'wikipedia': 'https://en.wikipedia.org/wiki/Intel_80386',
    },
    'mos6502': {
        'datasheet': 'http://archive.6502.org/datasheets/mos_6500_mpu_preliminary_may_1976.pdf',
        'wikichip': 'https://en.wikichip.org/wiki/mos_technology/6502',
        'wikipedia': 'https://en.wikipedia.org/wiki/MOS_Technology_6502',
        'vice': 'https://vice-emu.sourceforge.io/',
    },
    'z80': {
        'datasheet': 'http://www.z80.info/zip/z80.pdf',
        'wikichip': 'https://en.wikichip.org/wiki/zilog/z80',
        'wikipedia': 'https://en.wikipedia.org/wiki/Zilog_Z80',
        'mame': 'https://github.com/mamedev/mame/blob/master/src/devices/cpu/z80/z80.cpp',
    },
    'm6800': {
        'datasheet': 'http://www.bitsavers.org/components/motorola/6800/MC6800_8-Bit_Microprocessor_Data_Sheet.pdf',
        'wikipedia': 'https://en.wikipedia.org/wiki/Motorola_6800',
    },
    'm6809': {
        'datasheet': 'http://www.bitsavers.org/components/motorola/6809/MC6809_Datasheet.pdf',
        'wikipedia': 'https://en.wikipedia.org/wiki/Motorola_6809',
    },
    'm68000': {
        'datasheet': 'http://www.bitsavers.org/components/motorola/68000/MC68000_Users_Manual.pdf',
        'wikichip': 'https://en.wikichip.org/wiki/motorola/68000',
        'wikipedia': 'https://en.wikipedia.org/wiki/Motorola_68000',
        'mame': 'https://github.com/mamedev/mame/blob/master/src/devices/cpu/m68000/m68000.cpp',
    },
    'arm1': {
        'wikipedia': 'https://en.wikipedia.org/wiki/ARM_architecture',
        'wikichip': 'https://en.wikichip.org/wiki/acorn/microarchitectures/arm1',
    },
    'sparc': {
        'wikipedia': 'https://en.wikipedia.org/wiki/SPARC',
        'wikichip': 'https://en.wikichip.org/wiki/sun/sparc',
    },
}


# =============================================================================
# VALIDATION POPULATION FUNCTIONS
# =============================================================================

def get_timing_data(processor_name: str) -> Optional[Dict]:
    """Get timing data for a processor, checking aliases"""
    # Direct match
    if processor_name in TIMING_DATABASE:
        return TIMING_DATABASE[processor_name]
    
    # Check aliases
    alias = PROCESSOR_ALIASES.get(processor_name)
    if alias and alias in TIMING_DATABASE:
        return TIMING_DATABASE[alias]
    
    return None


def get_source_urls(processor_name: str) -> Dict[str, str]:
    """Get source URLs for a processor"""
    if processor_name in SOURCE_URLS:
        return SOURCE_URLS[processor_name]
    
    alias = PROCESSOR_ALIASES.get(processor_name)
    if alias and alias in SOURCE_URLS:
        return SOURCE_URLS[alias]
    
    return {}


def load_model(model_path: Path, repo_root: Path) -> Tuple[Any, Optional[str]]:
    """Load a processor model"""
    try:
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        
        spec = importlib.util.spec_from_file_location("model", model_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        for name in dir(module):
            if name.endswith('Model') and name != 'BaseProcessorModel':
                obj = getattr(module, name)
                if isinstance(obj, type):
                    return obj(), None
        
        return None, "No model class found"
    except Exception as e:
        return None, str(e)


def run_model_accuracy(model: Any, expected_cpi: float) -> Optional[float]:
    """Run model and calculate accuracy against expected CPI"""
    try:
        if hasattr(model, 'analyze'):
            result = model.analyze('typical')
            if hasattr(result, 'cpi') and result.cpi > 0:
                predicted_cpi = result.cpi
                error = abs(predicted_cpi - expected_cpi) / expected_cpi * 100
                return error
    except Exception:
        pass
    return None


def populate_validation_json(
    json_path: Path,
    processor_name: str,
    repo_root: Path,
    dry_run: bool = False,
    run_accuracy: bool = False
) -> Tuple[bool, List[str]]:
    """Populate a validation JSON file with timing data"""
    changes = []
    
    # Load existing JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return False, [f"Error loading JSON: {e}"]
    
    modified = False
    
    # Add processor name if missing
    if 'processor' not in data or not data['processor']:
        data['processor'] = processor_name
        changes.append(f"Added processor name: {processor_name}")
        modified = True
    
    # Add validation_date
    if 'validation_date' not in data or not data['validation_date']:
        data['validation_date'] = datetime.now().strftime('%Y-%m-%d')
        changes.append("Added validation_date")
        modified = True
    
    # Get timing data
    timing_data = get_timing_data(processor_name)
    
    # Add sources if we have URLs
    source_urls = get_source_urls(processor_name)
    if source_urls:
        existing_types = {s.get('type') for s in data.get('sources', [])}
        new_sources = []
        
        for source_type, url in source_urls.items():
            if source_type not in existing_types:
                new_sources.append({
                    'type': source_type,
                    'name': source_type.title(),
                    'url': url,
                    'verified': False
                })
        
        if new_sources:
            if 'sources' not in data:
                data['sources'] = []
            data['sources'].extend(new_sources)
            changes.append(f"Added {len(new_sources)} source(s): {[s['type'] for s in new_sources]}")
            modified = True
    
    # Add timing tests
    if timing_data and 'timing_tests' in timing_data:
        existing_tests = {t.get('name') for t in data.get('timing_tests', [])}
        new_tests = []
        
        for test in timing_data['timing_tests']:
            if test['name'] not in existing_tests:
                new_tests.append({
                    'name': test['name'],
                    'category': test['category'],
                    'expected_cycles': test['expected_cycles'],
                    'measured_cycles': None,
                    'error_percent': None,
                    'passed': False,
                    'source': test.get('source', 'datasheet')
                })
        
        if new_tests:
            if 'timing_tests' not in data:
                data['timing_tests'] = []
            data['timing_tests'].extend(new_tests)
            changes.append(f"Added {len(new_tests)} timing test(s)")
            modified = True
    
    # Add accuracy section if missing
    if 'accuracy' not in data:
        data['accuracy'] = {
            'ipc_error_percent': None,
            'cpi_error_percent': None,
            'validated_workloads': [],
            'notes': 'Validation pending'
        }
        changes.append("Added accuracy section")
        modified = True
    
    # Run accuracy measurement if requested
    if run_accuracy and timing_data:
        expected_cpi = timing_data.get('typical_cpi')
        if expected_cpi:
            # Find model file
            model_dir = json_path.parent.parent / 'current'
            model_files = list(model_dir.glob('*_validated.py'))
            
            if model_files:
                model, error = load_model(model_files[0], repo_root)
                if model:
                    accuracy_error = run_model_accuracy(model, expected_cpi)
                    if accuracy_error is not None:
                        data['accuracy']['cpi_error_percent'] = round(accuracy_error, 2)
                        data['accuracy']['ipc_error_percent'] = round(accuracy_error, 2)
                        data['accuracy']['notes'] = f"Model predicted CPI vs expected {expected_cpi}"
                        changes.append(f"Measured accuracy: {accuracy_error:.1f}% error")
                        modified = True
    
    # Write changes
    if modified and not dry_run:
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            return False, [f"Error writing JSON: {e}"]
    
    return modified, changes


def populate_repository(
    repo_path: Path,
    dry_run: bool = False,
    run_accuracy: bool = False
) -> Dict[str, Any]:
    """Populate validation data for entire repository"""
    results = {
        'processors_checked': 0,
        'processors_updated': 0,
        'changes': []
    }
    
    families = ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']
    
    for family in families:
        family_path = repo_path / family
        if not family_path.exists():
            continue
        
        for proc_dir in sorted(family_path.iterdir()):
            if not proc_dir.is_dir() or proc_dir.name.startswith('.'):
                continue
            
            validation_dir = proc_dir / 'validation'
            if not validation_dir.exists():
                continue
            
            json_files = list(validation_dir.glob('*_validation.json'))
            if not json_files:
                continue
            
            results['processors_checked'] += 1
            
            modified, changes = populate_validation_json(
                json_files[0],
                proc_dir.name,
                repo_path,
                dry_run,
                run_accuracy
            )
            
            if modified:
                results['processors_updated'] += 1
                results['changes'].append({
                    'processor': f"{family}/{proc_dir.name}",
                    'changes': changes
                })
    
    return results


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Populate validation data for Modeling_2026'
    )
    parser.add_argument(
        'repo_path',
        nargs='?',
        default='.',
        help='Repository path'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes only'
    )
    parser.add_argument(
        '--run-accuracy',
        action='store_true',
        help='Run models to measure actual accuracy'
    )
    parser.add_argument(
        '--processor', '-p',
        help='Update specific processor only'
    )
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    print("=" * 60)
    print("VALIDATION DATA POPULATION")
    print("=" * 60)
    print(f"Repository: {repo_path}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'APPLY CHANGES'}")
    print(f"Run accuracy: {'YES' if args.run_accuracy else 'NO'}")
    print()
    
    if args.processor:
        # Single processor
        for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
            json_path = repo_path / family / args.processor / 'validation' / f'{args.processor}_validation.json'
            if json_path.exists():
                modified, changes = populate_validation_json(
                    json_path, args.processor, repo_path, args.dry_run, args.run_accuracy
                )
                if changes:
                    print(f"{'Would update' if args.dry_run else 'Updated'}: {family}/{args.processor}")
                    for c in changes:
                        print(f"  - {c}")
                else:
                    print(f"No changes needed for {args.processor}")
                break
        else:
            print(f"Processor not found: {args.processor}")
    else:
        # All processors
        results = populate_repository(repo_path, args.dry_run, args.run_accuracy)
        
        print(f"Processors checked: {results['processors_checked']}")
        print(f"Processors {'to update' if args.dry_run else 'updated'}: {results['processors_updated']}")
        print()
        
        if results['changes']:
            print("CHANGES:")
            print("-" * 40)
            for item in results['changes']:
                print(f"\n📄 {item['processor']}")
                for c in item['changes']:
                    print(f"  - {c}")
    
    print()
    print("=" * 60)
    if args.dry_run:
        print("DRY RUN - No files modified")
        print("Run without --dry-run to apply changes")
    print("=" * 60)


if __name__ == '__main__':
    main()
