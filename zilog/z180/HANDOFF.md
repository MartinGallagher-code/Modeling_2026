# Z180 Model Handoff

## Current Status: VALIDATED (1.9% error)

## Quick Summary
The Z180 is an enhanced Z80 with faster instruction execution and on-chip peripherals. Model validated with 1.9% CPI error.

## Key Parameters
- Clock: 6.0 MHz (up to 20 MHz in later variants)
- Architecture: 8-bit, Z80-compatible, optimized timing
- Target CPI: 4.5
- Achieved CPI: 4.585

## Instruction Categories
| Category | Cycles | Notes |
|----------|--------|-------|
| alu | 3.2 | Optimized vs Z80's 4.0 |
| data_transfer | 3.2 | Faster than Z80 |
| memory | 4.8 | Optimized memory access |
| control | 4.5 | Faster branches |
| stack | 8.5 | Optimized PUSH/POP |
| block | 10.0 | Faster block ops |

## Related Models
- Z80/Z80A/Z80B: Base architecture, slower timing

## Potential Improvements
- Could model on-chip DMA separately
- Could add MMU address translation overhead
- UART/timer peripheral modeling if needed

## Files
- Model: `current/z180_validated.py`
- Validation: `validation/z180_validation.json`
