# Ferranti F100-L Queueing Model

## British Military 16-Bit Processor (1976)

The F100-L was Britain's radiation-hardened military microprocessor, designed for applications where reliability and supply independence mattered more than raw speed.

---

## Design Philosophy

```
Commercial Processors:    F100-L:
┌──────────────────┐     ┌──────────────────┐
│ Priority 1: Speed│     │ Priority 1: Reliability
│ Priority 2: Cost │     │ Priority 2: Rad-hard
│ Priority 3: Power│     │ Priority 3: UK supply
└──────────────────┘     └──────────────────┘
```

---

## Military Applications

| System | Role |
|--------|------|
| **Tornado** | Navigation/attack computer |
| **Rapier** | Missile fire control |
| **Naval** | Various UK ships |
| **Satellites** | UK space missions |

---

## Specifications

| Spec | Value |
|------|-------|
| Word size | 16-bit |
| Clock | 1.6 MHz |
| Address | 32K words |
| Instructions | 45 |
| Package | 64-pin ceramic |

---

## Why British?

During the Cold War, UK defense policy required critical military systems to use processors that were:

1. **Not dependent on foreign supply** (especially US)
2. **Radiation hardened** for nuclear environments
3. **Under UK government control**

Ferranti (later part of GEC, now BAE Systems) developed the F100-L to meet these requirements.

---

## Register Set

| Register | Function |
|----------|----------|
| ACC | 16-bit Accumulator |
| OR | Operand Register (pointer) |
| CR | Control/Status |
| PC | Program Counter |
| SP | Stack Pointer |

---

## Historical Significance

The F100-L represents:
- British computing independence
- Military-grade design priorities
- Cold War era defense policy
- Pre-COTS (Commercial Off-The-Shelf) era

By the 1990s, hardened commercial processors replaced dedicated mil-spec designs.

---

## Ferranti Heritage

Ferranti was a major UK electronics company with roots back to the 1880s:
- Built early UK computers (1950s)
- Designed military electronics
- Merged into GEC (1987)
- Now part of BAE Systems

---

**Version:** 1.0 | **Date:** January 25, 2026

*"The F100-L: British reliability in silicon."*
