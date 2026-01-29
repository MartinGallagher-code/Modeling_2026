# AT&T DSP-20 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.67%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 16-bit Improved Bell Labs DSP
- Clock: 10 MHz
- Target CPI: 3.0
- Predicted CPI: 2.95
- Key instruction categories: mac, alu, data_move, control, io

## Cross-Validation Status
- **Family comparison**: Successor to DSP-1 (CPI 4.0 -> 3.0)
- **Era comparison**: Contemporary with TMS320C10 (1983)
- **Architecture notes**: Improved microcode, doubled clock

## Known Issues
- None currently - model validates within 5% error
- Limited public documentation (Bell Labs internal)

## Suggested Next Steps
- Cross-validate timing improvements vs DSP-1
- Compare with contemporary TMS320C10
- Research transition to WE DSP32 series

## Key Architectural Notes
- Improved version of Bell Labs DSP-1
- Doubled clock speed (5 MHz -> 10 MHz)
- More efficient microcode reduces cycle counts
- Still primarily internal/captive use
- Predecessor to commercial WE DSP32 family
