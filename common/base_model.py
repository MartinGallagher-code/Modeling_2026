"""
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
            f"{info['name']} ({info['manufacturer']}, {info['year']})\n"
            f"  Clock: {info['clock_mhz']} MHz, {info['transistor_count']:,} transistors\n"
            f"  Categories: {info['category_count']}, Workloads: {info['workload_count']}"
        )
