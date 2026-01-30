# Sega 315-5124 VDP

**Sega Master System Video Display Processor**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Sega |
| Year | 1985 |
| Data Width | 8-bit |
| Clock | 10.7 MHz |
| Technology | NMOS |
| Transistors | ~25,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 3.8 |
| Predicted CPI | 3.800 |
| Error | 0.0% |
| Status | **PASSED** |

## Files

- `current/sega_315_5124_validated.py` - Active grey-box queueing model
- `validation/sega_315_5124_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/sega_315_5124/current')
from sega_315_5124_validated import Sega3155124Model

model = Sega3155124Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
