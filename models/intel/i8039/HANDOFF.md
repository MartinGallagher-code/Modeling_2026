# Intel 8035/8039 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: <5%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 8-bit NMOS microcontroller (MCS-48 ROM-less)
- Year: 1976
- Clock: 6.0 MHz
- Target CPI: 1.5 (same as 8048)
- Machine cycle: 15 clock periods = 2.5 us

Key instruction categories:
| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 1.0 | ALU operations |
| data_transfer | 1.0 | Register moves |
| memory | 2.5 | External memory access |
| control | 2.5 | Jumps and calls |

## Cross-Validation Status
- **Identical timing**: Intel 8048, 8748, 8035
- **Related processors**: Intel 8049 (larger memory), 8051 (successor)
- **Timing rule**: Register ops 1 cycle, memory/control 2 cycles

## Known Issues
- None - model uses validated 8048 timing

## Suggested Next Steps
- Model is complete based on 8048 timing
- Could add specific workload profiles for external ROM systems

## Key Architectural Notes
- The Intel 8035 and 8039 are ROM-less versions of the MCS-48 family
- 8035: 64 bytes internal RAM (same as 8048)
- 8039: 128 bytes internal RAM (same as 8049)
- Requires external ROM for program storage
- Same instruction set and timing as ROM versions
- Used for prototyping and systems needing larger/changeable code
- Harvard architecture with separate program and data memory

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 4
- **Corrections**: See `identification/sysid_result.json`
