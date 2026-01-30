# Western Digital WD9000 Pascal MicroEngine

## Overview
The WD9000 Pascal MicroEngine (1979) was a unique processor designed to execute UCSD Pascal p-code directly in hardware through microprogramming. Rather than using a general-purpose instruction set, the WD9000 implemented Pascal virtual machine operations as native instructions, providing significant performance gains over software p-code interpreters.

## Specifications
- **Manufacturer**: Western Digital
- **Year**: 1979
- **Data Width**: 16-bit
- **Clock Speed**: 10 MHz
- **Technology**: NMOS
- **Transistors**: ~10,000

## Model Details
- **Target CPI**: 8.0
- **Architecture**: Microprogrammed p-code execution, stack-based
- **Workloads**: typical, compute, memory, control

## Files
- `current/wd9000_validated.py` - Validated processor model
- `validation/wd9000_validation.json` - Validation data and test results
- `HANDOFF.md` - Current status and handoff notes
- `CHANGELOG.md` - Complete change history
