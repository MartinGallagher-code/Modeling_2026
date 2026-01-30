# Inmos T424

**32-bit transputer with 4KB on-chip RAM, T414 variant**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Inmos |
| Year | 1985 |
| Data Width | 32-bit |
| Clock | 15.0 MHz |
| Technology | CMOS |
| Transistors | ~150,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 2.0 |
| Predicted CPI | 2.400 |
| Error | 20.00% |
| Status | **MARGINAL** |

## Files

- `current/t424_validated.py` - Active grey-box queueing model
- `validation/t424_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/t424/current')
from t424_validated import T424Model

model = T424Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
