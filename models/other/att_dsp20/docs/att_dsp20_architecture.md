# AT&T DSP-20 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1983)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Improved Bell Labs DSP, successor to DSP-1
- 16-bit data width with improved microcode efficiency
- Doubled clock speed over DSP-1 (10 MHz vs 5 MHz)
- Lower CPI than DSP-1 (3.0 vs 4.0) due to microcode improvements
- Internal AT&T telecommunications design

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | AT&T Bell Labs |
| Year | 1983 |
| Clock | 10.0 MHz |
| Transistors | N/A (internal design) |
| Data Width | 16-bit |
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
   - Improved over DSP-1 with lower cycle counts across all categories
   - MAC/ALU/data move reduced to 2 cycles (from DSP-1's 3 cycles)
   - Control flow at 4 cycles (improved from DSP-1's 5 cycles)
   - I/O at 5 cycles (improved from DSP-1's 6 cycles)
   - Target CPI of 3.0 reflects microcode efficiency gains

## Validation Approach

- Compare against Bell Labs internal documentation
- Validate improvement ratio vs DSP-1
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link - internal Bell Labs document)
- [Wikipedia](https://en.wikipedia.org/wiki/Digital_signal_processor#History)

---
Generated: 2026-01-29
