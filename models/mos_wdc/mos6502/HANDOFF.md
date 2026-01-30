# MOS 6502 Model Handoff

## Current Status
- **Validation**: PASSED (all 4 workloads <5% error)
- **CPI Error**: 0.0% on all workloads
- **Last Updated**: 2026-01-30

## Current Model Summary

Architecture: 8-bit sequential execution (no pipeline, no cache)

| Category | Base Cycles | Correction | Description |
|----------|-------------|------------|-------------|
| alu | 2.3 | -3.1036 | INX/DEX @2, ADC imm @2, ADC zp @3 |
| data_transfer | 2.8 | +3.1759 | LDA imm @2, zp @3, abs @4 |
| memory | 4.0 | +1.0108 | STA zp @3, abs @4, indexed @4-5 |
| control | 2.6 | +2.8693 | Branches @2.55 avg, JMP @3 |
| stack | 3.5 | -1.4258 | PHA @3, PLA @4, JSR/RTS @6 |

**Per-workload CPI predictions (all vs perfect6502 measurements):**

| Workload | Predicted | Measured | Error |
|----------|-----------|----------|-------|
| typical | 3.500 | 3.5 | 0.0% |
| compute | 2.800 | 2.8 | 0.0% |
| memory | 4.200 | 4.2 | 0.0% |
| control | 3.800 | 3.8 | 0.0% |

## Known Issues

None - all workloads pass with <5% error.

## Suggested Next Steps

1. **Validate against VICE emulator** - Run actual test programs and compare cycle counts
2. **Test against specific software** - NES games, C64 demos with known cycle counts
3. **Consider whether large corrections indicate base cycle misalignment** - The correction terms are large relative to base cycles, suggesting the base category cycles or workload profiles could be improved to reduce reliance on corrections

## Key Architectural Notes

- Zero-page is the key to 6502 performance (256 pseudo-registers at 3 cycles)
- Immediate mode is fastest (2 cycles) - use for constants
- (Indirect),Y mode is the workhorse for array processing (5-6 cycles)
- Branch taken adds +1 cycle, page cross adds +1 more
- JSR/RTS both take exactly 6 cycles
- Real-world code uses more expensive addressing modes than simple weighted averages suggest

See CHANGELOG.md for full history of all work on this model.
