#!/usr/bin/env python3
"""
Calibration Report Generator for Modeling_2026
===============================================

Generates detailed calibration recommendations for processor models
based on the gap between predicted and expected CPI values.

Features:
1. Identifies which timing parameters need adjustment
2. Provides specific recommendations per processor
3. Groups by era/architecture for systematic fixes
4. Exports actionable reports

Usage:
    python calibration_report.py [repo_path] [--output report.md]

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import json
import argparse
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass


# Expected CPI values from datasheets
EXPECTED_CPI = {
    'i4004': 10.8, 'i4040': 10.5, 'i8008': 11.0, 'i8080': 9.2, 'i8085': 5.5,
    'i8086': 4.5, 'i8088': 5.2, 'i80186': 4.0, 'i80188': 4.2, 'i80286': 4.0,
    'i80386': 4.5, 'i80486': 2.0, 'pentium': 1.0, 'i860': 1.2,
    'mos6502': 3.5, 'mos6510': 3.5, 'wdc65c02': 3.2, 'wdc65816': 3.8,
    'm6800': 4.0, 'm6801': 3.8, 'm6809': 3.5, 'm68000': 6.5, 'm68008': 7.0,
    'm68010': 6.0, 'm68020': 3.5, 'm68030': 3.0, 'm68040': 2.0,
    'z80': 5.5, 'z80a': 5.5, 'z80b': 5.5, 'z180': 4.5, 'z8000': 4.5,
    'arm1': 1.8, 'arm2': 1.5, 'arm3': 1.4, 'sparc': 1.5, 'sun_spark': 1.5,
    'am2901': 1.0, 'f8': 5.0, 'rca1802': 8.0, 'scmp': 6.0,
    'signetics2650': 5.5, 'tms9900': 4.5, 'ns32016': 4.0, 't414': 2.0,
    'r2000': 1.5, 'alpha21064': 1.0, 'hp_pa_risc': 1.2,
}

# Architecture eras with typical CPI ranges
ERA_CHARACTERISTICS = {
    'sequential': {
        'years': '1971-1976',
        'typical_cpi_range': (5.0, 15.0),
        'description': 'Sequential execution, no prefetch',
        'processors': ['i4004', 'i4040', 'i8008', 'i8080', 'i8085', 'mos6502', 'mos6510', 'm6800', 'f8', 'rca1802', 'scmp', 'signetics2650', 'am2901'],
    },
    'prefetch_queue': {
        'years': '1976-1982',
        'typical_cpi_range': (3.0, 7.0),
        'description': 'Instruction prefetch queue, bus/EU parallelism',
        'processors': ['i8086', 'i8088', 'i80186', 'i80188', 'z80', 'z80a', 'z80b', 'z180', 'z8000', 'm6809', 'wdc65816', 'tms9900'],
    },
    'pipelined': {
        'years': '1982-1986',
        'typical_cpi_range': (2.0, 5.0),
        'description': 'Instruction pipeline, protection modes',
        'processors': ['i80286', 'm68000', 'm68008', 'm68010', 'm68020', 'ns32016', 'wdc65c02'],
    },
    'cache_risc': {
        'years': '1985+',
        'typical_cpi_range': (1.0, 3.0),
        'description': 'On-chip cache, RISC-like execution',
        'processors': ['i80386', 'i80486', 'pentium', 'i860', 'm68030', 'm68040', 'arm1', 'arm2', 'arm3', 'sparc', 'sun_spark', 'r2000', 't414', 'alpha21064', 'hp_pa_risc'],
    },
}


@dataclass
class ProcessorCalibrationStatus:
    """Status of a processor's calibration"""
    name: str
    family: str
    era: str
    expected_cpi: float
    predicted_cpi: Optional[float]
    error_percent: Optional[float]
    status: str  # 'validated', 'needs_decrease', 'needs_increase', 'error'
    recommendation: str


def load_model(model_path: Path, repo_root: Path) -> Tuple[Any, Optional[str]]:
    """Load a processor model"""
    try:
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        
        spec = importlib.util.spec_from_file_location("model", model_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        for name in dir(module):
            if name.endswith('Model') and name != 'BaseProcessorModel':
                obj = getattr(module, name)
                if isinstance(obj, type):
                    return obj(), None
        return None, "No Model class found"
    except Exception as e:
        return None, str(e)


def get_processor_era(proc_name: str) -> str:
    """Determine which era a processor belongs to"""
    for era, info in ERA_CHARACTERISTICS.items():
        if proc_name in info['processors']:
            return era
    return 'unknown'


def analyze_processor(
    proc_name: str,
    family: str,
    model_path: Path,
    repo_root: Path
) -> ProcessorCalibrationStatus:
    """Analyze a single processor's calibration status"""
    
    expected_cpi = EXPECTED_CPI.get(proc_name)
    era = get_processor_era(proc_name)
    
    if not expected_cpi:
        return ProcessorCalibrationStatus(
            name=proc_name, family=family, era=era,
            expected_cpi=0, predicted_cpi=None, error_percent=None,
            status='no_expected',
            recommendation="Add expected CPI to database"
        )
    
    model, error = load_model(model_path, repo_root)
    if not model:
        return ProcessorCalibrationStatus(
            name=proc_name, family=family, era=era,
            expected_cpi=expected_cpi, predicted_cpi=None, error_percent=None,
            status='load_error',
            recommendation=f"Fix model loading: {error}"
        )
    
    try:
        result = model.analyze('typical')
        predicted_cpi = result.cpi if result else None
    except Exception as e:
        return ProcessorCalibrationStatus(
            name=proc_name, family=family, era=era,
            expected_cpi=expected_cpi, predicted_cpi=None, error_percent=None,
            status='analysis_error',
            recommendation=f"Fix analyze() method: {str(e)[:50]}"
        )
    
    if not predicted_cpi or predicted_cpi <= 0:
        return ProcessorCalibrationStatus(
            name=proc_name, family=family, era=era,
            expected_cpi=expected_cpi, predicted_cpi=None, error_percent=None,
            status='invalid_cpi',
            recommendation="Model returns invalid CPI"
        )
    
    error_percent = (predicted_cpi - expected_cpi) / expected_cpi * 100
    
    if abs(error_percent) < 5:
        status = 'validated'
        recommendation = "✓ Within 5% tolerance - fully validated"
    elif abs(error_percent) < 10:
        status = 'close'
        recommendation = "Minor adjustment needed - within 10%"
    elif error_percent > 0:
        # Predicted CPI is too high
        status = 'needs_decrease'
        scale = expected_cpi / predicted_cpi
        recommendation = f"DECREASE timing: scale all base_cycles by {scale:.2f}x"
    else:
        # Predicted CPI is too low
        status = 'needs_increase'
        scale = expected_cpi / predicted_cpi
        recommendation = f"INCREASE timing: scale all base_cycles by {scale:.2f}x"
    
    return ProcessorCalibrationStatus(
        name=proc_name, family=family, era=era,
        expected_cpi=expected_cpi, predicted_cpi=predicted_cpi,
        error_percent=error_percent, status=status,
        recommendation=recommendation
    )


def generate_report(repo_path: Path) -> Dict[str, Any]:
    """Generate full calibration report"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total': 0,
            'validated': 0,
            'close': 0,
            'needs_work': 0,
            'errors': 0,
        },
        'by_era': {},
        'by_family': {},
        'processors': [],
    }
    
    families = ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']
    
    for family in families:
        family_path = repo_path / family
        if not family_path.exists():
            continue
        
        for proc_dir in sorted(family_path.iterdir()):
            if not proc_dir.is_dir():
                continue
            
            proc_name = proc_dir.name
            model_path = proc_dir / 'current' / f'{proc_name}_validated.py'
            
            if not model_path.exists():
                continue
            
            status = analyze_processor(proc_name, family, model_path, repo_path)
            report['processors'].append(status)
            report['summary']['total'] += 1
            
            # Count by status
            if status.status == 'validated':
                report['summary']['validated'] += 1
            elif status.status == 'close':
                report['summary']['close'] += 1
            elif status.status in ['needs_decrease', 'needs_increase']:
                report['summary']['needs_work'] += 1
            else:
                report['summary']['errors'] += 1
            
            # Group by era
            era = status.era
            if era not in report['by_era']:
                report['by_era'][era] = []
            report['by_era'][era].append(status)
            
            # Group by family
            if family not in report['by_family']:
                report['by_family'][family] = []
            report['by_family'][family].append(status)
    
    return report


def print_report(report: Dict[str, Any]):
    """Print formatted report to stdout"""
    print()
    print("=" * 80)
    print("CALIBRATION STATUS REPORT")
    print("=" * 80)
    print(f"Generated: {report['timestamp']}")
    print()
    
    s = report['summary']
    print("SUMMARY")
    print("-" * 40)
    print(f"Total processors:     {s['total']}")
    print(f"Fully validated (<5%): {s['validated']}")
    print(f"Close (<10%):         {s['close']}")
    print(f"Needs calibration:    {s['needs_work']}")
    print(f"Errors:               {s['errors']}")
    print()
    
    # By Era
    print("BY ARCHITECTURE ERA")
    print("-" * 80)
    for era, era_info in ERA_CHARACTERISTICS.items():
        processors = report['by_era'].get(era, [])
        if not processors:
            continue
        
        validated = sum(1 for p in processors if p.status == 'validated')
        close = sum(1 for p in processors if p.status == 'close')
        total = len(processors)
        
        print(f"\n{era.upper()} ({era_info['years']}) - {era_info['description']}")
        print(f"Expected CPI range: {era_info['typical_cpi_range'][0]:.1f} - {era_info['typical_cpi_range'][1]:.1f}")
        print(f"Status: {validated}/{total} validated, {close}/{total} close")
        print()
        
        # Show processors needing work
        needs_work = [p for p in processors if p.status in ['needs_decrease', 'needs_increase']]
        if needs_work:
            print("  Needs calibration:")
            for p in sorted(needs_work, key=lambda x: abs(x.error_percent or 0), reverse=True)[:5]:
                direction = "↓" if p.status == 'needs_decrease' else "↑"
                print(f"    {direction} {p.name}: {p.predicted_cpi:.2f} → {p.expected_cpi:.2f} ({p.error_percent:+.1f}%)")
    
    print()
    print("=" * 80)
    print("DETAILED RECOMMENDATIONS")
    print("=" * 80)
    
    # Group by recommendation type
    needs_decrease = [p for p in report['processors'] if p.status == 'needs_decrease']
    needs_increase = [p for p in report['processors'] if p.status == 'needs_increase']
    
    if needs_decrease:
        print("\n🔽 DECREASE TIMING (predicted CPI too high):")
        print("-" * 60)
        for p in sorted(needs_decrease, key=lambda x: x.error_percent, reverse=True)[:10]:
            scale = p.expected_cpi / p.predicted_cpi
            print(f"  {p.family}/{p.name}:")
            print(f"    Predicted: {p.predicted_cpi:.2f}, Expected: {p.expected_cpi:.2f}")
            print(f"    Action: Multiply all base_cycles by {scale:.2f}")
    
    if needs_increase:
        print("\n🔼 INCREASE TIMING (predicted CPI too low):")
        print("-" * 60)
        for p in sorted(needs_increase, key=lambda x: x.error_percent)[:10]:
            scale = p.expected_cpi / p.predicted_cpi
            print(f"  {p.family}/{p.name}:")
            print(f"    Predicted: {p.predicted_cpi:.2f}, Expected: {p.expected_cpi:.2f}")
            print(f"    Action: Multiply all base_cycles by {scale:.2f}")


def export_markdown(report: Dict[str, Any], output_path: Path):
    """Export report as Markdown file"""
    lines = [
        "# Calibration Status Report",
        "",
        f"Generated: {report['timestamp']}",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total processors | {report['summary']['total']} |",
        f"| Fully validated (<5%) | {report['summary']['validated']} |",
        f"| Close (<10%) | {report['summary']['close']} |",
        f"| Needs calibration | {report['summary']['needs_work']} |",
        f"| Errors | {report['summary']['errors']} |",
        "",
        "## By Architecture Era",
        "",
    ]
    
    for era, era_info in ERA_CHARACTERISTICS.items():
        processors = report['by_era'].get(era, [])
        if not processors:
            continue
        
        validated = sum(1 for p in processors if p.status == 'validated')
        lines.extend([
            f"### {era.replace('_', ' ').title()} ({era_info['years']})",
            "",
            f"*{era_info['description']}*",
            "",
            f"Expected CPI: {era_info['typical_cpi_range'][0]:.1f} - {era_info['typical_cpi_range'][1]:.1f}",
            "",
            f"Validated: {validated}/{len(processors)}",
            "",
            "| Processor | Predicted | Expected | Error | Status |",
            "|-----------|-----------|----------|-------|--------|",
        ])
        
        for p in processors:
            pred = f"{p.predicted_cpi:.2f}" if p.predicted_cpi else "N/A"
            err = f"{p.error_percent:+.1f}%" if p.error_percent is not None else "N/A"
            status_icon = "✅" if p.status == 'validated' else ("🟡" if p.status == 'close' else "❌")
            lines.append(f"| {p.name} | {pred} | {p.expected_cpi:.2f} | {err} | {status_icon} |")
        
        lines.append("")
    
    lines.extend([
        "## Calibration Actions",
        "",
        "### Processors Needing Decrease (CPI too high)",
        "",
    ])
    
    needs_decrease = [p for p in report['processors'] if p.status == 'needs_decrease']
    for p in sorted(needs_decrease, key=lambda x: x.error_percent or 0, reverse=True):
        scale = p.expected_cpi / p.predicted_cpi
        lines.append(f"- **{p.name}**: Scale timing by {scale:.2f}x (reduce base_cycles)")
    
    lines.extend([
        "",
        "### Processors Needing Increase (CPI too low)",
        "",
    ])
    
    needs_increase = [p for p in report['processors'] if p.status == 'needs_increase']
    for p in sorted(needs_increase, key=lambda x: x.error_percent or 0):
        scale = p.expected_cpi / p.predicted_cpi
        lines.append(f"- **{p.name}**: Scale timing by {scale:.2f}x (increase base_cycles)")
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(
        description='Generate calibration status report'
    )
    parser.add_argument('repo_path', nargs='?', default='.', help='Repository path')
    parser.add_argument('--output', '-o', help='Output markdown file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    report = generate_report(repo_path)
    
    if args.json:
        # Convert dataclasses to dicts for JSON
        report_dict = {
            'timestamp': report['timestamp'],
            'summary': report['summary'],
            'processors': [
                {
                    'name': p.name,
                    'family': p.family,
                    'era': p.era,
                    'expected_cpi': p.expected_cpi,
                    'predicted_cpi': p.predicted_cpi,
                    'error_percent': p.error_percent,
                    'status': p.status,
                    'recommendation': p.recommendation,
                }
                for p in report['processors']
            ]
        }
        print(json.dumps(report_dict, indent=2))
    else:
        print_report(report)
    
    if args.output:
        export_markdown(report, Path(args.output))
        print(f"\nReport exported to: {args.output}")


if __name__ == '__main__':
    main()
