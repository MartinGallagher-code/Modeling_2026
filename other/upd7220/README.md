# NEC uPD7220 Graphics Display Controller

## Overview
The NEC uPD7220 (1981) was the first single-chip LSI graphics display controller. Unlike a general-purpose CPU, it was a specialized graphics command processor capable of executing hardware-accelerated drawing operations including line drawing (Bresenham algorithm), arc generation, area fill, and character display. It handled DMA to display memory and generated video timing signals.

## Specifications
- **Manufacturer**: NEC
- **Year**: 1981
- **Data Width**: 16-bit internal
- **Clock Speed**: 5 MHz
- **Technology**: NMOS
- **Transistors**: ~60,000
- **Address Space**: 20-bit (1MB display memory)

## Model Details
- **Target CPI**: 12.0 (per graphics command)
- **Architecture**: Graphics command processor, not a general CPU
- **Workloads**: typical, compute (vector-heavy), memory (DMA-heavy), control (text-heavy)

## Files
- `current/upd7220_validated.py` - Validated processor model
- `validation/upd7220_validation.json` - Validation data and test results
- `HANDOFF.md` - Current status and handoff notes
- `CHANGELOG.md` - Complete change history
