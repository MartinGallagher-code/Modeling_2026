# TI SN76489

**Square wave PSG - 3 tone channels, noise generator, simple register interface**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Texas Instruments |
| Year | 1980 |
| Data Width | 8-bit |
| Clock | 4.0 MHz |
| Technology | NMOS |
| Transistors | ~4,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 2.5 |
| Predicted CPI | 2.500 |
| Error | 0.00% |
| Status | **PASSED** |

## Files

- `current/sn76489_validated.py` - Active grey-box queueing model
- `validation/sn76489_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/sn76489/current')
from sn76489_validated import Sn76489Model

model = Sn76489Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
