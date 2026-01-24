# NS32016 - Quick Start Guide

## The First 32-Bit Failure

The NS32016 (1982) was the first commercial 32-bit microprocessor. It was also a complete disaster.

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1982 |
| Claim | "First 32-bit micro" |
| Reality | Buggy, slow, failed |
| Actual IPC | ~0.10 (vs spec 0.40) |
| Market Share | ~0% |

---

## What Went Wrong

1. **Severe silicon bugs** - Required workarounds
2. **Late delivery** - 2 years behind schedule  
3. **Slow performance** - Worse than 16-bit 68000
4. **No ecosystem** - Customers fled

---

## The Lesson

```
WORKING SILICON > BEST ARCHITECTURE

Being "first" with broken product = failure
Being "later" with working product = possible success
```

---

## Basic Usage

```python
from ns32016_model import NS32016QueueModel

model = NS32016QueueModel('ns32016_model.json')

# See the poor performance
ipc, _ = model.predict_ipc(0.08)
print(f"IPC: {ipc:.4f}")  # ~0.05 (terrible)

# Compare with 68000
comp = model.compare_68000()
print(f"NS32016: {comp['ns32016']['status']}")  # Failed
print(f"68000: {comp['68000']['status']}")      # Success
```

---

**Version:** 1.0
