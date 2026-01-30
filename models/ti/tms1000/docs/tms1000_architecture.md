# TI TMS1000 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s Fixed-Cycle Microcontroller
**Queueing Model:** Serial M/M/1 chain (fixed-latency)

## Architectural Features

- First commercially available single-chip microcontroller
- 4-bit data path with BCD arithmetic support
- Harvard architecture (separate program and data memory)
- All instructions execute in exactly 6 clock cycles (fixed timing)
- No interrupts, single-level subroutine stack
- LFSR-based (Linear Feedback Shift Register) program counter
- 43 instructions in the base TMS1000 instruction set
- On-chip ROM (1KB) and RAM (64 nibbles)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Texas Instruments |
| Year | 1974 |
| Clock | 0.3 MHz (300 kHz internal) |
| Transistors | 8,000 |
| Data Width | 4-bit |
| Address Width | 10-bit (1KB ROM) |

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

Note: The TMS1000 has fixed 6-cycle timing for ALL instructions. The serial chain always sums to exactly 6 cycles regardless of instruction type. This simplifies the queueing model to a constant-service-time system.

Target CPI: 6.0 (fixed, workload-independent)

### Instruction Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 6 | ADD, SUB, comparisons |
| Data Transfer | 6 | TAM, TMA, TMY |
| Memory | 6 | LDP, LDX |
| Control | 6 | BR, CALL |
| I/O | 6 | TDO, SETR, RSTR |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template (fixed-cycle variant)
2. Key modeling considerations:
   - CPI is always exactly 6.0 -- the simplest possible timing model
   - Workload mix does not affect CPI because all instruction categories have identical cycle counts
   - At 300 kHz with CPI=6, throughput is exactly 50,000 instructions per second
   - The LFSR program counter means non-sequential addresses -- but this does not affect timing
   - Harvard architecture separates instruction fetch from data access, but both complete within the 6-cycle window
   - The fixed timing was a deliberate design choice for deterministic real-time behavior in embedded applications

## Validation Approach

- Compare against original Texas Instruments datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/ti/tms1000)
- [Wikipedia](https://en.wikipedia.org/wiki/Texas_Instruments_TMS1000)

---
Generated: 2026-01-29
