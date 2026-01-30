# Symbolics CADR Architectural Documentation

## Era Classification

**Era:** Sequential Execution (Microcoded)
**Period:** Early 1980s (1981)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 32-bit tagged data width (data + type tags)
- Microcoded instruction set for LISP operations
- Hardware CAR/CDR list access
- Hardware-assisted garbage collection
- ~50,000 transistors in TTL/MSI
- 5 MHz clock speed

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Symbolics (MIT AI Lab) |
| Year | 1981 |
| Clock | 5.0 MHz |
| Transistors | ~50,000 |
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

Microcoded: multi-cycle execution for LISP primitives
CPI = weighted sum of category cycles
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** (microcoded) template
2. Key modeling considerations:
   - CAR/CDR operations are fast (2 cycles) due to hardware support
   - CONS allocation requires memory management (5 cycles)
   - EVAL/function dispatch is microcoded (8 cycles)
   - GC is the most expensive at 12 cycles
   - Memory access includes type tag validation (6 cycles)
   - Type checking is hardware-accelerated (3 cycles)

## Validation Approach

- Compare against MIT AI Lab documentation
- Validate with LISP benchmark workloads
- Target: <5% CPI prediction error

## References

- [MIT AI Lab Memos](https://dspace.mit.edu/handle/1721.1/5458)
- [Wikipedia - LISP Machine](https://en.wikipedia.org/wiki/Lisp_machine)

---
Generated: 2026-01-29
