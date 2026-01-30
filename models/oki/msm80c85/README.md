# OKI MSM80C85

**CMOS 8085 second-source, notable for low-power portable use**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | OKI Semiconductor |
| Year | 1983 |
| Data Width | 8-bit |
| Clock | 5.0 MHz |
| Technology | CMOS |
| Transistors | ~6,500 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.5 |
| Predicted CPI | 6.400 |
| Error | 16.36% |
| Status | **MARGINAL** |

## Files

- `current/msm80c85_validated.py` - Active grey-box queueing model
- `validation/msm80c85_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/msm80c85/current')
from msm80c85_validated import Msm80c85Model

model = Msm80c85Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
