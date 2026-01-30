# TVC CPU

**Hungarian modified Z80 clone (1983)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1983 |
| Data Width | 8-bit |
| Clock | 3.5 MHz |
| CPI | ~5.2 |
| Performance | ~0.673 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 15/15 |

## Model Files

- `current/tvc_cpu_validated.py` - Active model
- `validation/tvc_cpu_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from tvc_cpu_validated import TVCCPUModel

model = TVCCPUModel()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The TVC CPU was a Hungarian modified Z80 clone produced by MEV/Tungsram in 1983.
It powered the Videoton TVC home computer, one of Hungary's most popular 8-bit
home computers. Running at 3.5 MHz (slightly faster than the standard Z80A's
3.5 MHz), it offered Z80-compatible instruction execution with minor
optimizations to block operations.
