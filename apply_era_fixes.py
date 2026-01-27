#!/usr/bin/env python3
"""
Apply Era-Specific Architecture Fixes for Modeling_2026
=======================================================

This script updates processor models to use the correct architectural
pattern for their era. It can:

1. Generate new model files using era-appropriate templates
2. Add missing era-specific features to existing models
3. Create architecture documentation

Usage:
    python apply_era_fixes.py [repo_path] [options]

Options:
    --dry-run       Show what would change without making changes
    --processor X   Fix only processor X
    --era ERA       Fix only processors of specified era
    --generate-all  Generate template files for all processors

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import re
import json
import shutil
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime

from era_architectures import (
    ProcessorEra,
    ERA_DEFINITIONS,
    PROCESSOR_ERA_MAP,
    get_processor_era,
    get_era_definition,
    ERA_TEMPLATES,
    SequentialArchitecture,
    PrefetchQueueArchitecture,
    PipelinedArchitecture,
    CacheRISCArchitecture,
)

from era_architecture_audit import (
    run_era_audit,
    EraAuditReport,
    ProcessorArchitectureAudit,
)


# =============================================================================
# PROCESSOR SPECIFICATIONS DATABASE
# =============================================================================

# Default specifications for processors (used when generating templates)
PROCESSOR_SPECS = {
    # Intel Sequential
    'i4004': {'year': 1971, 'clock': 0.74, 'transistors': 2300, 'data': 4, 'addr': 12, 'mfr': 'Intel'},
    'i4040': {'year': 1974, 'clock': 0.74, 'transistors': 3000, 'data': 4, 'addr': 12, 'mfr': 'Intel'},
    'i8008': {'year': 1972, 'clock': 0.5, 'transistors': 3500, 'data': 8, 'addr': 14, 'mfr': 'Intel'},
    'i8080': {'year': 1974, 'clock': 2.0, 'transistors': 4500, 'data': 8, 'addr': 16, 'mfr': 'Intel'},
    'i8085': {'year': 1976, 'clock': 3.0, 'transistors': 6500, 'data': 8, 'addr': 16, 'mfr': 'Intel'},
    
    # Intel Prefetch Queue
    'i8086': {'year': 1978, 'clock': 5.0, 'transistors': 29000, 'data': 16, 'addr': 20, 'mfr': 'Intel',
              'bus_width': 16, 'queue_size': 6},
    'i8088': {'year': 1979, 'clock': 5.0, 'transistors': 29000, 'data': 16, 'addr': 20, 'mfr': 'Intel',
              'bus_width': 8, 'queue_size': 4},
    'i80186': {'year': 1982, 'clock': 6.0, 'transistors': 55000, 'data': 16, 'addr': 20, 'mfr': 'Intel',
               'bus_width': 16, 'queue_size': 6},
    
    # Intel Pipelined
    'i80286': {'year': 1982, 'clock': 6.0, 'transistors': 134000, 'data': 16, 'addr': 24, 'mfr': 'Intel',
               'pipeline_stages': 4},
    
    # Intel Cache/RISC
    'i80386': {'year': 1985, 'clock': 16.0, 'transistors': 275000, 'data': 32, 'addr': 32, 'mfr': 'Intel',
               'pipeline_depth': 5, 'icache_kb': 0, 'dcache_kb': 0},
    
    # Motorola Sequential
    'm6800': {'year': 1974, 'clock': 1.0, 'transistors': 4100, 'data': 8, 'addr': 16, 'mfr': 'Motorola'},
    'm6802': {'year': 1977, 'clock': 1.0, 'transistors': 5000, 'data': 8, 'addr': 16, 'mfr': 'Motorola'},
    
    # Motorola Prefetch
    'm6809': {'year': 1978, 'clock': 1.0, 'transistors': 9000, 'data': 8, 'addr': 16, 'mfr': 'Motorola',
              'bus_width': 8, 'queue_size': 2},
    
    # Motorola Pipelined
    'm68000': {'year': 1979, 'clock': 8.0, 'transistors': 68000, 'data': 16, 'addr': 24, 'mfr': 'Motorola',
               'pipeline_stages': 3},
    'm68010': {'year': 1982, 'clock': 10.0, 'transistors': 84000, 'data': 16, 'addr': 24, 'mfr': 'Motorola',
               'pipeline_stages': 4},
    'm68020': {'year': 1984, 'clock': 16.0, 'transistors': 190000, 'data': 32, 'addr': 32, 'mfr': 'Motorola',
               'pipeline_stages': 5, 'icache_kb': 0.256},
    
    # MOS/WDC Sequential
    'mos6502': {'year': 1975, 'clock': 1.0, 'transistors': 3510, 'data': 8, 'addr': 16, 'mfr': 'MOS Technology'},
    'mos6510': {'year': 1982, 'clock': 1.0, 'transistors': 3510, 'data': 8, 'addr': 16, 'mfr': 'MOS Technology'},
    'wdc65c02': {'year': 1983, 'clock': 2.0, 'transistors': 4000, 'data': 8, 'addr': 16, 'mfr': 'WDC'},
    
    # Zilog
    'z80': {'year': 1976, 'clock': 2.5, 'transistors': 8500, 'data': 8, 'addr': 16, 'mfr': 'Zilog',
            'bus_width': 8, 'queue_size': 0},  # Limited prefetch
    'z8000': {'year': 1979, 'clock': 4.0, 'transistors': 17500, 'data': 16, 'addr': 16, 'mfr': 'Zilog',
              'bus_width': 16, 'queue_size': 4},
    
    # RISC processors
    'arm1': {'year': 1985, 'clock': 6.0, 'transistors': 25000, 'data': 32, 'addr': 26, 'mfr': 'Acorn',
             'pipeline_depth': 3, 'icache_kb': 0, 'delayed_branch': False},
    'mips_r2000': {'year': 1985, 'clock': 8.0, 'transistors': 110000, 'data': 32, 'addr': 32, 'mfr': 'MIPS',
                   'pipeline_depth': 5, 'icache_kb': 4, 'dcache_kb': 4, 'delayed_branch': True},
    'sparc': {'year': 1987, 'clock': 14.0, 'transistors': 80000, 'data': 32, 'addr': 32, 'mfr': 'Sun',
              'pipeline_depth': 4, 'icache_kb': 4, 'dcache_kb': 4, 'delayed_branch': True, 'register_windows': 8},
    'am29000': {'year': 1988, 'clock': 25.0, 'transistors': 120000, 'data': 32, 'addr': 32, 'mfr': 'AMD',
                'pipeline_depth': 4, 'icache_kb': 8, 'delayed_branch': True},
}


# =============================================================================
# TEMPLATE CUSTOMIZATION
# =============================================================================

def get_default_timing(era: ProcessorEra, processor: str) -> Dict[str, Any]:
    """Get default timing parameters for an era"""
    
    if era == ProcessorEra.SEQUENTIAL:
        return {
            'FetchCycles': 4,
            'DecodeCycles': 1,
            'ExecuteCycles': 3,
            'MemoryCycles': 3,
            'WritebackCycles': 0,
            'RegOpsCycles': 4,
            'ImmediateCycles': 7,
            'MemReadCycles': 7, 'MemReadMem': 3,
            'MemWriteCycles': 7, 'MemWriteMem': 3,
            'BranchCycles': 10,
            'CallRetCycles': 12, 'CallRetMem': 6,
        }
    
    elif era == ProcessorEra.PREFETCH_QUEUE:
        return {
            'BusCycleTime': 4,
            'RegOpsCycles': 2,
            'ImmediateCycles': 4,
            'MemReadCycles': 8, 'MemReadBus': 4,
            'MemWriteCycles': 8, 'MemWriteBus': 4,
            'BranchCycles': 15,
            'StringCycles': 9, 'StringBus': 4,
            'AvgInstLength': 3.0,
        }
    
    elif era == ProcessorEra.PIPELINED:
        return {
            'IFCycles': 1,
            'IDCycles': 1,
            'OFCycles': 1,
            'EXCycles': 1,
            'WBCycles': 1,
            'HasICache': False,
            'ICacheHitRate': 0.95,
            'ICacheMissPenalty': 10,
            'ALURegCycles': 2,
            'ALUMemCycles': 4, 'ALUMemMem': 2,
            'LoadCycles': 4, 'LoadMem': 2,
            'StoreCycles': 4, 'StoreMem': 2,
            'BranchCycles': 6,
            'MultiplyCycles': 20,
            'DivideCycles': 50,
        }
    
    else:  # CACHE_RISC
        return {
            'PipelineDepth': 5,
            'ICacheSize': 4,
            'ICacheHitRate': 0.95,
            'DCacheSize': 4,
            'DCacheHitRate': 0.90,
            'MemoryLatency': 10,
            'HasDelayedBranch': False,
            'BranchPenalty': 2,
            'LoadLatency': 1,
            'MultiplyCycles': 10,
            'DivideCycles': 30,
            'FPSingleCycles': 3,
            'FPDoubleCycles': 6,
        }


def customize_template(template: str, processor: str, family: str, specs: Dict) -> str:
    """Customize a template with processor-specific values"""
    
    era = get_processor_era(processor)
    timing = get_default_timing(era, processor)
    
    # Get processor specs or use defaults
    proc_specs = PROCESSOR_SPECS.get(processor, {})
    
    # Build class name
    class_name = ''.join(word.title() for word in processor.replace('_', ' ').split())
    
    # Build replacements
    replacements = {
        '{ClassName}': class_name,
        '{ProcessorName}': processor.upper(),
        '{Manufacturer}': proc_specs.get('mfr', family.title()),
        '{Year}': str(proc_specs.get('year', 1980)),
        '{ClockMHz}': str(proc_specs.get('clock', 1.0)),
        '{Transistors}': str(proc_specs.get('transistors', 10000)),
        '{DataWidth}': str(proc_specs.get('data', 8)),
        '{AddressWidth}': str(proc_specs.get('addr', 16)),
    }
    
    # Era-specific replacements
    if era == ProcessorEra.PREFETCH_QUEUE:
        replacements['{BusWidth}'] = str(proc_specs.get('bus_width', 16))
        replacements['{QueueSize}'] = str(proc_specs.get('queue_size', 6))
    
    if era in [ProcessorEra.PIPELINED, ProcessorEra.CACHE_RISC]:
        replacements['{NumStages}'] = str(proc_specs.get('pipeline_stages', 5))
        replacements['{PipelineDepth}'] = str(proc_specs.get('pipeline_depth', 5))
    
    if era == ProcessorEra.CACHE_RISC:
        replacements['{ICacheSize}'] = str(proc_specs.get('icache_kb', 4))
        replacements['{DCacheSize}'] = str(proc_specs.get('dcache_kb', 4))
        replacements['{CacheInfo}'] = f"{proc_specs.get('icache_kb', 4)}KB I-cache"
        replacements['{DCacheInfo}'] = f"{proc_specs.get('dcache_kb', 0)}KB D-cache" if proc_specs.get('dcache_kb', 0) > 0 else "No D-cache"
        replacements['{BranchInfo}'] = "Delayed branches" if proc_specs.get('delayed_branch', False) else "Standard branches"
        replacements['{HasDelayedBranch}'] = str(proc_specs.get('delayed_branch', False))
    
    # Add timing parameters
    for key, value in timing.items():
        replacements['{' + key + '}'] = str(value)
    
    # Apply replacements
    result = template
    for old, new in replacements.items():
        result = result.replace(old, new)
    
    return result


def generate_model_file(processor: str, family: str, output_path: Path) -> bool:
    """Generate a model file for a processor"""
    
    era = get_processor_era(processor)
    if not era:
        print(f"  Warning: Unknown era for {processor}, defaulting to SEQUENTIAL")
        era = ProcessorEra.SEQUENTIAL
    
    template = ERA_TEMPLATES.get(era)
    if not template:
        print(f"  Error: No template for era {era}")
        return False
    
    # Get processor specs
    specs = PROCESSOR_SPECS.get(processor, {})
    
    # Customize template
    content = customize_template(template, processor, family, specs)
    
    # Add header
    era_def = get_era_definition(era)
    header = f'''#!/usr/bin/env python3
"""
{processor.upper()} Grey-Box Queueing Model
{"=" * (len(processor) + 25)}

Architecture: {era_def.name} ({era_def.year_start}-{era_def.year_end})
Queueing Model: {era_def.queueing_model}

Features:
{chr(10).join("  - " + f for f in era_def.architectural_features[:5])}

Generated by era_architecture_fix.py
Date: {datetime.now().strftime("%Y-%m-%d")}

Note: This is a TEMPLATE. Customize timing values based on:
  - Original datasheet specifications
  - Cycle-accurate emulator validation (MAME, VICE, etc.)
  - WikiChip/Wikipedia technical specifications
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional

# Import from common (adjust path as needed)
try:
    from common.base_model import BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult
except ImportError:
    # Fallback definitions if common not available
    from dataclasses import dataclass
    
    @dataclass
    class InstructionCategory:
        name: str
        base_cycles: float
        memory_cycles: float = 0
        description: str = ""
        @property
        def total_cycles(self): return self.base_cycles + self.memory_cycles
    
    @dataclass
    class WorkloadProfile:
        name: str
        category_weights: Dict[str, float]
        description: str = ""
    
    @dataclass
    class AnalysisResult:
        processor: str
        workload: str
        ipc: float
        cpi: float
        ips: float
        bottleneck: str
        utilizations: Dict[str, float]
        
        @classmethod
        def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations):
            ipc = 1.0 / cpi
            ips = clock_mhz * 1e6 * ipc
            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations)
    
    class BaseProcessorModel:
        pass

'''
    
    full_content = header + content
    
    # Write file
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        return True
    except Exception as e:
        print(f"  Error writing file: {e}")
        return False


def generate_era_documentation(processor: str, family: str, output_path: Path) -> bool:
    """Generate architecture documentation for a processor"""
    
    era = get_processor_era(processor)
    if not era:
        return False
    
    era_def = get_era_definition(era)
    specs = PROCESSOR_SPECS.get(processor, {})
    
    # Format transistor count with commas if it's a number
    transistors = specs.get('transistors', 'Unknown')
    if isinstance(transistors, (int, float)):
        transistors_str = f"{transistors:,}"
    else:
        transistors_str = str(transistors)
    
    content = f'''# {processor.upper()} Architectural Documentation

## Era Classification

**Era:** {era_def.name}  
**Period:** {era_def.year_start}-{era_def.year_end}  
**Queueing Model:** {era_def.queueing_model}

## Architectural Features

{chr(10).join("- " + f for f in era_def.architectural_features)}

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | {specs.get('mfr', family.title())} |
| Year | {specs.get('year', 'Unknown')} |
| Clock | {specs.get('clock', 'Unknown')} MHz |
| Transistors | {transistors_str} |
| Data Width | {specs.get('data', 8)}-bit |
| Address Width | {specs.get('addr', 16)}-bit |

## Queueing Model Architecture

'''
    
    # Add era-specific architecture diagram
    if era == ProcessorEra.SEQUENTIAL:
        content += '''
```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  FETCH  │──►│ DECODE  │──►│ EXECUTE │──►│ MEMORY  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘
    │              │              │              │
    ▼              ▼              ▼              ▼
  M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue

CPI = Fetch + Decode + Execute + Memory (serial sum)
```
'''
    
    elif era == ProcessorEra.PREFETCH_QUEUE:
        content += '''
```
┌─────────────────────────────────────────┐
│              Bus Interface Unit (BIU)    │
│  ┌──────────┐    ┌──────────────────┐  │
│  │  Memory  │───►│  Prefetch Queue  │  │
│  │  Access  │    │  (4-6 bytes)     │  │
│  └──────────┘    └────────┬─────────┘  │
└───────────────────────────┼────────────┘
                            │
                            ▼
┌─────────────────────────────────────────┐
│            Execution Unit (EU)           │
│  ┌──────────┐    ┌──────────────────┐  │
│  │  Decode  │───►│     Execute      │  │
│  └──────────┘    └──────────────────┘  │
└─────────────────────────────────────────┘

BIU and EU operate in PARALLEL
CPI = max(BIU_time, EU_time) + contention + stalls
```
'''
    
    elif era == ProcessorEra.PIPELINED:
        content += '''
```
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│  IF  │─►│  ID  │─►│  OF  │─►│  EX  │─►│  WB  │
└──────┘  └──────┘  └──────┘  └──────┘  └──────┘
   │         │         │         │         │
   I1        I1        I1        I1        I1
             I2        I2        I2        I2
                       I3        I3        I3
                                 I4        I4
                                           I5

Ideal CPI = 1.0 (one instruction per cycle)
Actual CPI = 1.0 + hazards + stalls + cache_misses
```
'''
    
    else:  # CACHE_RISC
        content += '''
```
                    ┌────────────┐
                    │  I-Cache   │
                    └─────┬──────┘
                          │
┌──────┐  ┌──────┐  ┌─────▼────┐  ┌──────┐  ┌──────┐
│  IF  │─►│  ID  │─►│    EX    │─►│  MEM │─►│  WB  │
└──────┘  └──────┘  └──────────┘  └──┬───┘  └──────┘
                                     │
                               ┌─────▼──────┐
                               │  D-Cache   │
                               └────────────┘

RISC Goal: CPI ≈ 1.0
Actual CPI = 1.0 + cache_misses + hazards + branch_penalties
```
'''
    
    content += f'''
## Model Implementation Notes

1. This processor uses the **{era_def.name}** architectural template
2. Key modeling considerations:
   - {era_def.description}

## Validation Approach

- Compare against original {specs.get('mfr', 'manufacturer')} datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/{family}/{processor})
- [Wikipedia](https://en.wikipedia.org/wiki/{processor.replace("_", " ")})

---
Generated: {datetime.now().strftime("%Y-%m-%d")}
'''
    
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"  Error writing documentation: {e}")
        return False


# =============================================================================
# FIX APPLICATION
# =============================================================================

class EraFixApplicator:
    """Applies era-specific architecture fixes"""
    
    def __init__(self, repo_path: Path, dry_run: bool = False, backup: bool = True):
        self.repo_path = repo_path
        self.dry_run = dry_run
        self.backup = backup
        self.changes: List[str] = []
        self.errors: List[str] = []
    
    def log(self, message: str):
        prefix = "[DRY-RUN] " if self.dry_run else ""
        print(f"{prefix}{message}")
        self.changes.append(message)
    
    def backup_file(self, path: Path):
        if not self.backup or not path.exists():
            return
        
        backup_path = path.with_suffix(path.suffix + '.era_backup')
        if not self.dry_run:
            shutil.copy2(path, backup_path)
        self.log(f"  Backed up: {path.name}")
    
    def fix_processor(self, processor: str, family: str, proc_path: Path) -> bool:
        """Fix a single processor's architecture"""
        
        era = get_processor_era(processor)
        if not era:
            self.errors.append(f"{family}/{processor}: Unknown era")
            return False
        
        era_def = get_era_definition(era)
        self.log(f"\nFixing {family}/{processor} ({era_def.name})")
        
        # Ensure directory structure
        current_path = proc_path / 'current'
        docs_path = proc_path / 'docs'
        
        if not self.dry_run:
            current_path.mkdir(parents=True, exist_ok=True)
            docs_path.mkdir(parents=True, exist_ok=True)
        
        # Check for existing model
        py_files = list(current_path.glob('*_validated.py')) if current_path.exists() else []
        
        if py_files:
            # Backup existing
            self.backup_file(py_files[0])
        
        # Generate new model file
        model_path = current_path / f'{processor}_validated.py'
        self.log(f"  Generating model: {model_path.relative_to(self.repo_path)}")
        
        if not self.dry_run:
            if not generate_model_file(processor, family, model_path):
                self.errors.append(f"{family}/{processor}: Failed to generate model")
                return False
        
        # Generate documentation
        doc_path = docs_path / f'{processor}_architecture.md'
        self.log(f"  Generating docs: {doc_path.relative_to(self.repo_path)}")
        
        if not self.dry_run:
            generate_era_documentation(processor, family, doc_path)
        
        return True
    
    def fix_all_mismatched(self, report: EraAuditReport) -> int:
        """Fix all processors with architecture mismatches"""
        
        fixes = 0
        mismatched = [a for a in report.audits 
                     if a.detected_era != a.expected_era or not a.detected_era]
        
        for audit in mismatched:
            if self.fix_processor(audit.processor, audit.family, audit.path):
                fixes += 1
        
        return fixes
    
    def generate_all_templates(self) -> int:
        """Generate template files for all known processors"""
        
        fixes = 0
        families = ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']
        
        for family in families:
            family_path = self.repo_path / family
            if not family_path.exists():
                continue
            
            for proc_dir in family_path.iterdir():
                if proc_dir.is_dir() and not proc_dir.name.startswith('.'):
                    processor = proc_dir.name
                    if self.fix_processor(processor, family, proc_dir):
                        fixes += 1
        
        return fixes


def main():
    parser = argparse.ArgumentParser(
        description='Apply Era-Specific Architecture Fixes'
    )
    parser.add_argument(
        'repo_path',
        nargs='?',
        default='.',
        help='Path to Modeling_2026 repository'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would change without making changes'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create backups'
    )
    parser.add_argument(
        '--processor', '-p',
        help='Fix only specified processor'
    )
    parser.add_argument(
        '--era', '-e',
        choices=['sequential', 'prefetch_queue', 'pipelined', 'cache_risc'],
        help='Fix only processors of specified era'
    )
    parser.add_argument(
        '--fix-mismatched',
        action='store_true',
        help='Fix only processors with detected mismatches'
    )
    parser.add_argument(
        '--generate-all',
        action='store_true',
        help='Generate templates for all processors'
    )
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    applicator = EraFixApplicator(
        repo_path,
        dry_run=args.dry_run,
        backup=not args.no_backup
    )
    
    print("=" * 60)
    print("ERA-SPECIFIC ARCHITECTURE FIX")
    print("=" * 60)
    print(f"Repository: {repo_path}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'APPLY CHANGES'}")
    print("")
    
    fixes = 0
    
    if args.generate_all:
        print("Generating templates for ALL processors...")
        fixes = applicator.generate_all_templates()
    
    elif args.fix_mismatched:
        print("Running audit to find mismatches...")
        report = run_era_audit(repo_path)
        print(f"Found {report.mismatched + report.undetected} processors needing fixes")
        fixes = applicator.fix_all_mismatched(report)
    
    elif args.processor:
        # Find the processor
        for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
            proc_path = repo_path / family / args.processor
            if proc_path.exists():
                if applicator.fix_processor(args.processor, family, proc_path):
                    fixes = 1
                break
        else:
            print(f"Processor not found: {args.processor}")
            sys.exit(1)
    
    else:
        print("No action specified. Use one of:")
        print("  --generate-all     Generate templates for all processors")
        print("  --fix-mismatched   Fix processors with architecture mismatches")
        print("  --processor X      Fix specific processor X")
        sys.exit(0)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Processors fixed: {fixes}")
    print(f"Changes made: {len(applicator.changes)}")
    
    if applicator.errors:
        print(f"\nErrors: {len(applicator.errors)}")
        for error in applicator.errors:
            print(f"  - {error}")
    
    if args.dry_run:
        print("\n*** DRY RUN - No actual changes were made ***")
        print("Run without --dry-run to apply changes")


if __name__ == '__main__':
    main()
