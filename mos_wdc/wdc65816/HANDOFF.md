# WDC 65816 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.5%
- **Last Updated**: 2026-01-28

## Current Model Summary

Architecture: 16-bit CMOS (extended 65C02)

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 3.2 | +1 cycle in 16-bit mode |
| data_transfer | 3.8 | Mix of 8/16-bit modes |
| memory | 4.5 | Including long 24-bit addressing |
| control | 3.5 | Branches + long jumps (JML, JSL) |
| stack | 4.0 | 16-bit push/pull take longer |

## Validation

The model includes a `validate()` method that runs 16 self-tests:
- CPI accuracy (target 3.8 +/- 5%)
- Workload weight sums (4 profiles)
- Cycle count ranges (5 categories)
- IPC range check
- 65816 16-bit overhead (CPI > 3.2)
- All workloads produce valid output

Current: **16/16 tests passing, 99.5% accuracy**

## Known Issues

None - model is well-calibrated for mixed 8/16-bit operation.

## Suggested Next Steps

1. **Separate 8-bit vs 16-bit profiles** - could model pure 8-bit mode (like Apple IIGS ProDOS) vs 16-bit mode separately

2. **SNES-specific profiling** - DMA operations, PPU register access patterns

## Key Architectural Notes

- 65816 extends 65C02 to 16 bits with backward compatibility
- 8/16-bit modes switchable via processor status register
- 24-bit address bus (16 MB address space)
- SNES ran at ~3.58 MHz (slower than 65C02's 4 MHz typical)
- JSL/RTL for cross-bank subroutine calls
- MVN/MVP for block memory moves

See CHANGELOG.md for full history of all work on this model.
