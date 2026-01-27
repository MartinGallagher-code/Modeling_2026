#!/usr/bin/env python3
"""
Apply Consistency Fixes for Modeling_2026
==========================================

This script applies fixes identified by cross_family_audit.py:

1. Creates missing directories (current/, validation/, docs/, archive/)
2. Generates README templates
3. Generates validation JSON templates
4. Creates base model class in common/
5. Adds method stubs to incomplete models

Usage:
    python apply_consistency_fixes.py [repo_path] [options]

Options:
    --dry-run       Show what would change without making changes
    --fix-all       Apply all available fixes
    --fix-structure Create missing directories
    --fix-readme    Generate missing README files
    --fix-json      Generate missing validation JSON files
    --fix-base      Create/update common/base_model.py
    --fix-stubs     Add method stubs to incomplete models

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

EXPECTED_FAMILIES = ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']
EXPECTED_SUBDIRS = ['current', 'archive', 'validation', 'docs']


# =============================================================================
# TEMPLATE GENERATORS
# =============================================================================

def generate_readme_template(processor_name: str, family: str) -> str:
    """Generate README.md template for a processor"""
    return f'''# {processor_name.upper()} Grey-Box Queueing Model

## Overview

| Property | Value |
|----------|-------|
| **Manufacturer** | {family.title()} |
| **Architecture** | TODO |
| **Year** | TODO |
| **Clock Speed** | TODO MHz |
| **Transistors** | TODO |

## Model Description

This model implements a grey-box queueing network for the {processor_name.upper()} processor.

## File Structure

| File | Description |
|------|-------------|
| `current/{processor_name}_validated.py` | Current validated model |
| `validation/{processor_name}_validation.json` | Validation data and results |
| `docs/` | Additional documentation |
| `archive/` | Previous model versions |

## Usage

```python
from {processor_name}_validated import {processor_name.title().replace("_", "")}Model

model = {processor_name.title().replace("_", "")}Model()
result = model.analyze(workload='typical')
print(f"IPC: {{result.ipc:.3f}}")
```

## Validation Status

- [ ] Datasheet timing verified
- [ ] Emulator comparison (MAME/VICE)
- [ ] Cross-validation with other models
- [ ] IPC error < 5%

## Category-Based Timing

This model uses category-based timing with weighted averages rather than
exhaustive instruction enumeration. Categories should be limited to 5-15
for optimal accuracy and maintainability.

## References

- Original datasheet: TODO
- WikiChip: TODO
- Wikipedia: TODO

---
Generated: {datetime.now().strftime("%Y-%m-%d")}
'''


def generate_validation_json_template(processor_name: str, family: str) -> dict:
    """Generate validation JSON template"""
    return {
        "processor": processor_name,
        "family": family,
        "validation_date": datetime.now().strftime("%Y-%m-%d"),
        "model_version": "1.0.0",
        "sources": [
            {
                "type": "datasheet",
                "name": f"{processor_name.upper()} Datasheet",
                "url": "TODO",
                "verified": False
            },
            {
                "type": "wikichip",
                "name": "WikiChip",
                "url": f"https://en.wikichip.org/wiki/{family}/{processor_name}",
                "verified": False
            }
        ],
        "timing_tests": [],
        "accuracy": {
            "ipc_error_percent": None,
            "cpi_error_percent": None,
            "validated_workloads": [],
            "notes": "Validation pending"
        },
        "instruction_categories": {
            "count": 0,
            "list": []
        },
        "workload_profiles": {
            "available": [],
            "validated": []
        }
    }


def generate_base_model_template() -> str:
    """Generate common/base_model.py template"""
    return '''#!/usr/bin/env python3
"""
Base Model Classes for Modeling_2026
=====================================

Provides common interfaces and data classes for all processor models.

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class InstructionCategory:
    """Represents an instruction category with timing information"""
    name: str
    base_cycles: float
    memory_cycles: float = 0
    description: str = ""
    frequency: float = 0.0  # Fraction of instructions in this category
    
    @property
    def total_cycles(self) -> float:
        return self.base_cycles + self.memory_cycles


@dataclass
class WorkloadProfile:
    """Represents a workload with instruction category weights"""
    name: str
    category_weights: Dict[str, float]
    description: str = ""
    
    def validate(self) -> bool:
        """Check that weights sum to 1.0"""
        total = sum(self.category_weights.values())
        return abs(total - 1.0) < 0.01


@dataclass
class AnalysisResult:
    """Results from model analysis"""
    processor: str
    workload: str
    ipc: float
    cpi: float
    ips: float
    bottleneck: str
    utilizations: Dict[str, float] = field(default_factory=dict)
    stage_details: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_cpi(cls, processor: str, workload: str, cpi: float, 
                 clock_mhz: float, bottleneck: str, 
                 utilizations: Dict[str, float] = None):
        """Create result from CPI value"""
        ipc = 1.0 / cpi
        ips = clock_mhz * 1e6 * ipc
        return cls(
            processor=processor,
            workload=workload,
            ipc=ipc,
            cpi=cpi,
            ips=ips,
            bottleneck=bottleneck,
            utilizations=utilizations or {}
        )


class BaseProcessorModel(ABC):
    """
    Abstract base class for all processor models.
    
    All processor models should inherit from this class and implement
    the required methods.
    """
    
    # Required class attributes (override in subclass)
    name: str = "Unknown"
    manufacturer: str = "Unknown"
    year: int = 0
    clock_mhz: float = 1.0
    transistor_count: int = 0
    
    @abstractmethod
    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """
        Analyze processor performance for a given workload.
        
        Args:
            workload: Name of workload profile ('typical', 'compute', 'memory', 'control')
            
        Returns:
            AnalysisResult with IPC, CPI, IPS, and bottleneck information
        """
        pass
    
    @abstractmethod
    def validate(self) -> Dict[str, Any]:
        """
        Run validation tests against known data.
        
        Returns:
            Dictionary with validation results including:
            - tests: List of test results
            - passed: Number of tests passed
            - total: Total number of tests
            - accuracy_percent: Overall accuracy
        """
        pass
    
    @abstractmethod
    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        """
        Get all instruction categories with timing.
        
        Returns:
            Dictionary mapping category name to InstructionCategory
        """
        pass
    
    @abstractmethod
    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        """
        Get all available workload profiles.
        
        Returns:
            Dictionary mapping profile name to WorkloadProfile
        """
        pass
    
    def summary(self) -> str:
        """Return a summary string for the processor"""
        return f"{self.name} ({self.manufacturer}, {self.year}) @ {self.clock_mhz} MHz"


# Convenience function for creating models
def create_model(family: str, processor: str):
    """
    Factory function to create a processor model.
    
    Args:
        family: Processor family ('intel', 'motorola', etc.)
        processor: Processor name ('i8086', 'm68000', etc.)
        
    Returns:
        Instantiated processor model
    """
    # This would be implemented with dynamic imports
    raise NotImplementedError("Use direct imports for now")
'''


def generate_method_stubs() -> str:
    """Generate method stub code to add to incomplete models"""
    return '''
    # =========================================================================
    # REQUIRED INTERFACE METHODS (stubs - implement these)
    # =========================================================================
    
    def analyze(self, workload: str = 'typical') -> 'AnalysisResult':
        """Analyze processor performance for a given workload."""
        # TODO: Implement analysis
        raise NotImplementedError("analyze() not implemented")
    
    def validate(self) -> Dict[str, Any]:
        """Run validation tests against known data."""
        # TODO: Implement validation
        return {
            "tests": [],
            "passed": 0,
            "total": 0,
            "accuracy_percent": None
        }
    
    def get_instruction_categories(self) -> Dict[str, 'InstructionCategory']:
        """Get all instruction categories with timing."""
        # TODO: Implement instruction categories
        return {}
    
    def get_workload_profiles(self) -> Dict[str, 'WorkloadProfile']:
        """Get all available workload profiles."""
        # TODO: Implement workload profiles
        return {}
'''


# =============================================================================
# FIX APPLICATORS
# =============================================================================

class FixApplicator:
    """Applies fixes to the repository"""
    
    def __init__(self, repo_path: Path, dry_run: bool = False, backup: bool = True):
        self.repo_path = repo_path
        self.dry_run = dry_run
        self.backup = backup
        self.changes: List[str] = []
    
    def log(self, message: str):
        """Log a change"""
        prefix = "[DRY-RUN] " if self.dry_run else ""
        print(f"{prefix}{message}")
        self.changes.append(message)
    
    def create_directory(self, path: Path):
        """Create a directory if it doesn't exist"""
        if not path.exists():
            self.log(f"Creating directory: {path.relative_to(self.repo_path)}")
            if not self.dry_run:
                path.mkdir(parents=True, exist_ok=True)
    
    def write_file(self, path: Path, content: str):
        """Write content to a file"""
        self.log(f"Writing file: {path.relative_to(self.repo_path)}")
        if not self.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    def write_json(self, path: Path, data: dict):
        """Write JSON to a file"""
        self.log(f"Writing JSON: {path.relative_to(self.repo_path)}")
        if not self.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
    
    def backup_file(self, path: Path):
        """Create a backup of a file"""
        if not self.backup or not path.exists():
            return
        
        backup_path = path.with_suffix(path.suffix + '.backup')
        self.log(f"Backing up: {path.name} -> {backup_path.name}")
        if not self.dry_run:
            shutil.copy2(path, backup_path)
    
    def fix_structure(self):
        """Create missing directory structure"""
        print("\n=== Fixing Directory Structure ===")
        
        for family in EXPECTED_FAMILIES:
            family_path = self.repo_path / family
            self.create_directory(family_path)
            
            if family_path.exists():
                for item in family_path.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        for subdir in EXPECTED_SUBDIRS:
                            self.create_directory(item / subdir)
    
    def fix_readme(self):
        """Generate missing README files"""
        print("\n=== Generating README Files ===")
        
        for family in EXPECTED_FAMILIES:
            family_path = self.repo_path / family
            if not family_path.exists():
                continue
            
            for item in family_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    readme_path = item / 'README.md'
                    if not readme_path.exists():
                        content = generate_readme_template(item.name, family)
                        self.write_file(readme_path, content)
    
    def fix_validation_json(self):
        """Generate missing validation JSON files"""
        print("\n=== Generating Validation JSON Files ===")
        
        for family in EXPECTED_FAMILIES:
            family_path = self.repo_path / family
            if not family_path.exists():
                continue
            
            for item in family_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    validation_dir = item / 'validation'
                    json_path = validation_dir / f'{item.name}_validation.json'
                    
                    if not json_path.exists():
                        self.create_directory(validation_dir)
                        data = generate_validation_json_template(item.name, family)
                        self.write_json(json_path, data)
    
    def fix_base_model(self):
        """Create/update common/base_model.py"""
        print("\n=== Creating Base Model ===")
        
        common_path = self.repo_path / 'common'
        self.create_directory(common_path)
        
        base_model_path = common_path / 'base_model.py'
        init_path = common_path / '__init__.py'
        
        if base_model_path.exists():
            self.backup_file(base_model_path)
        
        self.write_file(base_model_path, generate_base_model_template())
        
        if not init_path.exists():
            self.write_file(init_path, '"""Common utilities for Modeling_2026"""\n\nfrom .base_model import *\n')
    
    def fix_init_files(self):
        """Create __init__.py files"""
        print("\n=== Creating __init__.py Files ===")
        
        for family in EXPECTED_FAMILIES:
            family_path = self.repo_path / family
            if not family_path.exists():
                continue
            
            init_path = family_path / '__init__.py'
            if not init_path.exists():
                processors = []
                for item in family_path.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        processors.append(item.name)
                
                content = f'"""{family.title()} processor family"""\n\n'
                content += f'PROCESSORS = {processors}\n'
                self.write_file(init_path, content)
    
    def fix_index(self):
        """Create/update index.json"""
        print("\n=== Creating Index ===")
        
        index = {
            "name": "Modeling_2026",
            "description": "Grey-box queueing models for historical microprocessors",
            "version": "1.0.0",
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "families": {}
        }
        
        for family in EXPECTED_FAMILIES:
            family_path = self.repo_path / family
            if not family_path.exists():
                continue
            
            processors = []
            for item in sorted(family_path.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    processors.append({
                        "name": item.name,
                        "path": f"{family}/{item.name}",
                        "has_model": (item / 'current').exists(),
                        "has_validation": (item / 'validation').exists()
                    })
            
            if processors:
                index["families"][family] = {
                    "count": len(processors),
                    "processors": processors
                }
        
        self.write_json(self.repo_path / 'index.json', index)
    
    def fix_all(self):
        """Apply all fixes"""
        self.fix_structure()
        self.fix_readme()
        self.fix_validation_json()
        self.fix_base_model()
        self.fix_init_files()
        self.fix_index()


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Apply Consistency Fixes for Modeling_2026'
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
        help='Do not create backups of modified files'
    )
    parser.add_argument(
        '--fix-all',
        action='store_true',
        help='Apply all available fixes'
    )
    parser.add_argument(
        '--fix-structure',
        action='store_true',
        help='Create missing directories'
    )
    parser.add_argument(
        '--fix-readme',
        action='store_true',
        help='Generate missing README files'
    )
    parser.add_argument(
        '--fix-json',
        action='store_true',
        help='Generate missing validation JSON files'
    )
    parser.add_argument(
        '--fix-base',
        action='store_true',
        help='Create/update common/base_model.py'
    )
    parser.add_argument(
        '--fix-stubs',
        action='store_true',
        help='Add method stubs to incomplete models'
    )
    parser.add_argument(
        '--fix-init',
        action='store_true',
        help='Create __init__.py files'
    )
    parser.add_argument(
        '--fix-index',
        action='store_true',
        help='Create/update index.json'
    )
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Path does not exist: {repo_path}")
        sys.exit(1)
    
    applicator = FixApplicator(
        repo_path,
        dry_run=args.dry_run,
        backup=not args.no_backup
    )
    
    print("=" * 60)
    print("CONSISTENCY FIX APPLICATION")
    print("=" * 60)
    print(f"Repository: {repo_path}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'APPLY CHANGES'}")
    
    # Determine which fixes to apply
    if args.fix_all:
        applicator.fix_all()
    else:
        any_fix = False
        
        if args.fix_structure:
            applicator.fix_structure()
            any_fix = True
        
        if args.fix_readme:
            applicator.fix_readme()
            any_fix = True
        
        if args.fix_json:
            applicator.fix_validation_json()
            any_fix = True
        
        if args.fix_base:
            applicator.fix_base_model()
            any_fix = True
        
        if args.fix_init:
            applicator.fix_init_files()
            any_fix = True
        
        if args.fix_index:
            applicator.fix_index()
            any_fix = True
        
        if not any_fix:
            print("\nNo fixes specified. Use --fix-all or specific --fix-* options.")
            print("\nAvailable options:")
            print("  --fix-all        Apply all fixes")
            print("  --fix-structure  Create missing directories")
            print("  --fix-readme     Generate missing README files")
            print("  --fix-json       Generate missing validation JSON files")
            print("  --fix-base       Create common/base_model.py")
            print("  --fix-init       Create __init__.py files")
            print("  --fix-index      Create index.json")
            sys.exit(0)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Changes {'proposed' if args.dry_run else 'made'}: {len(applicator.changes)}")
    
    if args.dry_run:
        print("\n*** DRY RUN - No actual changes were made ***")
        print("Run without --dry-run to apply changes")


if __name__ == '__main__':
    main()
