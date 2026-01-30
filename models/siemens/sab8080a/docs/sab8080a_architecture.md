# Siemens SAB8080A Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1970s (1976)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Second-source implementation of Intel 8080 by Siemens AG
- 8-bit data path with 16-bit address bus
- NMOS technology, 2 MHz clock
- Full 8080 instruction set compatibility
- Sequential execution with no pipeline
- Pin-compatible with Intel 8080
- Manufactured in West Germany

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Siemens |
| Year | 1976 |
| Clock | 2.0 MHz |
| Transistors | ~6,000 |
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
   - Identical timing to Intel 8080 (pin-compatible clone)
   - ALU operations at 4 cycles, data transfers at 5 cycles
   - Memory access at 7 cycles, control flow at 5 cycles
   - Stack operations slowest at 10 cycles
   - Siemens manufactured under license from Intel
   - Used primarily in European industrial/telecom applications

## Validation Approach

- Compare against Intel 8080 known timing
- Cross-validate against Siemens datasheet
- Target: <5% CPI prediction error

## References

- [Siemens SAB8080A Datasheet](TODO: Add link)
- [Intel 8080 Reference](https://en.wikipedia.org/wiki/Intel_8080)

---
Generated: 2026-01-29
