# Ensoniq ES5503 DOC

**32-oscillator wavetable synthesis chip with hardware interpolation**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Ensoniq |
| Year | 1985 |
| Data Width | 8-bit |
| Clock | 7.0 MHz |
| Technology | CMOS |
| Transistors | ~40,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.5 |
| Predicted CPI | 5.501 |
| Error | 0.02% |
| Status | **PASSED** |

## Files

- `current/es5503_validated.py` - Active grey-box queueing model
- `validation/es5503_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/es5503/current')
from es5503_validated import Es5503Model

model = Es5503Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
