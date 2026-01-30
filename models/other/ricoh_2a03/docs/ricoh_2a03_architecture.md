# Ricoh 2A03 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1983)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- MOS 6502 CPU core with BCD (decimal mode) disabled
- 8-bit data bus, 16-bit address bus
- On-chip Audio Processing Unit (APU) with 5 audio channels
- Sequential instruction execution (no pipeline)
- Multiple addressing modes including zero-page for fast access
- 2-7 cycles per instruction
- NTSC clock at 1.79 MHz (PAL variant 2A07 at 1.66 MHz)
- Used in Nintendo Entertainment System (NES) and Famicom

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Ricoh |
| Year | 1983 |
| Clock | 1.79 MHz (NTSC) |
| Transistors | 3,510 |
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
   - Identical instruction timing to MOS 6502 (cross-validated)
   - BCD mode disabled but ADC/SBC timing unchanged
   - Zero-page addressing provides fast variable access (3 cycles)
   - Indirect addressing modes are expensive (5-6 cycles)
   - Branch penalty: +1 cycle if taken, +1 more if page crossing
   - JSR/RTS pair costs 12 cycles total
   - Target CPI: ~3.0 for typical NES workloads

## Validation Approach

- Compare against original MOS 6502 datasheet timing
- Cross-validate with FCEUX and Nestopia cycle-accurate emulators
- Validate against actual NES software instruction mixes
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/ricoh/2a03)
- [Wikipedia](https://en.wikipedia.org/wiki/Ricoh_2A03)

---
Generated: 2026-01-29
