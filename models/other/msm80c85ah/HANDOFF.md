# OKI MSM80C85AH Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 8-bit sequential execution (1983)
- Clock: 5.0 MHz, CMOS technology
- Categories: alu (4.0c), data_transfer (4.0c), memory (6.0c), control (5.0c), stack (10.0c)
- Predicted typical CPI: 5.000 (target: 5.0)

## Known Issues
- Model uses simplified category-based timing
- Fixed workload profiles may not match all real-world use cases

## Suggested Next Steps
- Cross-validate against Intel 8085 and OKI MSM80C85 models
- Verify high-speed timing margins in AH variant
- Consider adding I/O instruction category

## Key Architectural Notes
- "AH" suffix denotes high-speed bin of OKI's CMOS 8085 clone
- CMOS process provides lower power consumption vs NMOS originals
- Pin-compatible with Intel 8085, same instruction timing
- Used in portable/battery-powered equipment where CMOS power savings are critical
- Distinguished from base MSM80C85 by tighter speed specifications

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
