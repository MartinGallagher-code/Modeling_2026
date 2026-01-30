# Thomson EFCIS 90435 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1980
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- French military-grade 8-bit microprocessor
- Radiation-hardened design for avionics applications
- Used in Mirage fighter aircraft systems
- 8-bit data path with 16-bit address bus
- Designed by Thomson-CSF (now Thales)
- 4 MHz clock
- Approximately 8,000 transistors
- Military reliability requirements drive conservative timing

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Thomson-CSF |
| Year | 1980 |
| Clock | 4.0 MHz |
| Transistors | ~8,000 |
| Data Width | 8-bit |
| Address Width | 16-bit |

## Queueing Model Architecture

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  FETCH  │──►│ DECODE  │──►│ EXECUTE │──►│ MEMORY  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘
    │              │              │              │
    ▼              ▼              ▼              ▼
  M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue

CPI = Fetch + Decode + Execute + Memory (serial sum)
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Military-grade design prioritizes reliability over speed
   - ALU and data transfer operations average 4 cycles
   - Memory operations are expensive at 6.5 cycles
   - Control flow (branch/call) costs 7.5 cycles
   - Stack operations are most expensive at 8 cycles
   - Radiation hardening adds overhead to all operations
   - Conservative timing margins for harsh environment operation

## Validation Approach

- Compare against original Thomson-CSF datasheet timing
- Validate against French military specification documents
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/thomson-csf/90435)
- [Wikipedia](https://en.wikipedia.org/wiki/Thomson-CSF)

---
Generated: 2026-01-29
