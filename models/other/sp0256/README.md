# GI SP0256

**Allophone speech processor, used in Intellivoice and Type & Talk**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | General Instrument |
| Year | 1981 |
| Data Width | 8-bit |
| Clock | 3.12 MHz |
| Technology | NMOS |
| Transistors | ~10,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 10.0 |
| Predicted CPI | 10.000 |
| Error | 0.00% |
| Status | **PASSED** |

## Files

- `current/sp0256_validated.py` - Active grey-box queueing model
- `validation/sp0256_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/sp0256/current')
from sp0256_validated import Sp0256Model

model = Sp0256Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
