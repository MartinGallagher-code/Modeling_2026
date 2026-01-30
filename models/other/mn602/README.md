# Data General mN602

**Enhanced microNova, Data General minicomputer lineage**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Data General |
| Year | 1982 |
| Data Width | 16-bit |
| Clock | 4.0 MHz |
| Technology | NMOS |
| Transistors | ~15,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.0 |
| Predicted CPI | 4.997 |
| Error | 0.05% |
| Status | **PASSED** |

## Files

- `current/mn602_validated.py` - Active grey-box queueing model
- `validation/mn602_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/mn602/current')
from mn602_validated import Mn602Model

model = Mn602Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
