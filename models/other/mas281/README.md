# Marconi Elliot MAS281

**British military 16-bit for naval systems**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Marconi |
| Year | 1979 |
| Data Width | 16-bit |
| Clock | 5.0 MHz |
| Technology | NMOS |
| Transistors | ~12,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.5 |
| Predicted CPI | 4.700 |
| Error | 4.44% |
| Status | **PASSED** |

## Files

- `current/mas281_validated.py` - Active grey-box queueing model
- `validation/mas281_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/mas281/current')
from mas281_validated import Mas281Model

model = Mas281Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
