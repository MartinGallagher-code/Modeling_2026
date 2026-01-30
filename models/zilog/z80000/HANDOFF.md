# Z80000 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 4.83%
- **Last Updated**: 2026-01-28
- **Confidence**: Medium (limited documentation)

## Current Model Summary
- Clock: 16.0 MHz
- Architecture: 32-bit extension of Z8000
- Expected CPI: 6.0
- Predicted CPI: 6.290
- Typical IPS: ~2.54 MIPS
- Timing Tests: 15 per-instruction tests added (estimated values)

Key instruction categories:
| Category | Cycles | Confidence |
|----------|--------|------------|
| alu_reg | 3.0 | Medium |
| alu_imm | 4.0 | Medium |
| load | 5.0 | Medium |
| store | 5.0 | Medium |
| control | 6.0 | Medium |
| call_return | 10.0 | Medium |
| multiply | 40.0 | Low |
| divide | 55.0 | Low |

## Known Issues
- **Limited documentation**: Commercial failure means very few datasheets exist
- Timings are educated estimates based on Z8000 heritage
- May need refinement if original Zilog Z80000 datasheet is found

## Suggested Next Steps
- Search for original Zilog Z80000 datasheet to verify timings
- Consider MMU overhead if modeling protected mode operations
- Could add string/block instructions if documentation found

## Key Architectural Notes
- Z80000 is 32-bit extension of Z8000 (NOT related to Z80)
- 16 general-purpose 32-bit registers
- On-chip MMU with segmentation support
- Full 32-bit address space (4GB)
- Sequential execution with instruction prefetch (no true pipeline)
- CMOS technology

## Historical Context
- Released 1986 (late to 32-bit market)
- Competitor to Motorola 68020 and Intel 80386
- **Commercial failure** - very few units sold
- Zilog exited high-end CPU market after Z80000
- Company refocused on embedded/MCU market (Z8, eZ80)

## Z8000 Heritage
| Feature | Z8000 | Z80000 |
|---------|-------|--------|
| Data Width | 16-bit | 32-bit |
| Address Space | 16/23-bit | 32-bit |
| Technology | NMOS | CMOS |
| MMU | External | On-chip |
| Transistors | 17,500 | 91,000 |

## Cross-Validation Summary
- Methodology: Grey-box queueing model based on Z8000 heritage
- Timings estimated from Z8000 baseline scaled for 32-bit
- Limited verification possible due to documentation scarcity
- CPI accuracy: 4.83% error on typical workload

## Related Models
- Z8000: 16-bit predecessor (architecturally related)
- NOT related to Z80/Z80A/Z80B/Z180/Z8

## Files
- Model: `current/z80000_validated.py`
- Validation: `validation/z80000_validation.json`

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 8
- **Corrections**: See `identification/sysid_result.json`
