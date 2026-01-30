#!/usr/bin/env python3
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))

COMMON_IMPORTS = """#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

try:
    from common.base_model import BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult
except ImportError:
    from dataclasses import dataclass

    @dataclass
    class InstructionCategory:
        name: str
        base_cycles: float
        memory_cycles: float = 0
        description: str = ""
        @property
        def total_cycles(self):
            return self.base_cycles + self.memory_cycles
