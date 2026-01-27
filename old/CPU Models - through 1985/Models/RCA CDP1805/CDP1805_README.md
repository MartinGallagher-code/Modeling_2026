# CDP1805 CPU Queueing Model

## Executive Summary

The CDP1805 (1984) is the **enhanced successor to the legendary RCA 1802**, designed for demanding space and high-reliability applications. With higher clock speeds, on-chip timer, and additional instructions, it powered missions to Jupiter, Venus, Saturn, and Pluto while maintaining the 1802's radiation tolerance and extreme reliability.

**Key Finding:** The 1805 proves that incremental improvement of proven technology is often better than revolutionary change for mission-critical applications. NASA trusted the 1805 with billion-dollar missions because it built on the 1802's space heritage.

---

## Technical Specifications

| Specification | Value |
|---------------|-------|
| Year | 1984 |
| Word Size | 8 bits |
| Address Space | 64 KB |
| Clock Speed | 4-5 MHz |
| Technology | **CMOS** |
| Registers | **16 × 16-bit** |
| Power | ~10 mW typical |
| Temperature | -55°C to +125°C |
| Radiation | Hardened versions available |

---

## Improvements Over 1802

| Feature | 1802 | 1805 |
|---------|------|------|
| Clock | 2 MHz | **4-5 MHz** |
| Timer | None | **On-chip** |
| BCD math | No | **Yes** |
| Instructions | 91 | **~107** |
| Idle mode | No | **Yes** |
| Performance | Baseline | **~2×** |

### New Instructions
```
Counter/Timer:
  LDC   - Load counter
  GEC   - Get counter
  STPC  - Stop counter
  DTC   - Decrement counter
  STM   - Set timer mode

BCD Arithmetic:
  DADD  - Decimal add
  DADI  - Decimal add immediate
  DSAV  - Decimal save
  
Register Operations:
  RLDI  - Register load immediate (faster)
  RLXA  - Register load via X, advance
  RSXD  - Register store via X, decrement
```

---

## Space Mission Heritage

### Major Missions Using CDP1805

| Mission | Target | Launch | Status |
|---------|--------|--------|--------|
| **Galileo** | Jupiter | 1989 | Completed 2003 |
| **Magellan** | Venus | 1989 | Completed 1994 |
| **Ulysses** | Sun | 1990 | Completed 2009 |
| **Cassini-Huygens** | Saturn | 1997 | Completed 2017 |
| **New Horizons** | Pluto | 2006 | **Still operating!** |

### Why Space Agencies Trust It
```
1. Radiation hardened (withstands cosmic rays)
2. Wide temperature range (-55°C to +125°C)
3. Low power (solar panel friendly)
4. Proven heritage (builds on 1802)
5. Simple architecture (fewer failure modes)
6. Long-term availability (still manufactured)
```

### New Horizons at Pluto
```
2006: Launch
2015: Pluto flyby (first ever!)
2019: Ultima Thule flyby
2026: Still operating, 8+ billion km from Earth

The CDP1805 is STILL WORKING in the outer solar system.
```

---

## Architecture

### Register Model (Same as 1802)
```
16 × 16-bit general registers (R0-RF)
- Any register can be Program Counter
- Any register can be stack pointer
- P register selects current PC (4 bits)
- X register selects index register (4 bits)

D: 8-bit data register (accumulator)
DF: 1-bit data flag (carry/borrow)
```

### Counter/Timer (New!)
```
8-bit programmable counter/timer:
- Count external events
- Generate interrupts
- Create time delays
- Pulse width measurement

Essential for spacecraft timing!
```

---

## Why Reliability Matters

### The Space Environment
```
Challenges:
- Cosmic radiation (bit flips, latch-up)
- Temperature extremes (-200°C to +120°C)
- Vacuum (no convection cooling)
- No repair possible
- Missions last decades

1805 solutions:
- CMOS (inherent radiation resistance)
- Simple design (fewer failure points)
- Wide operating margins
- Extensive space qualification
```

### Comparison to Modern Processors
```
Modern CPU: Faster, but...
- More transistors = more failure points
- Smaller features = radiation sensitive
- Complex design = harder to verify
- Consumer grade = short lifespan

1805: Slower, but...
- Simple = reliable
- CMOS = rad-hard
- Proven = trusted
- Qualified = space-ready
```

---

## Performance

### Timing
```
Clock: 4 MHz
Machine cycle: 8 clocks = 2 µs
Instructions: 2-3 machine cycles typical

~200,000-500,000 instructions/second
```

### Sufficient for Spacecraft
```
Spacecraft don't need speed:
- Attitude control: 10 Hz updates OK
- Telemetry: kbps rates
- Instrument control: Seconds between readings
- Navigation: Minutes between calculations

Reliability >> Speed for space
```

---

## Usage

```python
from cdp1805_model import CDP1805QueueModel

model = CDP1805QueueModel('cdp1805_model.json')
ipc, _ = model.predict_ipc(0.05)
print(f"IPC: {ipc:.4f}")

# See the missions it powered
missions = model.space_missions()
for name, info in missions.items():
    print(f"{name}: {info['target']}")
```

---

## Legacy

### Still Manufactured
The CDP1805 (and 1802) are still manufactured by Renesas (formerly Intersil, formerly Harris, formerly RCA). Some things are too important to discontinue.

### Still Flying
- Voyager 1 & 2: 1802s still working after 49 years!
- New Horizons: 1805 operating 8+ billion km away

---

## Conclusion

The CDP1805 exemplifies engineering wisdom: don't fix what isn't broken, just make it better. By enhancing the proven 1802 rather than creating something revolutionary, RCA created a processor that NASA trusted with missions worth billions of dollars to the outer planets.

**Lesson:** For mission-critical applications, proven reliability beats cutting-edge performance. The 1805 is still operating in deep space while countless "faster" processors have been retired.

---

**Version:** 1.0 | **Date:** January 24, 2026
