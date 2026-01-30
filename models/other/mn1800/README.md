# Matsushita MN1800

**Panasonic 8-bit MCU for consumer electronics**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Matsushita (Panasonic) |
| Year | 1980 |
| Data Width | 8-bit |
| Clock | 2.0 MHz |
| Technology | NMOS |
| Transistors | ~10,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.0 |
| Predicted CPI | 5.500 |
| Error | 10.00% |
| Status | **MARGINAL** |

## Files

- `current/mn1800_validated.py` - Active grey-box queueing model
- `validation/mn1800_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/mn1800/current')
from mn1800_validated import Mn1800Model

model = Mn1800Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
