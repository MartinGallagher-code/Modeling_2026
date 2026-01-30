# NEC uPD8080AF

**NEC second-source of Intel 8080, early Japanese 8080 clone**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1975 |
| Data Width | 8-bit |
| Clock | 2.0 MHz |
| Technology | NMOS |
| Transistors | ~6,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.5 |
| Predicted CPI | 5.500 |
| Error | 0.0% |
| Status | **PASSED** |

## Files

- `current/upd8080af_validated.py` - Active grey-box queueing model
- `validation/upd8080af_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/upd8080af/current')
from upd8080af_validated import Upd8080afModel

model = Upd8080afModel()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
