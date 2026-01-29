# AMI S2400

4-bit calculator chip (1973) - Improved S2000 series.

## Overview

| Property | Value |
|----------|-------|
| Manufacturer | American Microsystems Inc. |
| Year | 1973 |
| Data Width | 4-bit |
| Clock | 300 kHz |
| Target CPI | 7.0 |
| Technology | PMOS |

## Description

The AMI S2400 is an improved version of the S2000 series with a faster clock (300 kHz vs 200 kHz) and slightly better instruction timing (CPI 7.0 vs 8.0).

## Instruction Categories

| Category | Cycles |
|----------|--------|
| alu | 5 |
| data_transfer | 6 |
| memory | 8 |
| io | 9 |
| control | 7 |

## Files

- `current/ami_s2400_validated.py` - Validated processor model
- `validation/ami_s2400_validation.json` - Validation data
- `HANDOFF.md` - Model status and notes
- `CHANGELOG.md` - Change history
