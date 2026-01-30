# Intel 80387 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.5%
- **Last Updated**: 2026-01-28
- **Cross-Validation**: COMPLETE

## Current Model Summary
- Architecture: 80-bit floating-point coprocessor for 80386
- Year: 1987
- Clock: 16.0 MHz
- Target CPI: 50.0
- Predicted CPI: 49.25
- Instruction categories: fp_transfer, fp_add, fp_mul, fp_div, fp_sqrt, fp_trig

## Instruction Timing Tests
12 per-instruction timing tests added:
- FLD/FST: 16 cycles (within 14-18 documented range)
- FADD/FSUB: 35 cycles (within 30-40 documented range)
- FMUL: 65 cycles (within 60-70 documented range)
- FDIV: 100 cycles (within 95-105 documented range)
- FSQRT: 140 cycles (documented ~140)
- Transcendentals: 175 cycles (documented ~175-180)

## Cross-Validation Results
| Metric | 80287 | 80387 | Improvement |
|--------|-------|-------|-------------|
| fp_transfer | 20 | 16 | 20% |
| fp_add | 85 | 35 | 59% |
| fp_mul | 140 | 65 | 54% |
| fp_div | 200 | 100 | 50% |
| fp_sqrt | 180 | 140 | 22% |
| CPI (typical) | 96.9 | 49.25 | 49% |

The ~50% improvement over 80287 is consistent with CMOS technology and improved algorithms.

## Known Issues
- None - model validates within 5% error (best of the FPU models at 1.5%)

## Suggested Next Steps
- No changes needed unless better documentation emerges
- Could add 80486 FPU comparison (integrated on-die, even faster)

## Key Architectural Notes
- The 80387 was the x87 coprocessor for the 80386
- CMOS technology enabled higher clocks and better efficiency
- Improved algorithms reduced cycle counts by ~50%
- 80486 successor integrated FPU on-die for further improvement

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Did not converge
- **CPI Error**: 0.00%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
