# Zilog Z280 CPU Queueing Model

## The Failed Z80 Successor (1985)

The Z280 was Zilog's ambitious attempt to evolve the Z80 into a modern 16-bit processor. Despite impressive features, it was a commercial failure.

---

## Z280 vs Z80

| Feature | Z80 | Z280 |
|---------|-----|------|
| Bus | 8-bit | **16-bit** |
| Address | 64 KB | **16 MB** |
| Cache | None | **256 bytes** |
| MMU | None | **On-chip** |
| Multiply | None | **Hardware** |
| Pipeline | None | **4-stage** |
| Compatible | - | **Partial** |

---

## Impressive Features

### On-Chip MMU
- 512-byte pages
- User/System modes
- Memory protection

### Instruction Cache
- 256 bytes
- Reduced memory traffic

### New Instructions
- MULT (16×16→32)
- DIV, DIVU
- Enhanced block I/O
- Privileged instructions

---

## Why It Failed

```
1985 Market Reality:

┌─────────────────────────────────────────────────┐
│  "We want Z80 compatibility"                    │
│        │                                        │
│        ▼                                        │
│  Z280: "Well, sort of... timing is different"   │
│                                                 │
│  Market: "Never mind, we'll use 80286 or 68000" │
└─────────────────────────────────────────────────┘
```

### Key Problems:
1. **Compatibility issues** - Different instruction timing
2. **Late to market** - 1985 was too late for 8-bit evolution
3. **No ecosystem** - No compilers, no software
4. **Wrong competition** - 80286 and 68000 were better choices

---

## The Lesson

The Z280 proves that **compatibility matters more than features**.

Intel's 80286 was backward compatible with 8086.
The Z280 was NOT fully compatible with Z80.
The market chose compatibility.

---

## Legacy

The Z280 is largely forgotten today. Zilog eventually succeeded with the Z180 (which WAS Z80 compatible) for embedded applications.

---

**Version:** 1.0 | **Date:** January 25, 2026

*"The Z280: Great features, wrong market, wrong time."*
