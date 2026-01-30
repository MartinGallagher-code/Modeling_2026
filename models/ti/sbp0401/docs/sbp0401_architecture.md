# TI SBP0401 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s Bipolar Bit-Slice
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 4-bit I2L (Integrated Injection Logic) bit-slice ALU
- Enhanced control logic variant of SBP0400
- Improved microcode sequencing capabilities
- Cascadable to 16-bit configurations (4 slices)
- Low-power bipolar I2L process technology
- Bus interface for external I/O

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Texas Instruments |
| Year | 1975 |
| Clock | 10.0 MHz |
| Transistors | 2,000 |
| Data Width | 4-bit |
| Address Width | 16-bit (cascaded) |

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

Target CPI: 3.0

### Instruction Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 2 | ADD, SUB, INCR, DECR |
| Shift | 3 | Shift and rotate operations |
| Logic | 2 | AND, OR, XOR, NOT |
| Control | 4 | Enhanced microcode control and sequencing |
| I/O | 5 | I/O and bus interface operations |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Enhanced control variant of the SBP0400 with improved microcode sequencing
   - Same I2L process and identical cycle counts to SBP0400
   - The "enhanced control" refers to additional microcode sequencing features, not faster execution
   - CPI of 3.0 matches the base SBP0400 -- same weighted instruction mix
   - Control-flow intensive workloads benefit from enhanced sequencing flexibility, though not from reduced cycle counts

## Validation Approach

- Compare against original Texas Instruments datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/ti/sbp0401)
- [Wikipedia](https://en.wikipedia.org/wiki/Integrated_injection_logic)

---
Generated: 2026-01-29
