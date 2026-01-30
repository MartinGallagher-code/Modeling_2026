# Synertek SY6502A Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s (1978)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Licensed second-source of MOS Technology 6502
- Speed-binned for 2 MHz operation ("A" suffix)
- 8-bit NMOS microprocessor
- 16-bit address bus for 64KB memory space
- Efficient zero-page addressing mode for fast variable access
- Multiple addressing modes (immediate, zero-page, absolute, indirect)
- No pipeline, no cache
- 2-7 cycles per instruction
- Fully compatible with MOS 6502 instruction timing

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Synertek |
| Year | 1978 |
| Clock | 2.0 MHz |
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
   - Identical instruction timing to MOS 6502
   - Higher clock speed (2 MHz vs 1 MHz) yields higher IPS
   - ALU operations average 2.3 cycles (INX/DEX @2, ADC zp @3)
   - Data transfer averages 2.8 cycles (LDA imm @2, LDA abs @4)
   - Memory operations average 4.0 cycles (STA abs @4, indirect @5-6)
   - Control flow averages 2.6 cycles (branch @2.55, JMP @3)
   - Stack operations average 3.5 cycles (PHA @3, PLA @4, JSR @6)
   - Target CPI: ~3.0 (cross-validated from MOS 6502)

## Validation Approach

- Compare against original MOS 6502 datasheet timing
- Cross-validate CPI with MOS 6502 and Ricoh 2A03 models
- Verify higher IPS due to 2 MHz clock rating
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/synertek/sy6502)
- [Wikipedia](https://en.wikipedia.org/wiki/MOS_Technology_6502)

---
Generated: 2026-01-29
