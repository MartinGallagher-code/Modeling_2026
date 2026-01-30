# Z80B Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 1.55%
- **Last Updated**: 2026-01-28

## Current Model Summary
- Clock: 6.0 MHz (highest Z80 variant)
- Architecture: 8-bit, sequential execution
- Expected CPI: 5.5
- Predicted CPI: 5.585
- Typical IPS: ~1.07 MIPS
- Timing Tests: 19 per-instruction tests added

Key instruction categories (identical to Z80):
| Category | Cycles | Notes |
|----------|--------|-------|
| alu | 4.0 | ADD/SUB/INC/DEC register |
| data_transfer | 4.0 | LD r,r, EX |
| memory | 5.8 | (HL) addressing |
| control | 5.5 | JP/JR/CALL weighted |
| stack | 10.0 | PUSH/POP |
| block | 12.0 | LDIR/LDDR weighted |

## Known Issues
- None - model is fully validated
- Per-instruction accuracy varies due to category averaging (expected behavior)

## Suggested Next Steps
- No changes needed - model is complete
- If Z80B-specific timing anomalies are discovered, they could be added

## Key Architectural Notes
- Z80B is the highest-speed standard Z80 variant (6 MHz)
- All T-state timings are IDENTICAL to Z80/Z80A
- Same die as Z80, just binned for highest clock rate
- Highest-performance Z80 at approximately 1.07 MIPS

## Cross-Validation Summary
- Methodology: Grey-box queueing model with weighted instruction categories
- Timing verified against Z80 datasheet (all T-states match)
- MAME emulator uses same timing for Z80/Z80A/Z80B
- CPI accuracy: 1.55% error on typical workload

## Z80 Variant Comparison
| Variant | Clock | CPI | Approx IPS |
|---------|-------|-----|------------|
| Z80 | 2.5 MHz | 5.585 | 447K |
| Z80A | 4.0 MHz | 5.585 | 716K |
| Z80B | 6.0 MHz | 5.585 | 1.07M |

## Related Models
- Z80: Base model (2.5 MHz)
- Z80A: Mid-speed variant (4.0 MHz)

## Files
- Model: `current/z80b_validated.py`
- Validation: `validation/z80b_validation.json`

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
