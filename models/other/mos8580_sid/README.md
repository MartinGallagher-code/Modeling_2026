# MOS 8580 SID

**Revised C64/C128 Sound Interface Device with improved filter and lower voltage**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | MOS Technology |
| Year | 1986 |
| Data Width | 8-bit |
| Clock | 1.0 MHz |
| Technology | HMOS-II |
| Transistors | ~13,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.2 |
| Predicted CPI | 4.200 |
| Error | 0.00% |
| Status | **PASSED** |

## Files

- `current/mos8580_sid_validated.py` - Active grey-box queueing model
- `validation/mos8580_sid_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/mos8580_sid/current')
from mos8580_sid_validated import Mos8580SidModel

model = Mos8580SidModel()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
