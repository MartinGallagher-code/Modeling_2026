# Hitachi FD1089 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid-1980s encrypted arcade processors
**Queueing Model:** Serial M/M/1 chain with decryption overhead stage

## Architectural Features

- Motorola 68000 core with on-die instruction decryption logic
- Used by Sega for arcade copy protection (System 16, etc.)
- Battery-backed RAM stores encryption key tables
- Decryption layer adds ~0.5 CPI overhead vs standard 68000
- Full 68000 instruction set executed internally after decryption
- 16-bit external data bus, 24-bit address bus (16 MB address space)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Hitachi (for Sega) |
| Year | 1986 |
| Clock | 10.0 MHz |
| Transistors | ~70,000 |
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
| Control | 7.0 | Branches @10+1, JSR @16+2, RTS @16+1 |
| Address | 6.0 | LEA @4-12 + decrypt, PEA @12 + decrypt |
| Decrypt | 10.0 | Dedicated decryption overhead for opcode fetch |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The FD1089 is modeled as a standard 68000 with an additional decryption penalty stage
   - Decryption overhead adds approximately 2 cycles per instruction word fetched
   - The decrypt category captures the average opcode decryption cost
   - Target CPI is ~7.0 (compared to ~6.5 for a standard 68000)
   - Battery-backed key RAM failure renders the chip inoperable

## Validation Approach

- Compare against original Motorola 68000 datasheet timings plus measured decrypt penalty
- Validate that CPI exceeds standard 68000 baseline of ~6.5
- Validate with Sega System 16 emulator timing measurements (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/hitachi/fd1089)
- [Wikipedia - Sega System 16](https://en.wikipedia.org/wiki/Sega_System_16)

---
Generated: 2026-01-29
