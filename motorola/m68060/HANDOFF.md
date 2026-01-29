# M68060 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.40%
- **Last Updated**: 2026-01-28

## Current Model Summary
The Motorola 68060 (1994) is a superscalar 32-bit microprocessor. Features dual-issue superscalar architecture, 8KB instruction cache, 8KB data cache, branch prediction, and limited out-of-order execution. Target CPI is 1.5 cycles per instruction.

| Parameter | Value | Description |
|-----------|-------|-------------|
| Target CPI | 1.5 | Expected cycles per instruction |
| Predicted CPI | 1.479 | Model output |
| I-cache hit rate | 98% | 8KB instruction cache |
| D-cache hit rate | 94% | 8KB data cache |
| Superscalar | Dual-issue | Can execute 2 ops per cycle |
| Pipeline | 10-stage | Deeper than 68040 |

## Validation
The model includes a `validate()` method that runs 18 self-tests.
Current: **18/18 tests passing, 98.6% accuracy**

## Cross-Validation with 68K Family
- 25 per-instruction timing tests added (datasheet verified)
- Cross-validation section documents relationship to M68040/M68030/M68020
- **vs M68040**: 2-3x faster at same clock
- **vs M68030**: 5-6x faster
- **vs M68020**: 8-10x faster
- **vs PowerPC 601**: Comparable (but arrived too late)

## Known Issues
None - model accuracy is excellent (1.40% error).

## Suggested Next Steps
1. Could model dual-issue constraints in more detail
2. Branch prediction accuracy modeling could be refined

## Key Architectural Notes
- Last and fastest 68K processor
- Dual-issue superscalar architecture
- 10-stage integer pipeline
- Branch prediction with 256-entry branch cache
- Pipelined multiply (2 cycles vs 5 in 68040)
- Much faster divide (10 cycles vs 38 in 68040)
- 8KB I-cache, 8KB D-cache (4-way set-associative)
- Limited out-of-order execution
- 2.5M transistors
- 50-75 MHz clock range
- **Historical tragedy**: Released 1994, same year PowerPC Mac shipped
- Used in: Amiga 4000T/4060, Atari Falcon accelerators, embedded systems
- Some FPU instructions emulated in software (transcendentals)
