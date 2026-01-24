# RCA 1802 - Quick Start Guide

## The Space Processor

The RCA 1802 (1976) was the first CMOS microprocessor. Slow, but so reliable it's still running in Voyager spacecraft after 49 years!

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1976 |
| Technology | **CMOS** (first!) |
| Registers | 16 × 16-bit |
| IPC | ~0.05 (slow) |
| Power | ~1mW (1000× less than NMOS) |
| Voltage | 3V to 15V |
| Radiation | Tolerant |
| Voyager Status | **Still running (2026)** |

---

## Why It Matters

**For space missions:**
- Ultra-low power (solar panels limited)
- Radiation tolerant (cosmic rays)
- Wide temperature range
- Extreme reliability

**Voyager 1 & 2:**
- Launched 1977
- Still operating 2026
- 49 years continuous operation
- 15+ billion miles from Earth

---

## Basic Usage

```python
from rca_1802_model import RCA1802QueueModel

model = RCA1802QueueModel('rca_1802_model.json')

ipc, _ = model.predict_ipc(0.02)
print(f"IPC: {ipc:.5f}")  # Very slow, but reliable!

stats = model.space_mission_stats()
print(f"Years operating: {stats['years_operating']}")
print(f"Still working: {stats['still_working']}")
```

---

## The Lesson

**Reliability > Performance** (for critical applications)

The "best" processor isn't always the fastest. Sometimes it's the one that still works after 49 years in space.

---

**Version:** 1.0
