# Intel 8231

**Arithmetic Processing Unit, simpler than 8087**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intel |
| Year | 1977 |
| Data Width | 8-bit |
| Clock | 2.0 MHz |
| Technology | NMOS |
| Transistors | ~8,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 40.0 |
| Predicted CPI | 35.800 |
| Error | 10.50% |
| Status | **MARGINAL** |

## Files

- `current/i8231_validated.py` - Active grey-box queueing model
- `validation/i8231_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/intel/i8231/current')
from i8231_validated import I8231Model

model = I8231Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
