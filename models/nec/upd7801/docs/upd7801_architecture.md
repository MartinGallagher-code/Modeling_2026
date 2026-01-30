# NEC uPD7801 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1980-1988
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- NEC proprietary 8-bit microcontroller ISA (not Z80 or x86 compatible)
- Approximately 100 instructions
- Large Japanese market share for embedded applications
- Used primarily in printers and consumer electronics
- On-chip peripherals for embedded use
- 16-bit address space (64KB)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1980 |
| Clock | 4.0 MHz |
| Transistors | 15,000 |
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
   - NEC proprietary ISA, distinct from Z80-compatible uPD780 line
   - Instruction categories: ALU (4.5c), data_transfer (4c), memory (7c), control (8c), stack (9c)
   - Stack operations are most expensive at 9 cycles
   - Control flow (branch/call) operations take 7-12 cycles, averaged to 8
   - Memory operations at 7 cycles reflect 6-8 cycle range
   - Typical workload CPI depends on instruction mix with weights emphasizing ALU and data_transfer
   - Predecessor to the enhanced uPD7810

## Validation Approach

- Compare against original NEC datasheet timing specifications
- Cross-validate against contemporary 8-bit MCUs (Intel 8048, Z80)
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/nec/upd7801)
- [Wikipedia](https://en.wikipedia.org/wiki/NEC_%C2%B5PD7800_family)

---
Generated: 2026-01-29
