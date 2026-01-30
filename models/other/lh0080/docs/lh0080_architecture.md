# Sharp LH0080 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1970s (1976)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Second-source implementation of Zilog Z80 by Sharp Corporation
- 8-bit data path with 16-bit address bus
- NMOS technology, 2.5 MHz clock
- Full Z80 instruction set compatibility
- Block transfer and search instructions
- Two register banks for fast context switching
- Sequential execution with no pipeline
- Pin-compatible with Zilog Z80

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Sharp |
| Year | 1976 |
| Clock | 2.5 MHz |
| Transistors | ~8,500 |
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
   - Z80-compatible timing (pin-compatible clone)
   - ALU and data transfer at 4 T-states each
   - Memory indirect at 6 T-states, control at 5.5 T-states average
   - Block instructions at 12+ T-states
   - Used extensively in Sharp's own personal computer line

## Validation Approach

- Compare against Zilog Z80 known timing
- Cross-validate against Sharp datasheet
- Target: <5% CPI prediction error

## References

- [Sharp LH0080 Datasheet](TODO: Add link)
- [Zilog Z80 Reference](https://en.wikipedia.org/wiki/Zilog_Z80)
- [Sharp MZ-80K](https://en.wikipedia.org/wiki/Sharp_MZ)

---
Generated: 2026-01-29
