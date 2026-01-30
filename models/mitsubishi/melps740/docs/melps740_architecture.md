# Mitsubishi MELPS 740 (M50740) Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1984
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 8-bit MCU with enhanced 6502-compatible instruction set
- CMOS technology design
- 6502-compatible core with extensions: MUL, DIV, bit manipulation
- On-chip peripherals: timers, serial I/O, A/D converter
- Single instruction at a time, no pipelining
- 2 MHz clock speed
- Popular for embedded control in consumer electronics and appliances

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Mitsubishi Electric |
| Year | 1984 |
| Clock | 2.0 MHz |
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

## Instruction Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 2 | Arithmetic (ADC, SBC, INC, DEC) |
| Data Transfer | 3 | LDA/STA/LDX/STX register transfers |
| Memory | 4 | Indexed and indirect addressing modes |
| Control | 3 | Branch and jump operations |
| I/O | 5 | Timer, serial, and A/D I/O access |
| Bit Ops | 2 | Bit manipulation (SET, CLR, TST) |

**Target CPI:** 3.2 (typical workload)

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - This is the architecture-level model for the MELPS 740 family (M50740 is a specific implementation)
   - Enhanced 6502 core adds MUL, DIV, and bit manipulation beyond the standard 6502 ISA
   - On-chip A/D converter and serial I/O contribute to the 5-cycle I/O category
   - Workload profile uses non-uniform weighting (18% ALU, 22% data transfer, 24% memory, 15% control, 11% I/O, 10% bit ops) calibrated for CPI 3.18, within 5% of target 3.2
   - 15,000 transistors reflects the additional peripheral logic over the base M50740 (12,000)
   - 2 MHz clock with CPI ~3.2 yields approximately 625,000 IPS

## Relationship to M50740/M50747

The MELPS 740 is the architecture family; M50740 and M50747 are specific chip implementations:
- **M50740**: Base implementation with standard I/O configuration (12,000 transistors)
- **M50747**: Expanded I/O variant (13,000 transistors)
- **MELPS 740**: Architecture-level model with full peripheral set (15,000 transistors)

## Validation Approach

- Compare against original Mitsubishi datasheet timing specifications
- Cross-validate with M50740 and M50747 models (same core architecture)
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/mitsubishi/melps_740)
- [Wikipedia](https://en.wikipedia.org/wiki/MOS_Technology_6502)

---
Generated: 2026-01-29
