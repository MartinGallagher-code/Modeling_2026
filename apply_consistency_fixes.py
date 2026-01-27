#!/usr/bin/env python3
"""
Apply Consistency Fixes for Modeling_2026 Repository
====================================================

This script applies fixes identified by cross_family_audit.py.
It can:
1. Create missing directory structures
2. Generate README templates
3. Generate validation JSON templates  
4. Create/update base model classes
5. Add missing method stubs to existing models
6. Standardize class naming

Usage:
    python apply_consistency_fixes.py [repo_path] [options]
    
Options:
    --dry-run       Show what would be changed without making changes
    --backup        Create backups before modifying files
    --fix-all       Apply all available fixes
    --fix-structure Create missing directories
    --fix-readme    Generate missing READMEs
    --fix-json      Generate missing validation JSONs
    --fix-base      Create/update base model class
    --fix-stubs     Add method stubs to models missing required methods

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import json
import re
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# Import from audit script
from cross_family_audit import (
    run_audit, 
    AuditReport,
    ProcessorAudit,
    EXPECTED_FAMILIES,
    EXPECTED_SUBDIRS,
    REQUIRED_METHODS,
    STANDARD_WORKLOADS,
    MAX_RECOMMENDED_CATEGORIES,
    generate_readme_template,
    generate_validation_json_template,
    generate_base_model_class,
    generate_method_stubs,
)


class FixApplicator:
    """Applies fixes to the repository"""
    
    def __init__(self, repo_path: Path, dry_run: bool = False, backup: bool = True):
        self.repo_path = repo_path
        self.dry_run = dry_run
        self.backup = backup
        self.changes_made: List[str] = []
        self.errors: List[str] = []
        
    def log(self, message: str):
        """Log a change"""
        prefix = "[DRY-RUN] " if self.dry_run else ""
        print(f"{prefix}{message}")
        self.changes_made.append(message)
    
    def log_error(self, message: str):
        """Log an error"""
        print(f"ERROR: {message}")
        self.errors.append(message)
    
    def backup_file(self, path: Path) -> Optional[Path]:
        """Create backup of file before modification"""
        if not self.backup or not path.exists():
            return None
        
        backup_path = path.with_suffix(path.suffix + '.backup')
        counter = 1
        while backup_path.exists():
            backup_path = path.with_suffix(f'{path.suffix}.backup{counter}')
            counter += 1
        
        if not self.dry_run:
            shutil.copy2(path, backup_path)
        
        self.log(f"  Backed up: {path} -> {backup_path}")
        return backup_path
    
    def create_directory(self, path: Path) -> bool:
        """Create directory if it doesn't exist"""
        if path.exists():
            return True
        
        self.log(f"  Creating directory: {path.relative_to(self.repo_path)}")
        
        if not self.dry_run:
            try:
                path.mkdir(parents=True, exist_ok=True)
                return True
            except Exception as e:
                self.log_error(f"Failed to create {path}: {e}")
                return False
        return True
    
    def write_file(self, path: Path, content: str) -> bool:
        """Write content to file"""
        self.log(f"  Writing file: {path.relative_to(self.repo_path)}")
        
        if not self.dry_run:
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            except Exception as e:
                self.log_error(f"Failed to write {path}: {e}")
                return False
        return True
    
    def fix_directory_structure(self, report: AuditReport) -> int:
        """Create missing directories for all processors"""
        print("\n" + "=" * 60)
        print("FIX: Directory Structure")
        print("=" * 60)
        
        fixes = 0
        for audit in report.processors:
            needs_fix = False
            for subdir in EXPECTED_SUBDIRS:
                subdir_path = audit.path / subdir
                if not subdir_path.exists():
                    needs_fix = True
                    if self.create_directory(subdir_path):
                        fixes += 1
            
            if needs_fix:
                self.log(f"Fixed structure for: {audit.family}/{audit.name}")
        
        print(f"\nDirectories created: {fixes}")
        return fixes
    
    def fix_missing_readmes(self, report: AuditReport) -> int:
        """Generate README files for processors missing them"""
        print("\n" + "=" * 60)
        print("FIX: Missing README Files")
        print("=" * 60)
        
        fixes = 0
        for audit in report.processors:
            if not audit.has_readme:
                readme_path = audit.path / 'README.md'
                content = generate_readme_template(audit.name, audit.family)
                
                if self.write_file(readme_path, content):
                    fixes += 1
                    self.log(f"Generated README for: {audit.family}/{audit.name}")
        
        print(f"\nREADMEs generated: {fixes}")
        return fixes
    
    def fix_missing_validation_json(self, report: AuditReport) -> int:
        """Generate validation JSON templates for processors missing them"""
        print("\n" + "=" * 60)
        print("FIX: Missing Validation JSON Files")
        print("=" * 60)
        
        fixes = 0
        for audit in report.processors:
            if audit.has_validation_dir and not audit.has_validation_json:
                json_path = audit.path / 'validation' / f'{audit.name}_validation.json'
                content = generate_validation_json_template(audit.name, audit.family)
                
                if self.write_file(json_path, json.dumps(content, indent=2)):
                    fixes += 1
                    self.log(f"Generated validation JSON for: {audit.family}/{audit.name}")
        
        print(f"\nValidation JSONs generated: {fixes}")
        return fixes
    
    def fix_base_model_class(self) -> int:
        """Create or update the base model class in common/"""
        print("\n" + "=" * 60)
        print("FIX: Base Model Class")
        print("=" * 60)
        
        common_path = self.repo_path / 'common'
        base_model_path = common_path / 'base_model.py'
        
        self.create_directory(common_path)
        
        # Check if base_model.py exists and needs update
        if base_model_path.exists():
            with open(base_model_path, 'r') as f:
                existing = f.read()
            
            # Check if it has all required components
            new_content = generate_base_model_class()
            
            if 'BaseProcessorModel' not in existing:
                self.backup_file(base_model_path)
                self.write_file(base_model_path, new_content)
                self.log("Updated base_model.py with BaseProcessorModel class")
                return 1
            else:
                self.log("base_model.py already has BaseProcessorModel - skipping")
                return 0
        else:
            content = generate_base_model_class()
            if self.write_file(base_model_path, content):
                self.log("Created common/base_model.py")
                return 1
        
        return 0
    
    def fix_missing_init_files(self) -> int:
        """Create __init__.py files where missing"""
        print("\n" + "=" * 60)
        print("FIX: Missing __init__.py Files")
        print("=" * 60)
        
        fixes = 0
        
        # Common directory
        common_init = self.repo_path / 'common' / '__init__.py'
        if not common_init.exists():
            content = '''"""
Common utilities for Modeling_2026 processor models.
"""

from .base_model import (
    BaseProcessorModel,
    InstructionCategory,
    WorkloadProfile,
    AnalysisResult,
)

__all__ = [
    'BaseProcessorModel',
    'InstructionCategory', 
    'WorkloadProfile',
    'AnalysisResult',
]
'''
            if self.write_file(common_init, content):
                fixes += 1
        
        # Family directories
        for family in EXPECTED_FAMILIES:
            family_path = self.repo_path / family
            if family_path.exists():
                init_path = family_path / '__init__.py'
                if not init_path.exists():
                    # Generate __init__.py that imports all processors
                    processors = [d.name for d in family_path.iterdir() 
                                 if d.is_dir() and not d.name.startswith('_')]
                    
                    imports = []
                    all_exports = []
                    for proc in sorted(processors):
                        class_name = ''.join(word.title() for word in proc.split('_')) + 'Model'
                        imports.append(f"# from .{proc}.current.{proc}_validated import {class_name}")
                        all_exports.append(f"    # '{class_name}',")
                    
                    content = f'''"""
{family.title()} family processor models.
"""

# Uncomment imports as models are updated to use BaseProcessorModel
{chr(10).join(imports)}

__all__ = [
{chr(10).join(all_exports)}
]
'''
                    if self.write_file(init_path, content):
                        fixes += 1
        
        print(f"\n__init__.py files created: {fixes}")
        return fixes
    
    def add_method_stubs_to_model(self, py_file: Path, missing_methods: List[str]) -> bool:
        """Add missing method stubs to an existing model file"""
        if not missing_methods:
            return False
        
        self.backup_file(py_file)
        
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the main class and add stubs at the end
        # This is a simplified approach - proper AST manipulation would be better
        
        stub_code = "\n    # " + "=" * 60 + "\n"
        stub_code += "    # AUTO-GENERATED METHOD STUBS - Implement these!\n"
        stub_code += "    # " + "=" * 60 + "\n"
        
        all_stubs = generate_method_stubs()
        
        for method in missing_methods:
            # Extract just the stub for this method
            pattern = rf'(def {method}\(self.*?(?=\n    def |\nclass |\Z))'
            match = re.search(pattern, all_stubs, re.DOTALL)
            if match:
                stub_code += "\n" + match.group(1)
        
        # Find last method or class body end and insert stubs
        # Look for the last 'def' in the file and add after it
        last_def = list(re.finditer(r'\n(    def \w+\([^)]*\):.*?)(?=\n    def |\nclass |\Z)', content, re.DOTALL))
        
        if last_def:
            insert_pos = last_def[-1].end()
            new_content = content[:insert_pos] + stub_code + content[insert_pos:]
        else:
            # No methods found, append to end of file
            new_content = content + stub_code
        
        if not self.dry_run:
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        return True
    
    def fix_missing_method_stubs(self, report: AuditReport) -> int:
        """Add method stubs to models missing required methods"""
        print("\n" + "=" * 60)
        print("FIX: Missing Method Stubs")
        print("=" * 60)
        
        fixes = 0
        for audit in report.processors:
            if not audit.has_validated_py:
                continue
            
            missing = [m for m, has in audit.has_required_methods.items() if not has]
            if not missing:
                continue
            
            py_files = list((audit.path / 'current').glob('*_validated.py'))
            if not py_files:
                continue
            
            py_file = py_files[0]
            self.log(f"Adding stubs to {audit.family}/{audit.name}: {missing}")
            
            if self.add_method_stubs_to_model(py_file, missing):
                fixes += 1
        
        print(f"\nModels updated with stubs: {fixes}")
        return fixes
    
    def generate_index_json(self, report: AuditReport) -> int:
        """Generate or update index.json with all processors"""
        print("\n" + "=" * 60)
        print("FIX: Update index.json")
        print("=" * 60)
        
        index_path = self.repo_path / 'index.json'
        
        index_data = {
            "generated": datetime.now().isoformat(),
            "total_processors": len(report.processors),
            "families": {},
            "processors": {}
        }
        
        # Organize by family
        for family in EXPECTED_FAMILIES:
            family_processors = [a for a in report.processors if a.family == family]
            index_data["families"][family] = {
                "count": len(family_processors),
                "processors": [a.name for a in family_processors]
            }
        
        # Individual processor entries
        for audit in report.processors:
            index_data["processors"][f"{audit.family}/{audit.name}"] = {
                "family": audit.family,
                "name": audit.name,
                "has_validated_model": audit.has_validated_py,
                "has_validation_data": audit.has_validation_json,
                "has_documentation": audit.has_readme,
                "category_count": audit.category_count,
                "workload_profiles": audit.workload_profiles,
                "validation_sources": audit.validation_sources,
            }
        
        if self.backup and index_path.exists():
            self.backup_file(index_path)
        
        if self.write_file(index_path, json.dumps(index_data, indent=2)):
            self.log("Updated index.json")
            return 1
        
        return 0
    
    def generate_summary_report(self) -> str:
        """Generate summary of all changes made"""
        lines = []
        lines.append("\n" + "=" * 60)
        lines.append("FIX APPLICATION SUMMARY")
        lines.append("=" * 60)
        
        if self.dry_run:
            lines.append("\n*** DRY RUN - No actual changes were made ***\n")
        
        lines.append(f"\nTotal changes: {len(self.changes_made)}")
        
        if self.errors:
            lines.append(f"\nErrors encountered: {len(self.errors)}")
            for error in self.errors:
                lines.append(f"  - {error}")
        
        lines.append("\nChanges made:")
        for change in self.changes_made:
            lines.append(f"  ✓ {change}")
        
        if not self.dry_run:
            lines.append("\n" + "-" * 40)
            lines.append("Next steps:")
            lines.append("  1. Review generated files and customize as needed")
            lines.append("  2. Implement TODO items in method stubs")
            lines.append("  3. Add actual validation data to JSON files")
            lines.append("  4. Run audit again: python cross_family_audit.py --verbose")
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Apply consistency fixes to Modeling_2026 repository'
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
        help='Show what would be changed without making changes'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create backups before modifying files'
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
        help='Generate missing READMEs'
    )
    parser.add_argument(
        '--fix-json',
        action='store_true',
        help='Generate missing validation JSONs'
    )
    parser.add_argument(
        '--fix-base',
        action='store_true',
        help='Create/update base model class'
    )
    parser.add_argument(
        '--fix-stubs',
        action='store_true',
        help='Add method stubs to models'
    )
    parser.add_argument(
        '--fix-init',
        action='store_true',
        help='Create missing __init__.py files'
    )
    parser.add_argument(
        '--fix-index',
        action='store_true',
        help='Update index.json'
    )
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    # Determine which fixes to apply
    fix_all = args.fix_all
    fixes_requested = (
        args.fix_structure or args.fix_readme or args.fix_json or
        args.fix_base or args.fix_stubs or args.fix_init or args.fix_index
    )
    
    if not fix_all and not fixes_requested:
        print("No fixes requested. Use --fix-all or specific --fix-* options.")
        print("Run with --help for usage information.")
        sys.exit(0)
    
    # Run audit first
    print(f"Auditing repository: {repo_path}")
    report = run_audit(repo_path)
    print(f"Found {len(report.processors)} processors with {report.total_errors} errors")
    
    # Apply fixes
    applicator = FixApplicator(
        repo_path,
        dry_run=args.dry_run,
        backup=not args.no_backup
    )
    
    total_fixes = 0
    
    if fix_all or args.fix_structure:
        total_fixes += applicator.fix_directory_structure(report)
    
    if fix_all or args.fix_readme:
        total_fixes += applicator.fix_missing_readmes(report)
    
    if fix_all or args.fix_json:
        total_fixes += applicator.fix_missing_validation_json(report)
    
    if fix_all or args.fix_base:
        total_fixes += applicator.fix_base_model_class()
    
    if fix_all or args.fix_init:
        total_fixes += applicator.fix_missing_init_files()
    
    if fix_all or args.fix_stubs:
        total_fixes += applicator.fix_missing_method_stubs(report)
    
    if fix_all or args.fix_index:
        total_fixes += applicator.generate_index_json(report)
    
    # Print summary
    print(applicator.generate_summary_report())
    
    print(f"\nTotal fixes applied: {total_fixes}")
    
    if args.dry_run:
        print("\nTo apply these changes, run without --dry-run")


if __name__ == '__main__':
    main()
