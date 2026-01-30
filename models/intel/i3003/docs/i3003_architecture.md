# Intel 3003 Architectural Documentation

## Era Classification

**Era:** Combinational Logic
**Period:** Mid 1970s (1975)
**Queueing Model:** Single-stage M/M/1

## Architectural Features

- 2-bit carry lookahead generator
- Single-cycle operation for all functions
- Companion to Intel 3002 bit-slice ALU
- ~100 transistors in Schottky bipolar
- 10 MHz clock speed

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intel |
| Year | 1975 |
| Clock | 10.0 MHz |
| Transistors | ~100 |
| Data Width | 2-bit |
| Technology | Schottky bipolar |

## Queueing Model Architecture

```
+---------+
| EXECUTE |  (single-cycle combinational logic)
+---------+
     |
     v
   M/M/1
   Queue

CPI = 1.0 (all operations single-cycle)
```

## Model Implementation Notes

1. This component uses a trivial single-cycle model
2. Key modeling considerations:
   - All operations are combinational logic
   - No pipeline, no multi-cycle operations
   - CPI is always exactly 1.0
   - Designed as companion chip, not standalone processor

## Validation Approach

- Confirm single-cycle operation from datasheet
- Validate companion chip relationship with Intel 3002
- Target: exact CPI match (1.0)

## References

- [Intel 3003 Datasheet](https://bitsavers.org/components/intel/3000/)
- Intel 3000 family documentation

---
Generated: 2026-01-29
