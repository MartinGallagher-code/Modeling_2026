# National IMP-16 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1970s minicomputer-class microprocessors
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- One of the first 16-bit microprocessors (1973)
- Built using bit-slice technology for design flexibility
- 16-bit data path with register-to-register architecture
- Support for immediate, memory, and I/O addressing modes
- Subroutine call/return via dedicated instructions
- Shift operations (multi-cycle, not barrel shifter)
- Bit-slice construction allows customized instruction decoding
- Predecessor to the PACE processor

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | National Semiconductor |
| Year | 1973 |
| Clock | 0.5 MHz |
| Transistors | N/A (bit-slice) |
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

### Instruction Category Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| Register Ops | 6.0 | Register-to-register operations |
| Immediate | 8.0 | Immediate operand instructions |
| Memory Read | 10.0 | Load from memory |
| Memory Write | 8.0 | Store to memory |
| Branch | 9.0 | Branch and conditional instructions |
| Call/Return | 9.0 | Subroutine call and return |
| Shift | 12.0 | Shift operations (multi-cycle) |
| I/O | 10.0 | Input/output operations |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Bit-slice architecture means cycle counts depend on microcode implementation
   - Target CPI of 8.0 reflects the slow clock and multi-cycle execution
   - 0.5 MHz clock is very slow even by 1973 standards, reflecting early bit-slice technology
   - Shift operations are the most expensive at 12 cycles (no barrel shifter)
   - Memory operations dominate due to lack of on-chip cache or buffers
   - Register operations are fastest at 6 cycles but still multi-cycle

## Validation Approach

- Compare against original National Semiconductor IMP-16 datasheet timing tables
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/national_semiconductor/imp-16)
- [Wikipedia](https://en.wikipedia.org/wiki/IMP-16)

---
Generated: 2026-01-29
