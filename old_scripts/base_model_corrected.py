#!/usr/bin/env python3
"""
Base Model Classes for Modeling_2026
=====================================

Provides common interfaces and data classes for all processor models.

IMPORTANT: Field order in dataclasses must match how they're called!
WorkloadProfile is called as: WorkloadProfile(name, category_weights_dict, description)

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
    memory_cycles: float = 0.0
    description: str = ""
    frequency: float = 0.0  # Fraction of instructions in this category
    
    @property
    def total_cycles(self) -> float:
        return self.base_cycles + self.memory_cycles


@dataclass
class WorkloadProfile:
    """Represents a workload with instruction category weights
    
    IMPORTANT: Field order must match calling convention:
    WorkloadProfile('name', {'cat': weight, ...}, 'description')
    """
    name: str
    # category_weights MUST come before description to match calling code!
    category_weights: Dict[str, float] = field(default_factory=dict)
    description: str = ""
    
    def validate(self) -> bool:
        """Check that weights sum to 1.0"""
        if not self.category_weights:
            return False
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
        ipc = 1.0 / cpi if cpi > 0 else 0.0
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
    
    def __init__(self):
        """Initialize the model - override in subclass if needed"""
        # Initialize mutable attributes in __init__, not as class attributes
        self._instruction_categories: Dict[str, InstructionCategory] = {}
        self._workload_profiles: Dict[str, WorkloadProfile] = {}
    
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
        # Default implementation - override for actual validation
        return {
            "tests": [],
            "passed": 0,
            "total": 0,
            "accuracy_percent": None
        }
    
    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        """
        Get all instruction categories with timing.
        
        Returns:
            Dictionary mapping category name to InstructionCategory
        """
        return self._instruction_categories
    
    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        """
        Get all available workload profiles.
        
        Returns:
            Dictionary mapping profile name to WorkloadProfile
        """
        return self._workload_profiles
    
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
