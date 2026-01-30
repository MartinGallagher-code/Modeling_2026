# Harris HM6100 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s (1978)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Faster CMOS implementation of PDP-8/E instruction set
- Second-source to Intersil IM6100
- 12-bit word size (PDP-8 architecture)
- Improved process technology for faster operation than IM6100
- Full PDP-8/E instruction set compatibility
- Multi-state sequential execution (variable states per instruction)
- 4K word address space (expandable to 32K)
- Fully static CMOS design

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Harris |
| Year | 1978 |
| Clock | 4.0 MHz |
| Transistors | 4,500 |
| Data Width | 12-bit |
| Address Width | 12-bit |

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
   - Target CPI of 8.0 states (faster than Intersil 6100's 10.5)
   - Arithmetic (TAD) and logic (AND) operations at 8 states
   - Memory operations (DCA, ISZ) at 9 states average
   - Jump operations (JMP, JMS) at 9 states
   - I/O (IOT) at 8 states
   - Operate (OPR) group is fastest at 5 states
   - Each state = 400ns at 4 MHz (vs IM6100's 500ns)
   - Expected ~313 KIPS throughput

## Validation Approach

- Compare against original Harris HM6100 datasheet
- Validate faster operation vs Intersil 6100 (CPI < 10.5)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/Intersil_6100)

---
Generated: 2026-01-29
