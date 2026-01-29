# M68008 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 2.93%
- **Last Updated**: 2026-01-28

## Current Model Summary
The Motorola 68008 (1982) is an 8/32-bit microprocessor. Features 68000 core with 8-bit external data bus and 20-bit address space. Slower than 68000 due to narrower bus, but pin-compatible with 8-bit systems. Target CPI is 7.0 cycles per instruction.

| Parameter | Value | Description |
|-----------|-------|-------------|
| Target CPI | 7.0 | Expected cycles per instruction |
| Predicted CPI | 7.205 | Model output |
| External Bus | 8-bit | Narrower than 68000's 16-bit |
| Address Space | 20-bit | 1 MB addressable |

## Validation
The model includes a `validate()` method that runs 16 self-tests.
Current: **16/16 tests passing, 97.1% accuracy**

## Cross-Validation with 68K Family
- 25 per-instruction timing tests added (datasheet verified)
- Cross-validation section documents relationship to M68000/M68010/M68020
- **vs M68000**: 50-60% slower due to 8-bit bus
- **vs M68010**: 60-70% slower
- **vs M68020**: 5-8x slower

## Known Issues
None - model accuracy is within 5% target.

## Suggested Next Steps
1. Consider adding explicit bus width penalty for memory operations
2. Validate against Sinclair QL timing if emulator data available

## Key Architectural Notes
- 68000 core with 8-bit external data bus (same internal 32-bit architecture)
- Word operations take 2x bus cycles (vs 68000)
- Long operations take 4x bus cycles (vs 68000)
- 20-bit address space (1 MB)
- Same instruction set as 68000
- 70000 transistors
- 8 MHz typical clock
- Used in: Sinclair QL, cost-sensitive embedded systems
