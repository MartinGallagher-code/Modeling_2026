# Siemens SAB80515

**Enhanced 8051 derivative with on-chip ADC for industrial/automotive use**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Siemens |
| Year | 1983 |
| Data Width | 8-bit |
| Clock | 12.0 MHz |
| Technology | NMOS/CMOS |
| Transistors | ~60,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 2.2 |
| Predicted CPI | 2.200 |
| Error | 0.0% |
| Status | **PASSED** |

## Files

- `current/sab80515_validated.py` - Active grey-box queueing model
- `validation/sab80515_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/sab80515/current')
from sab80515_validated import Sab80515Model

model = Sab80515Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
