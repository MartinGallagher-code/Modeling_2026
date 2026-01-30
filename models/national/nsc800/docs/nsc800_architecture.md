# National NSC800 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s 8-bit CMOS microprocessors
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Z80-compatible instruction set and pinout
- CMOS process technology for low power consumption
- 8-bit data path with 16-bit address bus
- Full Z80 register set (main and alternate register banks)
- Stack-based subroutine and interrupt handling
- Used in Epson HX-20 (one of the first laptop computers)
- Military and aerospace applications due to CMOS low-power characteristics
- 2.5 MHz clock speed

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | National Semiconductor |
| Year | 1979 |
| Clock | 2.5 MHz |
| Transistors | 9,000 |
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

### Instruction Category Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 4.0 | Z80-compatible ALU operations (4 cycles) |
| Data Transfer | 4.5 | Register and memory transfers (4-5 cycles) |
| Memory | 6.0 | Memory access operations (5-7 cycles) |
| Control | 7.0 | Jump, call, and return (5-10 cycles) |
| Stack | 10.0 | Push/pop operations (10-11 cycles) |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Z80-compatible means identical instruction set and timing characteristics
   - CMOS process provides low power but does not change instruction timing significantly
   - Stack operations are the most expensive at 10 cycles due to multiple memory accesses
   - Control flow instructions average 7 cycles, reflecting the mix of short jumps and longer calls
   - Data transfer dominates typical workloads (~31% weight) as expected for an 8-bit processor
   - 16-bit address space allows 64 KB of memory addressing
   - 9,000 transistors reflect the Z80-class complexity in CMOS

## Validation Approach

- Compare against original National Semiconductor NSC800 datasheet timing tables
- Cross-reference with Z80 timing tables for instruction compatibility
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/national_semiconductor/nsc800)
- [Wikipedia](https://en.wikipedia.org/wiki/NSC800)

---
Generated: 2026-01-29
