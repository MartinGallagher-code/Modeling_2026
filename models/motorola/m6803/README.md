# Motorola 6803

**Enhanced 6801 with more I/O, widely used in automotive**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Motorola |
| Year | 1981 |
| Data Width | 8-bit |
| Clock | 1.0 MHz |
| Technology | NMOS |
| Transistors | ~9,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.5 |
| Predicted CPI | 4.800 |
| Error | 6.67% |
| Status | **MARGINAL** |

## Files

- `current/m6803_validated.py` - Active grey-box queueing model
- `validation/m6803_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/motorola/m6803/current')
from m6803_validated import M6803Model

model = M6803Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
