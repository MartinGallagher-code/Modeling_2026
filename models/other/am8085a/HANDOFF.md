# AMD Am8085A Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 8-bit sequential execution (1978)
- Clock: 3.0 MHz, NMOS technology
- Categories: alu (4.0c), data_transfer (4.0c), memory (6.0c), control (5.0c), stack (10.0c)
- Predicted typical CPI: 5.000 (target: 5.0)

## Known Issues
- Model uses simplified category-based timing
- Fixed workload profiles may not match all real-world use cases

## Suggested Next Steps
- Cross-validate against Intel 8085 model for consistency
- Verify timing against AMD datasheet if available
- Consider relationship to later AMD x86 products

## Key Architectural Notes
- AMD second-source of Intel 8085 under cross-licensing agreement
- Pin-compatible and timing-identical to Intel 8085
- Part of AMD's extensive Intel second-source portfolio (8080, 8085, 8086, 8088)
- This second-source agreement was the foundation of AMD's x86 business
- AMD later produced Am286, Am386, and eventually independent x86 designs

## System Identification (2026-01-29)
- **Status**: Did not converge
- **CPI Error**: 0.32%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
