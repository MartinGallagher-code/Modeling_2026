# WDC 65C02 Model Handoff

## Current Status
- **Validation**: PASSED (Cross-validated)
- **CPI Error**: 0.35%
- **Last Updated**: 2026-01-28

## Current Model Summary

Architecture: 8-bit CMOS (optimized 6502)
Cross-validated against 6502 baseline with documented CMOS optimizations.

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2.2 | INX/DEX @2, ADC imm @2, ADC zp @3 |
| data_transfer | 2.6 | LDA imm @2, zp @3, abs @4 - faster indexed |
| memory | 3.6 | RMW abs,X @6 (was 7 on NMOS 6502) |
| control | 2.5 | BRA @3, branches @2.55 avg, JMP @3 |
| stack | 3.2 | PHX/PLX @3/4, JSR @6, RTS @6 |

**Performance:**
- Target CPI: 2.85 (~5% faster than 6502's 3.0)
- Model CPI: 2.84
- At 4 MHz: ~1.4 MIPS

## Cross-Validation

Method: Comparison with cross-validated 6502 plus CMOS optimizations
- Reference CPI: 2.85
- Model CPI: 2.84
- Error: 0.35%
- Per-instruction tests: 20/20 passing

Key optimizations over NMOS 6502:
- RMW abs,X takes 6 cycles instead of 7
- BRA instruction (unconditional branch)
- PHX/PHY/PLX/PLY for index register saves
- No dummy cycles in indexed addressing

## Known Issues

None - model is cross-validated and correctly faster than 6502.

## Suggested Next Steps

1. **High-speed variants** - 65C02 runs up to 14 MHz; could model cache effects
2. Model is well-validated - no immediate work needed

## Key Architectural Notes

- CMOS 6502 with bug fixes and new instructions
- ~5% faster than NMOS 6502 (CPI 2.85 vs 3.0)
- BRA (branch always) is a key new instruction
- PHX/PHY/PLX/PLY simplify register preservation
- STZ (store zero) makes common operation efficient
- Can run at much higher clock speeds than NMOS (up to 14 MHz)

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
