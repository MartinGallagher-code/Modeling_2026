# Commodore VIC (6560)

**VIC-20 video chip with programmable character graphics**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Commodore/MOS |
| Year | 1980 |
| Data Width | 8-bit |
| Clock | 1.02 MHz |
| Technology | NMOS |
| Transistors | ~5,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.125 |
| Error | 3.12% |
| Status | **PASSED** |

## Files

- `current/vic_6560_validated.py` - Active grey-box queueing model
- `validation/vic_6560_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/vic_6560/current')
from vic_6560_validated import Vic6560Model

model = Vic6560Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
