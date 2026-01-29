# Toshiba TLCS-90 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 2.0%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: 8-bit Z80-like MCU (1985)
Z80-compatible instruction set with block operations.

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 4 | ADD, SUB, AND, OR, XOR, CP |
| data_transfer | 4 | LD, EX, PUSH, POP |
| memory | 5 | Indirect, indexed |
| io | 6 | IN, OUT |
| control | 5 | JP, JR, CALL, RET |
| block | 10 | LDIR, LDDR, CPIR (per iteration) |

**Performance:**
- Target CPI: 5.0
- Model CPI: 4.90
- At 6 MHz: ~1.2 MIPS

## Cross-Validation

Timing from TLCS-90 Series Data Sheet, cross-referenced with Z80 timing.
- Register ALU ops: 4 cycles (similar to Z80)
- Block transfers: 10 cycles per iteration
- I/O: 6 cycles (port synchronization)

## Known Issues

None - model matches expected CPI within tolerance.

## Suggested Next Steps

1. Add TLCS-900 (16-bit successor) model
2. Detailed comparison with Z80 instruction timing

## Key Architectural Notes

- Z80-compatible instruction set with Toshiba extensions
- Block transfer/search instructions (LDIR, LDDR, CPIR, CPDR)
- On-chip ROM, RAM, timer, UART, I/O
- 6 MHz clock (50% faster than original Z80)
- Designed for Z80 software migration to single-chip MCU

See CHANGELOG.md for full history of all work on this model.
