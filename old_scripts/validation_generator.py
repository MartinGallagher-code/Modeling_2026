#!/usr/bin/env python3
"""
Validation Data Generator for Modeling_2026
=============================================

This script generates and populates validation JSON files with:

1. Standard validation JSON templates
2. Known processor specifications from database
3. Standard timing test templates
4. Source URL templates for datasheets, WikiChip, etc.

Usage:
    python validation_generator.py [repo_path] [options]

Options:
    --generate-all      Generate validation files for all processors
    --processor NAME    Generate for specific processor
    --family NAME       Generate for specific family
    --update-sources    Add missing source URLs to existing files
    --dry-run           Show what would change without making changes

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple


# =============================================================================
# PROCESSOR SPECIFICATIONS DATABASE
# =============================================================================

PROCESSOR_SPECS = {
    # Intel Family
    'i4004': {
        'full_name': 'Intel 4004',
        'manufacturer': 'Intel',
        'year': 1971,
        'clock_mhz': 0.74,
        'transistors': 2300,
        'data_bits': 4,
        'address_bits': 12,
        'architecture': 'sequential',
        'datasheet_url': 'http://datasheets.chipdb.org/Intel/MCS-4/datashts/intel-4004.pdf',
        'wikichip_url': 'https://en.wikichip.org/wiki/intel/mcs-4/4004',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Intel_4004',
        'emulator': None,
        'typical_cpi': 10.8,
    },
    'i4040': {
        'full_name': 'Intel 4040',
        'manufacturer': 'Intel',
        'year': 1974,
        'clock_mhz': 0.74,
        'transistors': 3000,
        'data_bits': 4,
        'address_bits': 12,
        'architecture': 'sequential',
        'datasheet_url': 'http://datasheets.chipdb.org/Intel/MCS-4/datashts/intel-4040.pdf',
        'wikichip_url': 'https://en.wikichip.org/wiki/intel/mcs-4/4040',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Intel_4040',
    },
    'i8008': {
        'full_name': 'Intel 8008',
        'manufacturer': 'Intel',
        'year': 1972,
        'clock_mhz': 0.5,
        'transistors': 3500,
        'data_bits': 8,
        'address_bits': 14,
        'architecture': 'sequential',
        'datasheet_url': 'http://datasheets.chipdb.org/Intel/MCS-8/intel-8008.pdf',
        'wikichip_url': 'https://en.wikichip.org/wiki/intel/mcs-8/8008',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Intel_8008',
        'typical_cpi': 11.0,
    },
    'i8080': {
        'full_name': 'Intel 8080',
        'manufacturer': 'Intel',
        'year': 1974,
        'clock_mhz': 2.0,
        'transistors': 4500,
        'data_bits': 8,
        'address_bits': 16,
        'architecture': 'sequential',
        'datasheet_url': 'http://datasheets.chipdb.org/Intel/MCS-80/intel-8080.pdf',
        'wikichip_url': 'https://en.wikichip.org/wiki/intel/mcs-80/8080',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Intel_8080',
        'emulator': 'MAME',
        'mame_driver': 'i8080',
        'typical_cpi': 9.2,
    },
    'i8085': {
        'full_name': 'Intel 8085',
        'manufacturer': 'Intel',
        'year': 1976,
        'clock_mhz': 3.0,
        'transistors': 6500,
        'data_bits': 8,
        'address_bits': 16,
        'architecture': 'sequential',
        'datasheet_url': 'http://datasheets.chipdb.org/Intel/MCS-85/intel-8085.pdf',
        'wikichip_url': 'https://en.wikichip.org/wiki/intel/mcs-85/8085',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Intel_8085',
        'emulator': 'MAME',
        'typical_cpi': 5.5,
    },
    'i8086': {
        'full_name': 'Intel 8086',
        'manufacturer': 'Intel',
        'year': 1978,
        'clock_mhz': 5.0,
        'transistors': 29000,
        'data_bits': 16,
        'address_bits': 20,
        'architecture': 'prefetch_queue',
        'datasheet_url': 'http://datasheets.chipdb.org/Intel/x86/808x/datashts/8086.pdf',
        'wikichip_url': 'https://en.wikichip.org/wiki/intel/8086',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Intel_8086',
        'emulator': 'DOSBox',
        'mame_driver': 'i8086',
        'typical_cpi': 4.5,
    },
    'i8088': {
        'full_name': 'Intel 8088',
        'manufacturer': 'Intel',
        'year': 1979,
        'clock_mhz': 5.0,
        'transistors': 29000,
        'data_bits': 16,
        'address_bits': 20,
        'architecture': 'prefetch_queue',
        'datasheet_url': 'http://datasheets.chipdb.org/Intel/x86/808x/datashts/8088.pdf',
        'wikichip_url': 'https://en.wikichip.org/wiki/intel/8088',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Intel_8088',
        'emulator': 'DOSBox',
        'notes': 'IBM PC original CPU, 8-bit external bus',
        'typical_cpi': 5.2,
    },
    'i80186': {
        'full_name': 'Intel 80186',
        'manufacturer': 'Intel',
        'year': 1982,
        'clock_mhz': 6.0,
        'transistors': 55000,
        'data_bits': 16,
        'address_bits': 20,
        'architecture': 'prefetch_queue',
        'wikichip_url': 'https://en.wikichip.org/wiki/intel/80186',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Intel_80186',
    },
    'i80286': {
        'full_name': 'Intel 80286',
        'manufacturer': 'Intel',
        'year': 1982,
        'clock_mhz': 6.0,
        'transistors': 134000,
        'data_bits': 16,
        'address_bits': 24,
        'architecture': 'pipelined',
        'datasheet_url': 'http://datasheets.chipdb.org/Intel/x86/286/datashts/intel-80286.pdf',
        'wikichip_url': 'https://en.wikichip.org/wiki/intel/80286',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Intel_80286',
        'emulator': 'DOSBox',
        'typical_cpi': 4.0,
    },
    'i80386': {
        'full_name': 'Intel 80386',
        'manufacturer': 'Intel',
        'year': 1985,
        'clock_mhz': 16.0,
        'transistors': 275000,
        'data_bits': 32,
        'address_bits': 32,
        'architecture': 'cache_risc',
        'datasheet_url': 'http://datasheets.chipdb.org/Intel/x86/386/datashts/intel-80386.pdf',
        'wikichip_url': 'https://en.wikichip.org/wiki/intel/80386',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Intel_80386',
        'emulator': 'DOSBox-X',
        'typical_cpi': 4.5,
    },
    
    # Motorola Family
    'm6800': {
        'full_name': 'Motorola 6800',
        'manufacturer': 'Motorola',
        'year': 1974,
        'clock_mhz': 1.0,
        'transistors': 4100,
        'data_bits': 8,
        'address_bits': 16,
        'architecture': 'sequential',
        'datasheet_url': 'http://www.bitsavers.org/components/motorola/6800/MC6800_8-Bit_Microprocessor_Data_Sheet.pdf',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Motorola_6800',
        'emulator': 'MAME',
        'typical_cpi': 4.0,
    },
    'm6809': {
        'full_name': 'Motorola 6809',
        'manufacturer': 'Motorola',
        'year': 1978,
        'clock_mhz': 1.0,
        'transistors': 9000,
        'data_bits': 8,
        'address_bits': 16,
        'architecture': 'prefetch_queue',
        'datasheet_url': 'http://www.bitsavers.org/components/motorola/6809/MC6809_Datasheet.pdf',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Motorola_6809',
        'emulator': 'MAME',
        'typical_cpi': 3.5,
    },
    'm68000': {
        'full_name': 'Motorola 68000',
        'manufacturer': 'Motorola',
        'year': 1979,
        'clock_mhz': 8.0,
        'transistors': 68000,
        'data_bits': 16,
        'address_bits': 24,
        'architecture': 'pipelined',
        'datasheet_url': 'http://www.bitsavers.org/components/motorola/68000/MC68000_Users_Manual.pdf',
        'wikichip_url': 'https://en.wikichip.org/wiki/motorola/68000',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Motorola_68000',
        'emulator': 'MAME',
        'mame_driver': 'm68000',
        'typical_cpi': 6.5,
    },
    'm68020': {
        'full_name': 'Motorola 68020',
        'manufacturer': 'Motorola',
        'year': 1984,
        'clock_mhz': 16.0,
        'transistors': 190000,
        'data_bits': 32,
        'address_bits': 32,
        'architecture': 'pipelined',
        'datasheet_url': 'http://www.bitsavers.org/components/motorola/68000/MC68020_Users_Manual.pdf',
        'wikichip_url': 'https://en.wikichip.org/wiki/motorola/68020',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Motorola_68020',
        'emulator': 'MAME',
        'typical_cpi': 3.5,
    },
    
    # MOS/WDC Family
    'mos6502': {
        'full_name': 'MOS Technology 6502',
        'manufacturer': 'MOS Technology',
        'year': 1975,
        'clock_mhz': 1.0,
        'transistors': 3510,
        'data_bits': 8,
        'address_bits': 16,
        'architecture': 'sequential',
        'datasheet_url': 'http://archive.6502.org/datasheets/mos_6500_mpu_preliminary_may_1976.pdf',
        'wikichip_url': 'https://en.wikichip.org/wiki/mos_technology/6502',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/MOS_Technology_6502',
        'emulator': 'VICE',
        'mame_driver': 'm6502',
        'typical_cpi': 3.5,
        'notes': 'Apple II, Commodore 64, NES CPU',
    },
    'mos6510': {
        'full_name': 'MOS Technology 6510',
        'manufacturer': 'MOS Technology',
        'year': 1982,
        'clock_mhz': 1.0,
        'transistors': 3510,
        'data_bits': 8,
        'address_bits': 16,
        'architecture': 'sequential',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/MOS_Technology_6510',
        'emulator': 'VICE',
        'typical_cpi': 3.5,
        'notes': 'Commodore 64 CPU',
    },
    'wdc65c02': {
        'full_name': 'WDC 65C02',
        'manufacturer': 'Western Design Center',
        'year': 1983,
        'clock_mhz': 2.0,
        'transistors': 4000,
        'data_bits': 8,
        'address_bits': 16,
        'architecture': 'sequential',
        'datasheet_url': 'https://www.westerndesigncenter.com/wdc/documentation/w65c02s.pdf',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/WDC_65C02',
        'emulator': 'MAME',
        'typical_cpi': 3.2,
    },
    'wdc65816': {
        'full_name': 'WDC 65816',
        'manufacturer': 'Western Design Center',
        'year': 1984,
        'clock_mhz': 2.8,
        'transistors': 22000,
        'data_bits': 16,
        'address_bits': 24,
        'architecture': 'prefetch_queue',
        'datasheet_url': 'https://www.westerndesigncenter.com/wdc/documentation/w65c816s.pdf',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/WDC_65816',
        'emulator': 'MAME',
        'notes': 'Apple IIGS, Super Nintendo CPU',
        'typical_cpi': 3.8,
    },
    
    # Zilog Family
    'z80': {
        'full_name': 'Zilog Z80',
        'manufacturer': 'Zilog',
        'year': 1976,
        'clock_mhz': 2.5,
        'transistors': 8500,
        'data_bits': 8,
        'address_bits': 16,
        'architecture': 'prefetch_queue',
        'datasheet_url': 'http://www.z80.info/zip/z80.pdf',
        'wikichip_url': 'https://en.wikichip.org/wiki/zilog/z80',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Zilog_Z80',
        'emulator': 'MAME',
        'mame_driver': 'z80',
        'typical_cpi': 5.5,
        'notes': 'Most popular 8-bit CPU ever',
    },
    'z8000': {
        'full_name': 'Zilog Z8000',
        'manufacturer': 'Zilog',
        'year': 1979,
        'clock_mhz': 4.0,
        'transistors': 17500,
        'data_bits': 16,
        'address_bits': 16,
        'architecture': 'prefetch_queue',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Zilog_Z8000',
        'typical_cpi': 4.5,
    },
    
    # ARM Family
    'arm1': {
        'full_name': 'ARM1',
        'manufacturer': 'Acorn',
        'year': 1985,
        'clock_mhz': 6.0,
        'transistors': 25000,
        'data_bits': 32,
        'address_bits': 26,
        'architecture': 'cache_risc',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/ARM_architecture',
        'wikichip_url': 'https://en.wikichip.org/wiki/acorn/microarchitectures/arm1',
        'typical_cpi': 1.8,
        'notes': 'First ARM processor',
    },
    
    # SPARC
    'sparc': {
        'full_name': 'SPARC',
        'manufacturer': 'Sun Microsystems',
        'year': 1987,
        'clock_mhz': 14.0,
        'transistors': 80000,
        'data_bits': 32,
        'address_bits': 32,
        'architecture': 'cache_risc',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/SPARC',
        'wikichip_url': 'https://en.wikichip.org/wiki/sun/sparc',
        'typical_cpi': 1.5,
    },
    
    # MIPS
    'mips_r2000': {
        'full_name': 'MIPS R2000',
        'manufacturer': 'MIPS Computer Systems',
        'year': 1985,
        'clock_mhz': 8.0,
        'transistors': 110000,
        'data_bits': 32,
        'address_bits': 32,
        'architecture': 'cache_risc',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/R2000_(microprocessor)',
        'wikichip_url': 'https://en.wikichip.org/wiki/mips/r2000',
        'typical_cpi': 1.2,
    },
    
    # AMD
    'am2901': {
        'full_name': 'AMD Am2901',
        'manufacturer': 'AMD',
        'year': 1975,
        'clock_mhz': 10.0,
        'transistors': 200,
        'data_bits': 4,
        'address_bits': 4,
        'architecture': 'sequential',
        'datasheet_url': 'http://www.bitsavers.org/components/amd/Am2900/Am2901_Am2901A_Four-Bit_Bipolar_Microprocessor_Slice_May79.pdf',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/AMD_Am2900',
        'notes': '4-bit slice processor',
    },
    'am29000': {
        'full_name': 'AMD Am29000',
        'manufacturer': 'AMD',
        'year': 1988,
        'clock_mhz': 25.0,
        'transistors': 120000,
        'data_bits': 32,
        'address_bits': 32,
        'architecture': 'cache_risc',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/AMD_Am29000',
        'typical_cpi': 1.0,
    },
    
    # Other
    'f8': {
        'full_name': 'Fairchild F8',
        'manufacturer': 'Fairchild',
        'year': 1975,
        'clock_mhz': 2.0,
        'transistors': 3500,
        'data_bits': 8,
        'address_bits': 16,
        'architecture': 'sequential',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Fairchild_F8',
    },
    'rca1802': {
        'full_name': 'RCA CDP1802',
        'manufacturer': 'RCA',
        'year': 1976,
        'clock_mhz': 3.2,
        'transistors': 5000,
        'data_bits': 8,
        'address_bits': 16,
        'architecture': 'sequential',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/RCA_1802',
        'notes': 'Used in Voyager spacecraft',
    },
    'scmp': {
        'full_name': 'National SC/MP',
        'manufacturer': 'National Semiconductor',
        'year': 1974,
        'clock_mhz': 1.0,
        'transistors': 5000,
        'data_bits': 8,
        'address_bits': 16,
        'architecture': 'sequential',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/National_Semiconductor_SC/MP',
    },
    'signetics2650': {
        'full_name': 'Signetics 2650',
        'manufacturer': 'Signetics',
        'year': 1975,
        'clock_mhz': 1.25,
        'transistors': 6000,
        'data_bits': 8,
        'address_bits': 15,
        'architecture': 'sequential',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Signetics_2650',
        'emulator': 'MAME',
    },
    'tms9900': {
        'full_name': 'TI TMS9900',
        'manufacturer': 'Texas Instruments',
        'year': 1976,
        'clock_mhz': 3.0,
        'transistors': 8000,
        'data_bits': 16,
        'address_bits': 15,
        'architecture': 'sequential',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/TMS9900',
        'emulator': 'MAME',
        'notes': 'TI-99/4A CPU',
    },
    'ns32016': {
        'full_name': 'National Semiconductor NS32016',
        'manufacturer': 'National Semiconductor',
        'year': 1982,
        'clock_mhz': 10.0,
        'transistors': 60000,
        'data_bits': 32,
        'address_bits': 24,
        'architecture': 'pipelined',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/NS320xx',
    },
    't414': {
        'full_name': 'INMOS T414',
        'manufacturer': 'INMOS',
        'year': 1985,
        'clock_mhz': 15.0,
        'transistors': 250000,
        'data_bits': 32,
        'address_bits': 32,
        'architecture': 'cache_risc',
        'wikipedia_url': 'https://en.wikipedia.org/wiki/Transputer',
        'notes': 'Transputer with 2KB on-chip RAM',
    },
}


# =============================================================================
# STANDARD TIMING TESTS
# =============================================================================

def get_standard_timing_tests(architecture: str) -> List[Dict[str, Any]]:
    """Get standard timing tests for an architecture type"""
    
    base_tests = [
        {
            'name': 'NOP_timing',
            'category': 'control',
            'description': 'NOP instruction timing',
            'expected_cycles': None,  # To be filled from datasheet
            'source': 'datasheet',
        },
        {
            'name': 'register_move',
            'category': 'data_transfer',
            'description': 'Register to register move',
            'expected_cycles': None,
            'source': 'datasheet',
        },
        {
            'name': 'memory_load',
            'category': 'memory',
            'description': 'Load from memory',
            'expected_cycles': None,
            'source': 'datasheet',
        },
        {
            'name': 'memory_store',
            'category': 'memory',
            'description': 'Store to memory',
            'expected_cycles': None,
            'source': 'datasheet',
        },
        {
            'name': 'add_register',
            'category': 'alu',
            'description': 'Add two registers',
            'expected_cycles': None,
            'source': 'datasheet',
        },
        {
            'name': 'branch_taken',
            'category': 'control',
            'description': 'Conditional branch when taken',
            'expected_cycles': None,
            'source': 'datasheet',
        },
        {
            'name': 'branch_not_taken',
            'category': 'control',
            'description': 'Conditional branch when not taken',
            'expected_cycles': None,
            'source': 'datasheet',
        },
    ]
    
    # Add architecture-specific tests
    if architecture == 'prefetch_queue':
        base_tests.extend([
            {
                'name': 'queue_hit',
                'category': 'prefetch',
                'description': 'Instruction in prefetch queue',
                'expected_cycles': None,
                'source': 'measurement',
            },
            {
                'name': 'queue_miss',
                'category': 'prefetch',
                'description': 'Instruction not in prefetch queue',
                'expected_cycles': None,
                'source': 'measurement',
            },
        ])
    elif architecture == 'pipelined':
        base_tests.extend([
            {
                'name': 'pipeline_stall',
                'category': 'pipeline',
                'description': 'Pipeline stall on hazard',
                'expected_cycles': None,
                'source': 'measurement',
            },
        ])
    elif architecture == 'cache_risc':
        base_tests.extend([
            {
                'name': 'cache_hit',
                'category': 'cache',
                'description': 'L1 cache hit',
                'expected_cycles': 1,
                'source': 'architecture',
            },
            {
                'name': 'cache_miss',
                'category': 'cache',
                'description': 'L1 cache miss',
                'expected_cycles': None,
                'source': 'measurement',
            },
        ])
    
    return base_tests


# =============================================================================
# VALIDATION JSON GENERATION
# =============================================================================

def generate_validation_json(processor_name: str, family: str) -> Dict[str, Any]:
    """Generate a validation JSON file for a processor"""
    
    # Look up specs
    specs = PROCESSOR_SPECS.get(processor_name, {})
    
    # Build sources list
    sources = []
    
    if specs.get('datasheet_url'):
        sources.append({
            'type': 'datasheet',
            'name': f"{specs.get('full_name', processor_name)} Datasheet",
            'url': specs['datasheet_url'],
            'verified': False,
        })
    
    if specs.get('wikichip_url'):
        sources.append({
            'type': 'wikichip',
            'name': 'WikiChip',
            'url': specs['wikichip_url'],
            'verified': False,
        })
    
    if specs.get('wikipedia_url'):
        sources.append({
            'type': 'wikipedia',
            'name': 'Wikipedia',
            'url': specs['wikipedia_url'],
            'verified': False,
        })
    
    if specs.get('emulator'):
        sources.append({
            'type': 'emulator',
            'name': specs['emulator'],
            'url': None,
            'verified': False,
            'notes': f"MAME driver: {specs.get('mame_driver', 'unknown')}" if specs.get('mame_driver') else '',
        })
    
    # If no sources found, add template
    if not sources:
        sources = [
            {
                'type': 'datasheet',
                'name': f'{processor_name.upper()} Datasheet',
                'url': 'TODO',
                'verified': False,
            },
            {
                'type': 'wikichip',
                'name': 'WikiChip',
                'url': f'https://en.wikichip.org/wiki/{family}/{processor_name}',
                'verified': False,
            },
        ]
    
    # Get timing tests
    architecture = specs.get('architecture', 'sequential')
    timing_tests = get_standard_timing_tests(architecture)
    
    # Build validation JSON
    validation = {
        'processor': processor_name,
        'full_name': specs.get('full_name', processor_name.upper()),
        'family': family,
        'manufacturer': specs.get('manufacturer', 'Unknown'),
        'year': specs.get('year'),
        'validation_date': datetime.now().strftime('%Y-%m-%d'),
        'model_version': '1.0.0',
        'architecture': architecture,
        
        'specifications': {
            'clock_mhz': specs.get('clock_mhz'),
            'transistors': specs.get('transistors'),
            'data_bits': specs.get('data_bits'),
            'address_bits': specs.get('address_bits'),
        },
        
        'sources': sources,
        
        'timing_tests': timing_tests,
        
        'accuracy': {
            'ipc_error_percent': None,
            'cpi_error_percent': None,
            'validated_workloads': [],
            'notes': 'Validation pending',
        },
        
        'instruction_categories': {
            'count': 0,
            'list': [],
        },
        
        'workload_profiles': {
            'available': ['typical', 'compute', 'memory', 'control'],
            'validated': [],
        },
        
        'cross_validation': {
            'processors': [],
            'notes': '',
        },
        
        'notes': specs.get('notes', ''),
    }
    
    return validation


def update_sources_in_json(json_path: Path, processor_name: str) -> Tuple[bool, List[str]]:
    """Update sources in an existing validation JSON"""
    changes = []
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return False, [f"Failed to read: {e}"]
    
    specs = PROCESSOR_SPECS.get(processor_name, {})
    existing_urls = {s.get('url') for s in data.get('sources', []) if s.get('url')}
    
    # Add missing sources
    sources = data.get('sources', [])
    
    if specs.get('datasheet_url') and specs['datasheet_url'] not in existing_urls:
        sources.append({
            'type': 'datasheet',
            'name': f"{specs.get('full_name', processor_name)} Datasheet",
            'url': specs['datasheet_url'],
            'verified': False,
        })
        changes.append(f"Added datasheet source")
    
    if specs.get('wikichip_url') and specs['wikichip_url'] not in existing_urls:
        sources.append({
            'type': 'wikichip',
            'name': 'WikiChip',
            'url': specs['wikichip_url'],
            'verified': False,
        })
        changes.append(f"Added WikiChip source")
    
    if changes:
        data['sources'] = sources
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    return True, changes


# =============================================================================
# MAIN
# =============================================================================

class ValidationGenerator:
    """Generates validation files for processors"""
    
    def __init__(self, repo_path: Path, dry_run: bool = False):
        self.repo_path = repo_path
        self.dry_run = dry_run
        self.changes = []
    
    def log(self, message: str):
        prefix = "[DRY-RUN] " if self.dry_run else ""
        print(f"{prefix}{message}")
        self.changes.append(message)
    
    def generate_for_processor(self, processor_path: Path, processor_name: str, family: str):
        """Generate validation files for a single processor"""
        validation_dir = processor_path / 'validation'
        json_path = validation_dir / f'{processor_name}_validation.json'
        
        if json_path.exists():
            self.log(f"Skipping {family}/{processor_name} - validation JSON exists")
            return
        
        self.log(f"Generating validation for {family}/{processor_name}")
        
        if not self.dry_run:
            validation_dir.mkdir(parents=True, exist_ok=True)
            data = generate_validation_json(processor_name, family)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
    
    def generate_for_family(self, family: str):
        """Generate validation files for all processors in a family"""
        family_path = self.repo_path / family
        
        if not family_path.exists():
            self.log(f"Family directory not found: {family}")
            return
        
        for item in sorted(family_path.iterdir()):
            if item.is_dir() and not item.name.startswith('.'):
                self.generate_for_processor(item, item.name, family)
    
    def generate_all(self):
        """Generate validation files for all processors"""
        families = ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']
        for family in families:
            self.generate_for_family(family)
    
    def update_sources_all(self):
        """Update sources in all existing validation files"""
        families = ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']
        
        for family in families:
            family_path = self.repo_path / family
            if not family_path.exists():
                continue
            
            for item in sorted(family_path.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    validation_dir = item / 'validation'
                    json_files = list(validation_dir.glob('*_validation.json')) if validation_dir.exists() else []
                    
                    for json_path in json_files:
                        if not self.dry_run:
                            success, changes = update_sources_in_json(json_path, item.name)
                            if changes:
                                self.log(f"Updated {family}/{item.name}: {', '.join(changes)}")


def main():
    parser = argparse.ArgumentParser(
        description='Validation Data Generator for Modeling_2026'
    )
    parser.add_argument(
        'repo_path',
        nargs='?',
        default='.',
        help='Path to Modeling_2026 repository'
    )
    parser.add_argument(
        '--generate-all',
        action='store_true',
        help='Generate validation files for all processors'
    )
    parser.add_argument(
        '--processor',
        help='Generate for specific processor'
    )
    parser.add_argument(
        '--family',
        help='Generate for specific family'
    )
    parser.add_argument(
        '--update-sources',
        action='store_true',
        help='Add missing source URLs to existing files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would change without making changes'
    )
    parser.add_argument(
        '--list-specs',
        action='store_true',
        help='List all processors in specification database'
    )
    
    args = parser.parse_args()
    
    if args.list_specs:
        print("Processors in specification database:")
        print("-" * 50)
        for name, specs in sorted(PROCESSOR_SPECS.items()):
            sources = []
            if specs.get('datasheet_url'):
                sources.append('datasheet')
            if specs.get('wikichip_url'):
                sources.append('wikichip')
            if specs.get('emulator'):
                sources.append(specs['emulator'].lower())
            print(f"  {name:20} {specs.get('full_name', ''):25} [{', '.join(sources)}]")
        return
    
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Path does not exist: {repo_path}")
        sys.exit(1)
    
    generator = ValidationGenerator(repo_path, args.dry_run)
    
    print("=" * 60)
    print("VALIDATION DATA GENERATOR")
    print("=" * 60)
    print(f"Repository: {repo_path}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'APPLY CHANGES'}")
    print("")
    
    if args.generate_all:
        generator.generate_all()
    elif args.family:
        generator.generate_for_family(args.family)
    elif args.processor:
        # Find processor path
        for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
            proc_path = repo_path / family / args.processor
            if proc_path.exists():
                generator.generate_for_processor(proc_path, args.processor, family)
                break
        else:
            print(f"Processor not found: {args.processor}")
    elif args.update_sources:
        generator.update_sources_all()
    else:
        print("No action specified. Use --generate-all, --family, --processor, or --update-sources")
        return
    
    print("")
    print("=" * 60)
    print(f"Changes {'proposed' if args.dry_run else 'made'}: {len(generator.changes)}")
    print("=" * 60)


if __name__ == '__main__':
    main()
