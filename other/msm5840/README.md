# OKI MSM5840

4-bit microcontroller with LCD driver (1982).

## Overview

| Property | Value |
|----------|-------|
| Manufacturer | OKI Semiconductor |
| Year | 1982 |
| Data Width | 4-bit |
| Clock | 500 kHz |
| Target CPI | 6.0 |
| Key Feature | Integrated LCD driver |

## Description

The OKI MSM5840 is a 4-bit microcontroller with an integrated LCD controller/driver, designed for calculators, watches, and other LCD-equipped consumer devices. It features 6 instruction categories including dedicated LCD operations.

## Instruction Categories

| Category | Cycles |
|----------|--------|
| alu | 4 |
| data_transfer | 5 |
| memory | 6 |
| lcd | 8 |
| io | 7 |
| control | 6 |

## Files

- `current/msm5840_validated.py` - Validated processor model
- `validation/msm5840_validation.json` - Validation data
- `HANDOFF.md` - Model status and notes
- `CHANGELOG.md` - Change history
