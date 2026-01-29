# NEC V20 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 4.4%
- **Last Updated**: 2026-01-28

## Current Model Summary

Architecture: Improved 8088 compatible (1984)
Pin-compatible drop-in replacement, 10-20% faster overall.

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2 | ADD/SUB reg,reg @2 (was 3 on 8088) |
| data_transfer | 3 | MOV reg,reg @2, MOV reg,mem @4-6 |
| memory | 6 | Memory ops with faster EA calculation |
| control | 3 | JMP @3, Jcc @4-16 avg |
| multiply | 6 | MUL @29-30 (was 118-133 on 8088) |
| divide | 10 | DIV improved ~3x over 8088 |

**Performance:**
- Target CPI: 3.4 (~15% faster than 8088)
- Model CPI: 3.55
- At 8 MHz: ~2.25 MIPS

## Cross-Validation

Method: Comparison with Intel 8088 plus documented speedup factors
- 8088 CPI: ~4.0
- V20 CPI: ~3.55
- Speedup: ~1.13x (within documented 1.10-1.20x range)

## Known Issues

Model uses weighted average cycle counts for multiply/divide. Actual speedup
varies significantly based on instruction mix (multiply-heavy code sees >20% boost).

## Suggested Next Steps

1. **NEC V30 model** - V20's sibling with 16-bit external bus (8086 compatible)
2. **Separate multiply-heavy workload** - to show true V20 advantage
3. Model is well-validated for typical workloads

## Key Architectural Notes

- Pin-compatible 8088 replacement (swap chips, instant speedup)
- Hardware multiply/divide instead of microcode (3-4x faster)
- 50% duty cycle (vs 33% on 8088) - more work per clock
- Dual internal 16-bit buses
- Includes 80186 instruction set extensions
- 8080 emulation mode for legacy software
- Some timing-dependent software broke (LodeRunner needed patching)

See CHANGELOG.md for full history of all work on this model.
