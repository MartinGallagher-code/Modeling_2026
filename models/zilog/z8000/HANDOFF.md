# Z8000 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.67% (best accuracy in Zilog family)
- **Last Updated**: 2026-01-28

## Current Model Summary
- Clock: 4.0 MHz
- Architecture: 16-bit, orthogonal instruction set
- Expected CPI: 4.5
- Predicted CPI: 4.470
- Typical IPS: ~0.89 MIPS
- Timing Tests: 17 per-instruction tests added

Key instruction categories:
| Category | Cycles | Notes |
|----------|--------|-------|
| alu | 3.2 | ADD/SUB R,R weighted |
| data_transfer | 2.8 | LD R,R @3 (fast) |
| memory | 5.0 | Various addressing modes |
| control | 4.8 | JP/JR weighted |
| stack | 8.0 | PUSH/POP 16-bit |
| block | 9.0 | Block transfers |

## Known Issues
- None - model validates with best accuracy (0.67%)
- Compute workload is marginal (5.2% error)

## Suggested Next Steps
- Could model segmented addressing overhead for Z8001 variant
- Could add privileged mode switching overhead
- May want separate model for Z8001 vs Z8002 if needed

## Key Architectural Notes
**IMPORTANT: Z8000 is NOT related to Z80!**
- Completely different 16-bit architecture
- Orthogonal instruction set design
- 16 general-purpose 16-bit registers (R0-R15)
- Can be used as 8 32-bit register pairs
- Two variants: Z8001 (segmented), Z8002 (non-segmented)

## Z8001 vs Z8002
| Variant | Address Space | Package |
|---------|---------------|---------|
| Z8001 | 23-bit segmented (8MB) | 48-pin |
| Z8002 | 16-bit non-segmented (64KB) | 40-pin |

## Historical Context
- Released 1979
- Competitor to Motorola 68000 and Intel 8086
- Commercial failure due to:
  - Late market timing
  - 68000 had better performance
  - Limited software ecosystem
- Used in: Olivetti M20, some Unix workstations

## Cross-Validation Summary
- Methodology: Grey-box queueing model for orthogonal 16-bit architecture
- Timing verified against Z8000 datasheet (ps0045.pdf)
- Fast 16-bit register operations model well
- CPI accuracy: 0.67% error on typical workload (best in family)

## Related Models
- Z80000: 32-bit extension (architecturally related)
- NOT related to Z80/Z80A/Z80B/Z180/Z8

## Files
- Model: `current/z8000_validated.py`
- Validation: `validation/z8000_validation.json`

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
