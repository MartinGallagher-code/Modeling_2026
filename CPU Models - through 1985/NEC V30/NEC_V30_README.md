# NEC V30 CPU Queueing Model

## Faster 8086 - V20's 16-Bit Sibling (1984)

The V30 was to the 8086 what the V20 was to the 8088: a faster, pin-compatible replacement with hardware 8080 emulation.

---

## V20/V30 Family

| Chip | Replaces | Bus | Target |
|------|----------|-----|--------|
| V20 | 8088 | 8-bit | PC/XT |
| **V30** | **8086** | **16-bit** | **AT-class** |
| V40 | - | - | Embedded |
| V50 | - | - | Embedded |

---

## V30 vs 8086

| Operation | 8086 | V30 | Speedup |
|-----------|------|-----|---------|
| MUL 16×16 | 118 cyc | 22 cyc | **5.4×** |
| DIV 32/16 | 150 cyc | 28 cyc | **5.4×** |
| Shifts | 4+n cyc | 1 cyc | **Huge** |
| Overall | - | - | **10-40%** |

---

## Same Features as V20

- Hardware 8080 emulation mode
- New block I/O instructions
- Bit manipulation instructions
- Barrel shifter
- Optimized string operations

---

## Pin-Compatible

```
8086 Socket:              V30 Upgrade:
┌─────────────────┐      ┌─────────────────┐
│     8086        │      │      V30        │
│                 │ ───► │                 │
│   Original      │      │   10-40%        │
│   Speed         │      │   FASTER!       │
└─────────────────┘      └─────────────────┘

Just swap chips. No other changes.
```

---

## The Lawsuit (Same as V20)

Intel sued NEC in 1984. NEC won in 1989.
This enabled the entire x86 clone industry.

---

**Version:** 1.0 | **Date:** January 25, 2026

*"The V30: 8086 performance, legally."*
