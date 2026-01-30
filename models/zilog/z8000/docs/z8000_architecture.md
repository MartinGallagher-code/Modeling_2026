# Zilog Z8000 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s (1979)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 16-bit microprocessor (not Z80 compatible -- entirely different architecture)
- 16 general-purpose 16-bit registers
- Regular, orthogonal instruction set encoding
- Two variants: Z8001 (segmented, 23-bit address) and Z8002 (non-segmented, 16-bit address)
- 4 MHz clock
- ~17,500 transistors
- 3 to 100+ cycles per instruction (complex operations)
- Used in Olivetti M20 and some Unix workstations

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Zilog |
| Year | 1979 |
| Clock | 4.0 MHz |
| Transistors | 17,500 |
| Data Width | 16-bit |
| Address Width | 16-bit (Z8002) / 23-bit segmented (Z8001) |
| Registers | 16 x 16-bit general purpose |
| Target CPI | 4.5 |

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

## Instruction Categories

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 3.2 | ADD/SUB/INC/DEC (weighted average) |
| Data Transfer | 2.8 | LD R,R -- fast 16-bit register moves |
| Memory | 5.0 | Memory ops with various addressing modes |
| Control | 4.8 | JP/JR (weighted average) |
| Stack | 8.0 | PUSH/POP 16-bit registers |
| Block | 9.0 | Block transfer operations |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The Z8000 is architecturally distinct from the Z80 -- it is a clean 16-bit design, not an evolution of Z80
   - 16 general-purpose registers enable fast register-to-register operations (2.8 cycles for data transfer)
   - Orthogonal instruction encoding provides regular, predictable timing
   - Block transfer operations at 9 cycles reflect multi-word memory move capability
   - Stack operations are the slowest regular category at 8 cycles due to 16-bit push/pop through the bus
   - The Z8001 segmented variant adds address translation overhead not modeled here (Z8002 non-segmented is the base model)
   - Limited commercial success despite clean architecture, overshadowed by Intel 8086 and Motorola 68000

## Validation Approach

- Compare against original Zilog Z8000 datasheet timing specifications
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error
- Expected typical workload CPI: 4.5

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/zilog/z8000)
- [Wikipedia](https://en.wikipedia.org/wiki/Zilog_Z8000)

---
Generated: 2026-01-29
