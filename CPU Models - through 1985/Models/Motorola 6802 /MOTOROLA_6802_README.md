# Motorola 6802 CPU Queueing Model

## 6800 with On-Chip RAM and Clock (1977)

The 6802 integrated RAM and clock generator into the 6800, simplifying system design and reducing cost.

---

## 6802 vs 6800

| Feature | 6800 | 6802 |
|---------|------|------|
| On-chip RAM | None | **128 bytes** |
| Clock gen | External | **On-chip** |
| Power | +5V, -5V, +12V | **+5V only** |
| Standby | No | **RAM retention** |

---

## 6800 Family Tree

```
6800 (1974) - Original CPU
    │
    ├── 6802 (1977) - CPU + RAM + Clock
    │       │
    │       └── 6808 - 6802 at 4 MHz
    │
    └── 6801 (1978) - Full MCU (RAM + ROM + I/O)
            │
            └── 6803 - ROM-less 6801
```

**Key distinction:**
- 6802 = **CPU** (RAM, no I/O)
- 6801 = **MCU** (RAM + ROM + I/O)

---

## On-Chip RAM

```
Memory Map:
0x0000 ┌─────────────────┐
       │  On-chip RAM    │ ← 128 bytes
       │  (fast access)  │
0x007F └─────────────────┘
0x0080 ┌─────────────────┐
       │  External       │
       │  Memory         │
       │  ...            │
0xFFFF └─────────────────┘
```

The on-chip RAM was ideal for stack and frequently-used variables.

---

## Standby Mode

The 6802 could retain RAM contents with minimal power:
- Apply Vstandby (2V-5V)
- Stop clock
- RAM preserved
- Wake up with data intact

Great for battery-backed applications!

---

**Version:** 1.0 | **Date:** January 25, 2026

*"The 6802: 6800 made simple."*
