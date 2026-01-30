# Hitachi FD1094 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid-1980s encrypted arcade processors
**Queueing Model:** Serial M/M/1 chain with decryption overhead stage

## Architectural Features

- Improved version of FD1089 with faster decryption hardware
- Motorola 68000 core with enhanced on-die encryption scheme
- 8 KB battery-backed key RAM (larger than FD1089)
- More complex key schedule but faster decrypt throughput
- Used by Sega for arcade copy protection (System 16B, System 18)
- Full 68000 instruction set executed internally after decryption

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Hitachi (for Sega) |
| Year | 1987 |
| Clock | 10.0 MHz |
| Transistors | ~75,000 |
| Data Width | 16-bit |
| Address Width | 24-bit |

## Queueing Model Architecture

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  FETCH  │──►│ DECRYPT │──►│ DECODE  │──►│ EXECUTE │──►│ MEMORY  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
    │              │              │              │              │
    ▼              ▼              ▼              ▼              ▼
  M/M/1          M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue          Queue

CPI = Fetch + Decrypt + Decode + Execute + Memory (serial sum)
```

## Instruction Categories

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 5.0 | ADD/SUB @4 + 1 decrypt, MUL @70+, DIV @140+ |
| Data Transfer | 5.0 | MOVE reg-reg @4+1, MOVE imm @8+1 |
| Memory | 8.0 | MOVE.W (An) @8 + decrypt, indexed @10-14 |
| Control | 7.0 | Branches @10+1, JSR @16+1, RTS @16+1 |
| Address | 6.0 | LEA @4-12 + decrypt, PEA @12 + decrypt |
| Decrypt | 8.0 | Decryption overhead @8 cycles avg (faster than FD1089's 10) |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The FD1094 improves on the FD1089 with a faster decryption unit (8 vs 10 cycles average)
   - 8 KB key RAM enables a more complex but more efficient key schedule
   - Target CPI is ~6.8 (compared to FD1089's ~7.0 and standard 68000's ~6.5)
   - The decrypt stage is the primary differentiator from the standard 68000
   - Battery-backed key RAM failure renders the chip inoperable

## Validation Approach

- Compare against original Motorola 68000 datasheet timings plus measured decrypt penalty
- Validate that CPI is lower than FD1089 (< 7.0) but higher than standard 68000 (> 6.5)
- Validate with Sega System 16B/18 emulator timing measurements (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/hitachi/fd1094)
- [Wikipedia - Sega System 16](https://en.wikipedia.org/wiki/Sega_System_16)

---
Generated: 2026-01-29
