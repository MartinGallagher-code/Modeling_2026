# ARM2 CPU Queueing Model

## Executive Summary

The ARM2 (1986) was the **first production ARM processor**, powering the Acorn Archimedes - widely considered the **fastest personal computer of its time**. Building on ARM1's foundation, ARM2 added a hardware multiplier, coprocessor interface, and atomic swap instruction while remaining remarkably simple at just 30,000 transistors.

**Key Finding:** The ARM2-powered Archimedes demonstrated that RISC could deliver superior real-world performance in personal computers. While the Amiga and Atari ST used the 68000, the ARM2 was approximately 5-6× faster, proving ARM's efficiency wasn't just theoretical.

---

## Technical Specifications

| Specification | Value |
|---------------|-------|
| Year | 1986 |
| Word Size | 32 bits |
| Data Bus | 32 bits |
| Address Bus | 26 bits (64MB) |
| Clock Speed | 8-12 MHz |
| Transistors | **30,000** |
| Pipeline | 3 stages |
| Registers | 16 |
| Process | 2 µm |
| Power | ~120 mW |

---

## Improvements Over ARM1

| Feature | ARM1 | ARM2 |
|---------|------|------|
| Multiplier | Microcode (16 cycles) | **Hardware (8 cycles)** |
| Coprocessor | No | **Yes (FPA10)** |
| SWP instruction | No | **Yes (atomic swap)** |
| Max clock | 8 MHz | **12 MHz** |
| Process | 3 µm | **2 µm** |
| Status | Development | **Production** |

---

## The Acorn Archimedes

### Launch (July 1987)
```
The Archimedes was a revelation:
- ARM2 @ 8 MHz
- 512KB - 4MB RAM
- Custom VIDC graphics (up to 256 colors)
- Custom IOC I/O controller
- RISC OS (Arthur initially)

Performance: ~4.5 MIPS (vs ~0.8 MIPS for Amiga/ST)
```

### Models
| Model | RAM | Notes |
|-------|-----|-------|
| A305 | 512KB | Entry level |
| A310 | 1MB | Standard |
| A410 | 1MB | Business |
| A440 | 4MB | High-end |
| A3000 | 1MB | All-in-one (1989) |

### Market Impact
```
UK Education: Dominated (BBC Micro successor)
Enthusiast: Strong following
Business: Limited penetration
Gaming: Excellent but small library

The Archimedes was technically superior but
couldn't overcome Amiga/ST momentum outside UK.
```

---

## Performance Comparison (1987)

### Raw CPU Speed
| System | CPU | Clock | MIPS |
|--------|-----|-------|------|
| **Archimedes** | **ARM2** | **8 MHz** | **~4.5** |
| Amiga 500 | 68000 | 7.16 MHz | ~0.7 |
| Atari ST | 68000 | 8 MHz | ~0.8 |
| Mac Plus | 68000 | 8 MHz | ~0.8 |
| IBM PC/AT | 80286 | 8 MHz | ~1.0 |

**The ARM2 was 5-6× faster than the 68000!**

### Why ARM2 Was So Fast
```
1. RISC efficiency: Most instructions in 1 cycle
2. 16 registers: Fewer memory accesses
3. Conditional execution: Fewer branches
4. Barrel shifter: Complex ops in single instruction
5. Clean design: No legacy overhead
```

---

## Architecture Details

### Pipeline (Same as ARM1)
```
┌─────────┐    ┌─────────┐    ┌─────────┐
│  Fetch  │ →  │ Decode  │ →  │ Execute │
└─────────┘    └─────────┘    └─────────┘
```

### Hardware Multiplier
```
ARM1:  MUL was microcoded, ~16 cycles
ARM2:  MUL is hardware, ~8 cycles

32×32 → 32-bit result
MLA (Multiply-Accumulate) in 9 cycles

Important for graphics, DSP-like operations
```

### SWP Instruction
```
SWP Rd, Rm, [Rn]

Atomically:
1. Read word from [Rn]
2. Write Rm to [Rn]
3. Return old value to Rd

Essential for:
- Semaphores
- Mutexes
- Multi-processor synchronization
- OS development
```

### Coprocessor Interface
```
Supports external coprocessors:
- FPA10: Floating-point accelerator
- Custom: User-defined coprocessors

FPA10 provided ~5 MFLOPS
(vs software FP at ~0.1 MFLOPS)
```

---

## Register Banking (FIQ Mode)

```
Unique ARM feature for fast interrupts:

Normal mode: R0-R15
FIQ mode:    R0-R7, R8_fiq-R14_fiq, R15

FIQ has its own R8-R14!

Benefit: No register save/restore needed
Result: Extremely fast interrupt response
```

---

## MEMC (Memory Controller)

```
The Archimedes used MEMC chip with ARM2:

Features:
- Address translation (MMU function)
- DRAM refresh
- Page sizes: 4KB to 32KB
- Virtual memory support

MEMC + VIDC + IOC + ARM2 = Complete system
```

---

## Queueing Model

### Three-Stage Pipeline
```
λ → [Fetch] → [Decode] → [Execute] → Done
```

### Service Times
- Fetch: 1.0 cycle
- Decode: 1.0 cycle
- Execute: ~1.5 cycles average (with hardware multiply)

---

## Usage

```python
from arm2_model import ARM2QueueModel

model = ARM2QueueModel('arm2_model.json')

# Predict IPC
ipc, metrics = model.predict_ipc(0.50)
print(f"IPC: {ipc:.4f}")

# Compare to ARM1
comp_arm1 = model.compare_arm1()
for imp in comp_arm1['improvements']:
    print(f"+ {imp}")

# Compare to 1987 competition
comp_1987 = model.compare_1987_competitors()
print(comp_1987['conclusion'])
```

---

## Legacy

### Path Forward
```
ARM2 → ARM3 (1989, with cache)
     → ARM6 (1991, 3-stage, AMBA bus)
     → ARM7TDMI (1994, Thumb, Java)
     → ARM9 (5-stage pipeline)
     → ARM11 (mobile phones)
     → Cortex-A series (smartphones)
     → Apple M-series (Macs)
```

### The Archimedes Effect
```
Though commercially limited to UK education,
the Archimedes proved ARM's potential:

1. Real-world performance superiority
2. Power efficiency
3. System-on-chip vision (ARM+MEMC+VIDC+IOC)
4. RISC OS innovations

These lessons informed ARM's later mobile success.
```

---

## Conclusion

The ARM2 and Acorn Archimedes proved that ARM wasn't just an interesting experiment - it was a genuinely superior architecture. While commercial success eluded Acorn, the technical achievement was undeniable: with just 30,000 transistors, ARM2 outperformed the 68000 by 5-6×.

**Lesson:** Technical superiority matters, even if market success takes time. The ARM2's efficiency advantages became decisive two decades later in mobile.

---

**Version:** 1.0  
**Date:** January 24, 2026
