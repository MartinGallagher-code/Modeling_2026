# Inmos T212

**16-bit transputer, parallel processing pioneer with CSP-based concurrency**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Inmos |
| Year | 1985 |
| Data Width | 16-bit |
| Clock | 15.0 MHz |
| Technology | CMOS |
| Transistors | ~75,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 2.5 |
| Predicted CPI | 2.499 |
| Error | 0.04% |
| Status | **PASSED** |

## Files

- `current/t212_validated.py` - Active grey-box queueing model
- `validation/t212_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/t212/current')
from t212_validated import T212Model

model = T212Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
