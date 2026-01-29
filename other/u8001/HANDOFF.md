# VEB U8001 Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-29

## Quick Summary

The VEB U8001 is a Zilog Z8001 clone manufactured by VEB Mikroelektronik Erfurt. It was the first 16-bit microprocessor in the Eastern Bloc. The model uses identical timing to the Zilog Z8000.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Manufacturer | VEB Mikroelektronik Erfurt |
| Year | 1984 |
| Clock | 4.0 MHz |
| Architecture | 16-bit, sequential execution, segmented memory |
| Target CPI | 5.5 |
| Compatibility | Full Zilog Z8001 instruction set |

## Instruction Categories

| Category | Model Cycles | Description |
|----------|-------------|-------------|
| alu | 4.0 | ADD/SUB R,R @4, R,IM @7 |
| data_transfer | 4.0 | LD R,R @3, LD R,IM @7 |
| memory | 6.0 | LD R,@R @7, LD R,addr @9 |
| io | 7.0 | IN/OUT @10-12 |
| control | 6.0 | JP @7, CALL @12, RET @9 |
| string | 8.0 | Block transfer/search |

## Historical Context

The U8001 was a significant achievement for East German semiconductor industry, providing 16-bit capability for industrial and military applications. It was reverse-engineered from the Zilog Z8001 and represented a major step up from the 8-bit U880 (Z80 clone).

## Model Limitations

1. Uses category-weighted averages, not per-instruction timing
2. Does not model segmented memory overhead
3. Does not model multiply/divide latency in detail
4. Does not model interrupt response latency

## Related Models

- Zilog Z8001: Original processor (this is a clone)
- U880: Earlier East German Z80 clone (8-bit)

## Files

- **Model:** `current/u8001_validated.py`
- **Validation:** `validation/u8001_validation.json`
- **Changelog:** `CHANGELOG.md`
