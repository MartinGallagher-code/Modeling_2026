# OKI MSM80C85AH Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1983)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- CMOS second-source implementation of Intel 8085 by OKI
- 8-bit data path with 16-bit address bus
- CMOS technology for low-power operation
- Full 8085 instruction set compatibility
- Sequential execution with no pipeline
- 5 MHz clock (high-speed "AH" variant)
- Pin-compatible with Intel 8085

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | OKI Semiconductor |
| Year | 1983 |
| Clock | 5.0 MHz |
| Transistors | ~6,500 |
| Data Width | 8-bit |
| Address Width | 16-bit |
| Technology | CMOS |
| Variant | High-speed (AH) |

## Queueing Model Architecture

```
+----------+   +----------+   +----------+   +----------+
|  FETCH   |-->|  DECODE  |-->| EXECUTE  |-->|  MEMORY  |
+----------+   +----------+   +----------+   +----------+
    |              |              |              |
    v              v              v              v
  M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue

CPI = Fetch + Decode + Execute + Memory (serial sum)
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Identical timing to Intel 8085 (pin-compatible clone)
   - ALU and data transfer at 4 cycles each
   - Memory at 6 cycles, control flow at 5 cycles
   - Stack operations slowest at 10 cycles
   - CMOS technology same timing but lower power than NMOS

## Validation Approach

- Compare against Intel 8085 known timing
- Cross-validate against OKI MSM80C85 base variant
- Target: <5% CPI prediction error

## References

- [OKI MSM80C85AH Datasheet](TODO: Add link)
- [Intel 8085 Reference](https://en.wikipedia.org/wiki/Intel_8085)

---
Generated: 2026-01-29
