# Williams SC1

**Blitter/DMA for Williams arcade games (Defender, Robotron)**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Williams Electronics |
| Year | 1981 |
| Data Width | 8-bit |
| Clock | 1.0 MHz |
| Technology | TTL |
| Transistors | ~3,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 8.0 |
| Predicted CPI | 8.000 |
| Error | 0.00% |
| Status | **PASSED** |

## Files

- `current/williams_sc1_validated.py` - Active grey-box queueing model
- `validation/williams_sc1_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/williams_sc1/current')
from williams_sc1_validated import WilliamsSc1Model

model = WilliamsSc1Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
