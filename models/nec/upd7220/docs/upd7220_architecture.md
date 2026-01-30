# NEC uPD7220 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1981-1990
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- First single-chip LSI graphics display controller (NOT a general-purpose CPU)
- Hardware line drawing, arc drawing, area fill, and character display
- DMA transfer to display memory
- Video timing signal generation
- Command FIFO for host CPU interface
- 1MB display memory addressing capability
- Used in NEC PC-9801 and IBM Professional Graphics Controller

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1981 |
| Clock | 5.0 MHz |
| Transistors | 60,000 |
| Data Width | 16-bit |
| Address Width | 20-bit |

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
   - This is a graphics command processor, not a general CPU; "CPI" represents cycles per command step
   - Command categories: draw_line (16c), draw_arc (24c), area_fill (14c), char_display (8c), dma_transfer (4c), control (3c)
   - Stage timing: command_fetch (2c), decode (1c), execute (6c avg), memory (3c)
   - Target CPI of 12.0 represents average command execution time
   - Arc drawing is most expensive at 24 cycles per step due to trigonometric computation
   - DMA transfers are most efficient at 4 cycles per word
   - Workload mix varies significantly between vector graphics, text, and fill operations

## Validation Approach

- Compare against original NEC datasheet command timing specifications
- Cross-validate with NEC PC-9801 graphics performance benchmarks
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/nec/upd7220)
- [Wikipedia](https://en.wikipedia.org/wiki/NEC_%C2%B5PD7220)

---
Generated: 2026-01-29
