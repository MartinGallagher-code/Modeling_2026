# Sanyo LC87

**8-bit Microcontroller (1983)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1983 |
| Data Width | 8-bit |
| Clock | 4 MHz |
| CPI | ~5.0 |
| Performance | ~800 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 1.6% |
| Tests Passing | 8/8 |

## Model Files

- `current/lc87_validated.py` - Active model
- `validation/lc87_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from lc87_validated import Lc87Model

model = Lc87Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The Sanyo LC87 was an 8-bit MCU family used primarily in consumer
electronics, particularly audio equipment and home appliances. Simple
instruction set with on-chip ROM, RAM, and I/O. Sequential execution
with no pipeline.
