# KR1858VM1 (T34VM1) Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-29

## Quick Summary

The KR1858VM1 (T34VM1) is a Soviet Z80 clone derived from East German U880 photomasks. It uses identical timing to the Zilog Z80 and U880.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union |
| Year | 1991 |
| Clock | 4.0 MHz |
| Architecture | 8-bit, sequential execution, no pipeline |
| Target CPI | 5.5 |
| Compatibility | Full Z80/U880 instruction set |

## Instruction Categories

| Category | Model Cycles | Description |
|----------|-------------|-------------|
| alu | 4.0 | ADD/SUB/INC/DEC register @4 |
| data_transfer | 4.0 | LD r,r @4 dominates |
| memory | 5.8 | LD r,(HL) @7 weighted |
| control | 5.5 | JP @10, JR @9.5 avg |
| stack | 10.0 | PUSH @11, POP @10 |
| block | 12.0 | LDIR weighted for termination |

## Historical Context

The KR1858VM1 represents the end of Soviet-era processor development. By using East German U880 photomasks, it maintained identical timing to the original Zilog Z80. It was one of the last processors designed under the Soviet system before the dissolution of the USSR.

## Model Limitations

1. Uses category-weighted averages, not per-instruction timing
2. Does not model wait states for slow memory
3. Does not model IX/IY prefix overhead (+4 cycles per instruction)
4. Does not model interrupt response latency

## Related Models

- Zilog Z80: Original processor
- VEB U880: East German Z80 clone (source of photomasks)
- NEC uPD780: Japanese Z80 clone

## Files

- **Model:** `current/kr1858vm1_validated.py`
- **Validation:** `validation/kr1858vm1_validation.json`
- **Changelog:** `CHANGELOG.md`

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 6
- **Corrections**: See `identification/sysid_result.json`
