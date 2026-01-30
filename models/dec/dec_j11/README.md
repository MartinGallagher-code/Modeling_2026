# DEC J-11

**Fastest PDP-11 chip, used in PDP-11/73 and 11/84**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Digital Equipment Corporation |
| Year | 1983 |
| Data Width | 16-bit |
| Clock | 15.0 MHz |
| Technology | CMOS |
| Transistors | ~175,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.026 |
| Error | 0.64% |
| Status | **PASSED** |

## Files

- `current/dec_j11_validated.py` - Active grey-box queueing model
- `validation/dec_j11_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/dec_j11/current')
from dec_j11_validated import DecJ11Model

model = DecJ11Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
