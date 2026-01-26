# Western Design Center W65C802 Queueing Model

## THE 65816 IN A 6502 PACKAGE! (1984)

The W65C802 is Bill Mensch's brilliant solution to the 6502 upgrade problem: take the powerful 65816 and put it in a 40-pin package that drops right into existing 6502 systems.

---

## The Key Insight

```
65816 (Full version):           65802 (This chip):
┌─────────────────────┐         ┌─────────────────────┐
│    64-pin package   │         │   40-pin package    │
│    24-bit address   │         │   16-bit address    │
│    16 MB memory     │         │   64 KB memory      │
│    Apple IIGS, SNES │         │   Fits 6502 socket! │
└─────────────────────┘         └─────────────────────┘
           │                              │
           └──────────┬───────────────────┘
                      │
              SAME CPU CORE!
              Same registers!
              Same instructions!
```

---

## Drop-In Upgrade

```
Before:                         After:
┌─────────────────────┐         ┌─────────────────────┐
│     Apple II        │         │     Apple II        │
│  ┌───────────────┐  │         │  ┌───────────────┐  │
│  │     6502      │  │  ───►   │  │    65802      │  │
│  │   (40-pin)    │  │         │  │   (40-pin)    │  │
│  └───────────────┘  │         │  └───────────────┘  │
│     8-bit CPU       │         │    16-bit CPU!      │
└─────────────────────┘         └─────────────────────┘

Same socket. Same board. New capabilities!
```

---

## Two Modes

### Emulation Mode (Default on reset)
- Acts exactly like 6502/65C02
- 8-bit A, X, Y registers
- Stack in page 1
- **All existing software runs!**

### Native Mode (Set E=0)
- Full 16-bit registers
- 16-bit math
- Relocatable direct page
- Stack anywhere in memory
- New addressing modes

---

## New Features Over 6502

| Feature | 6502 | 65802 Native |
|---------|------|--------------|
| Accumulator | 8-bit | **16-bit** |
| Index regs | 8-bit | **16-bit** |
| Stack | Page 1 | **Anywhere** |
| Direct page | $00 only | **Relocatable!** |
| Block move | No | **MVN, MVP** |
| Stack relative | No | **Yes** |

---

## 6502 Family Tree

```
6502 (1975) - The original
    │
    ├── 65C02 (1983) - CMOS, new instructions
    │
    ├── 65802 (1984) - 65816 in 40-pin ← THIS
    │       │
    │       └── Same core as ↓
    │
    └── 65816 (1984) - Full 16-bit, 16MB
            │
            ├── Apple IIGS
            └── Super Nintendo
```

---

## Performance

| Mode | IPC | Notes |
|------|-----|-------|
| Emulation | 0.10 | 6502 compatible |
| Native | 0.14 | 16-bit operations |

The 16-bit registers provide ~2× speedup for 16-bit work.

---

## Still Available!

Western Design Center **still sells the W65C802** today. Bill Mensch's company continues producing 6502-family chips decades later.

---

## Practical Applications

- **Upgrade existing systems**: Apple II, C64, BBC Micro
- **New embedded designs**: 16-bit with small footprint
- **Learning platform**: Same socket as 6502

---

**Version:** 1.0 | **Date:** January 25, 2026

*"The W65C802: 16-bit power, 6502 socket."*
