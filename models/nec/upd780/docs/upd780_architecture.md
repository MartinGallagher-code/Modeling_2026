# NEC uPD780 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1976-1985
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Z80-compatible clone manufactured by NEC
- 8-bit data bus, 16-bit address bus
- Full Zilog Z80 instruction set compatibility
- Two register sets (main + alternate) for fast context switching
- IX and IY index registers for efficient addressing
- Block transfer/search instructions (LDIR, CPIR, etc.)
- 4-23 cycles per instruction (variable timing)
- Sequential execution with no pipeline
- Used in NEC PC-8001, PC-8801, and various Japanese computers

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1976 |
| Clock | 2.5 MHz |
| Transistors | 8,500 |
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
   - Instruction timing identical to Zilog Z80 (NEC's clone maintains full timing compatibility)
   - Instruction categories: ALU (4c), data_transfer (4c), memory (5.8c), control (5.5c), stack (10c), block (12c)
   - Target CPI of 5.5 matches Z80 typical workload performance
   - Block operations (LDIR/LDDR) are most expensive at ~12 cycles average (21/16 for BC!=0/BC=0)
   - Stack operations (PUSH/POP) are expensive at ~10 cycles
   - Register-to-register operations are fastest at 4 cycles
   - Wide variation in instruction timing (4-23 cycles) makes workload mix critical

## Validation Approach

- Compare against original NEC datasheet timing specifications (identical to Z80)
- Cross-validate against Zilog Z80 model (should produce identical CPI)
- Validate with NEC PC-8001/PC-8801 benchmark data
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/nec/upd780)
- [Wikipedia](https://en.wikipedia.org/wiki/NEC_%C2%B5PD780)

---
Generated: 2026-01-29
