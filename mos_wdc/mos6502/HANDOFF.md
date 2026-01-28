# MOS 6502 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.4%
- **Last Updated**: 2026-01-28

## Current Model Summary

Architecture: 8-bit sequential execution (no pipeline)

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 3.0 | Mix of implied @2 and memory-based @3-4 |
| data_transfer | 3.5 | LDA/STA with various addressing modes |
| memory | 4.2 | Including indexed/indirect modes |
| control | 3.0 | Branches @2.5 avg, JMP @3 |
| stack | 3.5 | PHA @3, PLA @4, JSR/RTS @6 weighted |

## Known Issues

None - model is well-calibrated.

## Suggested Next Steps

1. **Add more workload profiles** - could add game-specific profiles (NES, C64) if usage data available

2. **Individual instruction validation** - the validation JSON has per-instruction timing tests that could be implemented

3. **Decimal mode** - BCD operations have same timing but could model separately for completeness

## Key Architectural Notes

- Zero-page is the key to 6502 performance (256 pseudo-registers)
- Only 3 general-purpose registers (A, X, Y) but addressing modes compensate
- Fixed stack at $0100-$01FF (only 256 bytes)
- Branch taken adds +1 cycle, page cross adds +1 more
- (Indirect),Y mode is the workhorse for array processing

See CHANGELOG.md for full history of all work on this model.
