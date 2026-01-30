# Toshiba TLCS-47 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.83%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: 4-bit consumer MCU (1982)
Simple instruction set with fixed timing per category.

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 4 | ADD, SUB, AND, OR |
| data_transfer | 5 | MOV, XCHG |
| memory | 7 | Indirect load/store |
| io | 8 | Port read/write |
| control | 6 | BR, CALL, RET |
| timer | 6 | Timer control |

**Performance:**
- Target CPI: 6.0
- Model CPI: 5.95
- At 500 kHz: ~83 KIPS

## Cross-Validation

Timing from TLCS-47 Series Data Sheet. Comparable to TMS1000 class.
- ALU operations: 4 cycles
- I/O operations: 8 cycles (slowest)
- Control flow: 6 cycles

## Known Issues

None - model matches expected CPI within tolerance.

## Suggested Next Steps

1. Add TLCS-47xx variant models (TLCS-470, TLCS-471, etc.)
2. Model sleep/low-power modes for battery applications

## Key Architectural Notes

- 4-bit data path with Harvard architecture
- On-chip ROM (up to 4K), RAM, timer, I/O
- Low power CMOS process
- Widely used in Japanese consumer electronics
- Compatible with standard 4-bit MCU programming model

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
