# Hitachi HD6301 Model Handoff

## Current Status: VALIDATED

**Last Updated:** 2026-01-29

## Quick Summary

The Hitachi HD6301 is an enhanced version of the Motorola 6801 microcontroller with improved instruction timing. It offers approximately 8% better performance than the original 6801.

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Manufacturer | Hitachi |
| Year | 1983 |
| Clock | 1.0 MHz internal (4x external) |
| Architecture | 8-bit, sequential execution |
| Target CPI | 3.5 |
| Compatibility | 6801 instruction set |

## Instruction Categories

| Category | Model Cycles | 6801 Cycles | Improvement |
|----------|-------------|-------------|-------------|
| alu | 2.4 | 2.7 | 11% faster |
| data_transfer | 2.6 | 2.9 | 10% faster |
| memory | 3.8 | 4.3 | 12% faster |
| control | 3.8 | 4.3 | 12% faster |
| stack | 4.5 | 5.3 | 15% faster |
| call_return | 7.5 | 8.5 | 12% faster |

## On-Chip Features

- **RAM:** 128 bytes internal
- **ROM:** Up to 4K mask ROM (HD6301V variant)
- **Timer:** 16-bit free-running timer with output compare
- **Serial I/O:** Full-duplex UART
- **I/O Ports:** Multiple programmable I/O ports
- **External Memory:** Up to 64K with external expansion

## Historical Context

The HD6301 was developed by Hitachi as an enhanced 6801:
- Fully compatible with 6801 instruction set
- Optimized microcode for faster execution
- CMOS versions available for low power
- Popular in automotive ECUs and industrial control

## Model Limitations

1. Uses category-weighted averages, not per-instruction timing
2. Does not model wait states for slow memory
3. Does not model on-chip peripheral timing
4. Does not model power modes

## Related Models

- Motorola M6801: Original processor (baseline)
- Motorola M6800: Predecessor architecture
- HD6303: Further enhanced variant

## Files

- **Model:** `current/hd6301_validated.py`
- **Validation:** `validation/hd6301_validation.json`
- **Changelog:** `CHANGELOG.md`
