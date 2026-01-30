# TMS7000 Processor Model

## Overview
- **Manufacturer**: Texas Instruments
- **Year**: 1981
- **Architecture**: 8-bit MCU with 128 on-chip registers
- **Clock**: 2 MHz
- **Transistors**: ~20,000

## Validation Status
| Metric | Value |
|--------|-------|
| Target CPI | 7.000 |
| Predicted CPI | 6.992 |
| Error | 0.11% |
| Status | PASSED |

## Workload Results
| Workload | CPI | IPC | IPS |
|----------|-----|-----|-----|
| Typical | 6.992 | 0.143 | 286,041 |
| Compute | 6.692 | 0.149 | 298,864 |
| Memory | 6.692 | 0.149 | 298,864 |
| Control | 7.317 | 0.137 | 273,336 |

## Files
- `current/tms7000_validated.py` - Active model
- `validation/tms7000_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state and next steps
