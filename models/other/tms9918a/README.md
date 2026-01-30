# TI TMS9918A VDP

**Video Display Processor for TI-99/4A, MSX, ColecoVision, SG-1000**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Texas Instruments |
| Year | 1979 |
| Data Width | 8-bit |
| Clock | 10.7 MHz |
| Technology | NMOS |
| Transistors | ~20,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.5 |
| Predicted CPI | 4.500 |
| Error | 0.0% |
| Status | **PASSED** |

## Files

- `current/tms9918a_validated.py` - Active grey-box queueing model
- `validation/tms9918a_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/tms9918a/current')
from tms9918a_validated import Tms9918aModel

model = Tms9918aModel()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
