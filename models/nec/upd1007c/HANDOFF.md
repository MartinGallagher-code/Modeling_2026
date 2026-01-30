# NEC uPD1007C Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: 4-bit CMOS calculator CPU (1978)

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 5 | ADD, SUB, INC, DEC, CMP |
| bcd | 7 | Multi-digit BCD arithmetic, DAA |
| memory | 6 | Load/store to register file |
| control | 4 | Branch, skip, call/return |
| display | 9 | LCD segment drive, scan |

**Performance:**
- Target CPI: 6.0
- Model CPI: 6.0
- At 500 kHz: ~83 KIPS

## Known Issues

None - model validates at target CPI.

## Suggested Next Steps

1. **uPD557/uPD546 family** - Model related NEC calculator CPUs
2. **Scientific function profiling** - Profile trig/log execution on Casio calculators
3. **Power consumption modeling** - CMOS power characteristics for battery life estimation

## Key Architectural Notes

- 4-bit data path with native BCD arithmetic
- Integrated LCD/LED display driver
- Low-power CMOS design for battery operation
- Used in Casio scientific and programmable calculators
- Register file for multi-digit BCD storage
- Display operations are the most cycle-expensive category

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
