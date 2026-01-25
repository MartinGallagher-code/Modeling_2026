# Intel MCS-96 8096 Queueing Model

## THE AUTOMOTIVE MCU (1982)

The Intel 8096 dominated automotive engine control from the mid-1980s through the 2000s. If your car was built in that era, it probably had an 8096-family chip.

---

## Why Automotive Loved the 8096

```
Engine Control Unit (ECU):
┌─────────────────────────────────────────────────────────┐
│                     Intel 8096                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   A/D       │  │    HSI      │  │    HSO      │     │
│  │ Converter   │  │ High-Speed  │  │ High-Speed  │     │
│  │             │  │   Input     │  │   Output    │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │             │
│    Sensors          Crankshaft       Spark/Fuel        │
│  (O2, Temp,         Position         Timing            │
│   Throttle)                                            │
└─────────────────────────────────────────────────────────┘
```

---

## Feature-to-Function Mapping

| 8096 Feature | Automotive Use |
|--------------|----------------|
| **A/D Converter** | Throttle position, O2 sensor, coolant temp |
| **HSI** | Crankshaft/camshaft position capture |
| **HSO** | Spark plug firing, injector opening |
| **PWM** | Idle air control, EGR valve |
| **Multiply** | Fuel calculation algorithms |
| **Timers** | RPM measurement |

---

## On-Chip Peripherals

| Peripheral | Specification |
|------------|---------------|
| A/D Converter | 8-channel, 10-bit |
| HSI | 4 capture inputs |
| HSO | 6 compare outputs |
| PWM | 1 channel |
| Serial | Full-duplex UART |
| Timer | 16-bit |
| RAM | 232 bytes |
| ROM | 8 KB |

---

## Register Architecture

Unlike most CPUs with fixed registers, the 8096 uses a **register file in RAM**:

```
Address Map:
0x00-0x17  Special Function Registers (SFRs)
0x18-0xFF  General Purpose Registers (232 bytes)

Any location can be used as:
- 8-bit register (byte)
- 16-bit register (word, even address)
- 32-bit register (double-word, mod 4 address)
```

---

## MCS-96 Family

```
8096 (1982) ← This chip
    │
    ├── 8097 (ROM version)
    ├── 8098 (ROM-less)
    │
    └── 80196 (1987) - Enhanced
            │
            └── 80296 - Further enhanced
```

---

## Performance

| Metric | Value |
|--------|-------|
| Clock | 12 MHz |
| IPC | ~0.12 |
| MIPS | ~0.72 |
| Multiply | 6.5 µs |
| Divide | 13 µs |

---

## Historical Impact

**1985-2005:** The 8096 family was in the majority of automotive ECUs worldwide.

Applications beyond automotive:
- Industrial motor control
- Robotics
- Medical devices
- Appliances

---

**Version:** 1.0 | **Date:** January 25, 2026

*"The 8096: Powering every car's brain."*
