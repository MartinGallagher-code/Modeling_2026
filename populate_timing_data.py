#!/usr/bin/env python3
"""
Populate Timing Data for Modeling_2026
=======================================

Auto-populates validation JSON files with:
1. Timing tests based on datasheet values
2. Expected cycle counts for instruction categories
3. Accuracy measurement framework
4. Source URLs

Usage:
    python populate_timing_data.py [repo_path] [--dry-run]

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


# =============================================================================
# PROCESSOR TIMING DATABASE
# Based on original datasheets and technical references
# =============================================================================

PROCESSOR_TIMING_DATA = {
    # =========================================================================
    # INTEL FAMILY
    # =========================================================================
    'i4004': {
        'full_name': 'Intel 4004',
        'manufacturer': 'Intel',
        'year': 1971,
        'clock_mhz': 0.74,
        'architecture': 'sequential',
        'sources': [
            {'type': 'datasheet', 'name': 'Intel 4004 Datasheet', 'url': 'http://datasheets.chipdb.org/Intel/MCS-4/datashts/intel-4004.pdf', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip 4004', 'url': 'https://en.wikichip.org/wiki/intel/mcs-4/4004', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'ADD', 'category': 'alu', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'SUB', 'category': 'alu', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'LD', 'category': 'data_transfer', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'XCH', 'category': 'data_transfer', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'JUN', 'category': 'control', 'expected_cycles': 16, 'source': 'datasheet'},
            {'name': 'JCN', 'category': 'control', 'expected_cycles': 16, 'source': 'datasheet'},
            {'name': 'FIM', 'category': 'data_transfer', 'expected_cycles': 16, 'source': 'datasheet'},
        ],
        'typical_cpi': 10.8,
        'instruction_mix': {'alu': 0.30, 'data_transfer': 0.35, 'control': 0.25, 'memory': 0.10},
    },
    
    'i4040': {
        'full_name': 'Intel 4040',
        'manufacturer': 'Intel',
        'year': 1974,
        'clock_mhz': 0.74,
        'architecture': 'sequential',
        'sources': [
            {'type': 'datasheet', 'name': 'Intel 4040 Datasheet', 'url': 'http://datasheets.chipdb.org/Intel/MCS-4/datashts/intel-4040.pdf', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip 4040', 'url': 'https://en.wikichip.org/wiki/intel/mcs-4/4040', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'ADD', 'category': 'alu', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'HLT', 'category': 'control', 'expected_cycles': 8, 'source': 'datasheet'},
        ],
        'typical_cpi': 10.5,
    },
    
    'i8008': {
        'full_name': 'Intel 8008',
        'manufacturer': 'Intel',
        'year': 1972,
        'clock_mhz': 0.5,
        'architecture': 'sequential',
        'sources': [
            {'type': 'datasheet', 'name': 'Intel 8008 Datasheet', 'url': 'http://datasheets.chipdb.org/Intel/MCS-8/intel-8008.pdf', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip 8008', 'url': 'https://en.wikichip.org/wiki/intel/mcs-8/8008', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'MOV_r_r', 'category': 'data_transfer', 'expected_cycles': 5, 'source': 'datasheet'},
            {'name': 'MOV_r_M', 'category': 'memory', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'ADD_r', 'category': 'alu', 'expected_cycles': 5, 'source': 'datasheet'},
            {'name': 'ADD_M', 'category': 'alu', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'JMP', 'category': 'control', 'expected_cycles': 11, 'source': 'datasheet'},
            {'name': 'CALL', 'category': 'control', 'expected_cycles': 11, 'source': 'datasheet'},
            {'name': 'RET', 'category': 'control', 'expected_cycles': 5, 'source': 'datasheet'},
            {'name': 'INR', 'category': 'alu', 'expected_cycles': 5, 'source': 'datasheet'},
        ],
        'typical_cpi': 11.0,
    },
    
    'i8080': {
        'full_name': 'Intel 8080',
        'manufacturer': 'Intel',
        'year': 1974,
        'clock_mhz': 2.0,
        'architecture': 'sequential',
        'sources': [
            {'type': 'datasheet', 'name': 'Intel 8080 Datasheet', 'url': 'http://datasheets.chipdb.org/Intel/MCS-80/intel-8080.pdf', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip 8080', 'url': 'https://en.wikichip.org/wiki/intel/mcs-80/8080', 'verified': True},
            {'type': 'emulator', 'name': 'MAME i8080', 'url': 'https://github.com/mamedev/mame/blob/master/src/devices/cpu/i8085/i8085.cpp', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'MOV_r_r', 'category': 'data_transfer', 'expected_cycles': 5, 'source': 'datasheet'},
            {'name': 'MOV_r_M', 'category': 'memory', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'MOV_M_r', 'category': 'memory', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'MVI_r', 'category': 'data_transfer', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'MVI_M', 'category': 'memory', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'ADD_r', 'category': 'alu', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADD_M', 'category': 'alu', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'ADI', 'category': 'alu', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'JMP', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'JZ', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'CALL', 'category': 'control', 'expected_cycles': 17, 'source': 'datasheet'},
            {'name': 'RET', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'PUSH', 'category': 'stack', 'expected_cycles': 11, 'source': 'datasheet'},
            {'name': 'POP', 'category': 'stack', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 4, 'source': 'datasheet'},
        ],
        'typical_cpi': 9.2,
        'instruction_mix': {'alu': 0.25, 'data_transfer': 0.30, 'memory': 0.20, 'control': 0.15, 'stack': 0.10},
    },
    
    'i8085': {
        'full_name': 'Intel 8085',
        'manufacturer': 'Intel',
        'year': 1976,
        'clock_mhz': 3.0,
        'architecture': 'sequential',
        'sources': [
            {'type': 'datasheet', 'name': 'Intel 8085 Datasheet', 'url': 'http://datasheets.chipdb.org/Intel/MCS-85/intel-8085.pdf', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip 8085', 'url': 'https://en.wikichip.org/wiki/intel/mcs-85/8085', 'verified': True},
            {'type': 'emulator', 'name': 'MAME i8085', 'url': 'https://github.com/mamedev/mame/blob/master/src/devices/cpu/i8085/i8085.cpp', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'MOV_r_r', 'category': 'data_transfer', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'MOV_r_M', 'category': 'memory', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'ADD_r', 'category': 'alu', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADD_M', 'category': 'alu', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'JMP', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'CALL', 'category': 'control', 'expected_cycles': 18, 'source': 'datasheet'},
            {'name': 'RET', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 4, 'source': 'datasheet'},
        ],
        'typical_cpi': 5.5,
    },
    
    'i8086': {
        'full_name': 'Intel 8086',
        'manufacturer': 'Intel',
        'year': 1978,
        'clock_mhz': 5.0,
        'architecture': 'prefetch_queue',
        'sources': [
            {'type': 'datasheet', 'name': 'Intel 8086 Datasheet', 'url': 'http://datasheets.chipdb.org/Intel/x86/808x/datashts/8086.pdf', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip 8086', 'url': 'https://en.wikichip.org/wiki/intel/8086', 'verified': True},
            {'type': 'emulator', 'name': 'DOSBox', 'url': 'https://www.dosbox.com/', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'MOV_reg_reg', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MOV_reg_mem', 'category': 'memory', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'MOV_mem_reg', 'category': 'memory', 'expected_cycles': 9, 'source': 'datasheet'},
            {'name': 'MOV_reg_imm', 'category': 'data_transfer', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADD_reg_reg', 'category': 'alu', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'ADD_reg_mem', 'category': 'alu', 'expected_cycles': 9, 'source': 'datasheet'},
            {'name': 'ADD_reg_imm', 'category': 'alu', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'MUL_reg8', 'category': 'mul_div', 'expected_cycles': 77, 'source': 'datasheet'},
            {'name': 'MUL_reg16', 'category': 'mul_div', 'expected_cycles': 133, 'source': 'datasheet'},
            {'name': 'DIV_reg8', 'category': 'mul_div', 'expected_cycles': 90, 'source': 'datasheet'},
            {'name': 'JMP_near', 'category': 'control', 'expected_cycles': 15, 'source': 'datasheet'},
            {'name': 'JZ', 'category': 'control', 'expected_cycles': 16, 'source': 'datasheet'},
            {'name': 'CALL_near', 'category': 'control', 'expected_cycles': 19, 'source': 'datasheet'},
            {'name': 'RET', 'category': 'control', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'PUSH', 'category': 'stack', 'expected_cycles': 11, 'source': 'datasheet'},
            {'name': 'POP', 'category': 'stack', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'MOVSB', 'category': 'string', 'expected_cycles': 18, 'source': 'datasheet'},
            {'name': 'REP_MOVSB', 'category': 'string', 'expected_cycles': 9, 'source': 'datasheet', 'notes': 'per iteration'},
        ],
        'typical_cpi': 4.5,
        'instruction_mix': {'alu': 0.25, 'data_transfer': 0.25, 'memory': 0.20, 'control': 0.15, 'stack': 0.10, 'string': 0.05},
    },
    
    'i8088': {
        'full_name': 'Intel 8088',
        'manufacturer': 'Intel',
        'year': 1979,
        'clock_mhz': 5.0,
        'architecture': 'prefetch_queue',
        'sources': [
            {'type': 'datasheet', 'name': 'Intel 8088 Datasheet', 'url': 'http://datasheets.chipdb.org/Intel/x86/808x/datashts/8088.pdf', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip 8088', 'url': 'https://en.wikichip.org/wiki/intel/8088', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'MOV_reg_reg', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MOV_reg_mem', 'category': 'memory', 'expected_cycles': 12, 'source': 'datasheet', 'notes': '8-bit bus penalty'},
            {'name': 'ADD_reg_reg', 'category': 'alu', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'JMP_near', 'category': 'control', 'expected_cycles': 15, 'source': 'datasheet'},
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
        ],
        'typical_cpi': 5.2,
        'notes': 'Same as 8086 but with 8-bit external bus, causing memory access penalties',
    },
    
    'i80186': {
        'full_name': 'Intel 80186',
        'manufacturer': 'Intel',
        'year': 1982,
        'clock_mhz': 6.0,
        'architecture': 'prefetch_queue',
        'sources': [
            {'type': 'wikichip', 'name': 'WikiChip 80186', 'url': 'https://en.wikichip.org/wiki/intel/80186', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'MOV_reg_reg', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'reference'},
            {'name': 'ADD_reg_reg', 'category': 'alu', 'expected_cycles': 3, 'source': 'reference'},
            {'name': 'MUL_reg16', 'category': 'mul_div', 'expected_cycles': 36, 'source': 'reference', 'notes': 'Faster than 8086'},
            {'name': 'DIV_reg16', 'category': 'mul_div', 'expected_cycles': 38, 'source': 'reference'},
        ],
        'typical_cpi': 4.0,
    },
    
    'i80286': {
        'full_name': 'Intel 80286',
        'manufacturer': 'Intel',
        'year': 1982,
        'clock_mhz': 6.0,
        'architecture': 'pipelined',
        'sources': [
            {'type': 'datasheet', 'name': 'Intel 80286 Datasheet', 'url': 'http://datasheets.chipdb.org/Intel/x86/286/datashts/intel-80286.pdf', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip 80286', 'url': 'https://en.wikichip.org/wiki/intel/80286', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'MOV_reg_reg', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MOV_reg_mem', 'category': 'memory', 'expected_cycles': 5, 'source': 'datasheet'},
            {'name': 'ADD_reg_reg', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MUL_reg16', 'category': 'mul_div', 'expected_cycles': 21, 'source': 'datasheet'},
            {'name': 'DIV_reg16', 'category': 'mul_div', 'expected_cycles': 22, 'source': 'datasheet'},
            {'name': 'JMP_near', 'category': 'control', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'CALL_near', 'category': 'control', 'expected_cycles': 7, 'source': 'datasheet'},
        ],
        'typical_cpi': 4.0,
    },
    
    'i80386': {
        'full_name': 'Intel 80386',
        'manufacturer': 'Intel',
        'year': 1985,
        'clock_mhz': 16.0,
        'architecture': 'cache_risc',
        'sources': [
            {'type': 'datasheet', 'name': 'Intel 80386 Datasheet', 'url': 'http://datasheets.chipdb.org/Intel/x86/386/datashts/intel-80386.pdf', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip 80386', 'url': 'https://en.wikichip.org/wiki/intel/80386', 'verified': True},
            {'type': 'emulator', 'name': 'DOSBox-X', 'url': 'https://dosbox-x.com/', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'MOV_reg_reg', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MOV_reg_mem', 'category': 'memory', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADD_reg_reg', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MUL_reg32', 'category': 'mul_div', 'expected_cycles': 14, 'source': 'datasheet'},
            {'name': 'DIV_reg32', 'category': 'mul_div', 'expected_cycles': 40, 'source': 'datasheet'},
            {'name': 'JMP_near', 'category': 'control', 'expected_cycles': 7, 'source': 'datasheet'},
        ],
        'typical_cpi': 4.5,
    },
    
    # =========================================================================
    # MOS/WDC FAMILY
    # =========================================================================
    'mos6502': {
        'full_name': 'MOS Technology 6502',
        'manufacturer': 'MOS Technology',
        'year': 1975,
        'clock_mhz': 1.0,
        'architecture': 'sequential',
        'sources': [
            {'type': 'datasheet', 'name': 'MOS 6502 Datasheet', 'url': 'http://archive.6502.org/datasheets/mos_6500_mpu_preliminary_may_1976.pdf', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip 6502', 'url': 'https://en.wikichip.org/wiki/mos_technology/6502', 'verified': True},
            {'type': 'emulator', 'name': 'VICE', 'url': 'https://vice-emu.sourceforge.io/', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'LDA_imm', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'LDA_zp', 'category': 'memory', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'LDA_abs', 'category': 'memory', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'LDA_abs_x', 'category': 'memory', 'expected_cycles': 4, 'source': 'datasheet', 'notes': '+1 if page crossed'},
            {'name': 'STA_zp', 'category': 'memory', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'STA_abs', 'category': 'memory', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADC_imm', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'ADC_zp', 'category': 'alu', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'INX', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'DEX', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'JMP_abs', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'JSR', 'category': 'control', 'expected_cycles': 6, 'source': 'datasheet'},
            {'name': 'RTS', 'category': 'control', 'expected_cycles': 6, 'source': 'datasheet'},
            {'name': 'BEQ', 'category': 'control', 'expected_cycles': 2, 'source': 'datasheet', 'notes': '+1 if branch taken, +2 if page crossed'},
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'PHA', 'category': 'stack', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'PLA', 'category': 'stack', 'expected_cycles': 4, 'source': 'datasheet'},
        ],
        'typical_cpi': 3.5,
        'instruction_mix': {'alu': 0.25, 'data_transfer': 0.15, 'memory': 0.30, 'control': 0.20, 'stack': 0.10},
    },
    
    'mos6510': {
        'full_name': 'MOS Technology 6510',
        'manufacturer': 'MOS Technology',
        'year': 1982,
        'clock_mhz': 1.0,
        'architecture': 'sequential',
        'sources': [
            {'type': 'wikipedia', 'name': 'Wikipedia 6510', 'url': 'https://en.wikipedia.org/wiki/MOS_Technology_6510', 'verified': True},
            {'type': 'emulator', 'name': 'VICE', 'url': 'https://vice-emu.sourceforge.io/', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'LDA_imm', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'reference'},
            {'name': 'STA_abs', 'category': 'memory', 'expected_cycles': 4, 'source': 'reference'},
            {'name': 'ADC_imm', 'category': 'alu', 'expected_cycles': 2, 'source': 'reference'},
            {'name': 'JMP_abs', 'category': 'control', 'expected_cycles': 3, 'source': 'reference'},
        ],
        'typical_cpi': 3.5,
        'notes': 'Same timing as 6502, adds I/O port',
    },
    
    'wdc65c02': {
        'full_name': 'WDC 65C02',
        'manufacturer': 'Western Design Center',
        'year': 1983,
        'clock_mhz': 2.0,
        'architecture': 'sequential',
        'sources': [
            {'type': 'datasheet', 'name': 'WDC 65C02 Datasheet', 'url': 'https://www.westerndesigncenter.com/wdc/documentation/w65c02s.pdf', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'LDA_imm', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'LDA_zp', 'category': 'memory', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'ADC_imm', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'BRA', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet', 'notes': 'New instruction'},
        ],
        'typical_cpi': 3.2,
    },
    
    'wdc65816': {
        'full_name': 'WDC 65816',
        'manufacturer': 'Western Design Center',
        'year': 1984,
        'clock_mhz': 2.8,
        'architecture': 'prefetch_queue',
        'sources': [
            {'type': 'datasheet', 'name': 'WDC 65816 Datasheet', 'url': 'https://www.westerndesigncenter.com/wdc/documentation/w65c816s.pdf', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'LDA_imm_8', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'LDA_imm_16', 'category': 'data_transfer', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'ADC_imm', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'JMP_abs', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'JSL', 'category': 'control', 'expected_cycles': 8, 'source': 'datasheet', 'notes': 'Long jump to subroutine'},
        ],
        'typical_cpi': 3.8,
    },
    
    # =========================================================================
    # MOTOROLA FAMILY
    # =========================================================================
    'm6800': {
        'full_name': 'Motorola 6800',
        'manufacturer': 'Motorola',
        'year': 1974,
        'clock_mhz': 1.0,
        'architecture': 'sequential',
        'sources': [
            {'type': 'datasheet', 'name': 'Motorola 6800 Datasheet', 'url': 'http://www.bitsavers.org/components/motorola/6800/MC6800_8-Bit_Microprocessor_Data_Sheet.pdf', 'verified': True},
            {'type': 'wikipedia', 'name': 'Wikipedia 6800', 'url': 'https://en.wikipedia.org/wiki/Motorola_6800', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'LDAA_imm', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'LDAA_dir', 'category': 'memory', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'LDAA_ext', 'category': 'memory', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'STAA_dir', 'category': 'memory', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADDA_imm', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'JMP_ext', 'category': 'control', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'JSR_ext', 'category': 'control', 'expected_cycles': 9, 'source': 'datasheet'},
            {'name': 'RTS', 'category': 'control', 'expected_cycles': 5, 'source': 'datasheet'},
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 2, 'source': 'datasheet'},
        ],
        'typical_cpi': 4.0,
    },
    
    'm6809': {
        'full_name': 'Motorola 6809',
        'manufacturer': 'Motorola',
        'year': 1978,
        'clock_mhz': 1.0,
        'architecture': 'prefetch_queue',
        'sources': [
            {'type': 'datasheet', 'name': 'Motorola 6809 Datasheet', 'url': 'http://www.bitsavers.org/components/motorola/6809/MC6809_Datasheet.pdf', 'verified': True},
            {'type': 'wikipedia', 'name': 'Wikipedia 6809', 'url': 'https://en.wikipedia.org/wiki/Motorola_6809', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'LDA_imm', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'LDA_dir', 'category': 'memory', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'LDD_imm', 'category': 'data_transfer', 'expected_cycles': 3, 'source': 'datasheet'},
            {'name': 'ADDA_imm', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MUL', 'category': 'mul_div', 'expected_cycles': 11, 'source': 'datasheet'},
            {'name': 'JMP_ext', 'category': 'control', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'JSR_ext', 'category': 'control', 'expected_cycles': 8, 'source': 'datasheet'},
        ],
        'typical_cpi': 3.5,
    },
    
    'm68000': {
        'full_name': 'Motorola 68000',
        'manufacturer': 'Motorola',
        'year': 1979,
        'clock_mhz': 8.0,
        'architecture': 'pipelined',
        'sources': [
            {'type': 'datasheet', 'name': 'Motorola 68000 Users Manual', 'url': 'http://www.bitsavers.org/components/motorola/68000/MC68000_Users_Manual.pdf', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip 68000', 'url': 'https://en.wikichip.org/wiki/motorola/68000', 'verified': True},
            {'type': 'emulator', 'name': 'MAME m68000', 'url': 'https://github.com/mamedev/mame/tree/master/src/devices/cpu/m68000', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'MOVE.L_Dn_Dn', 'category': 'data_transfer', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'MOVE.L_Dn_An', 'category': 'data_transfer', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'MOVE.L_mem_Dn', 'category': 'memory', 'expected_cycles': 12, 'source': 'datasheet'},
            {'name': 'ADD.L_Dn_Dn', 'category': 'alu', 'expected_cycles': 8, 'source': 'datasheet'},
            {'name': 'MULU', 'category': 'mul_div', 'expected_cycles': 70, 'source': 'datasheet'},
            {'name': 'MULS', 'category': 'mul_div', 'expected_cycles': 70, 'source': 'datasheet'},
            {'name': 'DIVU', 'category': 'mul_div', 'expected_cycles': 140, 'source': 'datasheet'},
            {'name': 'DIVS', 'category': 'mul_div', 'expected_cycles': 158, 'source': 'datasheet'},
            {'name': 'JMP_abs', 'category': 'control', 'expected_cycles': 12, 'source': 'datasheet'},
            {'name': 'JSR_abs', 'category': 'control', 'expected_cycles': 18, 'source': 'datasheet'},
            {'name': 'RTS', 'category': 'control', 'expected_cycles': 16, 'source': 'datasheet'},
            {'name': 'BRA', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 4, 'source': 'datasheet'},
        ],
        'typical_cpi': 6.5,
    },
    
    'm68020': {
        'full_name': 'Motorola 68020',
        'manufacturer': 'Motorola',
        'year': 1984,
        'clock_mhz': 16.0,
        'architecture': 'pipelined',
        'sources': [
            {'type': 'datasheet', 'name': 'Motorola 68020 Users Manual', 'url': 'http://www.bitsavers.org/components/motorola/68000/MC68020_Users_Manual.pdf', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip 68020', 'url': 'https://en.wikichip.org/wiki/motorola/68020', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'MOVE.L_Dn_Dn', 'category': 'data_transfer', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'ADD.L_Dn_Dn', 'category': 'alu', 'expected_cycles': 2, 'source': 'datasheet'},
            {'name': 'MULU.L', 'category': 'mul_div', 'expected_cycles': 44, 'source': 'datasheet'},
            {'name': 'DIVU.L', 'category': 'mul_div', 'expected_cycles': 90, 'source': 'datasheet'},
        ],
        'typical_cpi': 3.5,
    },
    
    # =========================================================================
    # ZILOG FAMILY
    # =========================================================================
    'z80': {
        'full_name': 'Zilog Z80',
        'manufacturer': 'Zilog',
        'year': 1976,
        'clock_mhz': 2.5,
        'architecture': 'prefetch_queue',
        'sources': [
            {'type': 'datasheet', 'name': 'Zilog Z80 CPU Manual', 'url': 'http://www.z80.info/zip/z80.pdf', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip Z80', 'url': 'https://en.wikichip.org/wiki/zilog/z80', 'verified': True},
            {'type': 'emulator', 'name': 'MAME Z80', 'url': 'https://github.com/mamedev/mame/blob/master/src/devices/cpu/z80/z80.cpp', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'LD_r_r', 'category': 'data_transfer', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'LD_r_n', 'category': 'data_transfer', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'LD_r_HL', 'category': 'memory', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'LD_HL_r', 'category': 'memory', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'LD_A_nn', 'category': 'memory', 'expected_cycles': 13, 'source': 'datasheet'},
            {'name': 'ADD_A_r', 'category': 'alu', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'ADD_A_n', 'category': 'alu', 'expected_cycles': 7, 'source': 'datasheet'},
            {'name': 'ADD_HL_rr', 'category': 'alu', 'expected_cycles': 11, 'source': 'datasheet'},
            {'name': 'INC_r', 'category': 'alu', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'JP_nn', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'JP_cc_nn', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'JR_e', 'category': 'control', 'expected_cycles': 12, 'source': 'datasheet'},
            {'name': 'CALL_nn', 'category': 'control', 'expected_cycles': 17, 'source': 'datasheet'},
            {'name': 'RET', 'category': 'control', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'PUSH_rr', 'category': 'stack', 'expected_cycles': 11, 'source': 'datasheet'},
            {'name': 'POP_rr', 'category': 'stack', 'expected_cycles': 10, 'source': 'datasheet'},
            {'name': 'NOP', 'category': 'control', 'expected_cycles': 4, 'source': 'datasheet'},
            {'name': 'LDIR', 'category': 'block', 'expected_cycles': 21, 'source': 'datasheet', 'notes': 'per iteration when BC!=0'},
        ],
        'typical_cpi': 5.5,
        'instruction_mix': {'alu': 0.25, 'data_transfer': 0.25, 'memory': 0.20, 'control': 0.15, 'stack': 0.10, 'block': 0.05},
    },
    
    'z8000': {
        'full_name': 'Zilog Z8000',
        'manufacturer': 'Zilog',
        'year': 1979,
        'clock_mhz': 4.0,
        'architecture': 'prefetch_queue',
        'sources': [
            {'type': 'wikipedia', 'name': 'Wikipedia Z8000', 'url': 'https://en.wikipedia.org/wiki/Zilog_Z8000', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'LD_R_R', 'category': 'data_transfer', 'expected_cycles': 3, 'source': 'reference'},
            {'name': 'ADD_R_R', 'category': 'alu', 'expected_cycles': 4, 'source': 'reference'},
            {'name': 'JP', 'category': 'control', 'expected_cycles': 7, 'source': 'reference'},
        ],
        'typical_cpi': 4.5,
    },
    
    # =========================================================================
    # OTHER PROCESSORS
    # =========================================================================
    'arm1': {
        'full_name': 'ARM1',
        'manufacturer': 'Acorn',
        'year': 1985,
        'clock_mhz': 6.0,
        'architecture': 'cache_risc',
        'sources': [
            {'type': 'wikipedia', 'name': 'Wikipedia ARM', 'url': 'https://en.wikipedia.org/wiki/ARM_architecture', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip ARM1', 'url': 'https://en.wikichip.org/wiki/acorn/microarchitectures/arm1', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'MOV_R_R', 'category': 'data_transfer', 'expected_cycles': 1, 'source': 'reference'},
            {'name': 'ADD_R_R_R', 'category': 'alu', 'expected_cycles': 1, 'source': 'reference'},
            {'name': 'LDR', 'category': 'memory', 'expected_cycles': 3, 'source': 'reference'},
            {'name': 'STR', 'category': 'memory', 'expected_cycles': 2, 'source': 'reference'},
            {'name': 'B', 'category': 'control', 'expected_cycles': 3, 'source': 'reference'},
            {'name': 'BL', 'category': 'control', 'expected_cycles': 3, 'source': 'reference'},
            {'name': 'MUL', 'category': 'mul_div', 'expected_cycles': 16, 'source': 'reference', 'notes': 'variable, 2-17 cycles'},
        ],
        'typical_cpi': 1.8,
    },
    
    'sparc': {
        'full_name': 'SPARC',
        'manufacturer': 'Sun Microsystems',
        'year': 1987,
        'clock_mhz': 14.0,
        'architecture': 'cache_risc',
        'sources': [
            {'type': 'wikipedia', 'name': 'Wikipedia SPARC', 'url': 'https://en.wikipedia.org/wiki/SPARC', 'verified': True},
            {'type': 'wikichip', 'name': 'WikiChip SPARC', 'url': 'https://en.wikichip.org/wiki/sun/sparc', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'ADD', 'category': 'alu', 'expected_cycles': 1, 'source': 'reference'},
            {'name': 'LD', 'category': 'memory', 'expected_cycles': 1, 'source': 'reference', 'notes': 'cache hit'},
            {'name': 'ST', 'category': 'memory', 'expected_cycles': 1, 'source': 'reference', 'notes': 'cache hit'},
            {'name': 'CALL', 'category': 'control', 'expected_cycles': 1, 'source': 'reference', 'notes': 'delayed branch'},
        ],
        'typical_cpi': 1.5,
    },
    
    'am2901': {
        'full_name': 'AMD Am2901',
        'manufacturer': 'AMD',
        'year': 1975,
        'clock_mhz': 10.0,
        'architecture': 'sequential',
        'sources': [
            {'type': 'datasheet', 'name': 'AMD Am2901 Datasheet', 'url': 'http://www.bitsavers.org/components/amd/Am2900/Am2901_Am2901A_Four-Bit_Bipolar_Microprocessor_Slice_May79.pdf', 'verified': True},
            {'type': 'wikipedia', 'name': 'Wikipedia Am2900', 'url': 'https://en.wikipedia.org/wiki/AMD_Am2900', 'verified': True},
        ],
        'timing_tests': [
            {'name': 'ALU_op', 'category': 'alu', 'expected_cycles': 1, 'source': 'datasheet', 'notes': '4-bit slice, 100ns cycle'},
            {'name': 'SHIFT', 'category': 'alu', 'expected_cycles': 1, 'source': 'datasheet'},
        ],
        'typical_cpi': 1.0,
        'notes': '4-bit slice processor, timing is per microinstruction',
    },
}


# =============================================================================
# FUNCTIONS
# =============================================================================

def get_timing_data(processor_name: str) -> Optional[Dict[str, Any]]:
    """Get timing data for a processor from the database"""
    # Try exact match
    if processor_name in PROCESSOR_TIMING_DATA:
        return PROCESSOR_TIMING_DATA[processor_name]
    
    # Try with common prefixes/suffixes removed
    normalized = processor_name.lower().replace('_', '').replace('-', '')
    
    for key, data in PROCESSOR_TIMING_DATA.items():
        key_normalized = key.lower().replace('_', '').replace('-', '')
        if key_normalized == normalized:
            return data
    
    return None


def update_validation_json(json_path: Path, timing_data: Dict[str, Any], dry_run: bool = False) -> tuple:
    """Update a validation JSON file with timing data"""
    changes = []
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return False, [f"Error reading {json_path}: {e}"]
    
    original = json.dumps(data, sort_keys=True)
    
    # Update processor name if missing
    if 'processor' not in data or not data['processor']:
        data['processor'] = timing_data.get('full_name', json_path.stem.replace('_validation', ''))
        changes.append("Added processor name")
    
    # Update validation date
    data['validation_date'] = datetime.now().strftime('%Y-%m-%d')
    changes.append("Updated validation date")
    
    # Update sources
    if 'sources' not in data or not data['sources']:
        data['sources'] = timing_data.get('sources', [])
        changes.append(f"Added {len(data['sources'])} sources")
    else:
        # Merge sources, avoiding duplicates
        existing_urls = {s.get('url') for s in data['sources'] if s.get('url')}
        for new_source in timing_data.get('sources', []):
            if new_source.get('url') not in existing_urls:
                data['sources'].append(new_source)
                changes.append(f"Added source: {new_source.get('name')}")
    
    # Update timing tests
    if 'timing_tests' not in data or not data['timing_tests']:
        data['timing_tests'] = timing_data.get('timing_tests', [])
        changes.append(f"Added {len(data['timing_tests'])} timing tests")
    else:
        # Merge timing tests
        existing_tests = {t.get('name') for t in data['timing_tests']}
        for new_test in timing_data.get('timing_tests', []):
            if new_test.get('name') not in existing_tests:
                data['timing_tests'].append(new_test)
                changes.append(f"Added timing test: {new_test.get('name')}")
    
    # Update accuracy section
    if 'accuracy' not in data:
        data['accuracy'] = {}
    
    if 'ipc_error_percent' not in data['accuracy'] or data['accuracy']['ipc_error_percent'] is None:
        # Calculate expected IPC from typical_cpi
        if 'typical_cpi' in timing_data:
            typical_cpi = timing_data['typical_cpi']
            data['accuracy']['expected_cpi'] = typical_cpi
            data['accuracy']['expected_ipc'] = round(1.0 / typical_cpi, 4)
            changes.append(f"Added expected CPI: {typical_cpi}")
    
    if 'validated_workloads' not in data['accuracy']:
        data['accuracy']['validated_workloads'] = []
    
    # Update instruction mix if provided
    if 'instruction_mix' in timing_data:
        data['instruction_mix'] = timing_data['instruction_mix']
        changes.append("Added instruction mix")
    
    # Add notes
    if 'notes' in timing_data and timing_data['notes']:
        data['notes'] = timing_data['notes']
        changes.append("Added notes")
    
    # Check if anything changed
    if json.dumps(data, sort_keys=True) == original:
        return False, []
    
    # Write updated file
    if not dry_run:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    return True, changes


def populate_repository(repo_path: Path, dry_run: bool = False) -> dict:
    """Populate timing data for all processors in the repository"""
    results = {
        'files_checked': 0,
        'files_updated': 0,
        'files_skipped': 0,
        'no_data': [],
        'updated': [],
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
            
            json_path = json_files[0]
            results['files_checked'] += 1
            
            # Get timing data
            timing_data = get_timing_data(proc_dir.name)
            
            if timing_data is None:
                results['no_data'].append(proc_dir.name)
                results['files_skipped'] += 1
                continue
            
            # Update the file
            updated, changes = update_validation_json(json_path, timing_data, dry_run)
            
            if updated:
                results['files_updated'] += 1
                results['updated'].append({
                    'processor': proc_dir.name,
                    'changes': changes
                })
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Populate validation JSON files with timing data from datasheets'
    )
    parser.add_argument(
        'repo_path',
        nargs='?',
        default='.',
        help='Path to repository'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    parser.add_argument(
        '--processor',
        help='Update specific processor only'
    )
    parser.add_argument(
        '--list-available',
        action='store_true',
        help='List processors with timing data available'
    )
    
    args = parser.parse_args()
    
    if args.list_available:
        print("Processors with timing data available:")
        print("=" * 50)
        for name, data in sorted(PROCESSOR_TIMING_DATA.items()):
            sources = len(data.get('sources', []))
            tests = len(data.get('timing_tests', []))
            print(f"  {name:15} - {data.get('full_name', 'Unknown'):25} ({sources} sources, {tests} tests)")
        print(f"\nTotal: {len(PROCESSOR_TIMING_DATA)} processors")
        return
    
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Path does not exist: {repo_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("TIMING DATA POPULATION TOOL")
    print("=" * 60)
    print(f"Repository: {repo_path}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'APPLY CHANGES'}")
    print(f"Database: {len(PROCESSOR_TIMING_DATA)} processors with timing data")
    print()
    
    if args.processor:
        # Single processor mode
        timing_data = get_timing_data(args.processor)
        if not timing_data:
            print(f"No timing data available for: {args.processor}")
            print("Use --list-available to see available processors")
            return
        
        # Find the validation file
        for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
            json_path = repo_path / family / args.processor / 'validation' / f'{args.processor}_validation.json'
            if json_path.exists():
                updated, changes = update_validation_json(json_path, timing_data, args.dry_run)
                if updated:
                    print(f"{'Would update' if args.dry_run else 'Updated'}: {args.processor}")
                    for c in changes:
                        print(f"  - {c}")
                else:
                    print(f"No changes needed for: {args.processor}")
                return
        
        print(f"Validation file not found for: {args.processor}")
        return
    
    # Full repository mode
    results = populate_repository(repo_path, args.dry_run)
    
    print("RESULTS")
    print("-" * 40)
    print(f"Files checked: {results['files_checked']}")
    print(f"Files updated: {results['files_updated']}")
    print(f"Files skipped (no data): {results['files_skipped']}")
    print()
    
    if results['updated']:
        print("UPDATED PROCESSORS:")
        for item in results['updated']:
            print(f"\n  📄 {item['processor']}")
            for c in item['changes']:
                print(f"      - {c}")
    
    if results['no_data']:
        print(f"\nNO TIMING DATA AVAILABLE FOR ({len(results['no_data'])} processors):")
        for name in results['no_data'][:20]:
            print(f"  - {name}")
        if len(results['no_data']) > 20:
            print(f"  ... and {len(results['no_data']) - 20} more")
    
    print()
    print("=" * 60)
    if args.dry_run:
        print("DRY RUN - No files were modified")
        print("Run without --dry-run to apply changes")
    else:
        print("DONE")
    print("=" * 60)


if __name__ == '__main__':
    main()
