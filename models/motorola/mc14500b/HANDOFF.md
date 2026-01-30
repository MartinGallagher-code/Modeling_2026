# MC14500B Model Handoff

## Current Status
- Validation: Fully validated (0% CPI error - fixed 1-cycle timing)
- Last Updated: 2026-01-29

## Summary
- Architecture: 1-bit Industrial Control Unit (ICU), CMOS, 1976
- Era: Fixed-cycle combinational execution (no pipeline)
- All 16 instructions execute in exactly 1 clock cycle
- No program counter (external sequencer)

**Performance:**
- CPI = 1.0 (fixed, all workloads)
- IPC = 1.0
- At 1 MHz: 1,000,000 IPS
- At 4 MHz (15V): 4,000,000 IPS

## Cross-Validation
- Confirmed by Motorola MC14500B Handbook (1977)
- Confirmed by Ken Shirriff reverse-engineering analysis (2021)
- Confirmed by WikiChip specifications
- All 16 instructions verified as single-cycle

## Model Category Breakdown
| Category | Instructions | Cycles | Typical Weight |
|----------|-------------|--------|----------------|
| logic | AND, ANDC, OR, ORC, XNOR | 1 | 0.35 |
| load_store | LD, LDC, STO, STOC | 1 | 0.30 |
| control | JMP, RTN, SKZ, IEN, OEN | 1 | 0.30 |
| nop | NOPO, NOPF | 1 | 0.05 |

## Key Architectural Notes
- JMP/RTN are output flags, NOT internal branches
- SKZ gates the write enable of the next instruction
- IEN/OEN gate data input/output respectively
- External memory and program counter required

See CHANGELOG.md for work history.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 4
- **Corrections**: See `identification/sysid_result.json`
