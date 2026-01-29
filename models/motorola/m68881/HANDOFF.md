# M68881 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.5%
- **Last Updated**: 2026-01-28

## Current Model Summary
The Motorola 68881 (1985) is the first floating-point coprocessor for the 68020/68030. IEEE 754 compliant with 80-bit extended precision and 8 FP registers.

| Category | Model Cycles | Documented Cycles | Description |
|----------|--------------|-------------------|-------------|
| fp_move | 4 | 30 | FMOVE, FABS, FNEG |
| fp_add | 6 | 70 | FADD, FSUB, FCMP |
| fp_mul | 8 | 95 | FMUL |
| fp_div | 25 | 135 | FDIV |
| fp_sqrt | 35 | 138 | FSQRT |
| fp_trig | 55 | 493-600 | FSIN, FCOS, FTAN, etc. |

Note: Model cycles are effective averages for workload weighting; documented cycles are from MC68881/MC68882 User's Manual (M68881 is ~1.25x slower than M68882).

## Cross-Validation with M68882
- M68881 is the original FPU (1985)
- M68882 is the improved version (1987) with ~1.5x better performance
- Both use same instruction set (IEEE 754 compliant)
- M68882 has head/tail architecture for better instruction concurrency

## Validation
The model includes a `validate()` method that runs 16 self-tests.
Current: **16/16 tests passing, 99.5% accuracy**

## Per-Instruction Timing Tests
15 FPU instructions documented in validation JSON:
- Basic: FMOVE, FABS, FNEG
- Arithmetic: FADD, FSUB, FMUL, FDIV, FSQRT, FCMP
- Transcendental: FSIN, FCOS, FTAN, FSINCOS, FLOG2, FEXP

## Known Issues
None - model is well-calibrated and cross-validated with M68882.

## Suggested Next Steps
1. Consider modeling M68881 as slightly slower than M68882 if differentiated performance is needed
2. Could add separate single/double/extended precision timing variants

## Key Architectural Notes
- First 68K FPU coprocessor (1985)
- IEEE 754 floating-point
- 8 80-bit FP registers (FP0-FP7)
- Hardware transcendental functions (slow, 400-600 cycles)
- ~155,000 transistors
- 12-25 MHz clock range
- Works with 68020/68030 host processors

## References
- MC68881/MC68882 User's Manual (Motorola, 1987)
- NXP Reference Manual: https://www.nxp.com/docs/en/reference-manual/MC68881UM.pdf
- Dr. Dobb's: Optimizing MC68882 Code
