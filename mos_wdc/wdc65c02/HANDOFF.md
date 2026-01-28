# WDC 65C02 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-28

## Current Model Summary

Architecture: 8-bit CMOS (optimized 6502)

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2.8 | Slightly faster than 6502 |
| data_transfer | 3.2 | Optimized indexed modes |
| memory | 3.8 | Faster indexed operations |
| control | 2.8 | Branches + BRA instruction |
| stack | 3.2 | Includes PHX/PHY/PLX/PLY |

## Validation

The model includes a `validate()` method that runs 16 self-tests:
- CPI accuracy (target 3.2 +/- 5%)
- Workload weight sums (4 profiles)
- Cycle count ranges (5 categories)
- IPC range check
- 65C02 faster than 6502 (CPI < 3.5)
- All workloads produce valid output

Current: **16/16 tests passing, 100.0% accuracy**

## Known Issues

None - model is well-calibrated and self-validates.

## Suggested Next Steps

1. **High-speed variants** - 65C02 runs up to 14 MHz; could model cache effects at higher speeds

## Key Architectural Notes

- CMOS 6502 with bug fixes and new instructions
- Faster than NMOS 6502 (CPI 3.2 vs 3.5)
- BRA (branch always) is a key new instruction
- PHX/PHY/PLX/PLY simplify register preservation
- STZ (store zero) common operation made efficient
- Can run at much higher clock speeds than NMOS

See CHANGELOG.md for full history of all work on this model.
