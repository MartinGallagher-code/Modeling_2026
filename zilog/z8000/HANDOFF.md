# Z8000 Model Handoff

## Current Status: VALIDATED (0.7% error)

## Quick Summary
The Z8000 is Zilog's 16-bit processor (NOT Z80 compatible). Model validated with 0.7% CPI error.

## Key Parameters
- Clock: 4.0 MHz
- Architecture: 16-bit, 16 general-purpose registers, orthogonal encoding
- Target CPI: 4.5
- Achieved CPI: 4.470

## Instruction Categories
| Category | Cycles | Notes |
|----------|--------|-------|
| alu | 3.2 | ADD R,R @4, weighted |
| data_transfer | 2.8 | LD R,R @3, fast 16-bit |
| memory | 5.0 | Various addressing modes |
| control | 4.8 | JP @7, weighted |
| stack | 8.0 | PUSH/POP 16-bit |
| block | 9.0 | Block transfers |

## Important Notes
- Z8000 is NOT compatible with Z80 - completely different ISA
- Two variants: Z8001 (segmented), Z8002 (non-segmented)

## Related Models
- None - Z8000 is architecturally distinct from Z80 family

## Potential Improvements
- Could model segmented addressing overhead for Z8001
- Could add privileged mode switching overhead

## Files
- Model: `current/z8000_validated.py`
- Validation: `validation/z8000_validation.json`
