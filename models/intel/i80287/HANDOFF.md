# Intel 80287 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 3.1%
- **Last Updated**: 2026-01-28
- **Cross-Validation**: COMPLETE

## Current Model Summary
- Architecture: 80-bit floating-point coprocessor for 80286
- Year: 1983
- Clock: 8.0 MHz
- Target CPI: 100.0
- Predicted CPI: 96.9
- Instruction categories: fp_transfer, fp_add, fp_mul, fp_div, fp_sqrt, fp_trig

## Instruction Timing Tests
12 per-instruction timing tests added:
- FLD/FST: 20 cycles (within 17-22 documented range)
- FADD/FSUB: 85 cycles (within 80-90 documented range)
- FMUL: 140 cycles (within 130-145 documented range)
- FDIV: 200 cycles (within 190-210 documented range)
- FSQRT: 180 cycles (within 175-185 documented range)
- Transcendentals: 250 cycles (documented ~250)

## Cross-Validation Results
| Metric | 80287 | 80387 | Ratio |
|--------|-------|-------|-------|
| fp_transfer | 20 | 16 | 1.25x |
| fp_add | 85 | 35 | 2.43x |
| fp_mul | 140 | 65 | 2.15x |
| fp_div | 200 | 100 | 2.00x |
| fp_sqrt | 180 | 140 | 1.29x |
| CPI (typical) | 96.9 | 49.25 | 1.97x |

The ~2x slowdown vs 80387 is consistent with NMOS vs CMOS technology and algorithm improvements.

## Known Issues
- None - model validates within 5% error

## Suggested Next Steps
- No changes needed unless better documentation emerges
- Could add 8087 comparison if that model is created

## Key Architectural Notes
- The 80287 was the x87 coprocessor for the 80286
- NMOS technology limited clock speed and efficiency
- High CPI reflects the non-pipelined nature of FP operations
- 80387 successor achieved ~2x speedup with CMOS and improved algorithms

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Did not converge
- **CPI Error**: 0.09%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
