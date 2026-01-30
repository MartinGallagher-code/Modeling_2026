# Intel 2920 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s (1979)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- First Intel DSP attempt (analog signal processor)
- 25-bit data path for analog signal processing
- On-chip ADC (8-bit) and DAC (8-bit)
- NO hardware multiplier (software MAC required)
- 192 x 24-bit program ROM
- 40 x 25-bit data RAM
- 5 MHz clock, 400ns minimum instruction time
- ~50 signal processing instructions

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intel |
| Year | 1979 |
| Clock | 5.0 MHz |
| Transistors | 15,000 |
| Data Width | 25-bit |
| Address Width | 8-bit |

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
   - Target CPI of 5.0 for typical analog signal processing workloads
   - Arithmetic is expensive at 7 cycles (no HW multiplier, software MAC)
   - Data transfer at 3 cycles (limited RAM addressing)
   - ADC/DAC conversion most expensive at 8 cycles (conversion overhead)
   - Control flow at 3.5 cycles
   - Shift operations at 3 cycles (single-bit shift per instruction)
   - Lack of hardware multiplier is the primary performance limitation

## Validation Approach

- Compare against original Intel 2920 datasheet
- Validate with known analog signal processing benchmarks
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/Intel_2920)

---
Generated: 2026-01-29
