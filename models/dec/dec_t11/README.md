# DEC T-11

**PDP-11 on a chip, used in PDP-11/03 and military systems**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Digital Equipment Corporation |
| Year | 1981 |
| Data Width | 16-bit |
| Clock | 2.5 MHz |
| Technology | NMOS |
| Transistors | ~18,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 6.0 |
| Predicted CPI | 6.008 |
| Error | 0.13% |
| Status | **PASSED** |

## Files

- `current/dec_t11_validated.py` - Active grey-box queueing model
- `validation/dec_t11_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/dec_t11/current')
from dec_t11_validated import DecT11Model

model = DecT11Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
