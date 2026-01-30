# Sharp LH0080

**Japanese second-source of Zilog Z80, used in Sharp personal computers**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Sharp |
| Year | 1976 |
| Data Width | 8-bit |
| Clock | 2.5 MHz |
| Technology | NMOS |
| Transistors | ~8,500 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.3 |
| Predicted CPI | 5.300 |
| Error | 0.0% |
| Status | **PASSED** |

## Files

- `current/lh0080_validated.py` - Active grey-box queueing model
- `validation/lh0080_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/lh0080/current')
from lh0080_validated import Lh0080Model

model = Lh0080Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
