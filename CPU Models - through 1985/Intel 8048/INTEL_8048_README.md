# Intel 8048 CPU Queueing Model

## Executive Summary

The Intel 8048 (1976) was the **first widely successful single-chip microcontroller**. By integrating CPU, ROM, RAM, and I/O on a single chip, it enabled embedded computing in countless products. Most famously, every IBM PC (and compatible) contained an 8048 - in the keyboard controller.

**Key Finding:** The 8048 established the microcontroller paradigm: a complete computer on a single chip optimized for control tasks rather than computation. This approach proved so successful that billions of microcontrollers are now produced annually.

---

## Technical Specifications

| Specification | Value |
|---------------|-------|
| Year | 1976 |
| Word Size | 8 bits |
| Data Bus | 8 bits |
| Address Bus | 12 bits |
| Clock | 6 MHz (÷15 internally) |
| Effective Speed | 400 kHz |
| Transistors | ~6,000 |
| On-chip ROM | **1 KB** |
| On-chip RAM | **64 bytes** |
| I/O Lines | **27** |

---

## On-Chip Integration

### What Made 8048 Special
```
Previous approach (8080 system):
- 8080 CPU chip
- ROM chip(s)
- RAM chip(s)  
- I/O chip (8255)
- Clock generator
- Bus buffers
= 5-10+ chips minimum

8048 approach:
- ONE CHIP
= Complete microcomputer!

Cost reduction: 5-10× cheaper for simple applications
```

### On-Chip Resources
| Resource | Size | Notes |
|----------|------|-------|
| Program ROM | 1024 bytes | Mask-programmed |
| Data RAM | 64 bytes | Working memory |
| I/O Ports | 27 lines | 3 ports |
| Timer | 8-bit | Event counter |
| Interrupts | 2 | External + Timer |

---

## Architecture

### Register Set
```
Accumulator (A): 8-bit main register

Register Banks (switchable):
  Bank 0: R0-R7 (8 registers)
  Bank 1: R0-R7 (8 registers)

PSW: Program Status Word
PC:  12-bit Program Counter

Two banks enable fast interrupt handling
(switch banks instead of saving registers)
```

### Memory Map
```
Program Memory (ROM):
  0x000-0x3FF: 1KB internal ROM
  0x400-0xFFF: External ROM (optional)

Data Memory (RAM):
  0x00-0x07: Register Bank 0
  0x18-0x1F: Register Bank 1
  0x20-0x3F: General-purpose RAM
```

---

## The IBM PC Connection

### Every PC Had an 8048
```
The IBM PC keyboard (1981) contained an Intel 8048:

Functions:
- Key matrix scanning
- Debouncing
- Key code generation
- Serial communication to PC

The 8048 ran continuously, watching for keypresses
and sending scan codes to the main PC.

This continued through:
- IBM PC (1981)
- IBM PC/AT (1984) - upgraded to 8042
- All compatibles
```

### Why Not the Main CPU?
```
Keyboard scanning needs:
- Constant monitoring (interrupt-driven)
- Simple I/O operations
- Low cost
- Independent operation

Perfect microcontroller application!
```

---

## MCS-48 Family

| Variant | ROM | RAM | Notes |
|---------|-----|-----|-------|
| 8035 | None | 64B | External ROM |
| **8048** | **1KB** | **64B** | **Standard** |
| 8049 | 2KB | 128B | Enhanced |
| 8050 | 4KB | 256B | Large |
| 8748 | 1KB EPROM | 64B | Development |

---

## Performance

### Timing
```
External clock: 6 MHz
Internal divider: ÷15
Machine cycle: 2.5 µs
Instructions: 1-2 machine cycles

~400,000 instructions per second
```

### Instruction Examples
| Instruction | Cycles | Operation |
|-------------|--------|-----------|
| MOV A,Rn | 1 | Register to accumulator |
| MOV A,@Ri | 1 | Indirect load |
| ADD A,Rn | 1 | Add register |
| JMP addr | 2 | Jump |
| CALL addr | 2 | Subroutine call |
| IN A,Pp | 2 | Input from port |
| OUT Pp,A | 2 | Output to port |

---

## Historical Context

### Timeline
```
1976: 8048 introduced
1977: Adopted in consumer products
1980: 8051 introduced (successor)
1981: IBM PC uses 8048 in keyboard
1983: Billions of MCS-48 family shipped

The 8048 proved single-chip MCUs were viable.
```

### Applications
- **Keyboards** (IBM PC and compatibles)
- **Automotive** (engine control, dashboard)
- **Consumer** (appliances, toys, remotes)
- **Industrial** (sensors, controllers)
- **Medical** (portable devices)

---

## Legacy

### Path to 8051
```
8048 (1976) - Proved the concept
    ↓
8051 (1980) - Enhanced architecture
    ↓
Countless clones and derivatives
    ↓
8051 becomes most popular MCU architecture ever
```

### What 8048 Established
1. Single-chip microcontroller viability
2. Harvard architecture for MCUs
3. Register banking for fast interrupts
4. Integrated timer/counter
5. On-chip I/O ports

---

## Queueing Model

### Architecture
```
λ → [Fetch-Decode-Execute] → Completed
```

### Service Time
- Machine cycle: 15 clocks
- Average instruction: ~1.3 machine cycles
- Service time: ~20 clocks

---

## Usage

```python
from intel_8048_model import Intel8048QueueModel

model = Intel8048QueueModel('intel_8048_model.json')
ipc, metrics = model.predict_ipc(0.06)
print(f"IPC: {ipc:.4f}")

result = model.calibrate(0.07)
print(f"Error: {result['error_percent']:.2f}%")
```

---

## Conclusion

The Intel 8048 created the microcontroller market. By integrating a complete computer on one chip, it enabled embedded computing in products where a full microprocessor system was impractical. Its presence in every IBM PC keyboard made it one of the most ubiquitous processors of the PC era.

**Lesson:** Integration enables new markets. The 8048 didn't compete with microprocessors - it created an entirely new category.

---

**Version:** 1.0  
**Date:** January 24, 2026
