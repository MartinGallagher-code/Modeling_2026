# Thomson EFCIS 90435

**French 8-bit for military (Mirage fighter systems)**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Thomson-CSF |
| Year | 1980 |
| Data Width | 8-bit |
| Clock | 4.0 MHz |
| Technology | NMOS |
| Transistors | ~8,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.5 |
| Predicted CPI | 6.000 |
| Error | 9.09% |
| Status | **MARGINAL** |

## Files

- `current/thomson_90435_validated.py` - Active grey-box queueing model
- `validation/thomson_90435_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/thomson_90435/current')
from thomson_90435_validated import Thomson90435Model

model = Thomson90435Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
