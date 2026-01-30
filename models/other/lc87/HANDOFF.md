# Sanyo LC87 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.6%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: 8-bit MCU (1983)
Simple sequential execution with on-chip peripherals.

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 3 | ADD, SUB, AND, OR, XOR |
| data_transfer | 4 | MOV, LD |
| memory | 6 | Indirect, indexed |
| io | 6 | Port read/write |
| control | 5 | JP, CALL, RET |

**Performance:**
- Target CPI: 5.0
- Model CPI: 4.92
- At 4 MHz: ~800 KIPS

## Cross-Validation

Timing from LC87 Series Data Sheet.
- ALU register ops: 3 cycles (fastest)
- Memory/IO: 6 cycles (slowest)
- Control flow: 5 cycles

## Known Issues

None - model matches expected CPI within tolerance.

## Suggested Next Steps

1. Add LC87xx variant models with enhanced peripherals
2. Model ADC timing for analog-equipped variants

## Key Architectural Notes

- 8-bit data path, 16-bit address bus
- On-chip ROM, RAM, I/O ports, timer
- Sequential execution, no pipeline
- Low power CMOS design
- Used in Sanyo audio equipment, home appliances
- Part of Sanyo's broader LC8x MCU family

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.80%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
