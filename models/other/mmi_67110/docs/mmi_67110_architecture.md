# MMI 67110 Architectural Documentation

## Era Classification

**Era:** Sequential Execution (Microprogram Control)
**Period:** Late 1970s (1978)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 4-bit enhanced microprogram sequencer
- Subroutine call/return with hardware stack
- Loop counter for iteration control
- Conditional branching
- ~3,000 transistors in bipolar Schottky
- 10 MHz clock speed

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Monolithic Memories Inc. |
| Year | 1978 |
| Clock | 10.0 MHz |
| Transistors | ~3,000 |
| Data Width | 4-bit |
| Address Width | 12-bit |

## Queueing Model Architecture

```
+----------+   +----------+   +----------+
| SEQUENCE |-->|  BRANCH  |-->|  STACK   |
|   GEN    |   |  DECODE  |   | PUSH/POP |
+----------+   +----------+   +----------+
     |              |              |
     v              v              v
   M/M/1          M/M/1          M/M/1
   Queue          Queue          Queue

CPI = weighted sum of category cycles
```

## Model Implementation Notes

1. This component uses the **Sequential Execution** template
2. Key modeling considerations:
   - Sequential address generation is single-cycle
   - Branch requires address computation (2 cycles)
   - Subroutines need stack operations (3 cycles)
   - Loop counting is single-cycle
   - Not a standalone CPU but a sequencer component

## References

- [MMI 67110 Datasheet](TODO: Add link)
- Bit-slice processor design textbooks

---
Generated: 2026-01-29
