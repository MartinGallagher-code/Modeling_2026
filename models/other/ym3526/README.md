# Yamaha YM3526 OPL

**2-operator FM synthesis chip - 9 channels with rhythm mode**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Yamaha |
| Year | 1984 |
| Data Width | 8-bit |
| Clock | 3.58 MHz |
| Technology | NMOS |
| Transistors | ~15,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.000 |
| Error | 0.00% |
| Status | **PASSED** |

## Files

- `current/ym3526_validated.py` - Active grey-box queueing model
- `validation/ym3526_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/ym3526/current')
from ym3526_validated import Ym3526Model

model = Ym3526Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
