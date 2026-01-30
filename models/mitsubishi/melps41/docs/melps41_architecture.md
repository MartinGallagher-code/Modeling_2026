# Mitsubishi MELPS 41 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1980
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 4-bit microcontroller, enhanced successor to MELPS 4
- Upgraded from PMOS to NMOS technology for improved speed
- 500 kHz clock (25% faster than MELPS 4's 400 kHz)
- Improved instruction timing over PMOS predecessor
- Larger address space (4 KB ROM via 12-bit address)
- Designed for consumer electronics and embedded control

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Mitsubishi |
| Year | 1980 |
| Clock | 0.5 MHz (500 kHz) |
| Transistors | 8,000 |
| Data Width | 4-bit |
| Address Width | 12-bit |

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
| Memory | 6 | Load/store operations |
| I/O | 7 | Input/output operations |
| Control | 5.5 | Branch, call, return |

**Target CPI:** 5.5 (typical workload, improved over MELPS 4's 6.0)

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - NMOS technology reduces cycle counts by approximately 1 cycle per category compared to PMOS MELPS 4
   - Memory operations improved from 7 to 6 cycles; I/O from 8 to 7 cycles
   - Control flow uses fractional 5.5 cycles (weighted average of branch/call/return variants)
   - 500 kHz clock with CPI 5.5 yields approximately 90,909 IPS (36% improvement over MELPS 4)
   - Transistor count increased from 6,000 to 8,000 reflecting expanded ROM and improved logic

## Validation Approach

- Compare against original Mitsubishi datasheet timing specifications
- Cross-validate improvement ratio against MELPS 4 model
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/mitsubishi/melps)
- [Wikipedia](https://en.wikipedia.org/wiki/Mitsubishi_MELPS)

---
Generated: 2026-01-29
