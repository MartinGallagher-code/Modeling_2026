# Siemens SAB80C166

**16-bit automotive microcontroller with 4-stage pipeline**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Siemens |
| Year | 1985 |
| Data Width | 16-bit |
| Clock | 16.0 MHz |
| Technology | CMOS |
| Transistors | ~80,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 1.8 |
| Predicted CPI | 1.800 |
| Error | 0.0% |
| Status | **PASSED** |

## Files

- `current/sab80c166_validated.py` - Active grey-box queueing model
- `validation/sab80c166_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/sab80c166/current')
from sab80c166_validated import Sab80c166Model

model = Sab80c166Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
