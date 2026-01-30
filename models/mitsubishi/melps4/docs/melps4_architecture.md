# Mitsubishi MELPS 4 (M58840) Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1978
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 4-bit microcontroller, Mitsubishi's first in the MELPS family
- PMOS technology (inherently slow switching speeds)
- 400 kHz clock
- Variable instruction timing across categories
- Designed for consumer electronics and home appliances
- On-chip ROM (2 KB addressable via 11-bit address)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Mitsubishi |
| Year | 1978 |
| Clock | 0.4 MHz (400 kHz) |
| Transistors | 6,000 |
| Data Width | 4-bit |
| Address Width | 11-bit |

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

## Instruction Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 4 | ADD, SUB, logical operations |
| Data Transfer | 5 | Register-memory transfers |
| Memory | 7 | Load/store operations |
| I/O | 8 | Input/output operations (slow PMOS) |
| Control | 6 | Branch, call, return |

**Target CPI:** 6.0 (typical workload, reflecting slow PMOS technology)

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - PMOS technology results in significantly higher cycle counts than later NMOS/CMOS designs
   - I/O operations are the slowest at 8 cycles, reflecting PMOS port access latency
   - All instruction categories require 4-8 cycles, much higher than contemporary NMOS designs
   - Equal 20% workload weighting across all categories reflects the general-purpose embedded controller usage pattern
   - 400 kHz clock combined with high CPI yields approximately 66,667 IPS

## Validation Approach

- Compare against original Mitsubishi datasheet timing specifications
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/mitsubishi/melps)
- [Wikipedia](https://en.wikipedia.org/wiki/Mitsubishi_MELPS)

---
Generated: 2026-01-29
