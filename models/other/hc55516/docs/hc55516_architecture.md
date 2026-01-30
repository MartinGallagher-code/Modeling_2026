# Harris HC-55516 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1982)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- CVSD (Continuously Variable Slope Delta) audio codec chip
- Single-bit CVSD input, analog output
- Adaptive step size for slope tracking
- Simple decode-filter-DAC processing pipeline
- Used in Williams arcade games (Defender, Robotron, Sinistar)
- Used in Williams pinball machines for speech and sound effects
- Minimal logic -- not a general-purpose processor

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Harris |
| Year | 1982 |
| Clock | 2.0 MHz |
| Transistors | 1,500 |
| Data Width | 1-bit (CVSD) |
| Address Width | 0-bit (no addressable memory) |

## Queueing Model Architecture

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  FETCH  │──►│ DECODE  │──►│ EXECUTE │──►│ MEMORY  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘
    │              │              │              │
    ▼              ▼              ▼              ▼
  M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue

CPI = Fetch + Decode + Execute + Memory (serial sum)
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Target CPI of 2.0 (simple codec, few operations per sample)
   - CVSD bit decode and slope adaptation at 1.5 cycles
   - Syllabic filter / integrator update at 2 cycles
   - DAC analog output update at 2 cycles
   - Mode and clock control at 1.5 cycles
   - Sample rate synchronization is most expensive at 3 cycles
   - Decode and filter operations dominate typical workload (55%)

## Validation Approach

- Compare against original Harris HC-55516 datasheet
- Validate with Williams arcade hardware timing analysis
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/Continuously_variable_slope_delta_modulation)

---
Generated: 2026-01-29
