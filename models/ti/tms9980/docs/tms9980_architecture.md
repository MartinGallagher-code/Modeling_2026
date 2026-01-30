# TI TMS9980 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s 16-bit Microprocessor
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Cost-reduced variant of the TMS9900 with 8-bit external data bus
- 16-bit internal architecture with memory-to-memory operations
- Workspace pointer register architecture (no on-chip general-purpose registers)
- All "registers" are memory-mapped workspace locations
- Context switch via workspace pointer change (BLWP instruction)
- Used in TI-99/4 home computer
- 8-bit external bus doubles memory access cycles for 16-bit data

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Texas Instruments |
| Year | 1976 |
| Clock | 2.0 MHz |
| Transistors | 8,000 |
| Data Width | 16-bit (8-bit external bus) |
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

Target CPI: 12.0

### Instruction Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 8 | Workspace ALU operations (6-10 cycles) |
| Data Transfer | 10 | Memory-to-memory moves (8-14 cycles) |
| Memory | 14 | Workspace + external memory (12-18 cycles) |
| Control | 16 | Branch and BLWP (10-26 cycles) |
| Stack | 18 | Context switch operations (14-22 cycles) |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The memory-to-memory architecture means ALL register access requires memory cycles -- this is the primary reason for the high CPI of 12.0
   - The 8-bit external bus halves bandwidth compared to the TMS9900's 16-bit bus, adding extra cycles for every 16-bit operation
   - Workspace pointer architecture trades register access speed for extremely fast context switches (just change the workspace pointer)
   - BLWP (Branch and Load Workspace Pointer) is the most expensive operation class at 16-18 cycles but enables rapid interrupt handling
   - Data transfer operations at 10 cycles reflect the memory-to-memory nature: source read + destination write, both through the 8-bit bus
   - The high CPI is characteristic of TI's 9900-family architecture -- it prioritizes context switching speed over raw instruction throughput

## Validation Approach

- Compare against original Texas Instruments datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/ti/tms9980)
- [Wikipedia](https://en.wikipedia.org/wiki/Texas_Instruments_TMS9900)

---
Generated: 2026-01-29
