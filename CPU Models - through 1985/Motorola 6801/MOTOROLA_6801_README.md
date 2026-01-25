# Motorola 6801 CPU Queueing Model

## Executive Summary

The Motorola 6801 (1978) was the **first single-chip microcontroller with on-chip RAM**. Before the 6801, MCUs had ROM only - you needed external RAM chips. The 6801's 128 bytes of integrated RAM enabled true single-chip computers for the first time.

**Key Innovation:** On-chip RAM transformed microcontrollers from "CPU + external memory" into "complete computer on a chip."

---

## Technical Specifications

| Specification | Value |
|---------------|-------|
| Year | 1978 |
| Word Size | 8 bits |
| Clock | 1-2 MHz |
| **On-chip RAM** | **128 bytes (FIRST!)** |
| On-chip ROM | 2 KB |
| I/O Lines | 29 |
| Timer | 16-bit programmable |
| Serial | Full-duplex UART (SCI) |
| Transistors | ~35,000 |

---

## Revolutionary On-Chip RAM

### Before 6801
```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  6800   │────►│External │────►│External │
│  CPU    │     │  ROM    │     │  RAM    │
└─────────┘     └─────────┘     └─────────┘
                     │               │
              3+ chips minimum for any system
```

### With 6801
```
┌─────────────────────────────────────────┐
│              Motorola 6801              │
│  ┌───────┐  ┌───────┐  ┌───────────┐   │
│  │ CPU   │  │ 2KB   │  │ 128 bytes │   │
│  │ Core  │  │ ROM   │  │ RAM       │   │
│  └───────┘  └───────┘  └───────────┘   │
│  ┌───────┐  ┌───────┐  ┌───────────┐   │
│  │ UART  │  │ Timer │  │ 29 I/O    │   │
│  │ (SCI) │  │ 16-bit│  │ lines     │   │
│  └───────┘  └───────┘  └───────────┘   │
└─────────────────────────────────────────┘
         ONE CHIP = Complete Computer
```

---

## 6800 Instruction Superset

The 6801 added powerful new instructions:

| Instruction | Operation | Cycles | Benefit |
|-------------|-----------|--------|---------|
| **MUL** | A × B → D | 10 | Hardware multiply! |
| **ADDD** | D + M:M+1 → D | 4 | 16-bit add |
| **LDD/STD** | Load/Store D | 4/5 | 16-bit transfers |
| **ABX** | B + X → X | 3 | Fast indexing |
| **PSHX/PULX** | Push/Pull X | 4/5 | Index on stack |

### Hardware Multiply

```
Before (6800): 8x8 multiply = 100+ cycles (software loop)
After (6801):  8x8 multiply = 10 cycles (MUL instruction)

10× faster multiplication!
```

---

## Variants

| Variant | ROM | Description |
|---------|-----|-------------|
| **6801** | 2KB mask ROM | Standard production |
| **68701** | 2KB EPROM | Development/low volume |
| **6803** | None | ROM-less for external memory |

---

## Applications

The 6801 enabled low-cost embedded systems:

- **Automotive**: Engine control units (ECUs)
- **Industrial**: PLCs, motor controllers
- **Communications**: Modems, protocol converters
- **Consumer**: Printers, appliances

---

## Evolution to 68HC11

```
6801 (1978)
  │
  ├── Added: On-chip RAM, hardware multiply, UART
  │
  ▼
68HC11 (1985)
  │
  ├── Added: A/D converter, EEPROM, SPI, more RAM
  │
  ▼
One of the most successful MCU families ever
```

The 6801's architecture directly led to the legendary 68HC11, which became one of the most widely used MCU families in history.

---

## Performance

| Metric | Value |
|--------|-------|
| IPC | ~0.08 |
| MIPS @ 1 MHz | ~0.08 |
| vs 6800 | Same core, but integrated |

Performance wasn't the point - **integration** was:

| Feature | 6800 System | 6801 |
|---------|-------------|------|
| Chips needed | 3-5+ | **1** |
| Board space | Large | **Minimal** |
| Cost | High | **Low** |
| Power | High | **Low** |

---

## Historical Significance

1. **First MCU with on-chip RAM** - enabled true single-chip computers
2. **Hardware multiply** - 10× faster than software
3. **Integrated UART** - eliminated external ACIA chip
4. **Foundation for 68HC11** - one of most successful MCU families
5. **Automotive standard** - established Motorola in automotive

---

## Usage

```python
from motorola_6801_model import Motorola6801QueueModel

model = Motorola6801QueueModel('motorola_6801_model.json')
ipc, _ = model.predict_ipc(0.07)
print(f"IPC: {ipc:.4f}")

# Compare to 6800
comp = model.compare_6800()
print(f"6801 RAM: {comp['6801']['on_chip_ram']}")
```

---

## Files

| File | Description |
|------|-------------|
| `motorola_6801_model.py` | Python implementation |
| `motorola_6801_model.json` | Configuration |
| `MOTOROLA_6801_README.md` | This document |
| `QUICK_START_6801.md` | Quick reference |
| `PROJECT_SUMMARY.md` | Executive summary |

---

**Version:** 1.0  
**Date:** January 24, 2026

*"The 6801 made single-chip computers possible."*
