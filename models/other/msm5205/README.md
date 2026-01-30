# OKI MSM5205

**ADPCM speech synthesis, used in hundreds of arcade games**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | OKI Semiconductor |
| Year | 1983 |
| Data Width | 4-bit |
| Clock | 0.384 MHz |
| Technology | NMOS |
| Transistors | ~3,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.000 |
| Error | 0.00% |
| Status | **PASSED** |

## Files

- `current/msm5205_validated.py` - Active grey-box queueing model
- `validation/msm5205_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/msm5205/current')
from msm5205_validated import Msm5205Model

model = Msm5205Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
