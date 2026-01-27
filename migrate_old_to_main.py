#!/usr/bin/env python3
"""
Modeling_2026 Migration Script
==============================
Migrates content from the 'old' directory to the main repository structure.

This script:
1. Identifies processors in 'old' that are missing from main directories
2. Converts old-style naming to new standardized naming
3. Restructures files into current/archive/validation/docs format
4. Preserves historical documentation
5. Updates the master index.json

Usage:
    python migrate_old_to_main.py [--dry-run] [--repo-path /path/to/repo]
    
    --dry-run     Show what would be done without making changes
    --repo-path   Path to the Modeling_2026 repository (default: current directory)
"""

import os
import sys
import json
import shutil
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

# Mapping of processor names to their target family directories
FAMILY_MAPPING = {
    # Intel processors
    'intel': ['4004', '4040', '8008', '8048', '8051', '8080', '8085', '8086', '8088',
              '80186', '80188', '80286', '80287', '80386', '80387', '8748', '8751',
              'iapx', 'i860', '80486', 'pentium'],
    # Motorola processors
    'motorola': ['6800', '6801', '6802', '6805', '6809', '68000', '68008', '68010',
                 '68020', '68030', '68040', '68060', '68881', '68882', '68hc'],
    # MOS/WDC processors
    'mos_wdc': ['6502', '6510', '65c02', '65816', 'mos', 'wdc'],
    # Zilog processors
    'zilog': ['z80', 'z180', 'z8', 'z8000', 'z80000'],
    # Other processors (default)
    'other': ['arm', 'sparc', 'mips', 'r2000', 'r3000', 'am29000', 'am2901', 'am2903',
              'ns32', 'alpha', 'ppc', 'powerpc', 'pa-risc', 'transputer', 'rca',
              '1802', '1805', 'f8', 'fairchild', 'signetics', '2650', 'intersil',
              '6100', 'tms', 'novix', 'nc4016', 'rtx', 'harris', 'we32', 't414',
              'inmos', 'sc/mp', 'scmp']
}

# Old directory names to new standardized names
NAME_STANDARDIZATION = {
    'Intel 4004': 'i4004',
    'Intel 4040': 'i4040',
    'Intel 8008': 'i8008',
    'Intel 8048': 'i8048',
    'Intel 8051': 'i8051',
    'Intel 8080': 'i8080',
    'Intel 8085': 'i8085',
    'Intel 8086': 'i8086',
    'Intel 8088': 'i8088',
    'Intel 80186': 'i80186',
    'Intel 80188': 'i80188',
    'Intel 80286': 'i80286',
    'Intel 80287': 'i80287',
    'Intel 80386': 'i80386',
    'Intel 80387': 'i80387',
    'Intel 80486': 'i80486',
    'Intel Pentium': 'pentium',
    'Intel i860': 'i860',
    'Intel 8748': 'i8748',
    'Intel 8751': 'i8751',
    'Intel iAPX 432': 'iapx432',
    'Motorola 6800': 'm6800',
    'Motorola 6801': 'm6801',
    'Motorola 6802': 'm6802',
    'Motorola 6805': 'm6805',
    'Motorola 6809': 'm6809',
    'Motorola 68000': 'm68000',
    'Motorola 68008': 'm68008',
    'Motorola 68010': 'm68010',
    'Motorola 68020': 'm68020',
    'Motorola 68030': 'm68030',
    'Motorola 68040': 'm68040',
    'Motorola 68060': 'm68060',
    'Motorola 68881': 'm68881',
    'Motorola 68882': 'm68882',
    'Motorola 68HC11': 'm68hc11',
    'MOS 6502': 'mos6502',
    'MOS 6510': 'mos6510',
    'WDC 65C02': 'wdc65c02',
    'WDC 65816': 'wdc65816',
    'Zilog Z80': 'z80',
    'Zilog Z80A': 'z80a',
    'Zilog Z80B': 'z80b',
    'Zilog Z180': 'z180',
    'Zilog Z8': 'z8',
    'Zilog Z8000': 'z8000',
    'Zilog Z80000': 'z80000',
    'ARM1': 'arm1',
    'ARM2': 'arm2',
    'ARM3': 'arm3',
    'ARM6': 'arm6',
    'Sun SPARC': 'sparc',
    'SPARC': 'sparc',
    'HP PA-RISC': 'pa_risc',
    'DEC Alpha 21064': 'alpha21064',
    'DEC Alpha': 'alpha21064',
    'AIM PPC 601': 'ppc601',
    'PowerPC 601': 'ppc601',
    'AMD Am29000': 'am29000',
    'AMD Am2901': 'am2901',
    'AMD Am2903': 'am2903',
    'Transputer': 't414',
    'INMOS T414': 't414',
    'MIPS R2000': 'r2000',
    'RCA 1802': 'rca1802',
    'RCA CDP1805': 'rca1805',
    'Fairchild F8': 'f8',
    'Signetics 2650': 'signetics2650',
    'Intersil 6100': 'intersil6100',
    'TI TMS9900': 'tms9900',
    'TI TMS9995': 'tms9995',
    'TI TMS320C10': 'tms320c10',
    'National Semiconductor NS32016': 'ns32016',
    'National Semiconductor NS32032': 'ns32032',
    'NS32016': 'ns32016',
    'NS32032': 'ns32032',
    'National SC/MP': 'scmp',
    'Novix NC4016': 'nc4016',
    'Harris RTX2000': 'rtx2000',
    'WE 32000': 'we32000',
}

# Historical documentation files to preserve
HISTORICAL_DOCS = [
    'Modeling_2026_Master_Prompt.docx',
    'Modeling_2026_Recreation_Guide_v2.docx',
    'Pre1986_CPU_Modeling_Lessons_Learned.docx',
    'METHODOLOGY.md',
    'PROCESSOR_EVOLUTION_1971-1985.md',
    'PROJECT_STATUS.md',
    'CHANGELOG.md',
    'CONTRIBUTING.md',
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def standardize_name(old_name: str) -> str:
    """Convert old-style processor name to standardized format."""
    # Direct mapping first
    if old_name in NAME_STANDARDIZATION:
        return NAME_STANDARDIZATION[old_name]
    
    # Try to match partial names
    for old, new in NAME_STANDARDIZATION.items():
        if old.lower() in old_name.lower() or old_name.lower() in old.lower():
            return new
    
    # Fallback: lowercase, replace spaces with underscores
    return old_name.lower().replace(' ', '_').replace('-', '_')


def determine_family(processor_name: str) -> str:
    """Determine which family directory a processor belongs to."""
    name_lower = processor_name.lower()
    
    for family, keywords in FAMILY_MAPPING.items():
        for keyword in keywords:
            if keyword in name_lower:
                return family
    
    return 'other'


def find_old_directories(repo_path: Path) -> Dict[str, Path]:
    """Find all processor directories in the old structure."""
    old_dirs = {}
    old_base = repo_path / 'old'
    
    if not old_base.exists():
        print(f"Warning: 'old' directory not found at {old_base}")
        return old_dirs
    
    # Check both era-based subdirectories
    for era_dir in ['CPU Models - through 1985', 'CPU Models - after 1985', 
                    'CPU Models - after 1985 - in process']:
        era_path = old_base / era_dir
        if era_path.exists():
            for item in era_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    old_dirs[item.name] = item
    
    # Also check direct subdirectories of old/
    for item in old_base.iterdir():
        if item.is_dir() and not item.name.startswith('.') and 'CPU Models' not in item.name:
            old_dirs[item.name] = item
    
    return old_dirs


def find_existing_processors(repo_path: Path) -> Dict[str, Path]:
    """Find all processors already in the main directory structure."""
    existing = {}
    
    for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
        family_path = repo_path / family
        if family_path.exists():
            for item in family_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    existing[item.name] = item
    
    return existing


def load_index(repo_path: Path) -> dict:
    """Load the existing index.json or create a new one."""
    index_path = repo_path / 'index.json'
    
    if index_path.exists():
        with open(index_path, 'r') as f:
            return json.load(f)
    
    return {
        "project": "Modeling_2026",
        "total_processors": 0,
        "families": {
            "intel": 0,
            "motorola": 0,
            "mos_wdc": 0,
            "zilog": 0,
            "other": 0
        },
        "processors": {}
    }


def save_index(repo_path: Path, index: dict):
    """Save the updated index.json."""
    index_path = repo_path / 'index.json'
    
    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2, sort_keys=True)


def create_readme(processor_name: str, std_name: str, family: str, source_path: Path) -> str:
    """Generate a README.md for the migrated processor."""
    # Try to extract info from existing docs
    description = f"{processor_name} Grey-Box Queueing Model"
    
    for readme_name in ['README.md', 'PROCESSOR_README.md', 'QUICK_START.md']:
        readme_path = source_path / readme_name
        if readme_path.exists():
            with open(readme_path, 'r', errors='ignore') as f:
                content = f.read()
                # Extract first paragraph as description
                paragraphs = content.split('\n\n')
                for p in paragraphs:
                    if len(p) > 50 and not p.startswith('#'):
                        description = p[:500].strip()
                        break
    
    return f"""# {processor_name}

## Overview

{description}

## Directory Structure

```
{std_name}/
├── README.md                    # This file
├── current/
│   └── {std_name}_validated.py  # Current validated model
├── archive/                     # Previous model versions
├── validation/
│   └── {std_name}_validation.json  # Validation data
└── docs/                        # Additional documentation
```

## Usage

```python
from {std_name}_validated import {std_name.upper().replace('_', '')}Model

model = {std_name.upper().replace('_', '')}Model()
result = model.analyze('typical')

print(f"IPC: {{result.ipc:.4f}}")
print(f"CPI: {{result.cpi:.2f}}")
print(f"Bottleneck: {{result.bottleneck}}")
```

## Migration Info

- **Migrated from**: `old/{source_path.name}`
- **Migration date**: {datetime.now().strftime('%Y-%m-%d')}
- **Family**: {family}

## Validation Status

⚠️ **MIGRATED** - Validation should be re-run after migration.

"""


def migrate_processor(old_path: Path, new_path: Path, processor_name: str, 
                      std_name: str, family: str, dry_run: bool = False) -> bool:
    """Migrate a single processor from old structure to new structure."""
    
    if dry_run:
        print(f"  [DRY RUN] Would migrate: {processor_name}")
        print(f"    From: {old_path}")
        print(f"    To:   {new_path}")
        return True
    
    try:
        # Create directory structure
        (new_path / 'current').mkdir(parents=True, exist_ok=True)
        (new_path / 'archive').mkdir(exist_ok=True)
        (new_path / 'validation').mkdir(exist_ok=True)
        (new_path / 'docs').mkdir(exist_ok=True)
        
        # Copy and rename Python files
        py_files = list(old_path.glob('*.py'))
        for py_file in py_files:
            # Determine if this is the main model file
            if 'model' in py_file.name.lower():
                new_name = f"{std_name}_validated.py"
                dest = new_path / 'current' / new_name
            else:
                dest = new_path / 'archive' / py_file.name
            
            shutil.copy2(py_file, dest)
            print(f"    Copied: {py_file.name} -> {dest.relative_to(new_path)}")
        
        # Copy JSON files to validation/
        json_files = list(old_path.glob('*.json'))
        for json_file in json_files:
            new_name = f"{std_name}_validation.json" if 'model' in json_file.name.lower() else json_file.name
            dest = new_path / 'validation' / new_name
            shutil.copy2(json_file, dest)
            print(f"    Copied: {json_file.name} -> {dest.relative_to(new_path)}")
        
        # Copy documentation to docs/
        doc_files = list(old_path.glob('*.md')) + list(old_path.glob('*.txt'))
        for doc_file in doc_files:
            dest = new_path / 'docs' / doc_file.name
            shutil.copy2(doc_file, dest)
            print(f"    Copied: {doc_file.name} -> {dest.relative_to(new_path)}")
        
        # Generate new README
        readme_content = create_readme(processor_name, std_name, family, old_path)
        readme_path = new_path / 'README.md'
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        print(f"    Created: README.md")
        
        return True
        
    except Exception as e:
        print(f"    ERROR: {e}")
        return False


def preserve_historical_docs(repo_path: Path, dry_run: bool = False):
    """Copy historical documentation to a preserved location."""
    old_base = repo_path / 'old'
    archive_path = repo_path / 'docs' / 'historical'
    
    if dry_run:
        print(f"\n[DRY RUN] Would preserve historical docs to: {archive_path}")
        return
    
    archive_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\nPreserving historical documentation to: {archive_path}")
    
    for doc_name in HISTORICAL_DOCS:
        doc_path = old_base / doc_name
        if doc_path.exists():
            dest = archive_path / doc_name
            shutil.copy2(doc_path, dest)
            print(f"  Preserved: {doc_name}")
    
    # Also check for zip files
    for zip_file in old_base.glob('*.zip'):
        dest = archive_path / zip_file.name
        shutil.copy2(zip_file, dest)
        print(f"  Preserved: {zip_file.name}")


# =============================================================================
# MAIN MIGRATION LOGIC
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Migrate processors from old/ to main directory structure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be done without making changes')
    parser.add_argument('--repo-path', type=str, default='.',
                        help='Path to the Modeling_2026 repository')
    parser.add_argument('--force', action='store_true',
                        help='Overwrite existing processors')
    parser.add_argument('--only', type=str, nargs='+',
                        help='Only migrate specific processors')
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    print("=" * 70)
    print("Modeling_2026 Migration Script")
    print("=" * 70)
    print(f"\nRepository path: {repo_path}")
    print(f"Dry run: {args.dry_run}")
    print(f"Force overwrite: {args.force}")
    
    # Validate repository structure
    if not (repo_path / 'old').exists():
        print(f"\nERROR: 'old' directory not found at {repo_path / 'old'}")
        print("Please run this script from the repository root or specify --repo-path")
        sys.exit(1)
    
    # Find processors
    print("\n" + "-" * 70)
    print("STEP 1: Discovering processors")
    print("-" * 70)
    
    old_processors = find_old_directories(repo_path)
    existing_processors = find_existing_processors(repo_path)
    
    print(f"\nFound {len(old_processors)} processors in old/")
    print(f"Found {len(existing_processors)} processors in main directories")
    
    # Determine what needs to be migrated
    print("\n" + "-" * 70)
    print("STEP 2: Analyzing migration candidates")
    print("-" * 70)
    
    to_migrate = []
    to_update = []
    skipped = []
    
    for old_name, old_path in old_processors.items():
        std_name = standardize_name(old_name)
        family = determine_family(old_name)
        
        # Apply --only filter if specified
        if args.only and std_name not in args.only and old_name not in args.only:
            continue
        
        if std_name in existing_processors:
            if args.force:
                to_update.append((old_name, old_path, std_name, family))
            else:
                skipped.append((old_name, std_name, 'already exists'))
        else:
            to_migrate.append((old_name, old_path, std_name, family))
    
    # Report findings
    print(f"\nTo migrate (new): {len(to_migrate)}")
    for old_name, _, std_name, family in to_migrate:
        print(f"  • {old_name} -> {family}/{std_name}")
    
    if to_update:
        print(f"\nTo update (--force): {len(to_update)}")
        for old_name, _, std_name, family in to_update:
            print(f"  • {old_name} -> {family}/{std_name}")
    
    if skipped:
        print(f"\nSkipped (already exist): {len(skipped)}")
        for old_name, std_name, reason in skipped:
            print(f"  • {old_name} ({std_name}): {reason}")
    
    # Perform migration
    print("\n" + "-" * 70)
    print("STEP 3: Migrating processors")
    print("-" * 70)
    
    index = load_index(repo_path)
    success_count = 0
    fail_count = 0
    
    all_migrations = to_migrate + to_update
    
    if not all_migrations:
        print("\nNo processors to migrate.")
    else:
        for old_name, old_path, std_name, family in all_migrations:
            print(f"\nMigrating: {old_name}")
            new_path = repo_path / family / std_name
            
            success = migrate_processor(
                old_path, new_path, old_name, std_name, family, 
                dry_run=args.dry_run
            )
            
            if success:
                success_count += 1
                if not args.dry_run:
                    # Update index
                    index['processors'][std_name] = old_name
                    index['families'][family] = index['families'].get(family, 0) + 1
            else:
                fail_count += 1
    
    # Preserve historical documentation
    print("\n" + "-" * 70)
    print("STEP 4: Preserving historical documentation")
    print("-" * 70)
    
    preserve_historical_docs(repo_path, dry_run=args.dry_run)
    
    # Update and save index
    if not args.dry_run and success_count > 0:
        print("\n" + "-" * 70)
        print("STEP 5: Updating index.json")
        print("-" * 70)
        
        index['total_processors'] = len(index['processors'])
        save_index(repo_path, index)
        print(f"Updated index.json with {index['total_processors']} processors")
    
    # Summary
    print("\n" + "=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)
    print(f"\nSuccessfully migrated: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Skipped: {len(skipped)}")
    
    if args.dry_run:
        print("\n⚠️  This was a DRY RUN. No changes were made.")
        print("   Run without --dry-run to perform the actual migration.")
    else:
        print("\n✅ Migration complete!")
        print("\nNext steps:")
        print("  1. Review the migrated files")
        print("  2. Run validation tests on migrated models")
        print("  3. Commit the changes to git")
        print("  4. Consider removing or archiving the old/ directory")


if __name__ == '__main__':
    main()
