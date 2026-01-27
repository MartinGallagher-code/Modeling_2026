#!/usr/bin/env python3
"""
Cross-Family Consistency Audit for Modeling_2026
=================================================

This script audits all processor models across the 5 families (Intel, Motorola,
MOS/WDC, Zilog, Other) for consistency in:

1. Directory structure (current/, validation/, docs/, archive/)
2. File naming (*_validated.py, *_validation.json)
3. Python model interface (required methods and attributes)
4. Validation JSON schema
5. README documentation

Usage:
    python cross_family_audit.py [repo_path] [--verbose] [--output FILE]

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import re
import ast
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import defaultdict
from datetime import datetime


# =============================================================================
# CONFIGURATION
# =============================================================================

EXPECTED_FAMILIES = ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']
EXPECTED_SUBDIRS = ['current', 'archive', 'validation', 'docs']
REQUIRED_SUBDIRS = ['current', 'validation']  # Must have these
OPTIONAL_SUBDIRS = ['archive', 'docs']  # Should have these

REQUIRED_METHODS = ['analyze', 'validate', 'get_instruction_categories', 'get_workload_profiles']
REQUIRED_ATTRIBUTES = ['name', 'manufacturer', 'year', 'clock_mhz', 'transistor_count']

STANDARD_WORKLOADS = ['typical', 'compute', 'memory', 'control']
MAX_RECOMMENDED_CATEGORIES = 15

VALIDATION_JSON_REQUIRED_KEYS = ['processor', 'validation_date', 'sources', 'timing_tests', 'accuracy']
VALIDATION_SOURCE_TYPES = ['datasheet', 'emulator', 'wikichip', 'wikipedia', 'mame', 'vice', 'hardware']


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class AuditIssue:
    """Represents a single audit issue"""
    family: str
    processor: str
    category: str
    severity: str  # 'error', 'warning', 'info'
    message: str
    fix_available: bool = False
    fix_command: str = ""


@dataclass
class ProcessorAudit:
    """Audit results for a single processor"""
    name: str
    family: str
    path: Path
    issues: List[AuditIssue] = field(default_factory=list)
    
    # Structure checks
    has_current_dir: bool = False
    has_validation_dir: bool = False
    has_docs_dir: bool = False
    has_archive_dir: bool = False
    has_readme: bool = False
    
    # File checks
    has_validated_py: bool = False
    has_validation_json: bool = False
    validated_py_path: Optional[Path] = None
    validation_json_path: Optional[Path] = None
    
    # Interface checks
    has_required_methods: Dict[str, bool] = field(default_factory=dict)
    has_required_attributes: Dict[str, bool] = field(default_factory=dict)
    
    # Content checks
    category_count: int = 0
    workload_profiles: List[str] = field(default_factory=list)
    
    @property
    def error_count(self) -> int:
        return len([i for i in self.issues if i.severity == 'error'])
    
    @property
    def warning_count(self) -> int:
        return len([i for i in self.issues if i.severity == 'warning'])


@dataclass
class FamilyAudit:
    """Audit results for a processor family"""
    name: str
    path: Path
    processors: List[ProcessorAudit] = field(default_factory=list)
    
    @property
    def total_errors(self) -> int:
        return sum(p.error_count for p in self.processors)
    
    @property
    def total_warnings(self) -> int:
        return sum(p.warning_count for p in self.processors)


@dataclass
class RepositoryAudit:
    """Complete audit results for the repository"""
    path: Path
    timestamp: str
    families: List[FamilyAudit] = field(default_factory=list)
    global_issues: List[AuditIssue] = field(default_factory=list)
    
    @property
    def total_processors(self) -> int:
        return sum(len(f.processors) for f in self.families)
    
    @property
    def total_errors(self) -> int:
        return sum(f.total_errors for f in self.families) + len([i for i in self.global_issues if i.severity == 'error'])
    
    @property
    def total_warnings(self) -> int:
        return sum(f.total_warnings for f in self.families) + len([i for i in self.global_issues if i.severity == 'warning'])


# =============================================================================
# AUDIT FUNCTIONS
# =============================================================================

def audit_directory_structure(processor_path: Path, processor_name: str, family: str) -> List[AuditIssue]:
    """Check processor directory structure"""
    issues = []
    
    for subdir in REQUIRED_SUBDIRS:
        subdir_path = processor_path / subdir
        if not subdir_path.exists():
            issues.append(AuditIssue(
                family=family,
                processor=processor_name,
                category='directory_structure',
                severity='error',
                message=f"Missing required directory: {subdir}/",
                fix_available=True,
                fix_command=f"mkdir -p {subdir_path}"
            ))
    
    for subdir in OPTIONAL_SUBDIRS:
        subdir_path = processor_path / subdir
        if not subdir_path.exists():
            issues.append(AuditIssue(
                family=family,
                processor=processor_name,
                category='directory_structure',
                severity='warning',
                message=f"Missing recommended directory: {subdir}/",
                fix_available=True,
                fix_command=f"mkdir -p {subdir_path}"
            ))
    
    return issues


def audit_file_naming(processor_path: Path, processor_name: str, family: str) -> Tuple[List[AuditIssue], Optional[Path], Optional[Path]]:
    """Check file naming conventions"""
    issues = []
    validated_py_path = None
    validation_json_path = None
    
    current_path = processor_path / 'current'
    if current_path.exists():
        # Look for *_validated.py
        py_files = list(current_path.glob('*_validated.py'))
        if not py_files:
            issues.append(AuditIssue(
                family=family,
                processor=processor_name,
                category='file_naming',
                severity='error',
                message=f"No *_validated.py file in current/",
                fix_available=True,
                fix_command=f"Generate {processor_name}_validated.py"
            ))
        elif len(py_files) > 1:
            issues.append(AuditIssue(
                family=family,
                processor=processor_name,
                category='file_naming',
                severity='warning',
                message=f"Multiple *_validated.py files found: {[f.name for f in py_files]}",
                fix_available=False
            ))
        else:
            validated_py_path = py_files[0]
            expected_name = f"{processor_name}_validated.py"
            if py_files[0].name != expected_name:
                issues.append(AuditIssue(
                    family=family,
                    processor=processor_name,
                    category='file_naming',
                    severity='warning',
                    message=f"File naming: expected {expected_name}, found {py_files[0].name}",
                    fix_available=True,
                    fix_command=f"mv {py_files[0]} {current_path / expected_name}"
                ))
    
    validation_path = processor_path / 'validation'
    if validation_path.exists():
        # Look for *_validation.json
        json_files = list(validation_path.glob('*_validation.json'))
        if not json_files:
            issues.append(AuditIssue(
                family=family,
                processor=processor_name,
                category='file_naming',
                severity='error',
                message=f"No *_validation.json file in validation/",
                fix_available=True,
                fix_command=f"Generate {processor_name}_validation.json"
            ))
        else:
            validation_json_path = json_files[0]
    
    # Check for README
    readme_path = processor_path / 'README.md'
    if not readme_path.exists():
        issues.append(AuditIssue(
            family=family,
            processor=processor_name,
            category='file_naming',
            severity='warning',
            message="Missing README.md",
            fix_available=True,
            fix_command=f"Generate README.md"
        ))
    
    return issues, validated_py_path, validation_json_path


def audit_python_interface(py_path: Path, processor_name: str, family: str) -> Tuple[List[AuditIssue], Dict[str, bool], Dict[str, bool], int, List[str]]:
    """Check Python model interface"""
    issues = []
    methods_found = {m: False for m in REQUIRED_METHODS}
    attributes_found = {a: False for a in REQUIRED_ATTRIBUTES}
    category_count = 0
    workload_profiles = []
    
    try:
        with open(py_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Parse AST
        try:
            tree = ast.parse(source)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.name in methods_found:
                        methods_found[node.name] = True
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            if target.id in attributes_found:
                                attributes_found[target.id] = True
        except SyntaxError as e:
            issues.append(AuditIssue(
                family=family,
                processor=processor_name,
                category='python_interface',
                severity='error',
                message=f"Python syntax error: {e}",
                fix_available=False
            ))
            return issues, methods_found, attributes_found, category_count, workload_profiles
        
        # Check for missing methods
        for method, found in methods_found.items():
            if not found:
                issues.append(AuditIssue(
                    family=family,
                    processor=processor_name,
                    category='python_interface',
                    severity='error',
                    message=f"Missing required method: {method}()",
                    fix_available=True,
                    fix_command=f"Add {method}() method stub"
                ))
        
        # Check for missing attributes (search in source text as fallback)
        for attr, found in attributes_found.items():
            if not found:
                # Try regex search
                if re.search(rf'\b{attr}\s*=', source):
                    attributes_found[attr] = True
                else:
                    issues.append(AuditIssue(
                        family=family,
                        processor=processor_name,
                        category='python_interface',
                        severity='warning',
                        message=f"Missing recommended attribute: {attr}",
                        fix_available=True,
                        fix_command=f"Add {attr} attribute"
                    ))
        
        # Count instruction categories
        cat_matches = re.findall(r"['\"](\w+)['\"]:\s*InstructionCategory", source)
        if not cat_matches:
            cat_matches = re.findall(r"instruction_categories\s*=\s*\{([^}]+)\}", source, re.DOTALL)
            if cat_matches:
                category_count = cat_matches[0].count(':')
        else:
            category_count = len(cat_matches)
        
        if category_count > MAX_RECOMMENDED_CATEGORIES:
            issues.append(AuditIssue(
                family=family,
                processor=processor_name,
                category='python_interface',
                severity='warning',
                message=f"Too many instruction categories ({category_count}). Recommended max: {MAX_RECOMMENDED_CATEGORIES}",
                fix_available=False
            ))
        
        # Find workload profiles
        profile_matches = re.findall(r"['\"](\w+)['\"]:\s*WorkloadProfile", source)
        if profile_matches:
            workload_profiles = profile_matches
        else:
            for wl in STANDARD_WORKLOADS:
                if re.search(rf"['\"]({wl})['\"]", source):
                    workload_profiles.append(wl)
        
        # Check for standard workloads
        missing_workloads = set(STANDARD_WORKLOADS) - set(workload_profiles)
        if missing_workloads:
            issues.append(AuditIssue(
                family=family,
                processor=processor_name,
                category='python_interface',
                severity='info',
                message=f"Missing standard workload profiles: {missing_workloads}",
                fix_available=True,
                fix_command=f"Add workload profiles: {missing_workloads}"
            ))
        
    except Exception as e:
        issues.append(AuditIssue(
            family=family,
            processor=processor_name,
            category='python_interface',
            severity='error',
            message=f"Failed to analyze Python file: {e}",
            fix_available=False
        ))
    
    return issues, methods_found, attributes_found, category_count, workload_profiles


def audit_validation_json(json_path: Path, processor_name: str, family: str) -> List[AuditIssue]:
    """Check validation JSON schema"""
    issues = []
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check required keys
        for key in VALIDATION_JSON_REQUIRED_KEYS:
            if key not in data:
                issues.append(AuditIssue(
                    family=family,
                    processor=processor_name,
                    category='validation_json',
                    severity='error',
                    message=f"Missing required key in validation JSON: {key}",
                    fix_available=True,
                    fix_command=f"Add '{key}' to validation JSON"
                ))
        
        # Check sources
        if 'sources' in data:
            sources = data['sources']
            if not sources:
                issues.append(AuditIssue(
                    family=family,
                    processor=processor_name,
                    category='validation_json',
                    severity='warning',
                    message="No validation sources listed",
                    fix_available=False
                ))
            else:
                source_types = set()
                for source in sources:
                    if isinstance(source, dict) and 'type' in source:
                        source_types.add(source['type'])
                
                if not source_types.intersection(set(VALIDATION_SOURCE_TYPES)):
                    issues.append(AuditIssue(
                        family=family,
                        processor=processor_name,
                        category='validation_json',
                        severity='info',
                        message=f"No standard source types. Expected one of: {VALIDATION_SOURCE_TYPES}",
                        fix_available=False
                    ))
        
        # Check accuracy
        if 'accuracy' in data:
            accuracy = data['accuracy']
            if isinstance(accuracy, dict):
                error = accuracy.get('ipc_error_percent') or accuracy.get('error_percent')
                if error and error > 5.0:
                    issues.append(AuditIssue(
                        family=family,
                        processor=processor_name,
                        category='validation_json',
                        severity='warning',
                        message=f"IPC error ({error}%) exceeds 5% target",
                        fix_available=False
                    ))
        
    except json.JSONDecodeError as e:
        issues.append(AuditIssue(
            family=family,
            processor=processor_name,
            category='validation_json',
            severity='error',
            message=f"Invalid JSON: {e}",
            fix_available=False
        ))
    except Exception as e:
        issues.append(AuditIssue(
            family=family,
            processor=processor_name,
            category='validation_json',
            severity='error',
            message=f"Failed to read validation JSON: {e}",
            fix_available=False
        ))
    
    return issues


def audit_processor(processor_path: Path, processor_name: str, family: str) -> ProcessorAudit:
    """Perform complete audit of a single processor"""
    audit = ProcessorAudit(
        name=processor_name,
        family=family,
        path=processor_path
    )
    
    # Directory structure
    audit.has_current_dir = (processor_path / 'current').exists()
    audit.has_validation_dir = (processor_path / 'validation').exists()
    audit.has_docs_dir = (processor_path / 'docs').exists()
    audit.has_archive_dir = (processor_path / 'archive').exists()
    audit.has_readme = (processor_path / 'README.md').exists()
    
    structure_issues = audit_directory_structure(processor_path, processor_name, family)
    audit.issues.extend(structure_issues)
    
    # File naming
    naming_issues, validated_py, validation_json = audit_file_naming(processor_path, processor_name, family)
    audit.issues.extend(naming_issues)
    audit.validated_py_path = validated_py
    audit.validation_json_path = validation_json
    audit.has_validated_py = validated_py is not None
    audit.has_validation_json = validation_json is not None
    
    # Python interface
    if validated_py and validated_py.exists():
        py_issues, methods, attrs, cat_count, workloads = audit_python_interface(validated_py, processor_name, family)
        audit.issues.extend(py_issues)
        audit.has_required_methods = methods
        audit.has_required_attributes = attrs
        audit.category_count = cat_count
        audit.workload_profiles = workloads
    
    # Validation JSON
    if validation_json and validation_json.exists():
        json_issues = audit_validation_json(validation_json, processor_name, family)
        audit.issues.extend(json_issues)
    
    return audit


def audit_family(family_path: Path, family_name: str) -> FamilyAudit:
    """Audit all processors in a family"""
    audit = FamilyAudit(name=family_name, path=family_path)
    
    if not family_path.exists():
        return audit
    
    for item in sorted(family_path.iterdir()):
        if item.is_dir() and not item.name.startswith('.') and item.name not in ['__pycache__', 'common']:
            processor_audit = audit_processor(item, item.name, family_name)
            audit.processors.append(processor_audit)
    
    return audit


def audit_repository(repo_path: Path) -> RepositoryAudit:
    """Perform complete repository audit"""
    audit = RepositoryAudit(
        path=repo_path,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    # Check for expected families
    for family in EXPECTED_FAMILIES:
        family_path = repo_path / family
        if not family_path.exists():
            audit.global_issues.append(AuditIssue(
                family='repository',
                processor='',
                category='structure',
                severity='warning',
                message=f"Missing family directory: {family}/",
                fix_available=True,
                fix_command=f"mkdir -p {family_path}"
            ))
        else:
            family_audit = audit_family(family_path, family)
            audit.families.append(family_audit)
    
    # Cross-family consistency checks
    all_workloads = defaultdict(set)
    all_methods = defaultdict(set)
    
    for family in audit.families:
        for processor in family.processors:
            for wl in processor.workload_profiles:
                all_workloads[wl].add(processor.name)
            for method, has in processor.has_required_methods.items():
                if has:
                    all_methods[method].add(processor.name)
    
    # Check workload profile consistency
    for wl in STANDARD_WORKLOADS:
        if wl in all_workloads:
            coverage = len(all_workloads[wl])
            total = audit.total_processors
            if coverage < total * 0.8:  # Less than 80% coverage
                audit.global_issues.append(AuditIssue(
                    family='cross-family',
                    processor='',
                    category='consistency',
                    severity='info',
                    message=f"Workload profile '{wl}' only in {coverage}/{total} processors",
                    fix_available=False
                ))
    
    return audit


# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_report(audit: RepositoryAudit, verbose: bool = False) -> str:
    """Generate human-readable audit report"""
    lines = []
    
    lines.append("=" * 70)
    lines.append("CROSS-FAMILY CONSISTENCY AUDIT REPORT")
    lines.append(f"Repository: {audit.path}")
    lines.append(f"Timestamp: {audit.timestamp}")
    lines.append("=" * 70)
    lines.append("")
    
    # Summary
    lines.append("SUMMARY")
    lines.append("-" * 40)
    lines.append(f"Total Families: {len(audit.families)}")
    lines.append(f"Total Processors: {audit.total_processors}")
    lines.append(f"Total Errors: {audit.total_errors}")
    lines.append(f"Total Warnings: {audit.total_warnings}")
    lines.append("")
    
    # By family
    lines.append("BY FAMILY")
    lines.append("-" * 40)
    for family in audit.families:
        lines.append(f"  {family.name}: {len(family.processors)} processors, "
                    f"{family.total_errors} errors, {family.total_warnings} warnings")
    lines.append("")
    
    # Global issues
    if audit.global_issues:
        lines.append("GLOBAL ISSUES")
        lines.append("-" * 40)
        for issue in audit.global_issues:
            icon = "❌" if issue.severity == 'error' else "⚠️" if issue.severity == 'warning' else "ℹ️"
            lines.append(f"  {icon} [{issue.category}] {issue.message}")
        lines.append("")
    
    # Errors
    all_errors = []
    for family in audit.families:
        for processor in family.processors:
            for issue in processor.issues:
                if issue.severity == 'error':
                    all_errors.append(issue)
    
    if all_errors:
        lines.append("ERRORS (Must Fix)")
        lines.append("-" * 40)
        for issue in all_errors[:50]:  # Limit to 50
            lines.append(f"  ❌ {issue.family}/{issue.processor}: {issue.message}")
        if len(all_errors) > 50:
            lines.append(f"  ... and {len(all_errors) - 50} more errors")
        lines.append("")
    
    # Warnings
    all_warnings = []
    for family in audit.families:
        for processor in family.processors:
            for issue in processor.issues:
                if issue.severity == 'warning':
                    all_warnings.append(issue)
    
    if all_warnings:
        lines.append("WARNINGS (Should Fix)")
        lines.append("-" * 40)
        for issue in all_warnings[:30]:  # Limit to 30
            lines.append(f"  ⚠️  {issue.family}/{issue.processor}: {issue.message}")
        if len(all_warnings) > 30:
            lines.append(f"  ... and {len(all_warnings) - 30} more warnings")
        lines.append("")
    
    # Verbose per-processor details
    if verbose:
        lines.append("DETAILED PROCESSOR AUDIT")
        lines.append("-" * 40)
        for family in audit.families:
            lines.append(f"\n{family.name.upper()}/")
            for processor in family.processors:
                status = "✓" if processor.error_count == 0 else "✗"
                lines.append(f"  {status} {processor.name}")
                lines.append(f"      Structure: current={processor.has_current_dir}, "
                           f"validation={processor.has_validation_dir}, "
                           f"docs={processor.has_docs_dir}")
                lines.append(f"      Files: validated.py={processor.has_validated_py}, "
                           f"validation.json={processor.has_validation_json}")
                lines.append(f"      Categories: {processor.category_count}, "
                           f"Workloads: {processor.workload_profiles}")
                if processor.issues:
                    for issue in processor.issues:
                        icon = "❌" if issue.severity == 'error' else "⚠️" if issue.severity == 'warning' else "ℹ️"
                        lines.append(f"      {icon} {issue.message}")
    
    lines.append("")
    lines.append("=" * 70)
    lines.append("END OF REPORT")
    lines.append("=" * 70)
    
    return '\n'.join(lines)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Cross-Family Consistency Audit for Modeling_2026'
    )
    parser.add_argument(
        'repo_path',
        nargs='?',
        default='.',
        help='Path to Modeling_2026 repository (default: current directory)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed per-processor audit results'
    )
    parser.add_argument(
        '--output', '-o',
        help='Write report to file instead of stdout'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Path does not exist: {repo_path}")
        sys.exit(1)
    
    print(f"Auditing repository: {repo_path}")
    print("")
    
    audit = audit_repository(repo_path)
    
    if args.json:
        # JSON output
        output = {
            'timestamp': audit.timestamp,
            'path': str(audit.path),
            'summary': {
                'families': len(audit.families),
                'processors': audit.total_processors,
                'errors': audit.total_errors,
                'warnings': audit.total_warnings,
            },
            'families': [{
                'name': f.name,
                'processors': [{
                    'name': p.name,
                    'errors': p.error_count,
                    'warnings': p.warning_count,
                    'issues': [{'severity': i.severity, 'category': i.category, 'message': i.message} for i in p.issues]
                } for p in f.processors]
            } for f in audit.families],
            'global_issues': [{'severity': i.severity, 'message': i.message} for i in audit.global_issues]
        }
        report = json.dumps(output, indent=2)
    else:
        report = generate_report(audit, args.verbose)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report written to: {args.output}")
    else:
        print(report)
    
    # Exit code based on errors
    sys.exit(1 if audit.total_errors > 0 else 0)


if __name__ == '__main__':
    main()
