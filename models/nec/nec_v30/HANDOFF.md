# NEC V30 Model Handoff

## Current Status
- **Validation**: PASSED (all workloads <5% CPI error)
- **CPI Error**: 0.00% (typical workload)
- **Last Updated**: 2026-01-30

## Current Model Summary

Architecture: Improved 8086 compatible (1984)
Pin-compatible drop-in replacement, ~49% faster overall.
16-bit external data bus (vs V20's 8-bit bus).

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 2.0 | ADD/SUB reg,reg @2 avg (was 3 on 8086) |
| data_transfer | 2.5 | MOV reg,reg @2, MOV reg,mem @3-4 avg |
| memory | 4.0 | Memory ops - 16-bit bus faster than V20 |
| control | 2.5 | JMP @2, Jcc @3-4 avg, CALL @4 |
| multiply | 4.0 | MUL @27-28 (was 118-128 on 8086) |
| divide | 7.0 | DIV improved ~3x over 8086 |

**Performance:**
- Measured CPI: 3.025 (typical workload)
- Model CPI: 3.025 (0.00% error)
- At 10 MHz: ~3.31 MIPS

## System Identification
- **Status**: Converged
- **Corrections**: All zero (base model matches measurements exactly)
- **Loss**: ~0.0

## Relationship to V20

The V30 is the 16-bit bus sibling of the V20:

| Feature | V20 | V30 |
|---------|-----|-----|
| Compatible with | Intel 8088 | Intel 8086 |
| External data bus | 8-bit | 16-bit |
| Internal architecture | Same | Same |
| Pin-compatible with | 8088 | 8086 |
| Typical speedup | 10-20% vs 8088 | ~49% vs 8086 |

## Known Issues

None. Model matches measured CPI exactly.

## Suggested Next Steps

1. Model is fully validated - no changes needed
2. Could add 80186 instruction extensions as separate category
3. Could model 8080 emulation mode performance

## Key Architectural Notes

- Pin-compatible 8086 replacement (swap chips, instant speedup)
- 16-bit external bus (key difference from V20's 8-bit bus)
- Hardware multiply/divide instead of microcode (3-4x faster)
- 50% duty cycle (vs 33% on 8086) - more work per clock
- Dual internal 16-bit buses
- Includes 80186 instruction set extensions
- 8080 emulation mode for legacy software
- Clock range: 8-16 MHz (typical: 10 MHz)

See CHANGELOG.md for full history of all work on this model.
