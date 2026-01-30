# Hitachi HD64180 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid-1980s enhanced 8-bit microprocessors
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Z180-compatible (enhanced Zilog Z80) architecture
- 8-bit data bus, 20-bit address bus (1 MB with on-chip MMU)
- Faster instruction execution than Z80 (most instructions 1-2 fewer cycles)
- On-chip Memory Management Unit (MMU)
- On-chip DMA controller (2 channels)
- On-chip UART (ASCI, 2 channels)
- On-chip programmable timers
- CMOS process for lower power consumption
- 3-20 cycles per instruction

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Hitachi |
| Year | 1985 |
| Clock | 6.0 MHz (up to 10 MHz in later variants) |
| Transistors | ~20,000 |
| Data Width | 8-bit |
| Address Width | 20-bit |

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

## Instruction Categories

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 3.2 | ALU operations, optimized vs Z80 |
| Data Transfer | 3.2 | LD operations, faster than Z80 |
| Memory | 4.8 | Memory operations, slightly optimized |
| Control | 4.5 | Control flow, faster branches |
| Stack | 8.5 | PUSH/POP operations, optimized |
| Block | 10.0 | Block operations (LDIR, etc.), faster than Z80 |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The HD64180 is modeled as an enhanced Z80 with optimized instruction timing
   - Most instructions take 1-2 fewer cycles than the original Z80
   - Target CPI is ~4.5 (compared to Z80's ~5.5)
   - On-chip MMU extends address space to 1 MB without external logic
   - On-chip DMA and UART reduce system-level component count
   - Despite Z180 compatibility, this is still a sequential execution machine with no pipelining

## Validation Approach

- Compare against original Hitachi HD64180 / Zilog Z180 datasheet timings
- Validate that CPI is lower than Z80 baseline (~5.5)
- Cross-reference with Z180-based system benchmarks
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/hitachi/hd64180)
- [Wikipedia - Zilog Z180](https://en.wikipedia.org/wiki/Zilog_Z180)

---
Generated: 2026-01-29
