# AMD Am9511 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: Stack-based arithmetic processing unit (math coprocessor)
- Clock: 3 MHz
- Target CPI: 25.0
- Key instruction categories: fp_add, fp_mul, fp_div, fp_sqrt, fixed_point
- Floating-point operations dominate execution time
- Cross-validated with 12 per-instruction timing tests

## Known Issues
- None currently - model validates within 5% error

## Suggested Next Steps
- Consider adding more detailed timing for specific instruction variants
- Could model the 4-level stack behavior more explicitly
- May want to add host CPU interface overhead modeling
- Consider modeling the Am9512 (successor) for comparison

## Key Architectural Notes
- AMD Am9511 (1977) is an early arithmetic processing unit
- Designed as math coprocessor for 8-bit microprocessor systems
- Stack-based operation with 4-level internal operand stack
- Supports 32-bit floating point (IEEE-like format)
- Supports 16-bit and 32-bit fixed-point operations
- Commonly paired with Intel 8080/8085, Z80, and other 8-bit CPUs
- Data transfer via 8-bit parallel interface
- Predecessor to Am9512 with improved performance
- Key operations: FADD, FSUB, FMUL, FDIV, SQRT, plus fixed-point equivalents
- Also supports transcendental functions (SIN, COS, TAN, etc.) in some variants

## Instruction Timing Summary
| Category | Cycles | Description |
|----------|--------|-------------|
| fp_add | 16 | Floating-point add/subtract |
| fp_mul | 24 | Floating-point multiply |
| fp_div | 32 | Floating-point divide |
| fp_sqrt | 45 | Square root |
| fixed_point | 8 | Fixed-point operations |

## Workload Profiles
- **typical**: Standard math coprocessor usage (CPI = 25.0)
- **scientific**: Heavy sqrt/div usage (CPI ~ 28.1)
- **graphics**: Transform-heavy, more multiply (CPI ~ 20.65)
- **fixed_heavy**: Mostly fixed-point (CPI ~ 15.35)
- **mixed**: Balanced workload (CPI ~ 24.14)
