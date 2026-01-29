# Toshiba TLCS-870 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.33%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: 8-bit proprietary MCU (1985)
Unique Toshiba ISA with bit manipulation support.

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 3 | ADD, SUB, AND, OR, XOR |
| data_transfer | 3 | LD, MOV |
| memory | 5 | Indirect, indexed |
| io | 6 | Port operations |
| control | 5 | JP, CALL, RET |
| bit_ops | 3 | SET, CLR, TEST |

**Performance:**
- Target CPI: 4.5
- Model CPI: 4.44
- At 8 MHz: ~1.78 MIPS

## Cross-Validation

Timing from TLCS-870 Series Data Sheet.
- Fast register/bit ops: 3 cycles
- Memory indirect: 5 cycles
- I/O: 6 cycles (slowest due to port sync)

## Known Issues

None - model matches expected CPI within tolerance.

## Suggested Next Steps

1. Add TLCS-870/C variant with enhanced peripherals
2. Model interrupt latency for real-time applications

## Key Architectural Notes

- Proprietary 8-bit ISA (not Z80 or 6502 based)
- Efficient bit manipulation instructions
- On-chip ROM, RAM, timer, UART, I/O
- Low power CMOS design
- Used in automotive, industrial, consumer applications

See CHANGELOG.md for full history of all work on this model.
