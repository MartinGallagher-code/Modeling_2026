# Yamaha YM2151 OPM

**4-operator FM synthesis chip - 8 channels, stereo output, hardware LFO**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Yamaha |
| Year | 1983 |
| Data Width | 8-bit |
| Clock | 3.58 MHz |
| Technology | NMOS |
| Transistors | ~20,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.5 |
| Predicted CPI | 4.500 |
| Error | 0.00% |
| Status | **PASSED** |

## Files

- `current/ym2151_validated.py` - Active grey-box queueing model
- `validation/ym2151_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/ym2151/current')
from ym2151_validated import Ym2151Model

model = Ym2151Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
