# NEC V30 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: ~5.5%
- **Last Updated**: 2026-01-29

## Current Model Summary

Architecture: Improved 8086 compatible (1984)
Pin-compatible drop-in replacement, ~30% faster overall.
16-bit external data bus (vs V20's 8-bit bus).

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2 | ADD/SUB reg,reg @2 (was 3 on 8086) |
| data_transfer | 2.5 | MOV reg,reg @2, MOV reg,mem @3-5 |
| memory | 4 | Memory ops - 16-bit bus faster than V20 |
| control | 2.5 | JMP @2-3, Jcc @4-14 avg |
| multiply | 4 | MUL @27-28 (was 118-128 on 8086) |
| divide | 7 | DIV improved ~3x over 8086 |

**Performance:**
- Target CPI: 3.2 (~30% faster than 8086)
- Model CPI: 3.025
- At 10 MHz: ~3.31 MIPS

## Relationship to V20

The V30 is the 16-bit bus sibling of the V20:

| Feature | V20 | V30 |
|---------|-----|-----|
| Compatible with | Intel 8088 | Intel 8086 |
| External data bus | 8-bit | 16-bit |
| Internal architecture | Same | Same |
| Pin-compatible with | 8088 | 8086 |
| Typical speedup | 10-20% vs 8088 | ~30% vs 8086 |

Both share:
- 63,000 transistors
- Hardware multiply/divide
- 80186 instruction extensions
- 8080 emulation mode
- Dual internal 16-bit buses

## Cross-Validation

Method: Comparison with Intel 8086 plus documented speedup factors
- 8086 CPI: ~4.5
- V30 CPI: ~3.0
- Speedup: ~1.49x (within documented 1.25-1.50x range)

Also cross-validated against V20 model:
- V20 CPI: ~3.4
- V30 should be faster due to 16-bit bus (confirmed)

## Known Issues

Model uses weighted average cycle counts for multiply/divide. Actual speedup
varies significantly based on instruction mix (multiply-heavy code sees >30% boost).

## Suggested Next Steps

1. Model is well-validated for typical workloads
2. Consider adding 80186 instruction extensions as separate category
3. Could model 8080 emulation mode performance

## Key Architectural Notes

- Pin-compatible 8086 replacement (swap chips, instant speedup)
- 16-bit external bus (key difference from V20's 8-bit bus)
- Hardware multiply/divide instead of microcode (3-4x faster)
- 50% duty cycle (vs 33% on 8086) - more work per clock
- Dual internal 16-bit buses
- Includes 80186 instruction set extensions
- 8080 emulation mode for legacy software
- Some timing-dependent software broke (ran too fast)
- Clock range: 8-16 MHz (typical: 10 MHz)

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
