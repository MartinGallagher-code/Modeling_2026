# MOS 8502

**Commodore C128 CPU, 2MHz 6502 variant**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | MOS Technology |
| Year | 1985 |
| Data Width | 8-bit |
| Clock | 2.0 MHz |
| Technology | HMOS |
| Transistors | ~7,500 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 3.8 |
| Predicted CPI | 3.900 |
| Error | 2.63% |
| Status | **PASSED** |

## Files

- `current/mos8502_validated.py` - Active grey-box queueing model
- `validation/mos8502_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/mos_wdc/mos8502/current')
from mos8502_validated import Mos8502Model

model = Mos8502Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
