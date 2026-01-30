# Hitachi HMCS40

**4-bit MCU behind the iconic HD44780 LCD controller**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Hitachi |
| Year | 1980 |
| Data Width | 4-bit |
| Clock | 0.4 MHz |
| Technology | CMOS |
| Transistors | ~5,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.5 |
| Predicted CPI | 4.700 |
| Error | 4.44% |
| Status | **PASSED** |

## Files

- `current/hmcs40_validated.py` - Active grey-box queueing model
- `validation/hmcs40_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/hitachi/hmcs40/current')
from hmcs40_validated import Hmcs40Model

model = Hmcs40Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
