# National NS32081 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.27%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 32-bit Floating-Point Unit (IEEE 754)
- Clock: 10 MHz
- Target CPI: 15.0
- Key instruction categories: fp_add, fp_mul, fp_div, fp_sqrt, dp_add, dp_mul, dp_div, conversion
- Supports both single and double precision operations

## Known Issues
- None currently - model validates within 5% error

## Suggested Next Steps
- Consider modeling the slave processor interface overhead
- Could add NS32016/NS32032 integration timing
- May want to model the NS32381 (successor) for comparison
- Consider adding denormalized number handling timing

## Key Architectural Notes
- National NS32081 (1982) was the FPU for the NS32000 family
- IEEE 754 floating-point standard compatible
- Single (32-bit) and double (64-bit) precision support
- Tightly coupled with NS32016/NS32032 processors
- Uses slave processor protocol for integration
- Hardware multiply and divide units
- 8 floating-point registers
- Exception handling support
- Part of complete NS32000 ecosystem (CPU, MMU, FPU)

## Instruction Timing Summary
| Category | Cycles | Description |
|----------|--------|-------------|
| fp_add | 8 | Single-precision add/subtract |
| fp_mul | 12 | Single-precision multiply |
| fp_div | 20 | Single-precision divide |
| fp_sqrt | 30 | Square root |
| dp_add | 12 | Double-precision add/subtract |
| dp_mul | 18 | Double-precision multiply |
| dp_div | 32 | Double-precision divide |
| conversion | 6 | Format conversion |

## Workload Profiles
- **typical**: Standard FPU usage (CPI = 15.0)
- **scientific**: Double-precision heavy (CPI ~ 18.8)
- **graphics**: Single-precision transforms (CPI ~ 11.5)
- **dsp**: Multiply-accumulate heavy (CPI ~ 10.9)
- **mixed**: Balanced workload (CPI ~ 14.5)

## NS32000 Family Integration
The NS32081 integrates with:
- NS32016: 16-bit data bus, 32-bit internal
- NS32032: Full 32-bit data bus
- NS32082: Memory Management Unit
- Uses slave processor protocol for seamless integration
