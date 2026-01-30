# KR1858VM1 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s-1980s (pre-pipeline microprocessors)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Soviet Z80 clone, derived from East German U880 masks
- Also known as T34VM1
- 8-bit data bus, 16-bit address bus (64KB addressable)
- Full Zilog Z80 instruction set compatibility
- Block transfer and search instructions (LDIR, CPIR, LDDR, etc.)
- Two complete register sets (main + alternate) for fast context switching
- IX and IY index registers for indexed addressing
- 4-23 cycles per instruction
- Late Soviet-era design (1991), one of the last Soviet processor clones

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union |
| Year | 1991 |
| Clock | 4.0 MHz |
| Transistors | ~8,500 |
| Data Width | 8-bit |
| Address Width | 16-bit |
| Process | CMOS |
| Western Equivalent | Zilog Z80 |

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
   - Instruction timing identical to Zilog Z80 and East German U880
   - Masks derived from East German U880 production
   - Block instructions (LDIR) take 21 cycles per iteration (BC!=0) or 16 (BC=0)
   - JR (relative jump) takes 12 cycles if taken, 7 if not taken
   - CALL takes 17 cycles, significantly more than JP at 10 cycles
   - Target CPI of ~5.5 for typical workloads matches Z80/U880

## Validation Approach

- Compare against original Zilog Z80 datasheet timing
- Validate with cycle-accurate Z80 emulator (if available)
- Cross-reference with U880 documentation (same masks)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/zilog/z80)
- [Wikipedia - Zilog Z80](https://en.wikipedia.org/wiki/Zilog_Z80)

---
Generated: 2026-01-29
