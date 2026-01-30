# Inmos T800

**32-bit transputer with on-chip FPU, IEEE 754**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Inmos |
| Year | 1987 |
| Data Width | 32-bit |
| Clock | 20.0 MHz |
| Technology | CMOS |
| Transistors | ~250,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 2.0 |
| Predicted CPI | 2.600 |
| Error | 30.00% |
| Status | **MARGINAL** |

## Files

- `current/t800_validated.py` - Active grey-box queueing model
- `validation/t800_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/t800/current')
from t800_validated import T800Model

model = T800Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
