#!/usr/bin/env python3
"""
Era-Specific Architecture Audit for Modeling_2026
=================================================

This script audits all processor models to verify they use the correct
architectural pattern for their era:

1. Sequential (1971-1976): Simple serial M/M/1 chain
2. Prefetch Queue (1976-1982): Parallel BIU/EU queues
3. Pipelined (1979-1985): Multi-stage pipeline network
4. Cache/RISC (1983-1988): Cache hierarchy + deep pipeline

Usage:
    python era_architecture_audit.py [repo_path] [--verbose] [--fix]

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
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from collections import defaultdict

from era_architectures import (
    ProcessorEra,
    ERA_DEFINITIONS,
    PROCESSOR_ERA_MAP,
    PROCESSOR_ALIASES,
    SKIP_DIRECTORIES,
    get_processor_era,
    get_era_definition,
    get_processors_by_era,
    should_skip_directory,
    is_valid_processor,
    ERA_TEMPLATES,
)


# =============================================================================
# ARCHITECTURAL PATTERN DETECTION
# =============================================================================

# Keywords that indicate each architectural pattern
ERA_KEYWORDS = {
    ProcessorEra.SEQUENTIAL: [
        'sequential', 'serial', 'no_pipeline', 'simple_execution',
        'fetch_decode_execute', 'single_stage', 'no_overlap',
    ],
    ProcessorEra.PREFETCH_QUEUE: [
        'prefetch', 'biu', 'eu', 'bus_interface', 'execution_unit',
        'instruction_queue', 'prefetch_queue', 'bus_contention',
    ],
    ProcessorEra.PIPELINED: [
        'pipeline', 'pipelined', 'pipeline_stages', 'if_id_ex',
        'fetch_decode_execute_memory_writeback', 'hazard', 'stall',
        'instruction_cache', 'microcoded',
    ],
    ProcessorEra.CACHE_RISC: [
        'risc', 'cache', 'icache', 'dcache', 'load_store',
        'register_window', 'delayed_branch', 'single_cycle',
        'cache_hierarchy', 'branch_prediction',
    ],
}

# Architectural features to check for
ERA_FEATURES = {
    ProcessorEra.SEQUENTIAL: {
        'required': ['instruction_categories', 'analyze'],
        'forbidden': ['prefetch_queue', 'pipeline_stages', 'icache', 'dcache'],
        'expected_classes': ['Sequential', 'Simple', 'Basic'],
    },
    ProcessorEra.PREFETCH_QUEUE: {
        'required': ['prefetch', 'bus_cycle'],  # Removed biu/eu - too generic
        'forbidden': ['icache', 'dcache', 'pipeline_depth'],
        'expected_classes': ['Prefetch', 'BIU', 'Queue'],
    },
    ProcessorEra.PIPELINED: {
        'required': ['pipeline', 'stages'],
        'forbidden': ['prefetch_queue'],  # Removed biu/eu - too generic
        'expected_classes': ['Pipeline', 'Pipelined'],
    },
    ProcessorEra.CACHE_RISC: {
        'required': ['cache', 'pipeline'],
        'forbidden': ['prefetch_queue'],  # Removed biu/eu - too generic
        'expected_classes': ['RISC', 'Cache'],
    },
}


@dataclass
class ArchitectureIssue:
    """Represents an architecture audit issue"""
    processor: str
    family: str
    expected_era: ProcessorEra
    detected_era: Optional[ProcessorEra]
    severity: str  # 'error', 'warning', 'info'
    category: str
    message: str
    fix_available: bool = False


@dataclass
class ProcessorArchitectureAudit:
    """Audit results for a single processor's architecture"""
    processor: str
    family: str
    path: Path
    expected_era: ProcessorEra
    detected_era: Optional[ProcessorEra]
    confidence: float  # 0.0 to 1.0
    issues: List[ArchitectureIssue] = field(default_factory=list)
    
    # Detected patterns
    keywords_found: Dict[ProcessorEra, List[str]] = field(default_factory=dict)
    features_found: List[str] = field(default_factory=list)
    missing_features: List[str] = field(default_factory=list)
    forbidden_features: List[str] = field(default_factory=list)
    
    @property
    def is_correct_architecture(self) -> bool:
        return self.expected_era == self.detected_era and self.confidence > 0.5
    
    @property
    def error_count(self) -> int:
        return len([i for i in self.issues if i.severity == 'error'])


def normalize_processor_name(name: str) -> str:
    """Normalize processor name for matching"""
    normalized = name.lower().replace('-', '_').replace(' ', '_')
    # Remove common prefixes
    for prefix in ['i', 'm', 'mos', 'wdc', 'mc', 'z', 'am', 'ns', 'tms', 'we', 'rca']:
        if normalized.startswith(prefix) and len(normalized) > len(prefix):
            # Check if it's a prefix (followed by number)
            rest = normalized[len(prefix):]
            if rest and rest[0].isdigit():
                pass  # Keep prefix for numbers like i8086
    return normalized


def detect_architecture_from_code(source_code: str) -> Tuple[Optional[ProcessorEra], float, Dict]:
    """
    Analyze source code to detect which architectural pattern is used.
    
    Returns:
        (detected_era, confidence, details)
    """
    source_lower = source_code.lower()
    
    # Count keyword matches for each era
    keyword_matches = {}
    for era, keywords in ERA_KEYWORDS.items():
        matches = []
        for keyword in keywords:
            if keyword in source_lower:
                matches.append(keyword)
        keyword_matches[era] = matches
    
    # Count feature matches
    feature_scores = {}
    for era, features in ERA_FEATURES.items():
        required_found = sum(1 for f in features['required'] if f in source_lower)
        forbidden_found = sum(1 for f in features['forbidden'] if f in source_lower)
        
        # Score = required found - forbidden found
        score = required_found - forbidden_found * 2
        feature_scores[era] = {
            'score': score,
            'required_found': required_found,
            'required_total': len(features['required']),
            'forbidden_found': forbidden_found,
        }
    
    # Combine scores
    combined_scores = {}
    for era in ProcessorEra:
        keyword_score = len(keyword_matches.get(era, []))
        feature_score = feature_scores.get(era, {}).get('score', 0)
        combined_scores[era] = keyword_score * 2 + feature_score * 3
    
    # Find best match
    if all(s <= 0 for s in combined_scores.values()):
        return None, 0.0, {'keyword_matches': keyword_matches, 'feature_scores': feature_scores}
    
    best_era = max(combined_scores, key=combined_scores.get)
    best_score = combined_scores[best_era]
    
    # Calculate confidence
    total_score = sum(max(0, s) for s in combined_scores.values())
    confidence = best_score / total_score if total_score > 0 else 0.0
    
    return best_era, confidence, {
        'keyword_matches': keyword_matches,
        'feature_scores': feature_scores,
        'combined_scores': combined_scores,
    }


def audit_processor_architecture(
    processor_name: str,
    processor_path: Path,
    family: str
) -> ProcessorArchitectureAudit:
    """Audit a single processor's architectural pattern"""
    
    # Get expected era
    expected_era = get_processor_era(processor_name)
    if not expected_era:
        # Try to find by path/name matching
        for key in PROCESSOR_ERA_MAP:
            if key in processor_name.lower() or processor_name.lower() in key:
                expected_era = PROCESSOR_ERA_MAP[key]
                break
    
    audit = ProcessorArchitectureAudit(
        processor=processor_name,
        family=family,
        path=processor_path,
        expected_era=expected_era or ProcessorEra.SEQUENTIAL,  # Default
        detected_era=None,
        confidence=0.0,
    )
    
    if not expected_era:
        audit.issues.append(ArchitectureIssue(
            processor=processor_name,
            family=family,
            expected_era=ProcessorEra.SEQUENTIAL,
            detected_era=None,
            severity='warning',
            category='era_mapping',
            message=f"Processor not found in era mapping - defaulting to SEQUENTIAL",
            fix_available=True,
        ))
    
    # Find validated model file
    current_path = processor_path / 'current'
    if not current_path.exists():
        audit.issues.append(ArchitectureIssue(
            processor=processor_name,
            family=family,
            expected_era=audit.expected_era,
            detected_era=None,
            severity='error',
            category='missing_model',
            message="No current/ directory found",
            fix_available=False,
        ))
        return audit
    
    py_files = list(current_path.glob('*_validated.py'))
    if not py_files:
        audit.issues.append(ArchitectureIssue(
            processor=processor_name,
            family=family,
            expected_era=audit.expected_era,
            detected_era=None,
            severity='error',
            category='missing_model',
            message="No *_validated.py file found",
            fix_available=False,
        ))
        return audit
    
    # Analyze the model file
    py_file = py_files[0]
    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        detected_era, confidence, details = detect_architecture_from_code(source_code)
        
        audit.detected_era = detected_era
        audit.confidence = confidence
        audit.keywords_found = details.get('keyword_matches', {})
        
        # Check for era mismatch
        if detected_era and detected_era != audit.expected_era:
            era_def = get_era_definition(audit.expected_era)
            detected_def = get_era_definition(detected_era) if detected_era else None
            
            audit.issues.append(ArchitectureIssue(
                processor=processor_name,
                family=family,
                expected_era=audit.expected_era,
                detected_era=detected_era,
                severity='error',
                category='era_mismatch',
                message=f"Architecture mismatch: expected {era_def.name} ({audit.expected_era.name}), "
                       f"detected {detected_def.name if detected_def else 'unknown'} ({detected_era.name if detected_era else 'N/A'})",
                fix_available=True,
            ))
        elif not detected_era:
            audit.issues.append(ArchitectureIssue(
                processor=processor_name,
                family=family,
                expected_era=audit.expected_era,
                detected_era=None,
                severity='warning',
                category='unrecognized_architecture',
                message="Could not detect architectural pattern from code",
                fix_available=True,
            ))
        
        # Check for missing required features
        if audit.expected_era:
            expected_features = ERA_FEATURES.get(audit.expected_era, {})
            source_lower = source_code.lower()
            
            for feature in expected_features.get('required', []):
                if feature not in source_lower:
                    audit.missing_features.append(feature)
            
            for feature in expected_features.get('forbidden', []):
                if feature in source_lower:
                    audit.forbidden_features.append(feature)
            
            if audit.missing_features:
                audit.issues.append(ArchitectureIssue(
                    processor=processor_name,
                    family=family,
                    expected_era=audit.expected_era,
                    detected_era=detected_era,
                    severity='warning',
                    category='missing_features',
                    message=f"Missing expected features for {audit.expected_era.name}: {audit.missing_features}",
                    fix_available=True,
                ))
            
            if audit.forbidden_features:
                audit.issues.append(ArchitectureIssue(
                    processor=processor_name,
                    family=family,
                    expected_era=audit.expected_era,
                    detected_era=detected_era,
                    severity='warning',
                    category='forbidden_features',
                    message=f"Contains features not appropriate for {audit.expected_era.name}: {audit.forbidden_features}",
                    fix_available=False,
                ))
        
    except Exception as e:
        audit.issues.append(ArchitectureIssue(
            processor=processor_name,
            family=family,
            expected_era=audit.expected_era,
            detected_era=None,
            severity='error',
            category='parse_error',
            message=f"Failed to analyze model file: {e}",
            fix_available=False,
        ))
    
    return audit


def discover_processors(repo_path: Path) -> Dict[str, List[Tuple[str, Path]]]:
    """Discover all processor directories organized by family"""
    families = ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']
    processors_by_family = defaultdict(list)
    
    for family in families:
        family_path = repo_path / family
        if family_path.exists() and family_path.is_dir():
            for item in family_path.iterdir():
                if item.is_dir() and not should_skip_directory(item.name):
                    processors_by_family[family].append((item.name, item))
    
    return dict(processors_by_family)


@dataclass
class EraAuditReport:
    """Complete era architecture audit report"""
    timestamp: str
    repo_path: Path
    audits: List[ProcessorArchitectureAudit] = field(default_factory=list)
    
    @property
    def total_processors(self) -> int:
        return len(self.audits)
    
    @property
    def correct_architecture(self) -> int:
        return len([a for a in self.audits if a.is_correct_architecture])
    
    @property
    def mismatched(self) -> int:
        return len([a for a in self.audits if a.detected_era and a.detected_era != a.expected_era])
    
    @property
    def undetected(self) -> int:
        return len([a for a in self.audits if not a.detected_era])
    
    @property
    def total_errors(self) -> int:
        return sum(a.error_count for a in self.audits)


def run_era_audit(repo_path: Path, verbose: bool = False) -> EraAuditReport:
    """Run complete era architecture audit"""
    report = EraAuditReport(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        repo_path=repo_path,
    )
    
    processors_by_family = discover_processors(repo_path)
    
    for family, processors in processors_by_family.items():
        for proc_name, proc_path in processors:
            audit = audit_processor_architecture(proc_name, proc_path, family)
            report.audits.append(audit)
            
            if verbose:
                status = "✓" if audit.is_correct_architecture else "✗"
                print(f"  {status} {family}/{proc_name}: {audit.expected_era.name} -> {audit.detected_era.name if audit.detected_era else 'UNKNOWN'} ({audit.confidence:.0%})")
    
    return report


def generate_era_report(report: EraAuditReport, verbose: bool = False) -> str:
    """Generate human-readable era audit report"""
    lines = []
    
    lines.append("=" * 70)
    lines.append("ERA-SPECIFIC ARCHITECTURE AUDIT REPORT")
    lines.append(f"Repository: {report.repo_path}")
    lines.append(f"Timestamp: {report.timestamp}")
    lines.append("=" * 70)
    lines.append("")
    
    # Summary
    lines.append("SUMMARY")
    lines.append("-" * 40)
    lines.append(f"Total Processors: {report.total_processors}")
    lines.append(f"Correct Architecture: {report.correct_architecture} ({report.correct_architecture/report.total_processors*100:.0f}%)")
    lines.append(f"Architecture Mismatch: {report.mismatched}")
    lines.append(f"Undetected Pattern: {report.undetected}")
    lines.append(f"Total Errors: {report.total_errors}")
    lines.append("")
    
    # By era breakdown
    lines.append("BY ERA")
    lines.append("-" * 40)
    for era in ProcessorEra:
        era_audits = [a for a in report.audits if a.expected_era == era]
        correct = len([a for a in era_audits if a.is_correct_architecture])
        era_def = get_era_definition(era)
        lines.append(f"  {era_def.name} ({era_def.year_start}-{era_def.year_end})")
        lines.append(f"    Processors: {len(era_audits)}, Correct: {correct}, Issues: {len(era_audits) - correct}")
    lines.append("")
    
    # Issues
    errors = [i for a in report.audits for i in a.issues if i.severity == 'error']
    warnings = [i for a in report.audits for i in a.issues if i.severity == 'warning']
    
    if errors:
        lines.append("ARCHITECTURE ERRORS (Must Fix)")
        lines.append("-" * 40)
        for issue in errors:
            lines.append(f"  ❌ {issue.family}/{issue.processor}: {issue.message}")
        lines.append("")
    
    if warnings:
        lines.append("ARCHITECTURE WARNINGS")
        lines.append("-" * 40)
        for issue in warnings[:20]:
            lines.append(f"  ⚠️  {issue.family}/{issue.processor}: {issue.message}")
        if len(warnings) > 20:
            lines.append(f"  ... and {len(warnings) - 20} more warnings")
        lines.append("")
    
    # Detailed by processor (verbose)
    if verbose:
        lines.append("DETAILED PROCESSOR AUDIT")
        lines.append("-" * 40)
        
        for era in ProcessorEra:
            era_audits = [a for a in report.audits if a.expected_era == era]
            if era_audits:
                era_def = get_era_definition(era)
                lines.append(f"\n{era_def.name} ({era.name}):")
                
                for audit in era_audits:
                    status = "✓" if audit.is_correct_architecture else "✗"
                    det = audit.detected_era.name if audit.detected_era else "UNKNOWN"
                    lines.append(f"  {status} {audit.family}/{audit.processor}: detected={det} ({audit.confidence:.0%})")
                    
                    if audit.missing_features:
                        lines.append(f"      Missing: {audit.missing_features}")
                    if audit.forbidden_features:
                        lines.append(f"      Forbidden: {audit.forbidden_features}")
    
    lines.append("")
    lines.append("=" * 70)
    lines.append("END OF REPORT")
    lines.append("=" * 70)
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Era-Specific Architecture Audit for Modeling_2026'
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
        help='Show detailed per-processor output'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file for report'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    print(f"Running era architecture audit on: {repo_path}")
    print("")
    
    report = run_era_audit(repo_path, args.verbose)
    
    if args.json:
        # JSON output
        output = {
            'timestamp': report.timestamp,
            'repo_path': str(report.repo_path),
            'summary': {
                'total': report.total_processors,
                'correct': report.correct_architecture,
                'mismatched': report.mismatched,
                'undetected': report.undetected,
                'errors': report.total_errors,
            },
            'processors': [{
                'name': a.processor,
                'family': a.family,
                'expected_era': a.expected_era.name,
                'detected_era': a.detected_era.name if a.detected_era else None,
                'confidence': a.confidence,
                'correct': a.is_correct_architecture,
                'issues': [{'severity': i.severity, 'message': i.message} for i in a.issues],
            } for a in report.audits],
        }
        report_text = json.dumps(output, indent=2)
    else:
        report_text = generate_era_report(report, args.verbose)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report_text)
        print(f"Report written to: {args.output}")
    else:
        print(report_text)
    
    sys.exit(1 if report.total_errors > 0 else 0)


if __name__ == '__main__':
    main()
