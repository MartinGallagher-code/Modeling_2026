# NEC uPD8080AF Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1970s (1975)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Second-source implementation of Intel 8080 by NEC Corporation
- 8-bit data path with 16-bit address bus
- NMOS technology, 2 MHz clock
- Full 8080 instruction set compatibility
- Sequential execution with no pipeline
- Pin-compatible with Intel 8080
- "AF" improved version with better electrical characteristics

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1975 |
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
   - ALU at 4 cycles, data transfer at 5 cycles
   - Memory access at 7 cycles, control at 5 cycles
   - Stack operations at 10 cycles
   - NEC was Intel's primary Japanese second-source partner

## Validation Approach

- Compare against Intel 8080 known timing
- Cross-validate against NEC datasheet
- Target: <5% CPI prediction error

## References

- [NEC uPD8080AF Datasheet](TODO: Add link)
- [Intel 8080 Reference](https://en.wikipedia.org/wiki/Intel_8080)

---
Generated: 2026-01-29
