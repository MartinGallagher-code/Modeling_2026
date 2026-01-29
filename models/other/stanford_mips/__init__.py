"""
Stanford MIPS Processor Model
=============================

The Stanford MIPS (1983) was the original academic RISC processor
developed by John Hennessy at Stanford University. It featured:

- 32-bit RISC architecture
- 5-stage pipeline (IF, ID, EX, MEM, WB)
- 32 general-purpose registers
- Delayed branches and load delay slots
- Hardwired control (no microcode)
- 2 MHz clock (research chip)
- Target CPI: ~1.2

MIPS = Microprocessor without Interlocked Pipeline Stages

Stanford MIPS directly led to the commercial MIPS R2000 (1986).
"""

from .current.stanford_mips_validated import (
    StanfordMipsModel,
    analyze_mips,
    validate,
)

__all__ = [
    'StanfordMipsModel',
    'analyze_mips',
    'validate',
]
