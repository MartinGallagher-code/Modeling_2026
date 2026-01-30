# Yamaha V9938

**MSX2 Video Display Processor with hardware blitter**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Yamaha |
| Year | 1985 |
| Data Width | 8-bit |
| Clock | 21.5 MHz |
| Technology | NMOS |
| Transistors | ~60,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.000 |
| Error | 0.0% |
| Status | **PASSED** |

## Files

- `current/v9938_validated.py` - Active grey-box queueing model
- `validation/v9938_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/v9938/current')
from v9938_validated import V9938Model

model = V9938Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
