# TMS9980 Processor Model

## Overview
- **Manufacturer**: Texas Instruments
- **Year**: 1976
- **Architecture**: 16-bit CPU with 8-bit external bus, memory-to-memory workspace
- **Clock**: 2 MHz
- **Transistors**: ~8,000

## Validation Status
| Metric | Value |
|--------|-------|
| Target CPI | 12.000 |
| Predicted CPI | 12.084 |
| Error | 0.70% |
| Status | PASSED |

## Workload Results
| Workload | CPI | IPC | IPS |
|----------|-----|-----|-----|
| Typical | 12.084 | 0.083 | 165,508 |
| Compute | 11.434 | 0.087 | 174,917 |
| Memory | 11.684 | 0.086 | 171,174 |
| Control | 12.434 | 0.080 | 160,849 |

## Files
- `current/tms9980_validated.py` - Active model
- `validation/tms9980_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state and next steps
