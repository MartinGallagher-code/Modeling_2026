# GTE G65SC802 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1980s (1985)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- WDC 65C816 second-source in 6502-compatible 40-pin DIP pinout
- 8/16-bit switchable CPU with emulation mode (6502 compatible)
- 24-bit internal addressing (16 MB), 16-bit external bus
- CMOS technology for low power consumption
- Pin-compatible with 6502 for drop-in upgrades
- Bank register accessible via data bus multiplexing

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | GTE Microcircuits |
| Year | 1985 |
| Clock | 4.0 MHz |
| Transistors | 22,000 |
| Data Width | 16-bit (internal) / 8-bit (external bus) |
| Address Width | 24-bit |

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
   - Target CPI of 3.5 for 65816 emulation mode workloads
   - ALU operations (ADC, SBC, AND, ORA) fastest at 2 cycles
   - Data transfer (LDA, STA, TAX) at 3 cycles
   - Memory operations (indirect, indexed) at 4 cycles
   - Control flow (BNE, JMP, JSR) at 3 cycles
   - Stack operations (PHA, PLA, PEA) at 4 cycles
   - Long addressing modes (24-bit) are slowest at 5 cycles

## Validation Approach

- Compare against WDC 65C816 datasheet timing (same core)
- Validate with 6502/65816 benchmark suites
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/WDC_65C816)

---
Generated: 2026-01-29
