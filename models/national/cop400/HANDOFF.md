# National COP400 Model Handoff

## Current Status
- **Validation**: MARGINAL
- **CPI Error**: 5.00%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 4-bit (1977)
- Clock: 1.0 MHz, NMOS technology
- Categories: alu (3.5c), data_transfer (3.5c), memory (4.5c), control (5.0c), io (4.5c)
- Predicted typical CPI: 4.200 (target: 4.0)

## Known Issues
- Model uses simplified category-based timing
- Fixed workload profiles may not match all real-world use cases

## Suggested Next Steps
- Validate against datasheet instruction timing tables
- Cross-reference with related processor models
- Add per-instruction timing tests

## Key Architectural Notes
- Hugely popular 4-bit MCU, billions manufactured, used in appliances and toys
- Features: Harvard architecture, 44 instructions, 512B ROM, 32 nibbles RAM, Billions manufactured

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 5
- **Corrections**: See `identification/sysid_result.json`
