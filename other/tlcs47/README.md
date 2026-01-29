# Toshiba TLCS-47

**4-bit Microcontroller for Consumer Electronics (1982)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1982 |
| Data Width | 4-bit |
| Clock | 500 kHz |
| CPI | ~6.0 |
| Performance | ~83 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.83% |
| Tests Passing | 8/8 |

## Model Files

- `current/tlcs47_validated.py` - Active model
- `validation/tlcs47_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from tlcs47_validated import Tlcs47Model

model = Tlcs47Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The TLCS-47 was Toshiba's 4-bit MCU family designed for high-volume
consumer electronics. Similar in class to the TI TMS1000, it features
on-chip ROM, RAM, timer, and I/O. Used extensively in calculators, toys,
remote controls, and household appliances.
