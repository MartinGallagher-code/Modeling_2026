#!/usr/bin/env python3
"""
Advanced Model Calibrator for Modeling_2026
=============================================

Architecture-specific calibration strategies for complex processor models
that don't respond well to simple uniform scaling.

Strategies by Architecture:
1. Sequential - Uniform scaling (already works)
2. Prefetch Queue - BIU/EU balance, queue effects
3. Pipelined - Pipeline depth, stall tuning
4. Cache/RISC - Cache parameters, branch prediction

Usage:
    python advanced_calibrator.py [repo_path] --processor i8086
    python advanced_calibrator.py [repo_path] --calibrate-failed
    python advanced_calibrator.py [repo_path] --diagnose i80286

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import os
import sys
import re
import json
import argparse
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod


# Expected CPI values
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

# Architecture classification
ARCHITECTURE_MAP = {
    'sequential': ['i4004', 'i4040', 'i8008', 'i8080', 'i8085', 'mos6502', 'mos6510', 
                   'm6800', 'm6801', 'f8', 'rca1802', 'scmp', 'signetics2650', 'am2901'],
    'prefetch_queue': ['i8086', 'i8088', 'i80186', 'i80188', 'z80', 'z80a', 'z80b', 
                       'z180', 'z8000', 'm6809', 'wdc65816', 'wdc65c02', 'tms9900'],
    'pipelined': ['i80286', 'm68000', 'm68008', 'm68010', 'm68020', 'ns32016'],
    'cache_risc': ['i80386', 'i80486', 'pentium', 'i860', 'm68030', 'm68040',
                   'arm1', 'arm2', 'arm3', 'sparc', 'sun_spark', 'r2000', 't414',
                   'alpha21064', 'hp_pa_risc'],
}


@dataclass
class CalibrationResult:
    """Results from calibration"""
    processor: str
    architecture: str
    original_cpi: float
    calibrated_cpi: float
    expected_cpi: float
    original_error: float
    calibrated_error: float
    parameters_changed: Dict[str, Any]
    strategy_used: str
    success: bool
    notes: str = ""


def get_architecture(proc_name: str) -> str:
    """Determine processor architecture"""
    for arch, processors in ARCHITECTURE_MAP.items():
        if proc_name in processors:
            return arch
    return 'unknown'


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


def get_model_cpi(model: Any, workload: str = 'typical') -> Optional[float]:
    """Get CPI from model"""
    try:
        result = model.analyze(workload)
        return result.cpi if result and hasattr(result, 'cpi') else None
    except:
        return None


def diagnose_model(model: Any, expected_cpi: float) -> Dict[str, Any]:
    """Deep diagnosis of model parameters and behavior"""
    diagnosis = {
        'current_cpi': None,
        'target_cpi': expected_cpi,
        'architecture_params': {},
        'instruction_categories': {},
        'workload_profiles': {},
        'issues': [],
        'recommendations': [],
    }
    
    # Get current CPI
    diagnosis['current_cpi'] = get_model_cpi(model)
    
    if diagnosis['current_cpi']:
        error = (diagnosis['current_cpi'] - expected_cpi) / expected_cpi * 100
        diagnosis['error_percent'] = error
        
        if error > 0:
            diagnosis['direction'] = 'DECREASE'
            diagnosis['issues'].append(f"CPI {error:.1f}% too HIGH - need faster execution")
        else:
            diagnosis['direction'] = 'INCREASE'
            diagnosis['issues'].append(f"CPI {abs(error):.1f}% too LOW - need slower execution")
    
    # Check architecture parameters
    arch_params = [
        'bus_cycle_time', 'bytes_per_access', 'prefetch_queue_size',
        'pipeline_stages', 'cache_hit_cycles', 'cache_miss_cycles',
        'branch_penalty', 'stall_cycles', 'memory_latency',
        'bus_width', 'data_width', 'address_width'
    ]
    
    for param in arch_params:
        if hasattr(model, param):
            diagnosis['architecture_params'][param] = getattr(model, param)
    
    # Check instruction categories
    if hasattr(model, 'instruction_categories'):
        for name, cat in model.instruction_categories.items():
            diagnosis['instruction_categories'][name] = {
                'base_cycles': getattr(cat, 'base_cycles', None),
                'memory_cycles': getattr(cat, 'memory_cycles', None),
                'total_cycles': getattr(cat, 'total_cycles', None) if hasattr(cat, 'total_cycles') else None,
            }
    
    # Check workload profiles
    if hasattr(model, 'workload_profiles'):
        for name, profile in model.workload_profiles.items():
            if hasattr(profile, 'category_weights'):
                diagnosis['workload_profiles'][name] = dict(profile.category_weights)
    
    # Generate recommendations based on architecture
    if diagnosis['architecture_params']:
        if 'prefetch_queue_size' in diagnosis['architecture_params']:
            diagnosis['recommendations'].append("Prefetch queue model - adjust BIU/EU timing balance")
        if 'pipeline_stages' in diagnosis['architecture_params']:
            diagnosis['recommendations'].append("Pipelined model - tune stall and hazard penalties")
        if 'cache_hit_cycles' in diagnosis['architecture_params']:
            diagnosis['recommendations'].append("Cache model - adjust hit/miss ratios and latencies")
    
    return diagnosis


# =============================================================================
# ARCHITECTURE-SPECIFIC CALIBRATORS
# =============================================================================

class BaseCalibrator(ABC):
    """Base class for architecture-specific calibrators"""
    
    def __init__(self, model: Any, expected_cpi: float):
        self.model = model
        self.expected_cpi = expected_cpi
        self.original_cpi = get_model_cpi(model)
        self.parameters_changed = {}
    
    @abstractmethod
    def calibrate(self) -> CalibrationResult:
        pass
    
    def get_error(self, cpi: float) -> float:
        return abs(cpi - self.expected_cpi) / self.expected_cpi * 100


class PrefetchQueueCalibrator(BaseCalibrator):
    """
    Calibrator for prefetch queue architecture (i8086, z80, etc.)
    
    Key parameters:
    - bus_cycle_time: Cycles per memory/bus access
    - prefetch_queue_size: Size of instruction queue (bytes)
    - BIU/EU parallelism balance
    """
    
    def calibrate(self) -> CalibrationResult:
        if not self.original_cpi:
            return self._fail("Could not get original CPI")
        
        original_error = self.get_error(self.original_cpi)
        
        # Strategy 1: Adjust bus_cycle_time
        if hasattr(self.model, 'bus_cycle_time'):
            original_bus = self.model.bus_cycle_time
            
            # Calculate target ratio
            ratio = self.expected_cpi / self.original_cpi
            
            # Adjust bus timing (major impact on prefetch models)
            new_bus = original_bus * ratio
            new_bus = max(1, min(10, new_bus))  # Reasonable bounds
            
            self.model.bus_cycle_time = new_bus
            new_cpi = get_model_cpi(self.model)
            
            if new_cpi and self.get_error(new_cpi) < original_error:
                self.parameters_changed['bus_cycle_time'] = (original_bus, new_bus)
            else:
                self.model.bus_cycle_time = original_bus
        
        # Strategy 2: Adjust base_cycles with weighted scaling
        if hasattr(self.model, 'instruction_categories'):
            current_cpi = get_model_cpi(self.model) or self.original_cpi
            
            if current_cpi > self.expected_cpi:
                # Need to decrease - scale down non-memory operations more
                scale = self.expected_cpi / current_cpi
                scale = max(0.3, scale)
                
                for name, cat in self.model.instruction_categories.items():
                    old_val = cat.base_cycles
                    # Memory ops already constrained by bus, scale less
                    if 'memory' in name.lower() or 'load' in name.lower() or 'store' in name.lower():
                        new_val = old_val * (scale ** 0.5)  # Less aggressive
                    else:
                        new_val = old_val * scale
                    
                    new_val = max(1, min(50, new_val))
                    cat.base_cycles = new_val
                    
                    if abs(new_val - old_val) > 0.1:
                        self.parameters_changed[f'{name}.base_cycles'] = (old_val, new_val)
            else:
                # Need to increase
                scale = self.expected_cpi / current_cpi
                scale = min(3.0, scale)
                
                for name, cat in self.model.instruction_categories.items():
                    old_val = cat.base_cycles
                    new_val = old_val * scale
                    new_val = max(1, min(50, new_val))
                    cat.base_cycles = new_val
                    
                    if abs(new_val - old_val) > 0.1:
                        self.parameters_changed[f'{name}.base_cycles'] = (old_val, new_val)
        
        # Strategy 3: Adjust prefetch queue size effect
        if hasattr(self.model, 'prefetch_queue_size'):
            current_cpi = get_model_cpi(self.model)
            if current_cpi and self.get_error(current_cpi) > 10:
                # Try adjusting queue size
                original_size = self.model.prefetch_queue_size
                
                if current_cpi > self.expected_cpi:
                    # Larger queue = less refill penalty
                    new_size = min(12, original_size + 2)
                else:
                    # Smaller queue = more refill penalty
                    new_size = max(2, original_size - 2)
                
                self.model.prefetch_queue_size = new_size
                test_cpi = get_model_cpi(self.model)
                
                if test_cpi and self.get_error(test_cpi) < self.get_error(current_cpi):
                    self.parameters_changed['prefetch_queue_size'] = (original_size, new_size)
                else:
                    self.model.prefetch_queue_size = original_size
        
        calibrated_cpi = get_model_cpi(self.model) or self.original_cpi
        calibrated_error = self.get_error(calibrated_cpi)
        
        return CalibrationResult(
            processor=getattr(self.model, 'name', 'Unknown'),
            architecture='prefetch_queue',
            original_cpi=self.original_cpi,
            calibrated_cpi=calibrated_cpi,
            expected_cpi=self.expected_cpi,
            original_error=original_error,
            calibrated_error=calibrated_error,
            parameters_changed=self.parameters_changed,
            strategy_used='prefetch_queue_calibration',
            success=calibrated_error < 5,
            notes=f"Adjusted {len(self.parameters_changed)} parameters"
        )
    
    def _fail(self, reason: str) -> CalibrationResult:
        return CalibrationResult(
            processor=getattr(self.model, 'name', 'Unknown'),
            architecture='prefetch_queue',
            original_cpi=0, calibrated_cpi=0, expected_cpi=self.expected_cpi,
            original_error=100, calibrated_error=100,
            parameters_changed={}, strategy_used='prefetch_queue_calibration',
            success=False, notes=reason
        )


class PipelinedCalibrator(BaseCalibrator):
    """
    Calibrator for pipelined architecture (i80286, m68000, etc.)
    
    Key parameters:
    - pipeline_stages: Number of pipeline stages
    - stall_cycles: Hazard/stall penalties
    - decode/execute timing balance
    """
    
    def calibrate(self) -> CalibrationResult:
        if not self.original_cpi:
            return self._fail("Could not get original CPI")
        
        original_error = self.get_error(self.original_cpi)
        
        # For pipelined models, the CPI should be close to 1.0 + stalls
        # If predicted CPI is too low, the model may be too optimistic
        # If predicted CPI is too high, stalls may be overestimated
        
        ratio = self.expected_cpi / self.original_cpi
        
        # Strategy 1: Scale instruction timing
        if hasattr(self.model, 'instruction_categories'):
            for name, cat in self.model.instruction_categories.items():
                old_val = cat.base_cycles
                
                # Pipelined processors: most instructions should be 1-4 cycles
                # Memory operations are the exception
                if 'memory' in name.lower() or 'load' in name.lower() or 'store' in name.lower():
                    new_val = old_val * ratio
                else:
                    # More aggressive scaling for non-memory
                    new_val = old_val * (ratio ** 1.2)
                
                new_val = max(1, min(30, new_val))
                cat.base_cycles = new_val
                
                if abs(new_val - old_val) > 0.1:
                    self.parameters_changed[f'{name}.base_cycles'] = (old_val, new_val)
        
        # Strategy 2: Adjust pipeline-specific parameters
        pipeline_params = ['decode_cycles', 'execute_cycles', 'writeback_cycles', 
                          'stall_penalty', 'hazard_cycles', 'branch_penalty']
        
        for param in pipeline_params:
            if hasattr(self.model, param):
                old_val = getattr(self.model, param)
                new_val = old_val * ratio
                new_val = max(0, min(20, new_val))
                setattr(self.model, param, new_val)
                
                if abs(new_val - old_val) > 0.1:
                    self.parameters_changed[param] = (old_val, new_val)
        
        calibrated_cpi = get_model_cpi(self.model) or self.original_cpi
        calibrated_error = self.get_error(calibrated_cpi)
        
        # If still not good, try second pass
        if calibrated_error > 10:
            second_ratio = self.expected_cpi / calibrated_cpi
            second_ratio = max(0.5, min(2.0, second_ratio))
            
            if hasattr(self.model, 'instruction_categories'):
                for name, cat in self.model.instruction_categories.items():
                    old_val = cat.base_cycles
                    new_val = old_val * second_ratio
                    new_val = max(1, min(30, new_val))
                    cat.base_cycles = new_val
                    
                    # Update change record
                    if f'{name}.base_cycles' in self.parameters_changed:
                        orig = self.parameters_changed[f'{name}.base_cycles'][0]
                        self.parameters_changed[f'{name}.base_cycles'] = (orig, new_val)
            
            calibrated_cpi = get_model_cpi(self.model) or calibrated_cpi
            calibrated_error = self.get_error(calibrated_cpi)
        
        return CalibrationResult(
            processor=getattr(self.model, 'name', 'Unknown'),
            architecture='pipelined',
            original_cpi=self.original_cpi,
            calibrated_cpi=calibrated_cpi,
            expected_cpi=self.expected_cpi,
            original_error=original_error,
            calibrated_error=calibrated_error,
            parameters_changed=self.parameters_changed,
            strategy_used='pipelined_calibration',
            success=calibrated_error < 5,
            notes=f"Pipeline-aware tuning"
        )
    
    def _fail(self, reason: str) -> CalibrationResult:
        return CalibrationResult(
            processor=getattr(self.model, 'name', 'Unknown'),
            architecture='pipelined',
            original_cpi=0, calibrated_cpi=0, expected_cpi=self.expected_cpi,
            original_error=100, calibrated_error=100,
            parameters_changed={}, strategy_used='pipelined_calibration',
            success=False, notes=reason
        )


class CacheRiscCalibrator(BaseCalibrator):
    """
    Calibrator for cache/RISC architecture (i80386+, ARM, SPARC, etc.)
    
    Key parameters:
    - cache_hit_cycles: L1 cache hit latency
    - cache_miss_cycles: Cache miss penalty
    - cache_hit_rate: Fraction of accesses that hit
    - branch_prediction_accuracy: Branch predictor success rate
    """
    
    def calibrate(self) -> CalibrationResult:
        if not self.original_cpi:
            return self._fail("Could not get original CPI")
        
        original_error = self.get_error(self.original_cpi)
        
        # RISC processors target CPI close to 1.0
        # Actual CPI = 1.0 + memory_stalls + branch_stalls + hazard_stalls
        
        ratio = self.expected_cpi / self.original_cpi
        
        # Strategy 1: Adjust cache parameters
        cache_params = {
            'cache_hit_cycles': (1, 5),      # bounds
            'cache_miss_cycles': (5, 100),
            'cache_hit_rate': (0.5, 0.99),
            'l1_hit_cycles': (1, 3),
            'l2_hit_cycles': (3, 15),
            'memory_cycles': (10, 200),
        }
        
        for param, (min_val, max_val) in cache_params.items():
            if hasattr(self.model, param):
                old_val = getattr(self.model, param)
                new_val = old_val * ratio
                new_val = max(min_val, min(max_val, new_val))
                setattr(self.model, param, new_val)
                
                if abs(new_val - old_val) > 0.01:
                    self.parameters_changed[param] = (old_val, new_val)
        
        # Strategy 2: Adjust instruction timing (RISC = mostly single-cycle)
        if hasattr(self.model, 'instruction_categories'):
            for name, cat in self.model.instruction_categories.items():
                old_val = cat.base_cycles
                
                # RISC instructions should be 1-2 cycles, memory 2-4
                if 'memory' in name.lower() or 'load' in name.lower() or 'store' in name.lower():
                    target = max(2, self.expected_cpi * 0.8)  # Memory slightly above average
                    new_val = old_val * (target / old_val) if old_val > 0 else target
                elif 'mul' in name.lower() or 'div' in name.lower():
                    # Keep multiply/divide longer
                    new_val = old_val * ratio
                else:
                    # Simple ops should be ~1 cycle for RISC
                    target = max(1, self.expected_cpi * 0.5)
                    new_val = old_val * (target / old_val) if old_val > 0 else target
                
                new_val = max(1, min(50, new_val))
                cat.base_cycles = new_val
                
                if abs(new_val - old_val) > 0.1:
                    self.parameters_changed[f'{name}.base_cycles'] = (old_val, new_val)
        
        # Strategy 3: Adjust branch prediction impact
        branch_params = ['branch_penalty', 'branch_mispredict_cycles', 
                        'branch_prediction_accuracy']
        
        for param in branch_params:
            if hasattr(self.model, param):
                old_val = getattr(self.model, param)
                if 'accuracy' in param:
                    # Higher accuracy = lower CPI
                    if ratio < 1:  # Need lower CPI
                        new_val = min(0.98, old_val * (2 - ratio))
                    else:  # Need higher CPI
                        new_val = max(0.5, old_val * ratio)
                else:
                    new_val = old_val * ratio
                    new_val = max(1, min(20, new_val))
                
                setattr(self.model, param, new_val)
                if abs(new_val - old_val) > 0.01:
                    self.parameters_changed[param] = (old_val, new_val)
        
        calibrated_cpi = get_model_cpi(self.model) or self.original_cpi
        calibrated_error = self.get_error(calibrated_cpi)
        
        # Iterative refinement
        for iteration in range(3):
            if calibrated_error < 5:
                break
            
            refine_ratio = self.expected_cpi / calibrated_cpi
            refine_ratio = max(0.7, min(1.4, refine_ratio))
            
            if hasattr(self.model, 'instruction_categories'):
                for name, cat in self.model.instruction_categories.items():
                    cat.base_cycles = max(1, cat.base_cycles * refine_ratio)
            
            calibrated_cpi = get_model_cpi(self.model) or calibrated_cpi
            calibrated_error = self.get_error(calibrated_cpi)
        
        return CalibrationResult(
            processor=getattr(self.model, 'name', 'Unknown'),
            architecture='cache_risc',
            original_cpi=self.original_cpi,
            calibrated_cpi=calibrated_cpi,
            expected_cpi=self.expected_cpi,
            original_error=original_error,
            calibrated_error=calibrated_error,
            parameters_changed=self.parameters_changed,
            strategy_used='cache_risc_calibration',
            success=calibrated_error < 5,
            notes=f"Cache/RISC-aware tuning with {len(self.parameters_changed)} params"
        )
    
    def _fail(self, reason: str) -> CalibrationResult:
        return CalibrationResult(
            processor=getattr(self.model, 'name', 'Unknown'),
            architecture='cache_risc',
            original_cpi=0, calibrated_cpi=0, expected_cpi=self.expected_cpi,
            original_error=100, calibrated_error=100,
            parameters_changed={}, strategy_used='cache_risc_calibration',
            success=False, notes=reason
        )


class SequentialCalibrator(BaseCalibrator):
    """Simple uniform scaling for sequential architecture"""
    
    def calibrate(self) -> CalibrationResult:
        if not self.original_cpi:
            return self._fail("Could not get original CPI")
        
        original_error = self.get_error(self.original_cpi)
        ratio = self.expected_cpi / self.original_cpi
        ratio = max(0.3, min(3.0, ratio))
        
        if hasattr(self.model, 'instruction_categories'):
            for name, cat in self.model.instruction_categories.items():
                old_val = cat.base_cycles
                new_val = max(1, min(50, old_val * ratio))
                cat.base_cycles = new_val
                
                if abs(new_val - old_val) > 0.1:
                    self.parameters_changed[f'{name}.base_cycles'] = (old_val, new_val)
        
        calibrated_cpi = get_model_cpi(self.model) or self.original_cpi
        calibrated_error = self.get_error(calibrated_cpi)
        
        return CalibrationResult(
            processor=getattr(self.model, 'name', 'Unknown'),
            architecture='sequential',
            original_cpi=self.original_cpi,
            calibrated_cpi=calibrated_cpi,
            expected_cpi=self.expected_cpi,
            original_error=original_error,
            calibrated_error=calibrated_error,
            parameters_changed=self.parameters_changed,
            strategy_used='uniform_scaling',
            success=calibrated_error < 5,
            notes=f"Scale factor: {ratio:.2f}"
        )
    
    def _fail(self, reason: str) -> CalibrationResult:
        return CalibrationResult(
            processor=getattr(self.model, 'name', 'Unknown'),
            architecture='sequential',
            original_cpi=0, calibrated_cpi=0, expected_cpi=self.expected_cpi,
            original_error=100, calibrated_error=100,
            parameters_changed={}, strategy_used='uniform_scaling',
            success=False, notes=reason
        )


def get_calibrator(model: Any, expected_cpi: float, architecture: str) -> BaseCalibrator:
    """Factory function to get appropriate calibrator"""
    calibrators = {
        'sequential': SequentialCalibrator,
        'prefetch_queue': PrefetchQueueCalibrator,
        'pipelined': PipelinedCalibrator,
        'cache_risc': CacheRiscCalibrator,
    }
    
    calibrator_class = calibrators.get(architecture, SequentialCalibrator)
    return calibrator_class(model, expected_cpi)


def calibrate_processor(
    proc_name: str,
    model_path: Path,
    repo_root: Path,
    verbose: bool = False
) -> CalibrationResult:
    """Calibrate a single processor with architecture-appropriate strategy"""
    
    expected_cpi = EXPECTED_CPI.get(proc_name)
    if not expected_cpi:
        return CalibrationResult(
            processor=proc_name, architecture='unknown',
            original_cpi=0, calibrated_cpi=0, expected_cpi=0,
            original_error=100, calibrated_error=100,
            parameters_changed={}, strategy_used='none',
            success=False, notes="No expected CPI in database"
        )
    
    model, error = load_model(model_path, repo_root)
    if not model:
        return CalibrationResult(
            processor=proc_name, architecture='unknown',
            original_cpi=0, calibrated_cpi=0, expected_cpi=expected_cpi,
            original_error=100, calibrated_error=100,
            parameters_changed={}, strategy_used='none',
            success=False, notes=f"Load error: {error}"
        )
    
    architecture = get_architecture(proc_name)
    calibrator = get_calibrator(model, expected_cpi, architecture)
    
    if verbose:
        print(f"  Architecture: {architecture}")
        print(f"  Calibrator: {type(calibrator).__name__}")
    
    return calibrator.calibrate()


def print_diagnosis(diagnosis: Dict[str, Any], proc_name: str):
    """Print diagnosis report"""
    print()
    print("=" * 70)
    print(f"DIAGNOSIS: {proc_name}")
    print("=" * 70)
    
    print(f"\nCurrent CPI:  {diagnosis.get('current_cpi', 'N/A')}")
    print(f"Target CPI:   {diagnosis.get('target_cpi', 'N/A')}")
    if 'error_percent' in diagnosis:
        print(f"Error:        {diagnosis['error_percent']:.1f}%")
        print(f"Direction:    {diagnosis.get('direction', 'N/A')}")
    
    if diagnosis.get('architecture_params'):
        print("\nArchitecture Parameters:")
        for param, value in diagnosis['architecture_params'].items():
            print(f"  {param}: {value}")
    
    if diagnosis.get('instruction_categories'):
        print("\nInstruction Categories:")
        for name, info in list(diagnosis['instruction_categories'].items())[:6]:
            print(f"  {name}: base={info.get('base_cycles')}, mem={info.get('memory_cycles')}")
    
    if diagnosis.get('issues'):
        print("\nIssues:")
        for issue in diagnosis['issues']:
            print(f"  ⚠️  {issue}")
    
    if diagnosis.get('recommendations'):
        print("\nRecommendations:")
        for rec in diagnosis['recommendations']:
            print(f"  → {rec}")


def print_calibration_result(result: CalibrationResult):
    """Print calibration result"""
    status = "✅" if result.success else ("🟡" if result.calibrated_error < result.original_error else "❌")
    
    print(f"\n{status} {result.processor} [{result.architecture}]")
    print(f"   Strategy: {result.strategy_used}")
    print(f"   CPI: {result.original_cpi:.2f} → {result.calibrated_cpi:.2f} (target: {result.expected_cpi:.2f})")
    print(f"   Error: {result.original_error:.1f}% → {result.calibrated_error:.1f}%")
    
    if result.parameters_changed:
        print(f"   Changed {len(result.parameters_changed)} parameters")


def main():
    parser = argparse.ArgumentParser(description='Advanced architecture-specific calibration')
    parser.add_argument('repo_path', nargs='?', default='.', help='Repository path')
    parser.add_argument('--processor', '-p', help='Specific processor')
    parser.add_argument('--diagnose', '-d', help='Diagnose processor (no changes)')
    parser.add_argument('--calibrate-failed', action='store_true', help='Calibrate processors that failed basic calibration')
    parser.add_argument('--calibrate-all', action='store_true', help='Calibrate all processors')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    
    print("=" * 70)
    print("ADVANCED MODEL CALIBRATOR")
    print("=" * 70)
    print(f"Repository: {repo_path}")
    print()
    
    if args.diagnose:
        # Diagnose mode
        proc_name = args.diagnose
        expected_cpi = EXPECTED_CPI.get(proc_name)
        
        if not expected_cpi:
            print(f"No expected CPI for: {proc_name}")
            return
        
        for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
            model_path = repo_path / family / proc_name / 'current' / f'{proc_name}_validated.py'
            if model_path.exists():
                model, error = load_model(model_path, repo_path)
                if model:
                    diagnosis = diagnose_model(model, expected_cpi)
                    print_diagnosis(diagnosis, proc_name)
                else:
                    print(f"Failed to load: {error}")
                return
        
        print(f"Processor not found: {proc_name}")
    
    elif args.processor:
        # Single processor calibration
        proc_name = args.processor
        
        for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
            model_path = repo_path / family / proc_name / 'current' / f'{proc_name}_validated.py'
            if model_path.exists():
                result = calibrate_processor(proc_name, model_path, repo_path, args.verbose)
                print_calibration_result(result)
                return
        
        print(f"Processor not found: {proc_name}")
    
    elif args.calibrate_failed or args.calibrate_all:
        # Batch calibration
        results = {'success': 0, 'improved': 0, 'failed': 0}
        
        # List of previously failed processors
        failed_processors = [
            'i8086', 'i8088', 'i80186', 'i80188', 'i80286', 'i80386', 'i80486',
            'pentium', 'i860', 'm68000', 'm68008', 'm68010', 'm68020', 'm68040',
            'm6809', 'wdc65816', 'wdc65c02', 'z80', 'z180', 'z8000', 'z80a', 'z80b',
            'arm1', 'arm2', 'arm3', 'sparc', 'sun_spark', 'r2000', 't414',
            'alpha21064', 'hp_pa_risc', 'ns32016', 'am2901'
        ]
        
        for family in ['intel', 'motorola', 'mos_wdc', 'zilog', 'other']:
            family_path = repo_path / family
            if not family_path.exists():
                continue
            
            for proc_dir in sorted(family_path.iterdir()):
                if not proc_dir.is_dir():
                    continue
                
                proc_name = proc_dir.name
                
                # Skip if not in failed list (unless calibrate-all)
                if not args.calibrate_all and proc_name not in failed_processors:
                    continue
                
                if proc_name not in EXPECTED_CPI:
                    continue
                
                model_path = proc_dir / 'current' / f'{proc_name}_validated.py'
                if not model_path.exists():
                    continue
                
                result = calibrate_processor(proc_name, model_path, repo_path, args.verbose)
                
                if result.success:
                    status = "✅"
                    results['success'] += 1
                elif result.calibrated_error < result.original_error:
                    status = "🟡"
                    results['improved'] += 1
                else:
                    status = "❌"
                    results['failed'] += 1
                
                print(f"{status} {family}/{proc_name}: {result.original_error:.1f}% → {result.calibrated_error:.1f}% [{result.architecture}]")
        
        print()
        print("=" * 50)
        print(f"Fully calibrated (<5%): {results['success']}")
        print(f"Improved (not <5%):     {results['improved']}")
        print(f"Failed to improve:      {results['failed']}")
    
    else:
        print("Usage:")
        print("  --diagnose PROCESSOR    Diagnose without changes")
        print("  --processor PROCESSOR   Calibrate single processor")
        print("  --calibrate-failed      Calibrate previously failed processors")
        print("  --calibrate-all         Calibrate all processors")


if __name__ == '__main__':
    main()
