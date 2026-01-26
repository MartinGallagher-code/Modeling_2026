# Intel 4040 CPU Queueing Model

## Enhanced 4004 with Interrupts (1974)

The Intel 4040 was the improved version of the 4004 - the world's first microprocessor. Its key addition was **interrupt capability**, making it suitable for real embedded applications.

---

## 4040 vs 4004

| Feature | 4004 | 4040 |
|---------|------|------|
| Year | 1971 | 1974 |
| Stack | 3 levels | **7 levels** |
| Interrupts | None | **Yes!** |
| Instructions | 46 | **60** |
| HLT instruction | No | **Yes** |

---

## Why Interrupts Matter

```
WITHOUT Interrupts (4004):
    ┌──────────────────────────────┐
    │  Main Program                │
    │                              │
    │  loop:                       │
    │    check_button              │ ← Must constantly poll
    │    check_sensor              │ ← Wastes cycles
    │    do_work                   │
    │    goto loop                 │
    └──────────────────────────────┘

WITH Interrupts (4040):
    ┌──────────────────────────────┐
    │  Main Program                │
    │                              │
    │  loop:                       │
    │    do_work                   │ ← Focus on real work
    │    do_more_work              │
    │    goto loop                 │
    │                              │
    │  [INTERRUPT!] ───────────────┼──► Handle event
    │                              │    Return to work
    └──────────────────────────────┘
```

---

## New Instructions in 4040

| Instruction | Function |
|-------------|----------|
| HLT | Halt processor |
| EIN | Enable interrupts |
| DIN | Disable interrupts |
| BBS | Branch on business |
| WPM | Write program memory |
| RPM | Read program memory |

---

## MCS-40 Family Complete

```
4004 (1971) - First microprocessor
    │
    ▼
4040 (1974) - Enhanced, with interrupts
    │
    └── End of 4-bit line

Intel then focused on 8-bit (8008, 8080)
```

---

**Version:** 1.0 | **Date:** January 25, 2026

*"The 4040: Finally, interrupts!"*
