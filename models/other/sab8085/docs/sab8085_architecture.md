# Siemens SAB8085 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s (1978)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Second-source implementation of Intel 8085 by Siemens AG
- 8-bit data path with 16-bit address bus
- NMOS technology, 3 MHz clock
- Full 8085 instruction set compatibility
- Sequential execution with no pipeline
- Pin-compatible with Intel 8085
- Multiplexed address/data bus
- On-chip clock generator and serial I/O

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Siemens |
| Year | 1978 |
| Clock | 3.0 MHz |
| Transistors | ~6,500 |
| Data Width | 8-bit |
| Address Width | 16-bit |
| Technology | NMOS |

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
   - Siemens manufactured under license from Intel

## Validation Approach

- Compare against Intel 8085 known timing
- Cross-validate against Siemens datasheet
- Target: <5% CPI prediction error

## References

- [Siemens SAB8085 Datasheet](TODO: Add link)
- [Intel 8085 Reference](https://en.wikipedia.org/wiki/Intel_8085)

---
Generated: 2026-01-29
