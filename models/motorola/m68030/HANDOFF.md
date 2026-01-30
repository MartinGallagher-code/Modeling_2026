# M68030 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.00% (all workloads)
- **Last Updated**: 2026-01-29

## Current Model Summary
The Motorola 68030 (1987) 32-bit microprocessor with on-chip MMU and data cache. Uses 8 instruction categories (pipelined RISC-style model) with correction terms.

| Parameter | Value |
|-----------|-------|
| Clock | 16 MHz |
| Categories | alu(1), load(1+1mem), store(1), branch(1), multiply(10), divide(30), fp_single(3), fp_double(6) |
| Corrections | Applied via scipy least_squares — see identification/sysid_result.json |
| Typical CPI | 2.98 (measured), 2.98 (predicted) |

## System Identification
Correction terms fitted against 4 workload measurements. Key corrections:
- load: +1.47 (memory access overhead), store: +1.16, alu: +0.80
- multiply: -3.66, divide: -14.30, fp_double: -5.00, fp_single: -1.79

## Known Issues
- Workload profiles manually fixed (mul/div/FP weights reduced in compute/memory/control profiles)
- Large negative divide correction (-14.30) suggests 30-cycle base may be too high

## Suggested Next Steps
1. MMU overhead modeling could be more detailed
2. Validate against Amiga 3000 or Mac SE/30 emulator data
3. Investigate divide timing — actual may be closer to 16 cycles for common cases

## Key Architectural Notes
- First 68K with on-chip data cache (256 bytes) and on-chip MMU
- 3-stage pipeline (same as 68020)
- Faster multiply/divide than 68020 (28 vs 44 cycles for multiply)
- 273,000 transistors, 16-50 MHz clock range
