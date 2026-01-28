# MOS 6510 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.4%
- **Last Updated**: 2026-01-28

## Current Model Summary

Architecture: 8-bit sequential execution (identical to 6502 + I/O port)

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 3.0 | Mix of implied @2 and memory-based @3-4 |
| data_transfer | 3.5 | LDA/STA with various addressing modes |
| memory | 4.2 | Including indexed/indirect modes |
| control | 3.0 | Branches @2.5 avg, JMP @3 |
| stack | 3.5 | PHA @3, PLA @4, JSR/RTS @6 weighted |

## Known Issues

None - timing is identical to well-validated 6502.

## Suggested Next Steps

1. **C64-specific workloads** - could profile actual C64 software for more accurate workload weights

2. **I/O port overhead** - accessing $00-$01 for bank switching might be worth modeling separately

## Key Architectural Notes

- 6510 = 6502 + 8-bit I/O port at addresses $00-$01
- The I/O port is used for C64 memory banking
- Clock is slightly under 1 MHz in C64 (0.985 MHz NTSC)
- All instruction timing identical to 6502

See CHANGELOG.md for full history of all work on this model.
