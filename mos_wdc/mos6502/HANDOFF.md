# MOS 6502 Model Handoff

## Current Status
- **Validation**: PASSED (Cross-validated)
- **CPI Error**: 1.22%
- **Last Updated**: 2026-01-28

## Current Model Summary

Architecture: 8-bit sequential execution (no pipeline)
Cross-validated against MOS datasheet timings and realistic instruction mix.

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2.3 | INX/DEX @2, ADC imm @2, ADC zp @3 |
| data_transfer | 2.8 | LDA imm @2, zp @3, abs @4 |
| memory | 4.0 | STA zp @3, abs @4, indexed @4-5 |
| control | 2.6 | Branches @2.55 avg, JMP @3 |
| stack | 3.5 | PHA @3, PLA @4, JSR/RTS @6 |

**Performance:**
- Target CPI: 3.0 (cross-validated)
- Model CPI: 3.065
- At 1 MHz: ~326,000 instructions/second

## Cross-Validation

Method: Weighted instruction timing analysis
- Reference CPI: 3.028 (from realistic instruction mix)
- Model CPI: 3.065
- Error: 1.22%

Sources:
- MOS Technology 6502 Datasheet (May 1976)
- Masswerk 6502 instruction reference
- NES/C64 software instruction distribution analysis

## Known Issues

None - model is cross-validated against actual 6502 timings.

## Suggested Next Steps

1. **Validate against VICE emulator** - Run actual test programs and compare cycle counts
2. **Add per-instruction validation** - Use timing_tests in validation JSON
3. **Test against specific software** - NES games, C64 demos with known cycle counts

## Key Architectural Notes

- Zero-page is the key to 6502 performance (256 pseudo-registers at 3 cycles)
- Immediate mode is fastest (2 cycles) - use for constants
- (Indirect),Y mode is the workhorse for array processing (5-6 cycles)
- Branch taken adds +1 cycle, page cross adds +1 more
- JSR/RTS both take exactly 6 cycles

See CHANGELOG.md for full history of all work on this model.
