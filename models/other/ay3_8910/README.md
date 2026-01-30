# GI AY-3-8910 PSG

**Programmable Sound Generator - 3 tone channels, noise, envelope, 2 I/O ports**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | General Instrument |
| Year | 1978 |
| Data Width | 8-bit |
| Clock | 1.79 MHz |
| Technology | NMOS |
| Transistors | ~5,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 3.5 |
| Predicted CPI | 3.499 |
| Error | 0.03% |
| Status | **PASSED** |

## Files

- `current/ay3_8910_validated.py` - Active grey-box queueing model
- `validation/ay3_8910_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/ay3_8910/current')
from ay3_8910_validated import Ay38910Model

model = Ay38910Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
