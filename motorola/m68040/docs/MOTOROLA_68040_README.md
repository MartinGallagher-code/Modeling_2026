# Motorola 68040 CPU Queueing Model

## Executive Summary

The Motorola 68040 (1990) was the **most powerful 68k processor ever made**. With 1.2 million transistors, a 6-stage pipeline, on-chip FPU, and 4KB caches, it represented a quantum leap from the 68030. This chip powered the Macintosh Quadra series - the pinnacle of 68k Macs.

**Key Finding:** The 68040 shows how far CISC could be pushed. By adding a deeper pipeline, larger caches, and integrated FPU, Motorola achieved near-1 IPC performance. However, the complexity also revealed limits: the 68060 was canceled, and Apple transitioned to PowerPC.

---

## Technical Specifications

| Specification | Value |
|---------------|-------|
| Year | 1990 |
| Word Size | 32 bits |
| Data Bus | 32 bits |
| Address Bus | 32 bits (4GB) |
| Clock Speed | 25-40 MHz |
| Transistors | **1,200,000** |
| Pipeline | **6 stages** |
| I-Cache | **4KB** (16× 68030) |
| D-Cache | **4KB** (16× 68030) |
| FPU | **On-chip** |
| Process | 800 nm |

---

## Revolutionary Improvements

### 1. On-Chip FPU
```
68030: Required external 68881/68882
- Separate chip, $100+ cost
- Slow communication over bus
- Many systems shipped without FPU

68040: FPU integrated
- 3-5× faster FP than 68882
- Lower system cost
- Every 68040 has FP capability*

*LC040 variant had no FPU (cost-reduced)
```

### 2. 6-Stage Pipeline
```
68030: 3-stage pipeline
68040: 6-stage pipeline

Stages:
1. Instruction Fetch
2. Instruction Decode
3. EA Calculate
4. EA Fetch
5. Execute
6. Write-back

Result: Near-1 IPC for integer code
```

### 3. Massively Larger Caches
```
         I-Cache    D-Cache    Total
68030:   256B       256B       512B
68040:   4KB        4KB        8KB
Ratio:   16×        16×        16×

Cache type: 4-way set associative
Line size: 16 bytes
D-cache: Copy-back (vs 68030's write-through)

Result: 95%+ cache hit rates
```

---

## Pipeline Detail

```
Stage 1: Instruction Fetch (IF)
    - Fetch from I-cache or memory
    - 4KB I-cache, 95% hit rate
    ↓
Stage 2: Instruction Decode (ID)
    - Decode opcode
    - Identify operands
    ↓
Stage 3: EA Calculate (EAC)
    - Calculate effective addresses
    - Index register arithmetic
    ↓
Stage 4: EA Fetch (EAF)
    - Fetch operands from D-cache/memory
    - 4KB D-cache, 92% hit rate
    ↓
Stage 5: Execute (EX)
    - ALU operation or FPU operation
    - Integer: 1 cycle typical
    - FP: 3-5 cycles typical
    ↓
Stage 6: Write-back (WB)
    - Write results to registers
    - Update D-cache if needed
```

---

## Famous Systems

### Macintosh Quadra Series
| Model | Clock | Year | Notes |
|-------|-------|------|-------|
| Quadra 700 | 25 MHz | 1991 | First Quadra |
| Quadra 900 | 25 MHz | 1991 | Tower workstation |
| Quadra 950 | 33 MHz | 1992 | High-end tower |
| Quadra 800 | 33 MHz | 1993 | Popular workstation |
| Quadra 840AV | 40 MHz | 1993 | Multimedia powerhouse |

### Other Platforms
| System | Clock | Notes |
|--------|-------|-------|
| Amiga 4000 | 25 MHz | Ultimate Amiga |
| NeXTstation Turbo | 33 MHz | Fast NeXT |
| HP 9000/400 | 25-50 MHz | Unix workstation |

---

## Performance

### vs 68030 at Same Clock
| Metric | 68030 | 68040 | Improvement |
|--------|-------|-------|-------------|
| Integer IPC | 0.80 | 0.90 | +12% |
| FP performance | External | Integrated | 3-5× |
| Cache hit rate | ~85% | ~95% | +10% |
| Memory bandwidth | Lower | Higher | 2× |
| Overall | Baseline | 2-3× | Huge |

### Real-World Performance
```
At 25 MHz:
- Integer: ~20 MIPS
- Floating-point: ~3.5 MFLOPS

At 40 MHz (Quadra 840AV):
- Integer: ~35 MIPS
- Floating-point: ~6 MFLOPS
```

### vs Intel 80486
```
68040 @ 25 MHz vs 486 @ 25 MHz:
- Integer: Comparable
- FP: 68040 slightly faster
- Market: Intel winning on volume
```

---

## Variants

| Variant | FPU | MMU | Use Case |
|---------|-----|-----|----------|
| 68040 | Yes | Yes | Full-featured |
| 68LC040 | **No** | Yes | Cost-reduced (Quadra 605) |
| 68EC040 | **No** | **No** | Embedded systems |

The LC040's missing FPU frustrated many Quadra 605 users.

---

## Queueing Model

### Six-Stage Pipeline
```
λ → [Fetch] → [Decode] → [EA Calc] → [EA Fetch] → [Execute] → [WB] → Done
```

### Service Times
- Fetch: ~1.25 cycles (with cache)
- Decode: ~1.0 cycle
- EA Calc: ~0.8 cycles
- EA Fetch: ~0.9 cycles
- Execute: ~1.5 cycles
- Writeback: ~0.5 cycles

---

## Usage

```python
from motorola_68040_model import Motorola68040QueueModel

model = Motorola68040QueueModel('motorola_68040_model.json')

# Predict IPC
ipc, metrics = model.predict_ipc(0.55)
print(f"IPC: {ipc:.4f}")  # Near 0.9!

# Compare to 68030
comp = model.compare_68030()
print(f"Performance gain: {comp['improvements']['performance']}")
```

---

## End of an Era

### The PowerPC Transition
```
1990: 68040 released
1991: Motorola joins Apple-IBM PowerPC alliance
1993: Last major 68k development
1994: First PowerPC Macs ship
1996: Last 68k Macs discontinued

The 68040 was the end of the line.
```

### Why No 68050?
```
68060 was developed but:
- Canceled for general market
- Only used in embedded systems
- PowerPC was the future

The 68040 represents peak 68k.
```

---

## Conclusion

The 68040 pushed CISC architecture to its practical limits. With a 6-stage pipeline, integrated FPU, and large caches, it achieved remarkable performance for its era. However, increasing complexity and the rise of RISC led Motorola to join the PowerPC alliance.

**Lesson:** There are limits to complexity. The 68040 showed what was possible with aggressive CISC design, but also why the industry moved toward RISC and eventually simpler-core/more-cores approaches.

---

**Version:** 1.0  
**Date:** January 24, 2026
