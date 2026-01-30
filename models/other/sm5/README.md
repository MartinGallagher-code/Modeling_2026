# Sharp SM5

**Enhanced SM4, massively produced for LCD games**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Sharp |
| Year | 1984 |
| Data Width | 4-bit |
| Clock | 0.5 MHz |
| Technology | CMOS |
| Transistors | ~5,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.200 |
| Error | 5.00% |
| Status | **MARGINAL** |

## Files

- `current/sm5_validated.py` - Active grey-box queueing model
- `validation/sm5_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/sm5/current')
from sm5_validated import Sm5Model

model = Sm5Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
