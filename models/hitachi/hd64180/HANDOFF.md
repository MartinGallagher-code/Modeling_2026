# Hitachi HD64180 Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-29

## Quick Summary

The Hitachi HD64180 is a Z180-equivalent enhanced Z80 microprocessor. It features faster instruction execution and integrated peripherals. The model uses timing equivalent to the Zilog Z180.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Manufacturer | Hitachi |
| Year | 1985 |
| Clock | 6.0 MHz (up to 10 MHz in R variants) |
| Architecture | 8-bit, sequential execution, no pipeline |
| Target CPI | 4.5 |
| Address Space | 1 MB (20-bit with MMU) |

## Instruction Categories

| Category | Model Cycles | Z80 Cycles | Improvement |
|----------|-------------|------------|-------------|
| alu | 3.2 | 4.0 | 20% faster |
| data_transfer | 3.2 | 4.0 | 20% faster |
| memory | 4.8 | 5.8 | 17% faster |
| control | 4.5 | 5.5 | 18% faster |
| stack | 8.5 | 10.0 | 15% faster |
| block | 10.0 | 12.0 | 17% faster |

## On-Chip Peripherals

- **MMU:** Memory Management Unit for 1 MB addressing
- **DMA:** Direct Memory Access controller
- **UART:** Asynchronous serial communication
- **Timers:** Programmable timer/counters
- **I/O:** Clocked serial I/O port

## Historical Context

The HD64180 was produced by Hitachi as part of the Z180 family. It was widely used in:
- Embedded systems
- Industrial controllers
- Point-of-sale terminals
- Some portable computers

## Model Limitations

1. Uses category-weighted averages, not per-instruction timing
2. Does not model wait states for slow memory
3. Does not model on-chip peripheral timing
4. Does not model MMU translation overhead
5. Does not model DMA activity impact

## Related Models

- Zilog Z180: Original specification
- Zilog Z80: Predecessor architecture
- NEC uPD780: Z80 clone

## Files

- **Model:** `current/hd64180_validated.py`
- **Validation:** `validation/hd64180_validation.json`
- **Changelog:** `CHANGELOG.md`

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
