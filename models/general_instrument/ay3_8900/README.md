# GI AY-3-8900 STIC

**Intellivision STIC graphics, programmable sprite processor**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | General Instrument |
| Year | 1978 |
| Data Width | 16-bit |
| Clock | 3.58 MHz |
| Technology | NMOS |
| Transistors | ~8,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 6.0 |
| Predicted CPI | 6.250 |
| Error | 4.17% |
| Status | **PASSED** |

## Files

- `current/ay3_8900_validated.py` - Active grey-box queueing model
- `validation/ay3_8900_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/ay3_8900/current')
from ay3_8900_validated import Ay38900Model

model = Ay38900Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
