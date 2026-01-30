# Atari POKEY

**Audio/I/O controller with 4 channels, serial I/O, random number**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Atari |
| Year | 1979 |
| Data Width | 8-bit |
| Clock | 1.79 MHz |
| Technology | NMOS |
| Transistors | ~5,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 3.0 |
| Predicted CPI | 3.125 |
| Error | 4.17% |
| Status | **PASSED** |

## Files

- `current/pokey_validated.py` - Active grey-box queueing model
- `validation/pokey_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/pokey/current')
from pokey_validated import PokeyModel

model = PokeyModel()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
