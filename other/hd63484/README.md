# Hitachi HD63484 ACRTC

**Advanced CRT Controller / Graphics Processor (1984)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1984 |
| Data Width | 16-bit internal |
| Clock | 8 MHz |
| CPI | ~10.0 (graphics commands) |
| Performance | ~800 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 1.3% |
| Tests Passing | 8/8 |

## Model Files

- `current/hd63484_validated.py` - Active model
- `validation/hd63484_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from hd63484_validated import Hd63484Model

model = Hd63484Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The HD63484 ACRTC is a dedicated graphics processor with hardware-accelerated
drawing commands. Graphics operations (line, circle, arc, fill, BitBLT) are
inherently multi-cycle. BitBLT is the most expensive operation at 12 base
cycles. Used in the Sharp X68000 and various arcade machines.
