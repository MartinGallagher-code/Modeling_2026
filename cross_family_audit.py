#!/usr/bin/env python3
"""
Cross-Family Consistency Audit Script for Modeling_2026 Repository
==================================================================

This script audits all processor models across the 5 manufacturer families
for consistency in:
1. Directory structure
2. File naming conventions
3. Python class interfaces
4. JSON validation schema
5. Documentation completeness

Usage:
    python cross_family_audit.py [repo_path] [--fix] [--report-only]
    
Arguments:
    repo_path     Path to Modeling_2026 repository (default: current directory)
    --fix         Automatically fix issues where possible
    --report-only Only generate report, don't suggest fixes
    --verbose     Show detailed output for each processor

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import json
import re
import ast
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from datetime import datetime
from collections import defaultdict
import shutil


# =============================================================================
# CONFIGURATION - Expected Standards
# =============================================================================

EXPECTED_FAMILIES = ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']

EXPECTED_SUBDIRS = ['current', 'archive', 'validation', 'docs']

EXPECTED_FILES = {
    'current': ['{processor}_validated.py'],
    'validation': ['{processor}_validation.json'],
    'docs': [],  # Optional but recommended
    'archive': [],  # Can be empty
}

# Required methods in all *_validated.py files
REQUIRED_METHODS = [
    'analyze',
    'validate', 
    'get_instruction_categories',
    'get_workload_profiles',
]

# Required attributes in all *_validated.py files
REQUIRED_ATTRIBUTES = [
    'name',
    'manufacturer', 
    'year',
    'clock_mhz',
    'transistor_count',
]

# Standard workload profiles every model should support
STANDARD_WORKLOADS = ['typical', 'compute', 'memory', 'control']

# Validation JSON schema requirements
VALIDATION_SCHEMA = {
    'required_keys': ['processor', 'validation_date', 'sources', 'timing_tests', 'accuracy'],
    'source_types': ['datasheet', 'emulator', 'wikichip', 'wikipedia', 'mame'],
}

# Maximum recommended instruction categories (your research finding)
MAX_RECOMMENDED_CATEGORIES = 15


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Issue:
    """Represents a single audit issue"""
    processor: str
    family: str
    severity: str  # 'error', 'warning', 'info'
    category: str
    message: str
    fix_available: bool = False
    fix_action: str = ""


@dataclass
class ProcessorAudit:
    """Audit results for a single processor"""
    name: str
    family: str
    path: Path
    issues: List[Issue] = field(default_factory=list)
    
    # Structure checks
    has_current_dir: bool = False
    has_validation_dir: bool = False
    has_docs_dir: bool = False
    has_archive_dir: bool = False
    
    # File checks
    has_validated_py: bool = False
    has_validation_json: bool = False
    has_readme: bool = False
    
    # Code checks
    has_required_methods: Dict[str, bool] = field(default_factory=dict)
    has_required_attributes: Dict[str, bool] = field(default_factory=dict)
    category_count: int = 0
    workload_profiles: List[str] = field(default_factory=list)
    
    # Validation data checks
    validation_sources: List[str] = field(default_factory=list)
    timing_tests_count: int = 0
    
    @property
    def error_count(self) -> int:
        return len([i for i in self.issues if i.severity == 'error'])
    
    @property
    def warning_count(self) -> int:
        return len([i for i in self.issues if i.severity == 'warning'])


@dataclass 
class AuditReport:
    """Complete audit report for all families"""
    timestamp: str
    repo_path: Path
    processors: List[ProcessorAudit] = field(default_factory=list)
    global_issues: List[Issue] = field(default_factory=list)
    
    @property
    def total_processors(self) -> int:
        return len(self.processors)
    
    @property
    def total_errors(self) -> int:
        return sum(p.error_count for p in self.processors) + len([i for i in self.global_issues if i.severity == 'error'])
    
    @property
    def total_warnings(self) -> int:
        return sum(p.warning_count for p in self.processors) + len([i for i in self.global_issues if i.severity == 'warning'])


# =============================================================================
# AUDIT FUNCTIONS
# =============================================================================

def discover_processors(repo_path: Path) -> Dict[str, List[Tuple[str, Path]]]:
    """Discover all processor directories organized by family"""
    processors_by_family = defaultdict(list)
    
    for family in EXPECTED_FAMILIES:
        family_path = repo_path / family
        if family_path.exists() and family_path.is_dir():
            for item in family_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    processors_by_family[family].append((item.name, item))
    
    return dict(processors_by_family)


def audit_directory_structure(processor_path: Path, processor_name: str, family: str) -> List[Issue]:
    """Check directory structure compliance"""
    issues = []
    
    for subdir in EXPECTED_SUBDIRS:
        subdir_path = processor_path / subdir
        if not subdir_path.exists():
            issues.append(Issue(
                processor=processor_name,
                family=family,
                severity='error' if subdir in ['current', 'validation'] else 'warning',
                category='directory_structure',
                message=f"Missing required directory: {subdir}/",
                fix_available=True,
                fix_action=f"mkdir -p {subdir_path}"
            ))
    
    return issues


def audit_file_naming(processor_path: Path, processor_name: str, family: str) -> List[Issue]:
    """Check file naming conventions"""
    issues = []
    
    # Check for validated.py file
    current_path = processor_path / 'current'
    if current_path.exists():
        expected_py = f"{processor_name}_validated.py"
        py_files = list(current_path.glob('*_validated.py'))
        
        if not py_files:
            issues.append(Issue(
                processor=processor_name,
                family=family,
                severity='error',
                category='file_naming',
                message=f"Missing validated model file in current/",
                fix_available=False,
                fix_action=""
            ))
        elif len(py_files) > 1:
            issues.append(Issue(
                processor=processor_name,
                family=family,
                severity='warning',
                category='file_naming',
                message=f"Multiple validated files found: {[f.name for f in py_files]}",
                fix_available=False,
                fix_action=""
            ))
        else:
            actual_name = py_files[0].name
            # Check naming pattern consistency
            if not actual_name.endswith('_validated.py'):
                issues.append(Issue(
                    processor=processor_name,
                    family=family,
                    severity='error',
                    category='file_naming',
                    message=f"Invalid file name pattern: {actual_name} (should end with _validated.py)",
                    fix_available=True,
                    fix_action=f"Rename to {processor_name}_validated.py"
                ))
    
    # Check for validation JSON
    validation_path = processor_path / 'validation'
    if validation_path.exists():
        json_files = list(validation_path.glob('*_validation.json'))
        if not json_files:
            issues.append(Issue(
                processor=processor_name,
                family=family,
                severity='warning',
                category='file_naming',
                message=f"Missing validation JSON file in validation/",
                fix_available=False,
                fix_action=""
            ))
    
    # Check for README
    readme_files = list(processor_path.glob('README*'))
    if not readme_files:
        issues.append(Issue(
            processor=processor_name,
            family=family,
            severity='info',
            category='documentation',
            message="Missing README.md file",
            fix_available=True,
            fix_action="Generate README template"
        ))
    
    return issues


def audit_python_model(processor_path: Path, processor_name: str, family: str) -> Tuple[List[Issue], Dict]:
    """Audit Python model file for required interface"""
    issues = []
    model_info = {
        'methods_found': [],
        'attributes_found': [],
        'category_count': 0,
        'workloads_found': [],
        'class_name': None,
    }
    
    current_path = processor_path / 'current'
    if not current_path.exists():
        return issues, model_info
    
    py_files = list(current_path.glob('*_validated.py'))
    if not py_files:
        return issues, model_info
    
    py_file = py_files[0]
    
    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        tree = ast.parse(source_code)
        
        # Find the main model class
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        model_class = None
        
        for cls in classes:
            if 'Model' in cls.name or 'model' in cls.name.lower():
                model_class = cls
                model_info['class_name'] = cls.name
                break
        
        if not model_class:
            # Try to find any class with the processor name
            for cls in classes:
                if processor_name.lower().replace('_', '') in cls.name.lower().replace('_', ''):
                    model_class = cls
                    model_info['class_name'] = cls.name
                    break
        
        if not model_class:
            issues.append(Issue(
                processor=processor_name,
                family=family,
                severity='error',
                category='code_structure',
                message=f"No model class found in {py_file.name}",
                fix_available=False,
                fix_action=""
            ))
            return issues, model_info
        
        # Check for required methods
        methods = [node.name for node in ast.walk(model_class) if isinstance(node, ast.FunctionDef)]
        model_info['methods_found'] = methods
        
        for required_method in REQUIRED_METHODS:
            if required_method not in methods:
                issues.append(Issue(
                    processor=processor_name,
                    family=family,
                    severity='error',
                    category='interface_compliance',
                    message=f"Missing required method: {required_method}()",
                    fix_available=True,
                    fix_action=f"Add {required_method}() method stub"
                ))
        
        # Check for required attributes (look in __init__ or class body)
        assignments = []
        for node in ast.walk(model_class):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                        if target.value.id == 'self':
                            assignments.append(target.attr)
                    elif isinstance(target, ast.Name):
                        assignments.append(target.id)
        
        model_info['attributes_found'] = assignments
        
        # Look for instruction categories
        category_pattern = re.compile(r'(?:instruction_categories|categories|CATEGORIES)\s*=\s*\{', re.IGNORECASE)
        category_match = category_pattern.search(source_code)
        if category_match:
            # Count categories by finding dictionary entries
            # This is a simplified count - looks for quoted keys
            start_pos = category_match.end()
            brace_count = 1
            end_pos = start_pos
            for i, char in enumerate(source_code[start_pos:], start_pos):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_pos = i
                        break
            
            category_section = source_code[start_pos:end_pos]
            # Count top-level keys
            key_pattern = re.compile(r"['\"](\w+)['\"]:\s*(?:\{|['\"]|\d)")
            keys = key_pattern.findall(category_section)
            model_info['category_count'] = len(keys)
            
            if len(keys) > MAX_RECOMMENDED_CATEGORIES:
                issues.append(Issue(
                    processor=processor_name,
                    family=family,
                    severity='warning',
                    category='model_design',
                    message=f"Too many instruction categories: {len(keys)} (recommended max: {MAX_RECOMMENDED_CATEGORIES})",
                    fix_available=False,
                    fix_action="Consider consolidating similar instruction categories"
                ))
        
        # Look for workload profiles
        workload_pattern = re.compile(r'(?:workload_profiles|WORKLOADS|profiles)\s*=\s*\{', re.IGNORECASE)
        workload_match = workload_pattern.search(source_code)
        if workload_match:
            start_pos = workload_match.end()
            brace_count = 1
            end_pos = start_pos
            for i, char in enumerate(source_code[start_pos:], start_pos):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_pos = i
                        break
            
            workload_section = source_code[start_pos:end_pos]
            key_pattern = re.compile(r"['\"](\w+)['\"]:\s*(?:\{|WorkloadProfile)")
            keys = key_pattern.findall(workload_section)
            model_info['workloads_found'] = keys
            
            # Check for standard workloads
            missing_workloads = [w for w in STANDARD_WORKLOADS if w not in keys]
            if missing_workloads:
                issues.append(Issue(
                    processor=processor_name,
                    family=family,
                    severity='warning',
                    category='workload_coverage',
                    message=f"Missing standard workload profiles: {missing_workloads}",
                    fix_available=True,
                    fix_action="Add missing workload profile definitions"
                ))
        
    except SyntaxError as e:
        issues.append(Issue(
            processor=processor_name,
            family=family,
            severity='error',
            category='syntax',
            message=f"Python syntax error in {py_file.name}: {e}",
            fix_available=False,
            fix_action=""
        ))
    except Exception as e:
        issues.append(Issue(
            processor=processor_name,
            family=family,
            severity='error',
            category='parse_error',
            message=f"Failed to parse {py_file.name}: {e}",
            fix_available=False,
            fix_action=""
        ))
    
    return issues, model_info


def audit_validation_json(processor_path: Path, processor_name: str, family: str) -> Tuple[List[Issue], Dict]:
    """Audit validation JSON file"""
    issues = []
    validation_info = {
        'sources': [],
        'timing_tests_count': 0,
        'accuracy_reported': False,
    }
    
    validation_path = processor_path / 'validation'
    if not validation_path.exists():
        return issues, validation_info
    
    json_files = list(validation_path.glob('*_validation.json'))
    if not json_files:
        return issues, validation_info
    
    json_file = json_files[0]
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check required keys
        for key in VALIDATION_SCHEMA['required_keys']:
            if key not in data:
                issues.append(Issue(
                    processor=processor_name,
                    family=family,
                    severity='warning',
                    category='validation_schema',
                    message=f"Missing required key in validation JSON: '{key}'",
                    fix_available=True,
                    fix_action=f"Add '{key}' field to validation JSON"
                ))
        
        # Check sources
        if 'sources' in data:
            sources = data['sources']
            if isinstance(sources, dict):
                validation_info['sources'] = list(sources.keys())
            elif isinstance(sources, list):
                validation_info['sources'] = sources
            
            if not validation_info['sources']:
                issues.append(Issue(
                    processor=processor_name,
                    family=family,
                    severity='warning',
                    category='validation_coverage',
                    message="No validation sources specified",
                    fix_available=False,
                    fix_action=""
                ))
        
        # Check timing tests
        if 'timing_tests' in data:
            tests = data['timing_tests']
            if isinstance(tests, list):
                validation_info['timing_tests_count'] = len(tests)
            elif isinstance(tests, dict):
                validation_info['timing_tests_count'] = len(tests)
            
            if validation_info['timing_tests_count'] == 0:
                issues.append(Issue(
                    processor=processor_name,
                    family=family,
                    severity='warning',
                    category='validation_coverage',
                    message="No timing tests defined",
                    fix_available=False,
                    fix_action=""
                ))
        
        # Check accuracy reporting
        if 'accuracy' in data:
            validation_info['accuracy_reported'] = True
            accuracy = data['accuracy']
            if isinstance(accuracy, dict):
                error_pct = accuracy.get('error_percent', accuracy.get('error_pct', accuracy.get('ipc_error', None)))
                if error_pct is not None and error_pct > 5.0:
                    issues.append(Issue(
                        processor=processor_name,
                        family=family,
                        severity='warning',
                        category='model_accuracy',
                        message=f"Model accuracy below target: {error_pct}% error (target: <5%)",
                        fix_available=False,
                        fix_action=""
                    ))
        
    except json.JSONDecodeError as e:
        issues.append(Issue(
            processor=processor_name,
            family=family,
            severity='error',
            category='json_syntax',
            message=f"Invalid JSON in {json_file.name}: {e}",
            fix_available=False,
            fix_action=""
        ))
    except Exception as e:
        issues.append(Issue(
            processor=processor_name,
            family=family,
            severity='error',
            category='file_error',
            message=f"Failed to read {json_file.name}: {e}",
            fix_available=False,
            fix_action=""
        ))
    
    return issues, validation_info


def audit_processor(processor_name: str, processor_path: Path, family: str) -> ProcessorAudit:
    """Complete audit of a single processor"""
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
    
    audit.issues.extend(audit_directory_structure(processor_path, processor_name, family))
    
    # File naming
    audit.issues.extend(audit_file_naming(processor_path, processor_name, family))
    
    audit.has_validated_py = bool(list((processor_path / 'current').glob('*_validated.py'))) if audit.has_current_dir else False
    audit.has_validation_json = bool(list((processor_path / 'validation').glob('*_validation.json'))) if audit.has_validation_dir else False
    audit.has_readme = bool(list(processor_path.glob('README*')))
    
    # Python model audit
    py_issues, model_info = audit_python_model(processor_path, processor_name, family)
    audit.issues.extend(py_issues)
    audit.has_required_methods = {m: m in model_info['methods_found'] for m in REQUIRED_METHODS}
    audit.category_count = model_info['category_count']
    audit.workload_profiles = model_info['workloads_found']
    
    # Validation JSON audit
    json_issues, validation_info = audit_validation_json(processor_path, processor_name, family)
    audit.issues.extend(json_issues)
    audit.validation_sources = validation_info['sources']
    audit.timing_tests_count = validation_info['timing_tests_count']
    
    return audit


def check_cross_family_consistency(audits: List[ProcessorAudit]) -> List[Issue]:
    """Check for inconsistencies across families"""
    issues = []
    
    # Check class naming patterns by family
    class_patterns = defaultdict(set)
    for audit in audits:
        if audit.has_validated_py:
            current_path = audit.path / 'current'
            py_files = list(current_path.glob('*_validated.py'))
            if py_files:
                try:
                    with open(py_files[0], 'r') as f:
                        content = f.read()
                    # Find class name
                    match = re.search(r'class\s+(\w+)', content)
                    if match:
                        class_name = match.group(1)
                        class_patterns[audit.family].add(class_name)
                except:
                    pass
    
    # Check for naming consistency within families
    for family, patterns in class_patterns.items():
        # Extract naming conventions
        suffixes = set()
        for name in patterns:
            if name.endswith('Model'):
                suffixes.add('Model')
            elif name.endswith('Processor'):
                suffixes.add('Processor')
            elif name.endswith('CPU'):
                suffixes.add('CPU')
            else:
                suffixes.add('other')
        
        if len(suffixes) > 1:
            issues.append(Issue(
                processor='[ALL]',
                family=family,
                severity='warning',
                category='naming_consistency',
                message=f"Inconsistent class naming suffixes in {family}: {suffixes}",
                fix_available=True,
                fix_action=f"Standardize to '*Model' suffix"
            ))
    
    # Check workload profile consistency
    all_workloads = set()
    for audit in audits:
        all_workloads.update(audit.workload_profiles)
    
    for audit in audits:
        if audit.workload_profiles:
            missing = all_workloads - set(audit.workload_profiles)
            # Only flag if missing common ones
            common_missing = missing & set(STANDARD_WORKLOADS)
            if common_missing and len(audit.workload_profiles) < 4:
                issues.append(Issue(
                    processor=audit.name,
                    family=audit.family,
                    severity='info',
                    category='workload_consistency',
                    message=f"Has fewer workloads than peers. Consider adding: {common_missing}",
                    fix_available=False,
                    fix_action=""
                ))
    
    return issues


# =============================================================================
# FIX GENERATION
# =============================================================================

def generate_missing_directory_fix(audit: ProcessorAudit) -> str:
    """Generate shell commands to create missing directories"""
    commands = []
    
    for subdir in EXPECTED_SUBDIRS:
        subdir_path = audit.path / subdir
        if not subdir_path.exists():
            commands.append(f"mkdir -p \"{subdir_path}\"")
    
    return '\n'.join(commands)


def generate_readme_template(processor_name: str, family: str) -> str:
    """Generate a README template for a processor"""
    return f'''# {processor_name.upper()} Grey-Box Queueing Model

## Overview

Grey-box queueing model for the {processor_name.upper()} microprocessor.

**Manufacturer:** {family.title()}  
**Architecture:** [8-bit/16-bit/32-bit]  
**Year:** [YYYY]  

## Model Characteristics

| Parameter | Value |
|-----------|-------|
| Clock Speed | X MHz |
| Transistors | X,XXX |
| Instruction Categories | X |
| Validation Accuracy | <X% error |

## Files

- `current/{processor_name}_validated.py` - Validated model (USE THIS)
- `validation/{processor_name}_validation.json` - Validation data
- `archive/` - Previous versions
- `docs/` - Additional documentation

## Usage

```python
from {processor_name}_validated import {processor_name.title().replace("_", "")}Model

model = {processor_name.title().replace("_", "")}Model()
result = model.analyze('typical')

print(f"IPC: {{result.ipc:.3f}}")
print(f"CPI: {{result.cpi:.2f}}")
print(f"Bottleneck: {{result.bottleneck}}")
```

## Validation Sources

- [ ] Original datasheet
- [ ] WikiChip
- [ ] MAME/emulator timing
- [ ] Wikipedia specifications

## Category-Based Timing

This model uses {MAX_RECOMMENDED_CATEGORIES} or fewer instruction categories
following the grey-box methodology principle that category-based timing 
with weighted averages is superior to exhaustive instruction enumeration.

## Last Updated

{datetime.now().strftime("%Y-%m-%d")}
'''


def generate_method_stubs() -> str:
    """Generate stub methods for required interface"""
    return '''
    def analyze(self, workload: str = 'typical') -> 'AnalysisResult':
        """
        Analyze processor performance for given workload.
        
        Args:
            workload: Workload profile name ('typical', 'compute', 'memory', 'control')
            
        Returns:
            AnalysisResult with IPC, CPI, bottleneck analysis
        """
        raise NotImplementedError("Implement analyze() method")
    
    def validate(self) -> Dict[str, Any]:
        """
        Run validation tests against known timing data.
        
        Returns:
            Dictionary with test results and pass/fail status
        """
        raise NotImplementedError("Implement validate() method")
    
    def get_instruction_categories(self) -> Dict[str, 'InstructionCategory']:
        """
        Return instruction category definitions.
        
        Returns:
            Dictionary mapping category name to InstructionCategory
        """
        raise NotImplementedError("Implement get_instruction_categories() method")
    
    def get_workload_profiles(self) -> Dict[str, 'WorkloadProfile']:
        """
        Return workload profile definitions.
        
        Returns:
            Dictionary mapping profile name to WorkloadProfile
        """
        raise NotImplementedError("Implement get_workload_profiles() method")
'''


def generate_validation_json_template(processor_name: str, family: str) -> dict:
    """Generate a validation JSON template"""
    return {
        "processor": processor_name,
        "family": family,
        "validation_date": datetime.now().strftime("%Y-%m-%d"),
        "sources": {
            "datasheet": {
                "name": f"{processor_name.upper()} Datasheet",
                "verified": False
            },
            "wikichip": {
                "url": f"https://en.wikichip.org/wiki/{family}/{processor_name}",
                "verified": False
            }
        },
        "timing_tests": [],
        "accuracy": {
            "ipc_error_percent": None,
            "timing_tests_passed": 0,
            "timing_tests_total": 0
        },
        "notes": "TODO: Add validation data"
    }


def generate_base_model_class() -> str:
    """Generate the base model class that all processors should inherit from"""
    return '''"""
Base Model Class for Modeling_2026 Processors
=============================================

All processor models should inherit from BaseProcessorModel to ensure
consistent interface across all 61 processors.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Any, Optional


@dataclass
class InstructionCategory:
    """Represents an instruction category with timing information"""
    name: str
    base_cycles: float
    memory_cycles: float = 0
    description: str = ""
    
    @property
    def total_cycles(self) -> float:
        return self.base_cycles + self.memory_cycles


@dataclass  
class WorkloadProfile:
    """Represents a workload mix for analysis"""
    name: str
    category_weights: Dict[str, float]  # category_name -> fraction (must sum to 1.0)
    description: str = ""
    
    def validate(self) -> bool:
        total = sum(self.category_weights.values())
        return abs(total - 1.0) < 0.001


@dataclass
class AnalysisResult:
    """Results from model analysis"""
    processor: str
    workload: str
    ipc: float  # Instructions per cycle
    cpi: float  # Cycles per instruction
    ips: float  # Instructions per second
    bottleneck: str
    utilizations: Dict[str, float]  # stage -> utilization
    
    @classmethod
    def from_cpi(cls, processor: str, workload: str, cpi: float, 
                 clock_mhz: float, bottleneck: str, utilizations: Dict[str, float]) -> 'AnalysisResult':
        ipc = 1.0 / cpi
        ips = clock_mhz * 1e6 * ipc
        return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations)


class BaseProcessorModel(ABC):
    """
    Abstract base class for all processor models.
    
    All 61 processors in Modeling_2026 should inherit from this class
    to ensure consistent interface and methodology.
    """
    
    # Required class attributes - subclasses must define these
    name: str = "Unknown"
    manufacturer: str = "Unknown"
    year: int = 0
    clock_mhz: float = 0.0
    transistor_count: int = 0
    data_width: int = 8  # bits
    address_width: int = 16  # bits
    
    @abstractmethod
    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """
        Analyze processor performance for given workload profile.
        
        Args:
            workload: Name of workload profile to use
            
        Returns:
            AnalysisResult containing IPC, CPI, IPS, bottleneck info
        """
        pass
    
    @abstractmethod
    def validate(self) -> Dict[str, Any]:
        """
        Run validation tests against known timing data.
        
        Returns:
            Dictionary containing:
                - 'tests': List of individual test results
                - 'passed': Number of passing tests
                - 'total': Total number of tests
                - 'accuracy_percent': Overall accuracy
        """
        pass
    
    @abstractmethod
    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        """
        Return instruction categories used by this model.
        
        Following the grey-box methodology, models should use 5-15 categories
        rather than exhaustive instruction enumeration.
        
        Returns:
            Dictionary mapping category name to InstructionCategory
        """
        pass
    
    @abstractmethod
    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        """
        Return workload profiles supported by this model.
        
        All models should support at minimum:
            - 'typical': General-purpose workload
            - 'compute': Compute-intensive (ALU-heavy)
            - 'memory': Memory-intensive (load/store heavy)
            - 'control': Control-flow intensive (branches)
        
        Returns:
            Dictionary mapping profile name to WorkloadProfile
        """
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """Return basic model information"""
        return {
            'name': self.name,
            'manufacturer': self.manufacturer,
            'year': self.year,
            'clock_mhz': self.clock_mhz,
            'transistor_count': self.transistor_count,
            'data_width': self.data_width,
            'address_width': self.address_width,
            'category_count': len(self.get_instruction_categories()),
            'workload_count': len(self.get_workload_profiles()),
        }
    
    def summary(self) -> str:
        """Return a summary string for the model"""
        info = self.get_model_info()
        return (
            f"{info['name']} ({info['manufacturer']}, {info['year']})\\n"
            f"  Clock: {info['clock_mhz']} MHz, {info['transistor_count']:,} transistors\\n"
            f"  Categories: {info['category_count']}, Workloads: {info['workload_count']}"
        )
'''


# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_report(report: AuditReport, verbose: bool = False) -> str:
    """Generate human-readable audit report"""
    lines = []
    
    lines.append("=" * 80)
    lines.append("CROSS-FAMILY CONSISTENCY AUDIT REPORT")
    lines.append(f"Repository: {report.repo_path}")
    lines.append(f"Timestamp: {report.timestamp}")
    lines.append("=" * 80)
    lines.append("")
    
    # Summary
    lines.append("SUMMARY")
    lines.append("-" * 40)
    lines.append(f"Total Processors Audited: {report.total_processors}")
    lines.append(f"Total Errors: {report.total_errors}")
    lines.append(f"Total Warnings: {report.total_warnings}")
    lines.append("")
    
    # By family breakdown
    lines.append("BY FAMILY")
    lines.append("-" * 40)
    family_counts = defaultdict(lambda: {'count': 0, 'errors': 0, 'warnings': 0})
    for audit in report.processors:
        family_counts[audit.family]['count'] += 1
        family_counts[audit.family]['errors'] += audit.error_count
        family_counts[audit.family]['warnings'] += audit.warning_count
    
    for family in EXPECTED_FAMILIES:
        counts = family_counts[family]
        status = "✓" if counts['errors'] == 0 else "✗"
        lines.append(f"  {status} {family:12} {counts['count']:3} processors, "
                    f"{counts['errors']:2} errors, {counts['warnings']:2} warnings")
    lines.append("")
    
    # Global issues
    if report.global_issues:
        lines.append("CROSS-FAMILY ISSUES")
        lines.append("-" * 40)
        for issue in report.global_issues:
            icon = "❌" if issue.severity == 'error' else "⚠️" if issue.severity == 'warning' else "ℹ️"
            lines.append(f"  {icon} [{issue.family}] {issue.message}")
        lines.append("")
    
    # Detailed issues by severity
    errors = [i for p in report.processors for i in p.issues if i.severity == 'error']
    warnings = [i for p in report.processors for i in p.issues if i.severity == 'warning']
    
    if errors:
        lines.append("ERRORS (Must Fix)")
        lines.append("-" * 40)
        for issue in errors[:50]:  # Limit output
            lines.append(f"  ❌ {issue.family}/{issue.processor}: {issue.message}")
            if issue.fix_available:
                lines.append(f"     Fix: {issue.fix_action}")
        if len(errors) > 50:
            lines.append(f"  ... and {len(errors) - 50} more errors")
        lines.append("")
    
    if warnings:
        lines.append("WARNINGS (Should Fix)")
        lines.append("-" * 40)
        for issue in warnings[:30]:  # Limit output
            lines.append(f"  ⚠️  {issue.family}/{issue.processor}: {issue.message}")
        if len(warnings) > 30:
            lines.append(f"  ... and {len(warnings) - 30} more warnings")
        lines.append("")
    
    # Verbose per-processor details
    if verbose:
        lines.append("DETAILED PROCESSOR AUDIT")
        lines.append("-" * 40)
        for audit in report.processors:
            status = "✓" if audit.error_count == 0 else "✗"
            lines.append(f"\n{status} {audit.family}/{audit.name}")
            lines.append(f"   Structure: current={audit.has_current_dir}, validation={audit.has_validation_dir}, "
                        f"docs={audit.has_docs_dir}")
            lines.append(f"   Files: py={audit.has_validated_py}, json={audit.has_validation_json}, "
                        f"readme={audit.has_readme}")
            lines.append(f"   Categories: {audit.category_count}, Workloads: {audit.workload_profiles}")
            lines.append(f"   Validation: {audit.timing_tests_count} tests, sources={audit.validation_sources}")
            if audit.issues:
                for issue in audit.issues:
                    icon = "❌" if issue.severity == 'error' else "⚠️" if issue.severity == 'warning' else "ℹ️"
                    lines.append(f"   {icon} {issue.message}")
    
    lines.append("")
    lines.append("=" * 80)
    lines.append("END OF REPORT")
    lines.append("=" * 80)
    
    return '\n'.join(lines)


def generate_fix_script(report: AuditReport, repo_path: Path) -> str:
    """Generate a shell script to fix identified issues"""
    lines = []
    
    lines.append("#!/bin/bash")
    lines.append("#")
    lines.append("# Auto-generated fix script for Modeling_2026 repository")
    lines.append(f"# Generated: {report.timestamp}")
    lines.append(f"# Repository: {repo_path}")
    lines.append("#")
    lines.append("# Review this script before running!")
    lines.append("# Run with: bash fix_consistency_issues.sh")
    lines.append("#")
    lines.append("")
    lines.append("set -e  # Exit on error")
    lines.append("")
    lines.append(f'REPO_PATH="{repo_path}"')
    lines.append('cd "$REPO_PATH"')
    lines.append("")
    
    # Section 1: Create missing directories
    lines.append("# " + "=" * 70)
    lines.append("# SECTION 1: Create Missing Directories")
    lines.append("# " + "=" * 70)
    lines.append("")
    
    dir_commands = set()
    for audit in report.processors:
        for subdir in EXPECTED_SUBDIRS:
            subdir_path = audit.path / subdir
            if not subdir_path.exists():
                rel_path = subdir_path.relative_to(repo_path)
                dir_commands.add(f'mkdir -p "{rel_path}"')
    
    if dir_commands:
        lines.append("echo 'Creating missing directories...'")
        for cmd in sorted(dir_commands):
            lines.append(cmd)
        lines.append("echo 'Done creating directories.'")
    else:
        lines.append("echo 'No missing directories.'")
    lines.append("")
    
    # Section 2: Generate missing READMEs
    lines.append("# " + "=" * 70)
    lines.append("# SECTION 2: Generate Missing README Files")
    lines.append("# " + "=" * 70)
    lines.append("")
    
    readme_processors = [(a.name, a.family, a.path) for a in report.processors if not a.has_readme]
    if readme_processors:
        lines.append("echo 'Generating README files...'")
        for proc_name, family, proc_path in readme_processors:
            rel_path = proc_path.relative_to(repo_path)
            lines.append(f"# README for {family}/{proc_name}")
            lines.append(f'if [ ! -f "{rel_path}/README.md" ]; then')
            lines.append(f'  python3 -c "')
            lines.append(f"import sys; sys.path.insert(0, '.'); ")
            lines.append(f"from cross_family_audit import generate_readme_template; ")
            lines.append(f"print(generate_readme_template('{proc_name}', '{family}'))")
            lines.append(f'" > "{rel_path}/README.md"')
            lines.append(f'  echo "  Created {rel_path}/README.md"')
            lines.append('fi')
        lines.append("echo 'Done generating READMEs.'")
    else:
        lines.append("echo 'All processors have README files.'")
    lines.append("")
    
    # Section 3: Generate missing validation JSONs
    lines.append("# " + "=" * 70)
    lines.append("# SECTION 3: Generate Missing Validation JSON Files")
    lines.append("# " + "=" * 70)
    lines.append("")
    
    missing_json = [(a.name, a.family, a.path) for a in report.processors 
                    if a.has_validation_dir and not a.has_validation_json]
    if missing_json:
        lines.append("echo 'Generating validation JSON templates...'")
        for proc_name, family, proc_path in missing_json:
            rel_path = proc_path.relative_to(repo_path)
            json_path = f"{rel_path}/validation/{proc_name}_validation.json"
            lines.append(f'if [ ! -f "{json_path}" ]; then')
            lines.append(f'  python3 -c "')
            lines.append(f"import json; ")
            lines.append(f"from cross_family_audit import generate_validation_json_template; ")
            lines.append(f"print(json.dumps(generate_validation_json_template('{proc_name}', '{family}'), indent=2))")
            lines.append(f'" > "{json_path}"')
            lines.append(f'  echo "  Created {json_path}"')
            lines.append('fi')
        lines.append("echo 'Done generating validation JSONs.'")
    else:
        lines.append("echo 'All processors have validation JSON files.'")
    lines.append("")
    
    # Section 4: Create base model class if missing
    lines.append("# " + "=" * 70)
    lines.append("# SECTION 4: Create/Update Common Base Classes")
    lines.append("# " + "=" * 70)
    lines.append("")
    lines.append('COMMON_DIR="$REPO_PATH/common"')
    lines.append('mkdir -p "$COMMON_DIR"')
    lines.append("")
    lines.append('if [ ! -f "$COMMON_DIR/base_model.py" ]; then')
    lines.append('  echo "Creating common/base_model.py..."')
    lines.append('  python3 -c "')
    lines.append("from cross_family_audit import generate_base_model_class; ")
    lines.append("print(generate_base_model_class())")
    lines.append('" > "$COMMON_DIR/base_model.py"')
    lines.append('  echo "  Created common/base_model.py"')
    lines.append('fi')
    lines.append("")
    
    # Section 5: Summary
    lines.append("# " + "=" * 70)
    lines.append("# SUMMARY")
    lines.append("# " + "=" * 70)
    lines.append("")
    lines.append("echo ''")
    lines.append("echo '======================================'")
    lines.append("echo 'Fix script completed!'")
    lines.append("echo '======================================'")
    lines.append("echo ''")
    lines.append("echo 'MANUAL ACTIONS STILL REQUIRED:'")
    lines.append("echo '  1. Update processor models to inherit from BaseProcessorModel'")
    lines.append("echo '  2. Implement missing required methods (analyze, validate, etc.)'")
    lines.append("echo '  3. Fill in validation JSON files with actual test data'")
    lines.append("echo '  4. Review and customize generated README files'")
    lines.append("echo ''")
    lines.append("echo 'Run the audit again to verify fixes:'")
    lines.append("echo '  python3 cross_family_audit.py --verbose'")
    lines.append("")
    
    return '\n'.join(lines)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def run_audit(repo_path: Path, verbose: bool = False) -> AuditReport:
    """Run complete audit of repository"""
    report = AuditReport(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        repo_path=repo_path
    )
    
    # Discover all processors
    processors_by_family = discover_processors(repo_path)
    
    if not processors_by_family:
        report.global_issues.append(Issue(
            processor='[REPO]',
            family='[ALL]',
            severity='error',
            category='structure',
            message=f"No processor families found in {repo_path}",
            fix_available=False,
            fix_action=""
        ))
        return report
    
    # Audit each processor
    for family, processors in processors_by_family.items():
        for proc_name, proc_path in processors:
            audit = audit_processor(proc_name, proc_path, family)
            report.processors.append(audit)
    
    # Check cross-family consistency
    report.global_issues.extend(check_cross_family_consistency(report.processors))
    
    return report


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
        '--fix',
        action='store_true',
        help='Generate fix script'
    )
    parser.add_argument(
        '--report-only',
        action='store_true',
        help='Only generate report, no fix suggestions'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed per-processor output'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file for report (default: stdout)'
    )
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    # Run audit
    print(f"Auditing repository: {repo_path}")
    report = run_audit(repo_path, args.verbose)
    
    # Generate report
    report_text = generate_report(report, args.verbose)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report_text)
        print(f"Report written to: {args.output}")
    else:
        print(report_text)
    
    # Generate fix script if requested
    if args.fix and not args.report_only:
        fix_script = generate_fix_script(report, repo_path)
        fix_path = repo_path / 'fix_consistency_issues.sh'
        with open(fix_path, 'w') as f:
            f.write(fix_script)
        print(f"\nFix script written to: {fix_path}")
        print("Review the script, then run: bash fix_consistency_issues.sh")
    
    # Exit with error code if issues found
    sys.exit(1 if report.total_errors > 0 else 0)


if __name__ == '__main__':
    main()
