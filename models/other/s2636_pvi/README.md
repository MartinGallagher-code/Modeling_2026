# Signetics 2636 PVI

**Programmable Video Interface for Arcadia 2001 / VC4000**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Signetics |
| Year | 1977 |
| Data Width | 8-bit |
| Clock | 3.58 MHz |
| Technology | NMOS |
| Transistors | ~5,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.0 |
| Predicted CPI | 5.250 |
| Error | 5.00% |
| Status | **MARGINAL** |

## Files

- `current/s2636_pvi_validated.py` - Active grey-box queueing model
- `validation/s2636_pvi_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/s2636_pvi/current')
from s2636_pvi_validated import S2636PviModel

model = S2636PviModel()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
