#!/usr/bin/env python3
import os, json, textwrap

BASE = os.path.dirname(os.path.abspath(__file__))

MODEL_TEMPLATE = textwrap.dedent(chr(39)*3 + chr(92) + chr(10) +
    '#!/usr/bin/env python3' + chr(10) +
    '"""' + '{name} Grey-Box Queueing Model' + chr(10) + chr(10) +
    '{desc}' + chr(10) +
    '"""' + chr(10) + chr(10) +
    'from dataclasses import dataclass' + chr(10) +
    'from typing import Dict, List, Any, Optional' + chr(10) + chr(10) +
    'try:' + chr(10) +
    '    from common.base_model import BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult' + chr(10) +
    'except ImportError:' + chr(10) +
    '    from dataclasses import dataclass' + chr(10) + chr(10) +
    '    @dataclass' + chr(10) +
    '    class InstructionCategory:' + chr(10) +
    '        name: str' + chr(10) +
    '        base_cycles: float' + chr(10) +
    '        memory_cycles: float = 0' + chr(10) +
    '        description: str = ""' + chr(10) +
    '        @property' + chr(10) +
    '        def total_cycles(self):' + chr(10) +
    '            return self.base_cycles + self.memory_cycles' + chr(10) + chr(10) +
    '    @dataclass' + chr(10) +
    '    class WorkloadProfile:' + chr(10) +
    '        name: str' + chr(10) +
    '        category_weights: Dict[str, float]' + chr(10) +
    '        description: str = ""' + chr(10) + chr(10) +
    '    @dataclass' + chr(10) +
    '    class AnalysisResult:' + chr(10) +
    '        processor: str' + chr(10) +
    '        workload: str' + chr(10) +
    '        ipc: float' + chr(10) +
    '        cpi: float' + chr(10) +
    '        ips: float' + chr(10) +
    '        bottleneck: str' + chr(10) +
    '        utilizations: Dict[str, float]' + chr(10) +
    '        @classmethod' + chr(10) +
    '        def from_cpi(cls, processor, workload, cpi, clock_mhz, bottleneck, utilizations):' + chr(10) +
    '            ipc = 1.0 / cpi' + chr(10) +
    '            ips = clock_mhz * 1e6 * ipc' + chr(10) +
    '            return cls(processor, workload, ipc, cpi, ips, bottleneck, utilizations)' + chr(10) + chr(10) +
    '    class BaseProcessorModel:' + chr(10) +
    '        pass' + chr(10) +
    chr(39)*3)
print('Script started - but this approach is too complex')
print('Switching to direct file writes per processor')
