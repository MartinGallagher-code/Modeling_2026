# NEC V20

**Pin-compatible 8088 replacement, 10-20% faster (1984)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1984 |
| Data Width | 16-bit |
| Clock | 5-16 MHz |
| CPI | ~3.4 |
| Performance | ~2.35 MIPS @ 8 MHz |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 4.4% |
| Speedup vs 8088 | ~1.15x |

## Model Files

- `current/nec_v20_validated.py` - Active model
- `validation/nec_v20_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from nec_v20_validated import NecV20Model

model = NecV20Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

Drop-in 8088 replacement with hardware multiply/divide (3-4x faster than
8088's microcode). 50% duty cycle vs 33% on 8088. Includes 80186
instruction set extensions and 8080 emulation mode.
