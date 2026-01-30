# National PACE Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid-1970s early 16-bit microprocessors
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Early 16-bit microprocessor using p-channel MOS technology
- 16-bit data path with register-based architecture
- Successor to the IMP-16 bit-slice processor
- Single-chip implementation (unlike IMP-16 bit-slice approach)
- Stack operations for subroutine management
- Support for immediate, register, memory, and I/O addressing modes
- p-channel MOS technology (slower than later n-channel designs)
- One of the earliest single-chip 16-bit processors

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | National Semiconductor |
| Year | 1975 |
| Clock | 2.0 MHz |
| Transistors | N/A |
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
| Register Ops | 8.0 | Register-to-register operations |
| Immediate | 10.0 | Immediate operand instructions |
| Memory Read | 12.0 | Load from memory |
| Memory Write | 11.0 | Store to memory |
| Branch | 10.0 | Branch and conditional instructions |
| Call/Return | 11.0 | Subroutine call and return |
| Stack | 14.0 | Stack operations (push/pop) |
| I/O | 12.0 | Input/output operations |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Target CPI of 10.0 reflects slow p-channel MOS technology
   - Cycle counts are higher than IMP-16 successor designs due to p-channel MOS gate delays
   - Stack operations are most expensive at 14 cycles (multiple memory accesses required)
   - Register operations at 8 cycles are fastest but still slow by later standards
   - Memory read (12 cycles) is slower than memory write (11 cycles) due to bus turnaround
   - 2.0 MHz clock is faster than IMP-16 (0.5 MHz) due to single-chip integration
   - p-channel MOS was chosen for availability, not speed -- n-channel would come later

## Validation Approach

- Compare against original National Semiconductor PACE datasheet timing tables
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/national_semiconductor/pace)
- [Wikipedia](https://en.wikipedia.org/wiki/National_Semiconductor_PACE)

---
Generated: 2026-01-29
