# ICL DAP

**4096-element SIMD array processor, early massively parallel**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | ICL |
| Year | 1980 |
| Data Width | 1-bit |
| Clock | 5.0 MHz |
| Technology | TTL/MSI |
| Transistors | N/A (board-level) |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 10.0 |
| Predicted CPI | 7.750 |
| Error | 22.50% |
| Status | **MARGINAL** |

## Files

- `current/icl_dap_validated.py` - Active grey-box queueing model
- `validation/icl_dap_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/icl_dap/current')
from icl_dap_validated import IclDapModel

model = IclDapModel()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
