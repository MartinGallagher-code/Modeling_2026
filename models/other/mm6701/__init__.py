"""
Monolithic Memories 6701 Processor Model
=========================================

The Monolithic Memories 6701 (1975) was a 4-bit slice ALU
similar to the AMD Am2901. It featured:

- 4-bit slice architecture
- Bipolar Schottky technology
- Single-cycle microinstructions
- 16 general-purpose registers
- Carry look-ahead support
- 8 MHz clock (125ns cycle)
- Target CPI: 1.0 (per microinstruction)

Part of the 67xx bit-slice family. Competitor to AMD Am2900 family.
Monolithic Memories was later acquired by AMD (1987).
"""

from .current.mm6701_validated import (
    Mm6701Model,
    analyze_mm6701,
    validate,
)

__all__ = [
    'Mm6701Model',
    'analyze_mm6701',
    'validate',
]
