# Weitek 1064/1065

**High-speed FPU pair for workstations and Cray**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Weitek |
| Year | 1985 |
| Data Width | 32-bit |
| Clock | 15.0 MHz |
| Technology | ECL/CMOS |
| Transistors | ~40,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 3.0 |
| Predicted CPI | 3.250 |
| Error | 8.33% |
| Status | **MARGINAL** |

## Files

- `current/weitek1064_validated.py` - Active grey-box queueing model
- `validation/weitek1064_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/weitek1064/current')
from weitek1064_validated import Weitek1064Model

model = Weitek1064Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
