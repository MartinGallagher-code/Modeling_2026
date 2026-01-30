# HP Saturn Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: 4-bit nibble-serial CPU with 64-bit registers (1984)

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 8 | ADD, SUB on register fields |
| register_op | 4 | SWAP, COPY, CLR, nibble moves |
| memory | 12 | DAT0/DAT1 load/store via pointer |
| control | 6 | GOTO, GOSUB, RTN |
| bcd | 10 | BCD arithmetic, field operations |

**Performance:**
- Target CPI: 8.0
- Model CPI: 8.0
- At 640 kHz: ~80 KIPS

## Known Issues

None - model validates at target CPI.

## Suggested Next Steps

1. **Later Saturn variants** - Model Lewis (2 MHz) and Sacajawea (4 MHz) versions
2. **RPL workload profiling** - More detailed profiling of HP RPL language execution
3. **Field-length effects** - Saturn operates on variable-width fields; could model field-length-dependent timing

## Key Architectural Notes

- 4-bit data path processes 64-bit registers nibble by nibble (16 steps)
- Variable-length instruction encoding (2-21 nibbles)
- Native BCD arithmetic for calculator-grade decimal precision
- Two pointer registers (D0, D1) for memory access
- Used in HP 71B, HP 48G/GX, HP 49G series
- Later versions (Lewis, Sacajawea) significantly faster

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
