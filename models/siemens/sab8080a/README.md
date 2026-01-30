# Siemens SAB8080A

**West German second-source of Intel 8080, pin-compatible clone**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Siemens |
| Year | 1976 |
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

- `current/sab8080a_validated.py` - Active grey-box queueing model
- `validation/sab8080a_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/sab8080a/current')
from sab8080a_validated import Sab8080aModel

model = Sab8080aModel()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
