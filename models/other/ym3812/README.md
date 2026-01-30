# Yamaha YM3812 OPL2

**Enhanced 2-operator FM synthesis - 4 waveforms, used in AdLib/Sound Blaster**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Yamaha |
| Year | 1985 |
| Data Width | 8-bit |
| Clock | 3.58 MHz |
| Technology | NMOS |
| Transistors | ~18,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.000 |
| Error | 0.00% |
| Status | **PASSED** |

## Files

- `current/ym3812_validated.py` - Active grey-box queueing model
- `validation/ym3812_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/ym3812/current')
from ym3812_validated import Ym3812Model

model = Ym3812Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
