# Intel 8086 Performance Models

## Dual-Approach Modeling: Queueing Theory + CPI Stack

This folder contains **two complementary performance models** for the Intel 8086, providing complete insight into processor performance.

---

## Files

| File | Model Type | Purpose |
|------|------------|---------|
| `ibm_pc_8086_model.py` | Queueing Theory | Identifies resource bottlenecks |
| `ibm_pc_8086_model.json` | Configuration | Parameters for queueing model |
| `ibm_pc_8086_cpi_stack.py` | CPI Stack | Breaks down where cycles go |
| `ibm_pc_8086_unified.py` | Combined | Unified interface to both |
| `README_8086.md` | Documentation | This file |
| `QUICK_START_8086.md` | Quick Reference | Fast overview |

---

## Two Approaches, Two Questions

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  QUEUEING THEORY                    CPI STACK                       │
│  ──────────────                     ─────────                       │
│                                                                     │
│  Asks: "What's saturated?"          Asks: "Where do cycles go?"    │
│                                                                     │
│  [BIU] → [Prefetch] → [EU]          CPI = base + prefetch + bus    │
│                                          + branch + memory + EA    │
│                                                                     │
│  Output: "EU is 65% utilized"       Output: "EA adds 4.4% overhead"│
│                                                                     │
│  Use for: Resource planning         Use for: Code optimization     │
│           System bottlenecks                  Penalty analysis     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Using CPI Stack Model

```python
from ibm_pc_8086_cpi_stack import Intel8086CPIStackModel, WORKLOADS

model = Intel8086CPIStackModel()
result = model.predict(WORKLOADS["dos_typical"])

print(f"IPC: {result.ipc:.4f}")
print(f"Largest penalty: {result.bottleneck}")
print(f"Breakdown: {result.component_percentages}")
```

### Using Queueing Model

```python
from ibm_pc_8086_model import Intel8086QueueModel

model = Intel8086QueueModel('ibm_pc_8086_model.json')
ipc, metrics = model.predict_ipc(arrival_rate=0.10)

print(f"IPC: {ipc:.4f}")
print(f"Bottleneck: {metrics[0].name if metrics else 'unknown'}")
```

### Using Unified Model (Both Together)

```python
from ibm_pc_8086_unified import Intel8086UnifiedModel, WORKLOADS

model = Intel8086UnifiedModel()
result = model.analyze(WORKLOADS["dos_typical"])

model.print_combined_analysis(result, "My Workload")
```

---

## Sample Output

### CPI Stack Breakdown

```
============================================================
CPI STACK: DOS Typical
============================================================

Component               CPI       %  Bar
------------------------------------------------------------
Base (ideal)           9.05   89.7%  ████████████████████████████████████████
Prefetch stalls        0.00    0.0%  
Bus contention         0.24    2.4%  █
Branch penalty         0.36    3.6%  █
Memory delay           0.00    0.0%  
EA calculation         0.44    4.4%  ██ ←
------------------------------------------------------------
TOTAL                 10.09  100.0%

IPC: 0.0991  |  MIPS: 0.495  |  Penalty: ea_calc
```

### Combined Analysis

```
┌────────────────────────────────────────────────────────────────────┐
│ COMBINED INSIGHT                                                   │
├────────────────────────────────────────────────────────────────────┤
│ CPI Stack: Largest penalty is ea_calc (4.4%)                       │
│ Queueing: Bottleneck is execution_unit                             │
│ → Optimize: Use simpler addressing modes                           │
└────────────────────────────────────────────────────────────────────┘
```

---

## When to Use Each Model

| Question | Use This Model |
|----------|----------------|
| "Is my system CPU-bound or memory-bound?" | Queueing |
| "Would a faster bus help?" | Queueing |
| "What's causing my code to be slow?" | CPI Stack |
| "How much do branches cost me?" | CPI Stack |
| "Complete performance picture" | Unified (both) |

---

## 8086 Architecture Reference

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Intel 8086                                  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   Bus Interface Unit (BIU)                   │   │
│  │  ┌──────────────┐    ┌───────────────────────────────────┐  │   │
│  │  │   Address    │    │  6-Byte Prefetch Queue            │  │   │
│  │  │  Generation  │    │  [  ][  ][  ][  ][  ][  ]         │  │   │
│  │  └──────────────┘    └───────────────────────────────────┘  │   │
│  └──────────────────────────────┬──────────────────────────────┘   │
│                                 │                                   │
│  ┌──────────────────────────────▼──────────────────────────────┐   │
│  │                   Execution Unit (EU)                        │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────────┐ │   │
│  │  │    ALU     │  │  Registers │  │   Control Unit         │ │   │
│  │  │            │  │  AX,BX,CX  │  │   (microcode)          │ │   │
│  │  └────────────┘  │  DX,SI,DI  │  └────────────────────────┘ │   │
│  │                  │  SP,BP,Flags│                             │   │
│  │                  └────────────┘                              │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Clock: 5-10 MHz  |  Bus: 16-bit  |  Address: 20-bit (1 MB)       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## CPI Penalty Components

| Component | Description | Typical Impact |
|-----------|-------------|----------------|
| **Base** | Ideal instruction execution | 85-95% |
| **Prefetch** | Queue empty, waiting for bytes | 0-5% |
| **Bus** | EU and BIU competing for bus | 2-5% |
| **Branch** | Taken branches flush queue | 2-8% |
| **Memory** | Wait states for slow memory | 0-10% |
| **EA calc** | Complex addressing modes | 2-6% |

---

## Optimization Guidelines

Based on model analysis:

| If Penalty Is... | Optimization Strategy |
|------------------|----------------------|
| **EA calculation** | Use [BX] instead of [BX+SI+disp] |
| **Branch** | Reorganize loops, reduce conditionals |
| **Bus contention** | Use register variables, reduce memory ops |
| **Memory** | Add wait state optimization, use faster RAM |
| **Prefetch** | Shorten instruction sequences |

---

## References

- Intel 8086 Family User's Manual
- iAPX 86/88, 186/188 User's Manual
- IBM PC Technical Reference

---

**Version:** 2.0 (Added CPI Stack model)  
**Last Updated:** January 25, 2026
