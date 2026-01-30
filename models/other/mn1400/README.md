# Matsushita MN1400

**Early Japanese 4-bit MCU, used in Panasonic consumer products**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Matsushita (Panasonic) |
| Year | 1974 |
| Data Width | 4-bit |
| Clock | 0.4 MHz |
| Technology | PMOS |
| Transistors | ~3,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.200 |
| Error | 5.00% |
| Status | **MARGINAL** |

## Files

- `current/mn1400_validated.py` - Active grey-box queueing model
- `validation/mn1400_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/mn1400/current')
from mn1400_validated import Mn1400Model

model = Mn1400Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
