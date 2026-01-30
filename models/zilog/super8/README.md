# Zilog Super8

**Enhanced Z8 with pipelining and expanded addressing**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Zilog |
| Year | 1982 |
| Data Width | 8-bit |
| Clock | 8.0 MHz |
| Technology | NMOS |
| Transistors | ~12,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.0 |
| Predicted CPI | 5.400 |
| Error | 8.00% |
| Status | **MARGINAL** |

## Files

- `current/super8_validated.py` - Active grey-box queueing model
- `validation/super8_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/zilog/super8/current')
from super8_validated import Super8Model

model = Super8Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
