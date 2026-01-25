# Intel 80188 - Quick Start Guide

## The Cost-Performance Tradeoff

The 80188 is to the 80186 what the 8088 is to the 8086:
- **Same** CPU core (16-bit internal)
- **Same** integrated peripherals
- **8-bit** external bus (vs 16-bit)
- **~18% slower** but **cheaper**

---

## Quick Facts

| Specification | 80188 | 80186 |
|---------------|-------|-------|
| Internal | 16-bit | 16-bit |
| External Bus | **8-bit** | 16-bit |
| Prefetch Queue | 4 bytes | 6 bytes |
| IPC | ~0.33 | ~0.40 |
| Peripherals | Integrated | Integrated |
| Bottleneck | **BIU** | EU |
| System Cost | **Lower** | Higher |

---

## Basic Usage

```python
from intel_80188_model import Intel80188QueueModel

model = Intel80188QueueModel('intel_80188_model.json')

# IPC prediction
ipc, metrics = model.predict_ipc(arrival_rate=0.08)
print(f"IPC: {ipc:.4f}")  # ~0.05

# Compare with 80186
comparison = model.compare_with_80186()
print(f"vs 80186: {comparison['performance_ratio']['penalty']}")
# Output: ~15-18% slower

# Bottleneck analysis
print(f"Bottleneck: {comparison['80188']['bottleneck']}")
# Output: BIU (8-bit) - bus is the limit!
```

---

## Key Insight: Bottleneck Shift

```
80186 (16-bit bus):
  BIU: ρ = 0.40 (not saturated)
  EU:  ρ = 0.65 (BOTTLENECK)
  
80188 (8-bit bus):
  BIU: ρ = 0.80 (BOTTLENECK!)
  EU:  ρ = 0.61 (waiting for data)
```

The 8-bit bus **starves** the EU!

---

## When to Use 80188

**Choose 80188 when:**
- Cost is critical
- Performance adequate (~18% slower OK)
- 8-bit memory/peripherals available
- High volume, cost-sensitive embedded

**Choose 80186 when:**
- Performance critical
- 16-bit peripherals needed
- Memory bandwidth important

---

## Historical Pattern

| Pair | Internal | External | Penalty |
|------|----------|----------|---------|
| 8086/8088 | 16-bit | 16/8-bit | ~18% |
| **80186/80188** | 16-bit | 16/8-bit | **~18%** |

Same tradeoff, same lesson!

---

**Version:** 1.0  
**Date:** January 24, 2026
