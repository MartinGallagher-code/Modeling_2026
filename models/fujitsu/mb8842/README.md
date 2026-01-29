# Fujitsu MB8842

4-bit microcontroller (1977) - MB8841 variant for arcade applications.

## Overview

| Property | Value |
|----------|-------|
| Manufacturer | Fujitsu |
| Year | 1977 |
| Data Width | 4-bit |
| Clock | 1 MHz |
| Target CPI | 4.0 |
| Architecture | Harvard, parallel ALU |

## Description

The MB8842 is a variant of the Fujitsu MB8841 4-bit microcontroller, specifically used in arcade machines (notably Namco arcade hardware). It shares the same instruction set and timing as the MB8841 base model.

All instructions execute in exactly 4 clock cycles (1 machine cycle), giving a fixed CPI of 4.0.

## Files

- `current/mb8842_validated.py` - Validated processor model
- `validation/mb8842_validation.json` - Validation data
- `HANDOFF.md` - Model status and notes
- `CHANGELOG.md` - Change history
