# Commodore VIC-II (6567)

**Commodore 64 Video Interface Controller**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | MOS Technology/Commodore |
| Year | 1982 |
| Data Width | 12-bit |
| Clock | 8 MHz |
| Technology | NMOS |
| Transistors | ~16,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.000 |
| Error | 0.0% |
| Status | **PASSED** |

## Files

- `current/vic_ii_validated.py` - Active grey-box queueing model
- `validation/vic_ii_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/vic_ii/current')
from vic_ii_validated import VicIiModel

model = VicIiModel()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
