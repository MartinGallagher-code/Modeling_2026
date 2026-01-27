# Motorola 68030 CPU Queueing Model

## Executive Summary

The Motorola 68030 (1987) integrated an **on-chip MMU** and **data cache** into the 68020 architecture. This chip powered some of the most beloved computers ever made: the Macintosh SE/30, IIci, NeXT Computer, and Amiga 3000.

**Key Finding:** The 68030 demonstrates the power of integration. By bringing the MMU on-chip (vs. the external 68851), Motorola reduced system cost and complexity while improving performance 20-30% over the 68020 at the same clock speed.

---

## Technical Specifications

| Specification | Value |
|---------------|-------|
| Year | 1987 |
| Word Size | 32 bits |
| Data Bus | 32 bits |
| Address Bus | 32 bits (4GB) |
| Clock Speed | 16-50 MHz |
| Transistors | 273,000 |
| I-Cache | 256 bytes |
| D-Cache | **256 bytes** (new!) |
| MMU | **On-chip** (new!) |
| Process | 800 nm |

---

## Key Improvements Over 68020

### 1. On-Chip MMU
```
68020: Required external 68851 MMU
- Additional chip cost
- Board space
- Design complexity

68030: MMU integrated
- 22-entry TLB
- Multiple page sizes (256B to 32KB)
- Lower system cost
- Simpler design
```

### 2. Data Cache
```
68020: Instruction cache only (256 bytes)
68030: I-cache (256B) + D-cache (256B)

Data cache benefit:
- Faster memory reads
- Faster memory writes
- ~15-20% speedup for data-intensive code
```

### 3. Burst Mode
```
New burst fill for caches:
- 4 longwords in 5 cycles (vs 8)
- Faster cache refills
- Better memory bandwidth utilization
```

---

## Famous Systems

### Macintosh
| Model | Clock | Year | Notes |
|-------|-------|------|-------|
| SE/30 | 16 MHz | 1989 | Beloved compact Mac |
| IIx | 16 MHz | 1988 | First Mac with 68030 |
| IIcx | 16 MHz | 1989 | Compact tower |
| IIci | 25 MHz | 1989 | Popular workstation |
| IIfx | 40 MHz | 1990 | "Wicked Fast" |

### Other Platforms
| System | Clock | Notes |
|--------|-------|-------|
| NeXT Computer | 25 MHz | Steve Jobs' next venture |
| Amiga 3000 | 25 MHz | Advanced multimedia |
| Atari TT030 | 32 MHz | Workstation |
| Atari Falcon | 16 MHz | Last Atari computer |
| Sun 3/80 | 20 MHz | Unix workstation |

### The Mac SE/30 Legend
```
The SE/30 (1989) is often called the greatest compact Mac ever:
- 68030 @ 16 MHz in compact form factor
- Expandable RAM to 128MB
- Fast SCSI
- Color video card slot
- Ran System 7 well
- Still has devoted fans in 2026!
```

---

## Architecture

### Pipeline (3-stage)
```
┌─────────────┐    ┌────────────┐    ┌─────────────────┐
│ Fetch + I$  │ →  │   Decode   │ →  │ Execute + D$    │
└─────────────┘    └────────────┘    └─────────────────┘
      ↓                                      ↓
  256B I-cache                          256B D-cache
```

### Cache Details
```
Both caches:
- 256 bytes
- Direct-mapped
- 4-byte line size
- Write-through (D-cache)

Hit rates (typical):
- I-cache: ~90%
- D-cache: ~85%
```

### MMU Details
```
22-entry TLB (fully associative)
Page sizes: 256B to 32KB
Separate user/supervisor spaces
Access control per page
Hardware support for demand paging
```

---

## Performance

### vs 68020 at Same Clock
| Metric | 68020 | 68030 | Improvement |
|--------|-------|-------|-------------|
| IPC | 0.70 | 0.85 | +21% |
| Data access | Slow | Cached | +30% |
| VM overhead | High | Low | +15% |

### Real-World Performance
```
At 25 MHz:
- ~8 MIPS typical
- ~20 MIPS peak (cache hits)

Compared to:
- 68020 @ 16 MHz: ~5 MIPS
- 80386 @ 25 MHz: ~6 MIPS
```

---

## Queueing Model

### Three-Stage Pipeline
```
λ → [Fetch+I$] → [Decode] → [Execute+D$] → Completed
```

### Service Times
- Fetch (with I-cache): ~1.4 cycles
- Decode: ~1.0 cycle
- Execute (with D-cache): ~3.0 cycles

---

## Usage

```python
from motorola_68030_model import Motorola68030QueueModel

model = Motorola68030QueueModel('motorola_68030_model.json')

# Predict IPC
ipc, metrics = model.predict_ipc(0.50)
print(f"IPC: {ipc:.4f}")

# Compare to 68020
comp = model.compare_68020()
print(f"68030 improvements: {comp['improvements']}")
```

---

## Legacy

### The Classic Mac Era
```
The 68030 defined the "classic" high-end Macintosh:
- 1987-1991: Peak 68k Mac era
- SE/30, IIci remain legendary
- Last Mac before 68040

For many users, 68030 Macs were their first
experience with a "fast" computer.
```

### NeXT's Choice
```
Steve Jobs chose the 68030 for the NeXT Computer:
- Unix workstation
- Object-oriented development
- Eventually became macOS foundation

The 68030 helped create the Mac's future OS.
```

---

## Conclusion

The 68030 represents the peak of the "classic" 68k architecture before the 68040's radical changes. Its combination of integrated MMU, data cache, and higher clock speeds made it the heart of legendary computers.

**Lesson:** Integration reduces cost and complexity while improving performance. The 68030's on-chip MMU made high-end computing more accessible.

---

**Version:** 1.0  
**Date:** January 24, 2026
