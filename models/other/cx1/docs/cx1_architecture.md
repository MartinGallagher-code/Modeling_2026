# Nippon Columbia CX-1 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1983)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Custom arcade audio DSP
- 16-bit data width, sequential execution
- Optimized for audio filtering and waveform generation
- ~15,000 transistors in NMOS
- 5 MHz clock speed

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Nippon Columbia |
| Year | 1983 |
| Clock | 5.0 MHz |
| Transistors | ~15,000 |
| Data Width | 16-bit |
| Address Width | 12-bit |

## Queueing Model Architecture

```
+---------+   +---------+   +---------+   +---------+
|  FETCH  |-->| DECODE  |-->| EXECUTE |-->| OUTPUT  |
+---------+   +---------+   +---------+   +---------+
    |              |              |              |
    v              v              v              v
  M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue

CPI = weighted sum of category cycles (sequential)
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - MAC operations are 2 cycles (no hardware pipeline)
   - Filter operations are most expensive at 4 cycles
   - Audio output requires 3 cycles for DAC processing
   - Memory access for sample buffers takes 4 cycles
   - Control flow operations require 3 cycles

## Validation Approach

- Compare against arcade hardware documentation
- Validate with MAME emulator timing data
- Target: <5% CPI prediction error

## References

- [MAME Source](https://github.com/mamedev/mame)
- Arcade hardware schematics and documentation

---
Generated: 2026-01-29
