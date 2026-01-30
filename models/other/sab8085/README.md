# Siemens SAB8085

**West German second-source of Intel 8085, pin-compatible clone**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Siemens |
| Year | 1978 |
| Data Width | 8-bit |
| Clock | 3.0 MHz |
| Technology | NMOS |
| Transistors | ~6,500 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.0 |
| Predicted CPI | 5.000 |
| Error | 0.0% |
| Status | **PASSED** |

## Files

- `current/sab8085_validated.py` - Active grey-box queueing model
- `validation/sab8085_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/sab8085/current')
from sab8085_validated import Sab8085Model

model = Sab8085Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
