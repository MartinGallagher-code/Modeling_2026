#!/usr/bin/env python3
"""
Validation Coverage Completeness Audit for Modeling_2026
=========================================================

This script audits all processor models for validation coverage completeness:

1. Validation JSON presence and schema compliance
2. Source diversity (datasheet, emulator, wikichip, etc.)
3. Timing test coverage (instruction categories, workloads)
4. Accuracy metrics (IPC error < 5% target)
5. Cross-validation status

Usage:
    python validation_coverage_audit.py [repo_path] [--verbose] [--json] [--output FILE]

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any, Tuple
from datetime import datetime
from enum import Enum
import re


# =============================================================================
# CONFIGURATION
# =============================================================================

class ValidationLevel(Enum):
    """Validation completeness levels"""
    NONE = 0          # No validation data
    MINIMAL = 1       # Has JSON but incomplete
    PARTIAL = 2       # Has sources but no tests
    BASIC = 3         # Has tests but accuracy unknown
    VALIDATED = 4     # Has accuracy < 10%
    FULLY_VALIDATED = 5  # Has accuracy < 5% with multiple sources

# Source types and their weights for diversity scoring
SOURCE_TYPES = {
    'datasheet': {'weight': 3.0, 'description': 'Original manufacturer datasheet'},
    'emulator': {'weight': 2.5, 'description': 'Cycle-accurate emulator (MAME, VICE, etc.)'},
    'mame': {'weight': 2.5, 'description': 'MAME emulator source'},
    'vice': {'weight': 2.5, 'description': 'VICE emulator (C64/6502)'},
    'dosbox': {'weight': 2.0, 'description': 'DOSBox emulator (x86)'},
    'wikichip': {'weight': 2.0, 'description': 'WikiChip specifications'},
    'wikipedia': {'weight': 1.5, 'description': 'Wikipedia technical article'},
    'cpu_world': {'weight': 1.5, 'description': 'CPU-World specifications'},
    'bitsavers': {'weight': 2.0, 'description': 'Bitsavers documentation'},
    'hardware': {'weight': 3.0, 'description': 'Real hardware measurement'},
    'academic': {'weight': 2.0, 'description': 'Academic paper/publication'},
    'programming_manual': {'weight': 2.5, 'description': 'Official programming manual'},
    'technical_reference': {'weight': 2.5, 'description': 'Technical reference manual'},
}

# Required validation JSON fields
REQUIRED_JSON_FIELDS = ['processor', 'validation_date', 'sources', 'accuracy']
RECOMMENDED_JSON_FIELDS = ['timing_tests', 'instruction_categories', 'workload_profiles', 'cross_validation']

# Accuracy thresholds
ACCURACY_EXCELLENT = 2.0   # < 2% error
ACCURACY_GOOD = 5.0        # < 5% error
ACCURACY_ACCEPTABLE = 10.0 # < 10% error
ACCURACY_POOR = 20.0       # < 20% error

# Minimum requirements for different validation levels
MIN_SOURCES_BASIC = 1
MIN_SOURCES_VALIDATED = 2
MIN_SOURCES_FULL = 3
MIN_TIMING_TESTS = 3
MIN_WORKLOADS_TESTED = 2


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class ValidationSource:
    """Represents a validation source"""
    type: str
    name: str
    url: Optional[str] = None
    verified: bool = False
    notes: str = ""
    
    @property
    def weight(self) -> float:
        return SOURCE_TYPES.get(self.type, {}).get('weight', 1.0)


@dataclass
class TimingTest:
    """Represents a timing validation test"""
    name: str
    category: str
    expected_cycles: float
    measured_cycles: Optional[float] = None
    error_percent: Optional[float] = None
    passed: bool = False
    source: str = ""


@dataclass
class AccuracyMetrics:
    """Accuracy metrics for a processor"""
    ipc_error_percent: Optional[float] = None
    cpi_error_percent: Optional[float] = None
    timing_error_percent: Optional[float] = None
    overall_accuracy: Optional[float] = None
    validated_workloads: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class ProcessorValidation:
    """Complete validation status for a processor"""
    name: str
    family: str
    path: Path
    
    # File presence
    has_validation_json: bool = False
    has_validated_py: bool = False
    validation_json_path: Optional[Path] = None
    
    # Schema compliance
    has_required_fields: bool = False
    missing_fields: List[str] = field(default_factory=list)
    
    # Sources
    sources: List[ValidationSource] = field(default_factory=list)
    source_types: Set[str] = field(default_factory=set)
    source_diversity_score: float = 0.0
    
    # Timing tests
    timing_tests: List[TimingTest] = field(default_factory=list)
    timing_test_count: int = 0
    timing_tests_passed: int = 0
    
    # Accuracy
    accuracy: Optional[AccuracyMetrics] = None
    
    # Cross-validation
    cross_validated_with: List[str] = field(default_factory=list)
    
    # Computed metrics
    validation_level: ValidationLevel = ValidationLevel.NONE
    completeness_score: float = 0.0
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    def compute_validation_level(self):
        """Compute the validation level based on available data"""
        if not self.has_validation_json:
            self.validation_level = ValidationLevel.NONE
            return
        
        if not self.has_required_fields:
            self.validation_level = ValidationLevel.MINIMAL
            return
        
        if len(self.sources) == 0:
            self.validation_level = ValidationLevel.MINIMAL
            return
        
        if self.timing_test_count == 0:
            self.validation_level = ValidationLevel.PARTIAL
            return
        
        if self.accuracy is None or self.accuracy.ipc_error_percent is None:
            self.validation_level = ValidationLevel.BASIC
            return
        
        error = self.accuracy.ipc_error_percent
        if error <= ACCURACY_GOOD and len(self.sources) >= MIN_SOURCES_FULL:
            self.validation_level = ValidationLevel.FULLY_VALIDATED
        elif error <= ACCURACY_ACCEPTABLE:
            self.validation_level = ValidationLevel.VALIDATED
        else:
            self.validation_level = ValidationLevel.BASIC
    
    def compute_completeness_score(self):
        """Compute overall completeness score (0-100)"""
        score = 0.0
        
        # File presence (20 points)
        if self.has_validation_json:
            score += 10
        if self.has_validated_py:
            score += 10
        
        # Schema compliance (10 points)
        if self.has_required_fields:
            score += 10
        
        # Source diversity (25 points)
        # Score based on number and diversity of sources
        if len(self.sources) >= 1:
            score += 5
        if len(self.sources) >= 2:
            score += 5
        if len(self.sources) >= 3:
            score += 5
        # Bonus for diverse source types
        if len(self.source_types) >= 2:
            score += 5
        if len(self.source_types) >= 3:
            score += 5
        
        # Timing tests (20 points)
        if self.timing_test_count >= 1:
            score += 5
        if self.timing_test_count >= 3:
            score += 5
        if self.timing_test_count >= 5:
            score += 5
        if self.timing_tests_passed >= self.timing_test_count * 0.8:
            score += 5
        
        # Accuracy (25 points)
        if self.accuracy and self.accuracy.ipc_error_percent is not None:
            error = self.accuracy.ipc_error_percent
            if error <= ACCURACY_EXCELLENT:
                score += 25
            elif error <= ACCURACY_GOOD:
                score += 20
            elif error <= ACCURACY_ACCEPTABLE:
                score += 15
            elif error <= ACCURACY_POOR:
                score += 10
            else:
                score += 5
        
        self.completeness_score = min(100.0, score)
    
    def generate_recommendations(self):
        """Generate recommendations for improving validation"""
        self.recommendations = []
        
        if not self.has_validation_json:
            self.recommendations.append("Create validation JSON file")
            return
        
        if not self.has_required_fields:
            self.recommendations.append(f"Add missing fields: {', '.join(self.missing_fields)}")
        
        if len(self.sources) < MIN_SOURCES_BASIC:
            self.recommendations.append("Add at least one validation source")
        elif len(self.sources) < MIN_SOURCES_VALIDATED:
            self.recommendations.append("Add more validation sources for cross-referencing")
        
        # Check for high-value missing sources
        if 'datasheet' not in self.source_types:
            self.recommendations.append("Add original datasheet as source")
        if 'emulator' not in self.source_types and 'mame' not in self.source_types:
            self.recommendations.append("Consider emulator validation (MAME, VICE, etc.)")
        
        if self.timing_test_count < MIN_TIMING_TESTS:
            self.recommendations.append(f"Add more timing tests (have {self.timing_test_count}, need {MIN_TIMING_TESTS})")
        
        if self.accuracy is None or self.accuracy.ipc_error_percent is None:
            self.recommendations.append("Run accuracy measurements and record IPC error")
        elif self.accuracy.ipc_error_percent > ACCURACY_GOOD:
            self.recommendations.append(f"Improve model accuracy (currently {self.accuracy.ipc_error_percent:.1f}%, target <{ACCURACY_GOOD}%)")
        
        if len(self.cross_validated_with) == 0:
            self.recommendations.append("Cross-validate with related processors")


@dataclass
class FamilyValidationSummary:
    """Validation summary for a processor family"""
    name: str
    processor_count: int = 0
    validated_count: int = 0
    fully_validated_count: int = 0
    average_completeness: float = 0.0
    processors: List[ProcessorValidation] = field(default_factory=list)


@dataclass
class RepositoryValidationReport:
    """Complete validation report for the repository"""
    path: Path
    timestamp: str
    families: Dict[str, FamilyValidationSummary] = field(default_factory=dict)
    
    # Aggregate statistics
    total_processors: int = 0
    validated_count: int = 0
    fully_validated_count: int = 0
    average_completeness: float = 0.0
    
    # By validation level
    level_counts: Dict[ValidationLevel, int] = field(default_factory=dict)
    
    # Source statistics
    source_type_counts: Dict[str, int] = field(default_factory=dict)
    
    # Issues summary
    processors_without_validation: List[str] = field(default_factory=list)
    processors_with_poor_accuracy: List[str] = field(default_factory=list)


# =============================================================================
# AUDIT FUNCTIONS
# =============================================================================

def parse_validation_json(json_path: Path) -> Tuple[Dict[str, Any], List[str]]:
    """Parse and validate a validation JSON file"""
    issues = []
    data = {}
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        issues.append(f"Invalid JSON: {e}")
        return {}, issues
    except Exception as e:
        issues.append(f"Failed to read file: {e}")
        return {}, issues
    
    return data, issues


def extract_sources(data: Dict[str, Any]) -> List[ValidationSource]:
    """Extract validation sources from JSON data"""
    sources = []
    
    if 'sources' not in data:
        return sources
    
    for src in data['sources']:
        if isinstance(src, dict):
            source = ValidationSource(
                type=src.get('type', 'unknown'),
                name=src.get('name', 'Unknown'),
                url=src.get('url'),
                verified=src.get('verified', False),
                notes=src.get('notes', '')
            )
            sources.append(source)
        elif isinstance(src, str):
            # Simple string source
            sources.append(ValidationSource(type='unknown', name=src))
    
    return sources


def extract_timing_tests(data: Dict[str, Any]) -> List[TimingTest]:
    """Extract timing tests from JSON data"""
    tests = []
    
    if 'timing_tests' not in data:
        return tests
    
    for test in data['timing_tests']:
        if isinstance(test, dict):
            timing_test = TimingTest(
                name=test.get('name', 'Unknown'),
                category=test.get('category', 'general'),
                expected_cycles=test.get('expected_cycles', 0),
                measured_cycles=test.get('measured_cycles'),
                error_percent=test.get('error_percent'),
                passed=test.get('passed', False),
                source=test.get('source', '')
            )
            tests.append(timing_test)
    
    return tests


def extract_accuracy(data: Dict[str, Any]) -> Optional[AccuracyMetrics]:
    """Extract accuracy metrics from JSON data"""
    if 'accuracy' not in data:
        return None
    
    acc = data['accuracy']
    if not isinstance(acc, dict):
        return None
    
    return AccuracyMetrics(
        ipc_error_percent=acc.get('ipc_error_percent') or acc.get('error_percent'),
        cpi_error_percent=acc.get('cpi_error_percent'),
        timing_error_percent=acc.get('timing_error_percent'),
        overall_accuracy=acc.get('overall_accuracy'),
        validated_workloads=acc.get('validated_workloads', []),
        notes=acc.get('notes', '')
    )


def audit_processor_validation(processor_path: Path, processor_name: str, family: str) -> ProcessorValidation:
    """Audit validation coverage for a single processor"""
    validation = ProcessorValidation(
        name=processor_name,
        family=family,
        path=processor_path
    )
    
    # Check for validation directory and files
    validation_dir = processor_path / 'validation'
    current_dir = processor_path / 'current'
    
    # Find validation JSON
    json_files = list(validation_dir.glob('*_validation.json')) if validation_dir.exists() else []
    if json_files:
        validation.has_validation_json = True
        validation.validation_json_path = json_files[0]
    
    # Find validated Python file
    py_files = list(current_dir.glob('*_validated.py')) if current_dir.exists() else []
    validation.has_validated_py = len(py_files) > 0
    
    # If no validation JSON, we're done
    if not validation.has_validation_json:
        validation.issues.append("No validation JSON file found")
        validation.compute_validation_level()
        validation.compute_completeness_score()
        validation.generate_recommendations()
        return validation
    
    # Parse validation JSON
    data, parse_issues = parse_validation_json(validation.validation_json_path)
    validation.issues.extend(parse_issues)
    
    if not data:
        validation.compute_validation_level()
        validation.compute_completeness_score()
        validation.generate_recommendations()
        return validation
    
    # Check required fields
    validation.missing_fields = [f for f in REQUIRED_JSON_FIELDS if f not in data]
    validation.has_required_fields = len(validation.missing_fields) == 0
    
    if validation.missing_fields:
        validation.issues.append(f"Missing required fields: {', '.join(validation.missing_fields)}")
    
    # Extract sources
    validation.sources = extract_sources(data)
    validation.source_types = {s.type for s in validation.sources}
    
    # Calculate source diversity score
    validation.source_diversity_score = sum(s.weight for s in validation.sources)
    
    if len(validation.sources) == 0:
        validation.issues.append("No validation sources listed")
    
    # Extract timing tests
    validation.timing_tests = extract_timing_tests(data)
    validation.timing_test_count = len(validation.timing_tests)
    validation.timing_tests_passed = sum(1 for t in validation.timing_tests if t.passed)
    
    # Extract accuracy
    validation.accuracy = extract_accuracy(data)
    
    if validation.accuracy:
        if validation.accuracy.ipc_error_percent is not None:
            if validation.accuracy.ipc_error_percent > ACCURACY_ACCEPTABLE:
                validation.issues.append(f"IPC error ({validation.accuracy.ipc_error_percent:.1f}%) exceeds {ACCURACY_ACCEPTABLE}% threshold")
        else:
            validation.issues.append("IPC error not measured")
    else:
        validation.issues.append("No accuracy metrics recorded")
    
    # Extract cross-validation
    if 'cross_validation' in data:
        cv = data['cross_validation']
        if isinstance(cv, list):
            validation.cross_validated_with = cv
        elif isinstance(cv, dict):
            validation.cross_validated_with = cv.get('processors', [])
    
    # Compute derived metrics
    validation.compute_validation_level()
    validation.compute_completeness_score()
    validation.generate_recommendations()
    
    return validation


def audit_family(family_path: Path, family_name: str) -> FamilyValidationSummary:
    """Audit all processors in a family"""
    summary = FamilyValidationSummary(name=family_name)
    
    if not family_path.exists():
        return summary
    
    for item in sorted(family_path.iterdir()):
        if item.is_dir() and not item.name.startswith('.') and item.name not in ['__pycache__', 'common']:
            processor_validation = audit_processor_validation(item, item.name, family_name)
            summary.processors.append(processor_validation)
    
    summary.processor_count = len(summary.processors)
    summary.validated_count = sum(1 for p in summary.processors 
                                   if p.validation_level.value >= ValidationLevel.VALIDATED.value)
    summary.fully_validated_count = sum(1 for p in summary.processors 
                                         if p.validation_level == ValidationLevel.FULLY_VALIDATED)
    
    if summary.processor_count > 0:
        summary.average_completeness = sum(p.completeness_score for p in summary.processors) / summary.processor_count
    
    return summary


def audit_repository(repo_path: Path) -> RepositoryValidationReport:
    """Audit validation coverage for entire repository"""
    report = RepositoryValidationReport(
        path=repo_path,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    # Initialize level counts
    for level in ValidationLevel:
        report.level_counts[level] = 0
    
    # Audit each family
    families = ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']
    
    for family in families:
        family_path = repo_path / family
        if family_path.exists():
            summary = audit_family(family_path, family)
            report.families[family] = summary
    
    # Aggregate statistics
    all_processors = []
    for family_summary in report.families.values():
        all_processors.extend(family_summary.processors)
    
    report.total_processors = len(all_processors)
    
    for processor in all_processors:
        report.level_counts[processor.validation_level] += 1
        
        # Track source types
        for source_type in processor.source_types:
            report.source_type_counts[source_type] = report.source_type_counts.get(source_type, 0) + 1
        
        # Track issues
        if processor.validation_level == ValidationLevel.NONE:
            report.processors_without_validation.append(f"{processor.family}/{processor.name}")
        
        if processor.accuracy and processor.accuracy.ipc_error_percent:
            if processor.accuracy.ipc_error_percent > ACCURACY_ACCEPTABLE:
                report.processors_with_poor_accuracy.append(
                    f"{processor.family}/{processor.name} ({processor.accuracy.ipc_error_percent:.1f}%)"
                )
    
    report.validated_count = report.level_counts.get(ValidationLevel.VALIDATED, 0) + \
                             report.level_counts.get(ValidationLevel.FULLY_VALIDATED, 0)
    report.fully_validated_count = report.level_counts.get(ValidationLevel.FULLY_VALIDATED, 0)
    
    if report.total_processors > 0:
        report.average_completeness = sum(p.completeness_score for p in all_processors) / report.total_processors
    
    return report


# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_text_report(report: RepositoryValidationReport, verbose: bool = False) -> str:
    """Generate human-readable validation coverage report"""
    lines = []
    
    lines.append("=" * 80)
    lines.append("VALIDATION COVERAGE COMPLETENESS REPORT")
    lines.append("=" * 80)
    lines.append(f"Repository: {report.path}")
    lines.append(f"Timestamp: {report.timestamp}")
    lines.append("")
    
    # Executive Summary
    lines.append("EXECUTIVE SUMMARY")
    lines.append("-" * 40)
    lines.append(f"Total Processors: {report.total_processors}")
    lines.append(f"Fully Validated (<5% error, 3+ sources): {report.fully_validated_count} ({100*report.fully_validated_count/max(1,report.total_processors):.1f}%)")
    lines.append(f"Validated (<10% error): {report.validated_count} ({100*report.validated_count/max(1,report.total_processors):.1f}%)")
    lines.append(f"Average Completeness Score: {report.average_completeness:.1f}/100")
    lines.append("")
    
    # Validation Level Distribution
    lines.append("VALIDATION LEVEL DISTRIBUTION")
    lines.append("-" * 40)
    level_names = {
        ValidationLevel.NONE: "No Validation",
        ValidationLevel.MINIMAL: "Minimal (JSON only)",
        ValidationLevel.PARTIAL: "Partial (sources, no tests)",
        ValidationLevel.BASIC: "Basic (tests, accuracy unknown)",
        ValidationLevel.VALIDATED: "Validated (<10% error)",
        ValidationLevel.FULLY_VALIDATED: "Fully Validated (<5% error)",
    }
    for level in ValidationLevel:
        count = report.level_counts.get(level, 0)
        bar = "█" * int(count * 40 / max(1, report.total_processors))
        lines.append(f"  {level_names[level]:30} {count:3} {bar}")
    lines.append("")
    
    # Source Type Coverage
    lines.append("SOURCE TYPE COVERAGE")
    lines.append("-" * 40)
    for source_type, count in sorted(report.source_type_counts.items(), key=lambda x: -x[1]):
        desc = SOURCE_TYPES.get(source_type, {}).get('description', source_type)
        lines.append(f"  {source_type:20} {count:3} processors - {desc}")
    lines.append("")
    
    # Family Summary
    lines.append("BY FAMILY")
    lines.append("-" * 40)
    for family_name, summary in sorted(report.families.items()):
        pct = 100 * summary.validated_count / max(1, summary.processor_count)
        lines.append(f"  {family_name:12} {summary.validated_count:2}/{summary.processor_count:2} validated ({pct:5.1f}%) "
                    f"avg score: {summary.average_completeness:.0f}")
    lines.append("")
    
    # Issues
    if report.processors_without_validation:
        lines.append("⚠️  PROCESSORS WITHOUT VALIDATION")
        lines.append("-" * 40)
        for proc in report.processors_without_validation[:20]:
            lines.append(f"  • {proc}")
        if len(report.processors_without_validation) > 20:
            lines.append(f"  ... and {len(report.processors_without_validation) - 20} more")
        lines.append("")
    
    if report.processors_with_poor_accuracy:
        lines.append("⚠️  PROCESSORS WITH POOR ACCURACY (>10% error)")
        lines.append("-" * 40)
        for proc in report.processors_with_poor_accuracy[:20]:
            lines.append(f"  • {proc}")
        if len(report.processors_with_poor_accuracy) > 20:
            lines.append(f"  ... and {len(report.processors_with_poor_accuracy) - 20} more")
        lines.append("")
    
    # Detailed per-processor (verbose mode)
    if verbose:
        lines.append("DETAILED PROCESSOR VALIDATION STATUS")
        lines.append("-" * 40)
        
        for family_name, summary in sorted(report.families.items()):
            lines.append(f"\n{family_name.upper()}/")
            for proc in sorted(summary.processors, key=lambda x: -x.completeness_score):
                level_icon = {
                    ValidationLevel.NONE: "❌",
                    ValidationLevel.MINIMAL: "🔸",
                    ValidationLevel.PARTIAL: "🔶",
                    ValidationLevel.BASIC: "🔷",
                    ValidationLevel.VALIDATED: "✅",
                    ValidationLevel.FULLY_VALIDATED: "🌟",
                }[proc.validation_level]
                
                accuracy_str = f"{proc.accuracy.ipc_error_percent:.1f}%" if proc.accuracy and proc.accuracy.ipc_error_percent else "N/A"
                
                lines.append(f"  {level_icon} {proc.name:20} Score:{proc.completeness_score:5.0f}  "
                           f"Sources:{len(proc.sources):2}  Tests:{proc.timing_test_count:2}  "
                           f"Error:{accuracy_str:>6}")
                
                if proc.recommendations:
                    for rec in proc.recommendations[:3]:
                        lines.append(f"      → {rec}")
    
    # Recommendations Summary
    lines.append("")
    lines.append("TOP RECOMMENDATIONS")
    lines.append("-" * 40)
    
    # Count recommendation types
    rec_counts = {}
    for family_summary in report.families.values():
        for proc in family_summary.processors:
            for rec in proc.recommendations:
                # Simplify recommendation to category
                if "datasheet" in rec.lower():
                    key = "Add datasheet sources"
                elif "emulator" in rec.lower():
                    key = "Add emulator validation"
                elif "timing test" in rec.lower():
                    key = "Add more timing tests"
                elif "accuracy" in rec.lower() or "error" in rec.lower():
                    key = "Improve model accuracy"
                elif "source" in rec.lower():
                    key = "Add more sources"
                elif "validation json" in rec.lower() or "create" in rec.lower():
                    key = "Create validation files"
                else:
                    key = rec[:50]
                rec_counts[key] = rec_counts.get(key, 0) + 1
    
    for rec, count in sorted(rec_counts.items(), key=lambda x: -x[1])[:10]:
        lines.append(f"  [{count:2} processors] {rec}")
    
    lines.append("")
    lines.append("=" * 80)
    lines.append("END OF REPORT")
    lines.append("=" * 80)
    
    return '\n'.join(lines)


def generate_json_report(report: RepositoryValidationReport) -> dict:
    """Generate JSON validation coverage report"""
    return {
        'timestamp': report.timestamp,
        'path': str(report.path),
        'summary': {
            'total_processors': report.total_processors,
            'validated_count': report.validated_count,
            'fully_validated_count': report.fully_validated_count,
            'average_completeness': round(report.average_completeness, 1),
            'validation_rate_percent': round(100 * report.validated_count / max(1, report.total_processors), 1),
        },
        'level_distribution': {
            level.name: count for level, count in report.level_counts.items()
        },
        'source_coverage': report.source_type_counts,
        'families': {
            name: {
                'processor_count': summary.processor_count,
                'validated_count': summary.validated_count,
                'fully_validated_count': summary.fully_validated_count,
                'average_completeness': round(summary.average_completeness, 1),
                'processors': [
                    {
                        'name': p.name,
                        'validation_level': p.validation_level.name,
                        'completeness_score': round(p.completeness_score, 1),
                        'sources_count': len(p.sources),
                        'timing_tests_count': p.timing_test_count,
                        'ipc_error_percent': p.accuracy.ipc_error_percent if p.accuracy else None,
                        'issues': p.issues,
                        'recommendations': p.recommendations,
                    }
                    for p in summary.processors
                ]
            }
            for name, summary in report.families.items()
        },
        'issues': {
            'processors_without_validation': report.processors_without_validation,
            'processors_with_poor_accuracy': report.processors_with_poor_accuracy,
        }
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Validation Coverage Completeness Audit for Modeling_2026'
    )
    parser.add_argument(
        'repo_path',
        nargs='?',
        default='.',
        help='Path to Modeling_2026 repository'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed per-processor information'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )
    parser.add_argument(
        '--output', '-o',
        help='Write report to file'
    )
    parser.add_argument(
        '--min-score',
        type=float,
        default=0,
        help='Only show processors below this completeness score'
    )
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Path does not exist: {repo_path}")
        sys.exit(1)
    
    print(f"Auditing validation coverage: {repo_path}")
    print("")
    
    report = audit_repository(repo_path)
    
    if args.json:
        output = json.dumps(generate_json_report(report), indent=2)
    else:
        output = generate_text_report(report, args.verbose)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Report written to: {args.output}")
    else:
        print(output)
    
    # Exit code based on validation coverage
    if report.validated_count < report.total_processors * 0.5:
        sys.exit(1)  # Less than 50% validated
    sys.exit(0)


if __name__ == '__main__':
    main()
