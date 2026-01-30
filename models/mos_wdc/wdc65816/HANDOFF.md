# WDC 65816 Model Handoff

## Current Status
- **Validation**: PASSED (Cross-validated)
- **CPI Error**: 0.53%
- **Last Updated**: 2026-01-28

## Current Model Summary

Architecture: 16-bit CMOS (extended 65C02)
Cross-validated with 16-bit mode overhead analysis.

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 3.2 | +1 cycle in 16-bit mode (m=0) |
| data_transfer | 3.8 | Mix of 8/16-bit modes |
| memory | 4.5 | Including long 24-bit addressing |
| control | 3.5 | Branches + long jumps (JML @4, JSL @8) |
| stack | 4.0 | 16-bit push/pull take +1 cycle |

**Performance:**
- Target CPI: 3.8 (~33% slower than 65C02's 2.85)
- Model CPI: 3.82
- At 4 MHz: ~1.05 MIPS

## Cross-Validation

Method: Comparison with 65C02 plus 16-bit mode overhead
- Reference CPI: 3.8
- Model CPI: 3.82
- Error: 0.53%
- Per-instruction tests: 26/26 passing

Mode assumptions for SNES/Apple IIGS usage:
- 50% accumulator 16-bit (m=0)
- 30% index 16-bit (x=0)
- 20% long addressing usage

16-bit overhead:
- LDA/STA/ADC add 1 cycle in 16-bit mode
- PHA/PLA add 1 cycle in 16-bit mode
- JSL = 8 cycles (vs JSR = 6)
- Long addressing adds 1 cycle

## Known Issues

None - model is well-calibrated for mixed 8/16-bit operation.

## Suggested Next Steps

1. **Separate 8-bit vs 16-bit profiles** - model pure 8-bit mode vs 16-bit mode
2. **SNES-specific profiling** - DMA operations, PPU register access patterns

## Key Architectural Notes

- 65816 extends 65C02 to 16 bits with backward compatibility
- 8/16-bit modes switchable via processor status register (SEP/REP)
- 24-bit address bus (16 MB address space)
- SNES ran at ~3.58 MHz (slower than 65C02's 4 MHz typical)
- JSL/RTL for cross-bank subroutine calls (8/6 cycles)
- MVN/MVP for block memory moves

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
