# Intel 80486 CPU Queueing Model

## Executive Summary

The Intel 80486 (April 1989) was a landmark processor that brought **RISC-like efficiency to x86**. With a 5-stage pipeline, 8KB on-chip cache, and integrated FPU, the 486 was 2× faster than a 386 at the same clock speed. It also pioneered **clock doubling** (DX2/DX4), a technique still used today.

**Key Finding:** The 486 proved that CISC architectures could adopt RISC techniques (pipelining, simple instruction timing) without breaking backward compatibility. This insight saved the x86 architecture and led to modern superscalar x86 processors.

---

## Technical Specifications

| Specification | Value |
|---------------|-------|
| Year | April 1989 |
| Word Size | 32 bits |
| Data Bus | 32 bits |
| Address Bus | 32 bits (4GB) |
| Clock Speed | 25-100 MHz |
| Transistors | **1,200,000** |
| Pipeline | **5 stages** (first x86!) |
| Cache | **8KB unified** (first x86!) |
| FPU | **On-chip** (first x86!) |
| Process | 1000 nm |
| Price (1989) | $950 |

---

## Revolutionary Improvements

### 1. First x86 Pipeline
```
80386: No pipeline - each instruction fully completes before next starts
80486: 5-stage pipeline - multiple instructions in flight

Stages:
1. Prefetch (PF)
2. Decode 1 (D1)
3. Decode 2 (D2)
4. Execute (EX)
5. Write-back (WB)

Result: Many simple instructions execute in 1 cycle!
```

### 2. On-Chip Cache
```
80386: No on-chip cache (external cache optional)
80486: 8KB unified cache on-chip

- 4-way set associative
- 16-byte line size
- ~93% hit rate typical
- 1 cycle hit, 8 cycle miss

Result: Dramatic reduction in memory wait states
```

### 3. Integrated FPU
```
80386: Required external 80387 ($200+ additional cost)
80486: FPU on same die

- Full 80387 compatibility
- 8-10× faster than external 80387
- Tightly integrated with integer unit

Result: Every 486DX has fast FP; no upgrade needed
```

### 4. Clock Doubling (DX2/DX4)
```
Innovation: Run CPU faster than motherboard bus

486DX2-66:
- Internal clock: 66 MHz
- Bus clock: 33 MHz
- Multiplier: 2×

486DX4-100:
- Internal clock: 100 MHz
- Bus clock: 33 MHz
- Multiplier: 3×

Result: Faster CPUs on existing motherboards
        This technique is used to this day!
```

---

## Instruction Timing Revolution

### 386 vs 486 Instruction Cycles

| Instruction | 80386 | 80486 | Improvement |
|-------------|-------|-------|-------------|
| MOV reg,reg | 2 | **1** | 2× |
| MOV reg,mem | 4 | **1** | 4× |
| ADD reg,reg | 2 | **1** | 2× |
| ADD reg,mem | 6 | **2** | 3× |
| PUSH | 2 | **1** | 2× |
| JMP | 7+ | **3** | 2× |

The 486 achieved **RISC-like timing** for common instructions.

---

## Variants

| Variant | Clock | FPU | Cache | Notes |
|---------|-------|-----|-------|-------|
| 486DX-25 | 25 MHz | Yes | 8KB | Original |
| 486DX-33 | 33 MHz | Yes | 8KB | Common |
| 486DX-50 | 50 MHz | Yes | 8KB | Hot, problematic |
| 486SX-25 | 25 MHz | **No** | 8KB | Cost-reduced |
| 486DX2-50 | 50 MHz | Yes | 8KB | Clock doubled |
| 486DX2-66 | 66 MHz | Yes | 8KB | Most popular |
| 486DX4-75 | 75 MHz | Yes | 16KB | Triple clock |
| 486DX4-100 | 100 MHz | Yes | 16KB | Fastest 486 |

### The 486SX Story
```
The 486SX was a 486DX with FPU disabled:
- Either defective FPUs, or artificially disabled
- Cost $333 vs $665 for DX (1991)
- Upgrade path: 487SX (actually a full 486DX!)

Classic Intel market segmentation.
```

---

## Performance

### vs 80386 at Same Clock
| Metric | 80386 | 80486 | Improvement |
|--------|-------|-------|-------------|
| Integer IPC | 0.40 | 0.85 | 2.1× |
| FP (external 387) | Slow | Integrated | 8-10× |
| Memory access | No cache | 8KB cache | 4× typical |
| Overall | Baseline | **~2×** | Major leap |

### Real-World Performance
```
486DX-33:  ~27 MIPS (vs 386DX-33: ~11 MIPS)
486DX2-66: ~54 MIPS
486DX4-100: ~70 MIPS

The 486DX2-66 was the sweet spot for most of the early 90s.
```

---

## Historical Context

### Market Impact
```
1989: 486 introduces at $950
1990: 486 systems become mainstream
1991: 486SX provides entry point
1992: 486DX2 clock doubling
1993: Intel's annual revenue hits $8.8B
1994: 486DX4 reaches 100 MHz

The 486 cemented x86 dominance.
```

### Competition
```
486 vs 68040 (1990):
- Similar performance
- Similar transistor count
- But 486 had x86 software compatibility
- Winner: 486 (market share)

486 vs RISC workstations:
- RISC was faster per clock
- But 486 was cheaper and had more software
- PC market exploded with 486
```

---

## Pipeline Detail

```
Stage 1: Prefetch (PF)
    - Fetch from cache or memory
    - 32 bytes prefetch buffer
    ↓
Stage 2: Decode 1 (D1)
    - Instruction decode begins
    - Identify opcode
    ↓
Stage 3: Decode 2 (D2)
    - Complete decode
    - Calculate addresses
    ↓
Stage 4: Execute (EX)
    - ALU operation or memory access
    - FPU operation starts here
    ↓
Stage 5: Write-back (WB)
    - Write results to registers
    - Update cache if needed
```

---

## Queueing Model

### Five-Stage Pipeline
```
λ → [PF] → [D1] → [D2] → [EX] → [WB] → Done
```

### Service Times
- Prefetch: ~1.5 cycles (with cache)
- Decode1: ~1.0 cycle
- Decode2: ~0.8 cycles
- Execute: ~1.4 cycles
- Writeback: ~0.5 cycles

---

## Usage

```python
from intel_80486_model import Intel80486QueueModel

model = Intel80486QueueModel('intel_80486_model.json')

# Predict IPC
ipc, metrics = model.predict_ipc(0.55)
print(f"IPC: {ipc:.4f}")

# Compare to 386
comp = model.compare_80386()
print(f"vs 386: {comp['improvements']}")

# See clock variants
variants = model.clock_variants()
for name, specs in variants.items():
    print(f"{name}: {specs['mips']:.1f} MIPS")
```

---

## Legacy

### RISC Techniques in CISC
```
The 486 proved CISC could be fast:
- Simple instructions in 1 cycle (like RISC)
- Complex instructions take longer (CISC advantage)
- Best of both worlds

This led to:
- Pentium (superscalar)
- Pentium Pro (out-of-order)
- Modern x86 (RISC internally, CISC externally)
```

### Clock Scaling
```
486DX2 pioneered clock multipliers:
- Pentium: 1.5×, 2×, 2.5×
- Pentium II: 3.5×, 4×, 4.5×
- Modern CPUs: 40×+ multipliers

The 486 invented modern CPU frequency scaling.
```

---

## Conclusion

The 80486 saved x86. By adopting RISC techniques (pipelining, single-cycle execution, on-chip cache) while maintaining CISC compatibility, Intel proved that x86 could be fast. The 486 also pioneered clock doubling, a technique used in every modern processor.

**Lesson:** Architecture can evolve. The 486 proved that legacy ISAs can adopt modern implementation techniques without breaking compatibility.

---

**Version:** 1.0  
**Date:** January 24, 2026
