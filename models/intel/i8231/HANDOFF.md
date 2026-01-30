# Intel 8231 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 4.4%
- **Last Updated**: 2026-01-29

## Current Model Summary
- 9 instruction categories ranging from data_transfer (14c) to float_sqrt (110c)
- Fixed-point: add=20c, mul=42c, div=60c
- Floating-point: add=36c, mul=60c, div=88c, sqrt=110c
- Data transfer: 14c (4 base + 10 memory for 32-bit via 8-bit bus)
- Bus penalty factor: 1.02x, queueing factor: 1.0 + rho*0.04
- Target CPI: 40.0, Model CPI: 38.222
- Clock: 2 MHz, ~10,000 transistors (1977)

## Known Issues
- Only the typical workload is validated against the target CPI of 40.0
- Compute workload CPI (49.1) is 22.8% above target -- expected since compute-heavy mixes weight expensive float operations
- Memory workload CPI (27.6) is 31.0% below target -- expected since data transfers are cheaper than math ops
- Per-workload targets would improve validation coverage

## Suggested Next Steps
- Model passes validation; no urgent changes needed
- Could establish per-workload expected CPIs for more thorough validation
- Could refine the bus penalty model if 8231 bus timing documentation is found
- Could add double-precision (64-bit) operation categories if needed

## Key Architectural Notes
- The 8231 is a math coprocessor, not a general-purpose CPU
- Stack-based architecture: operands pushed via 8-bit bus, results popped back
- Designed to pair with 8080/8085 CPUs for floating-point acceleration
- All 32-bit data must traverse an 8-bit bus, adding significant transfer overhead
- Predecessor to the more capable Intel 8087 FPU
