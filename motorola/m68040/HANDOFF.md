# M68040 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.75%
- **Last Updated**: 2026-01-28

## Current Model Summary
The Motorola 68040 (1990) is a high-performance 32-bit microprocessor. Features 6-stage pipeline, integrated FPU, 4KB instruction cache, 4KB data cache. First 68K with on-chip FPU. Target CPI is 2.0 cycles per instruction.

| Parameter | Value | Description |
|-----------|-------|-------------|
| Target CPI | 2.0 | Expected cycles per instruction |
| Predicted CPI | 2.035 | Model output |
| I-Cache | 4 KB | 4-way set-associative |
| D-Cache | 4 KB | 4-way set-associative |
| FPU | On-chip | First 68K with integrated FPU |
| Pipeline | 6-stage | Deeper than 68030 |

## Validation
The model includes a `validate()` method that runs 17 self-tests.
Current: **17/17 tests passing, 98.2% accuracy**

## Cross-Validation with 68K Family
- 25 per-instruction timing tests added (datasheet verified)
- Cross-validation section documents relationship to M68030/M68060
- **vs M68030**: 2-3x faster at same clock
- **vs M68020**: 3-4x faster
- **vs M68060**: 2-3x slower

## Known Issues
None - model accuracy is within 5% target.

## Suggested Next Steps
1. FPU timing could be modeled in more detail
2. Validate against Mac Quadra emulator if data available

## Key Architectural Notes
- First 68K with on-chip FPU
- 6-stage integer pipeline (vs 3 in 68020/030)
- Pipelined multiply (5 cycles vs 28 in 68030)
- 4KB I-cache, 4KB D-cache (4-way set-associative)
- On-chip MMU with 64-entry ATC
- Simple static branch prediction
- Copy-back cache with write allocation
- 1.2M transistors
- 25-40 MHz clock range
- Used in: Mac Quadra series, Amiga 4000, NeXTstation Turbo
- Variants: 68LC040 (no FPU), 68EC040 (no FPU/MMU)
