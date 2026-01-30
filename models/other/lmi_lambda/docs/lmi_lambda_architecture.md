# LMI Lambda Architectural Documentation

## Era Classification

**Era:** Sequential Execution (Microcoded)
**Period:** Mid 1980s (1984)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 32-bit tagged data width for native LISP support
- CADR-derivative microcoded architecture
- Hardware CAR/CDR operations
- Improved CONS allocation over original CADR
- ~60,000 transistors in TTL/MSI
- 4 MHz clock speed

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | LISP Machines Inc. |
| Year | 1984 |
| Clock | 4.0 MHz |
| Transistors | ~60,000 |
| Data Width | 32-bit (tagged) |
| Address Width | 24-bit |

## Queueing Model Architecture

```
+---------+   +----------+   +---------+   +----------+
|  FETCH  |-->| TYPE CHK |-->| EXECUTE |-->|  MEMORY  |
+---------+   +----------+   +---------+   +----------+
    |              |              |              |
    v              v              v              v
  M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue

CADR-derivative: microcoded with modest improvements
CPI = weighted sum of category cycles
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** (microcoded) template
2. Key modeling considerations:
   - CAR/CDR same as CADR at 2 cycles
   - CONS improved from 5 to 4 cycles
   - EVAL improved from 8 to 7 cycles
   - GC improved from 12 to 11 cycles
   - Memory improved from 6 to 5 cycles
   - Type checking unchanged at 3 cycles
   - Overall CPI between CADR (5.5) and TI Explorer (4.0)

## Validation Approach

- Compare against LMI documentation
- Cross-validate with Symbolics CADR and TI Explorer
- Target: <5% CPI prediction error

## References

- [Wikipedia - LISP Machine](https://en.wikipedia.org/wiki/Lisp_machine)
- LMI technical documentation

---
Generated: 2026-01-29
