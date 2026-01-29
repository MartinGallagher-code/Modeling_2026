"""
Berkeley RISC II Processor Model
================================

The Berkeley RISC II (1983) was the improved successor to RISC I,
developed at UC Berkeley by Patterson and Sequin. It featured:

- 32-bit RISC architecture
- 3-stage pipeline (fetch, decode, execute)
- 138 registers with 8 register windows
- Single-cycle ALU operations
- Load/store architecture
- 3 MHz clock
- Target CPI: ~1.2 (improved from RISC I's 1.3)

RISC II directly influenced the Sun SPARC architecture (1987).
"""

from .current.berkeley_risc2_validated import (
    BerkeleyRisc2Model,
    analyze_risc2,
    validate,
)

__all__ = [
    'BerkeleyRisc2Model',
    'analyze_risc2',
    'validate',
]
