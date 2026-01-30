# Z8 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 4.60%
- **Last Updated**: 2026-01-28

## Current Model Summary
- Clock: 8.0 MHz (external)
- Architecture: 8-bit single-chip MCU with register-file
- Expected CPI: 10.0
- Predicted CPI: 9.540
- Typical IPS: ~0.84 MIPS
- Timing Tests: 17 per-instruction tests added

Key instruction categories:
| Category | Cycles | Notes |
|----------|--------|-------|
| register_ops | 6.0 | LD/ADD/SUB r,r |
| immediate | 6.0 | LD/ADD r,IM |
| memory | 12.0 | Indexed/indirect |
| control | 12.0 | JP/JR/DJNZ |
| stack | 14.0 | PUSH/POP internal stack |
| call_return | 20.0 | CALL/RET |

## Known Issues
- None - model validates within 5% error target
- Higher CPI than Z80 due to MCU architecture overhead

## Suggested Next Steps
- Could refine timings if more detailed Z8 datasheet becomes available
- Consider adding I/O instruction category for peripheral operations
- May want to add interrupt handling overhead for real-time workloads

## Key Architectural Notes
**IMPORTANT: Z8 is NOT a Z80 variant!**
- Completely different architecture
- Register-file design: 144 general-purpose 8-bit registers in internal RAM
- Single-chip MCU, not just a CPU
- On-chip peripherals: timers, UART, I/O ports
- Internal clock is half external clock rate (2 external = 1 internal)

## Z80 vs Z8 Comparison
| Feature | Z80 | Z8 |
|---------|-----|-----|
| Type | CPU | MCU |
| Architecture | Register-based | Register-file |
| Registers | 14 (limited) | 144 GP |
| Memory | External | Internal ROM/RAM |
| Typical CPI | 5.5 | 10.0 |
| Target Use | General purpose | Embedded control |

## Cross-Validation Summary
- Methodology: Grey-box queueing model for MCU architecture
- Timing verified against Z8 datasheet (ps0199.pdf)
- Register-file overhead increases CPI vs traditional designs
- CPI accuracy: 4.60% error on typical workload

## Related Models
- None - Z8 is architecturally distinct from Z80 family

## Files
- Model: `current/z8_validated.py`
- Validation: `validation/z8_validation.json`

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 3.46%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
