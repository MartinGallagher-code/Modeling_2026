# KR580VM1 Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-29

## Quick Summary

The KR580VM1 is a Soviet 8080 extension (NOT a direct clone) that adds 128KB bank-switched memory addressing. Base instruction timing matches the Intel 8080, but bank-switch operations add overhead.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union (various fabs) |
| Year | 1980 |
| Clock | 2.5 MHz |
| Architecture | 8-bit, sequential execution, bank-switched memory |
| Target CPI | 8.0 |
| Compatibility | Intel 8080 base ISA + bank extensions |

## Instruction Categories

| Category | Model Cycles | Description |
|----------|-------------|-------------|
| alu | 5.0 | ADD/SUB r @4, ADD M @7, weighted |
| data_transfer | 5.0 | MOV r,r @5, MVI @7 |
| memory | 9.0 | LDA @13, MOV r,M @7, weighted |
| io | 10.0 | IN/OUT @10 states |
| control | 8.0 | JMP @10, CALL @17, weighted |
| bank_switch | 12.0 | Bank select with overhead |

## Historical Context

The KR580VM1 represents a unique Soviet approach to extending Western processor designs rather than simply cloning them. By adding bank-switching capability to the 8080 architecture, Soviet engineers doubled the addressable memory space while maintaining backward compatibility with existing 8080 software.

## Model Limitations

1. Uses category-weighted averages, not per-instruction timing
2. Bank-switch overhead is estimated from documentation
3. Does not model bank-switch latency in detail
4. Does not model interrupt response with bank switching

## Related Models

- Intel 8080: Base processor architecture
- KR580VM80A: Direct Soviet 8080 clone (without extensions)

## Files

- **Model:** `current/kr580vm1_validated.py`
- **Validation:** `validation/kr580vm1_validation.json`
- **Changelog:** `CHANGELOG.md`
