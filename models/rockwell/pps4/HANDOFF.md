# Rockwell PPS-4 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: <5%
- **Last Updated**: 2026-01-29

## Historical Significance

The Rockwell PPS-4 (Parallel Processing System - 4 bit) was the **third commercial microprocessor**, released in 1972:

1. **Intel 4004** (November 1971) - First commercial microprocessor
2. **Intel 4040** (1971) - Enhanced 4004
3. **Rockwell PPS-4** (1972) - Third commercial microprocessor

Despite its name containing "Parallel", the PPS-4 actually uses a **serial bit-processing architecture**, processing data one bit at a time through its ALU.

## Current Model Summary

Architecture: 4-bit serial ALU microprocessor (1972)

| Category | Cycles | Description |
|----------|--------|-------------|
| alu | 14 | Serial ADD/SUB (bit-by-bit processing) |
| memory | 11 | Load/Store operations |
| branch | 12 | Conditional/unconditional jumps |
| io | 10 | Discrete I/O operations |

**Performance:**
- Target CPI: 12.0
- Model CPI: ~12.0
- Clock: 200 kHz
- At 200 kHz: ~16,667 IPS

## Cross-Validation

Compared to contemporary 4-bit processors:

| Processor | Year | CPI | Clock | Notes |
|-----------|------|-----|-------|-------|
| Intel 4004 | 1971 | 10.8 | 740 kHz | Parallel ALU |
| TMS1000 | 1974 | 6.0 | 300 kHz | Fixed timing |
| **PPS-4** | 1972 | 12.0 | 200 kHz | Serial ALU |

The higher CPI and lower clock of PPS-4 reflects its serial architecture trade-off: fewer transistors (cost savings) for slower performance.

## Known Issues

None currently. Serial ALU architecture is correctly modeled.

## Suggested Next Steps

1. **PPS-4/1 and PPS-4/2 variants** - Later enhanced versions
2. **GM7xx family** - General Instrument's similar architecture
3. Model may benefit from more detailed instruction-level timing data if available

## Key Architectural Notes

- **Serial ALU**: Processes 4-bit data one bit at a time
- **Trade-off**: Smaller die area (fewer transistors) vs. slower execution
- **Harvard architecture**: Separate program and data memory
- **Applications**:
  - Calculators (simple arithmetic needs)
  - Pinball machines (Bally used PPS-4 extensively)
  - Point-of-sale terminals
  - Simple controllers

## Serial vs Parallel ALU

The PPS-4's serial ALU architecture explains its slower performance:

```
Parallel ALU (e.g., 4004):
  Input:  [b3 b2 b1 b0] -> ALU -> [r3 r2 r1 r0] Output
  (All 4 bits processed simultaneously)

Serial ALU (PPS-4):
  Clock 1: b0 -> ALU -> r0
  Clock 2: b1 -> ALU -> r1
  Clock 3: b2 -> ALU -> r2
  Clock 4: b3 -> ALU -> r3
  (4 clocks minimum for 4-bit operation)
```

This serial approach reduces transistor count but increases cycle count for arithmetic operations.

See CHANGELOG.md for full history of all work on this model.

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.00%
- **Free Parameters**: 4
- **Corrections**: See `identification/sysid_result.json`
