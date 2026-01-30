# U880 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s-1980s (pre-pipeline microprocessors)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- East German clone of the Zilog Z80 by VEB Mikroelektronik Erfurt
- Full Z80 instruction set and timing compatibility (pin-compatible)
- 8-bit data bus, 16-bit address bus (64KB addressable)
- Block transfer and search instructions (LDIR, CPIR, LDDR, etc.)
- Two complete register sets (main + alternate) for fast context switching
- IX and IY index registers for indexed addressing
- 4-23 cycles per instruction
- Most widely used microprocessor in the Eastern Bloc
- Basis for Soviet KR1858VM1 clone masks

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | VEB Mikroelektronik Erfurt (East Germany) |
| Year | 1980 |
| Clock | 2.5 MHz |
| Transistors | ~8,500 |
| Data Width | 8-bit |
| Address Width | 16-bit |
| Process | NMOS |
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
   - Instruction timing identical to Zilog Z80 (pin-compatible, timing-compatible clone)
   - Block instructions (LDIR) take 21 cycles per iteration when BC!=0, 16 when BC=0
   - JR (relative jump) takes 12 cycles if taken, 7 if not taken
   - CALL takes 17 cycles -- subroutine overhead is significant
   - PUSH takes 11 cycles, POP takes 10 cycles
   - ADD HL,rr takes 11 cycles (16-bit add is slow on 8-bit ALU)
   - The U880 masks were later used by the Soviet Union to produce the KR1858VM1
   - Target CPI of ~5.5 for typical workloads matches Zilog Z80

## Validation Approach

- Compare against original Zilog Z80 datasheet timing
- Validate with cycle-accurate Z80 emulator (if available)
- Cross-reference with VEB Mikroelektronik Erfurt documentation
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/zilog/z80)
- [Wikipedia - Zilog Z80](https://en.wikipedia.org/wiki/Zilog_Z80)

---
Generated: 2026-01-29
