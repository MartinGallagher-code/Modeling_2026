# TMS9985 Processor Model

## Overview
- **Manufacturer**: Texas Instruments
- **Year**: 1978
- **Architecture**: 16-bit single-chip CPU with 256B on-chip RAM, memory-to-memory workspace
- **Clock**: 2.5 MHz
- **Transistors**: ~10,000

## Validation Status
| Metric | Value |
|--------|-------|
| Target CPI | 10.000 |
| Predicted CPI | 10.089 |
| Error | 0.89% |
| Status | PASSED |

## Workload Results
| Workload | CPI | IPC | IPS |
|----------|-----|-----|-----|
| Typical | 10.089 | 0.099 | 247,795 |
| Compute | 9.514 | 0.105 | 262,771 |
| Memory | 9.702 | 0.103 | 257,692 |
| Control | 10.452 | 0.096 | 239,200 |

## Files
- `current/tms9985_validated.py` - Active model
- `validation/tms9985_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state and next steps
