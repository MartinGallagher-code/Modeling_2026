# MOS 6581 SID

**C64 Sound Interface Device - 3-voice analog synthesis with programmable filter**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | MOS Technology |
| Year | 1982 |
| Data Width | 8-bit |
| Clock | 1.0 MHz |
| Technology | NMOS |
| Transistors | ~11,500 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.0 |
| Predicted CPI | 5.000 |
| Error | 0.00% |
| Status | **PASSED** |

## Files

- `current/mos6581_sid_validated.py` - Active grey-box queueing model
- `validation/mos6581_sid_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/mos6581_sid/current')
from mos6581_sid_validated import Mos6581SidModel

model = Mos6581SidModel()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
