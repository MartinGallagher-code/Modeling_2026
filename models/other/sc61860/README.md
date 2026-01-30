# Sharp SC61860

**Custom Sharp pocket computer CPU (1980)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1980 |
| Data Width | 8-bit |
| Clock | 576 kHz |
| Transistors | ~8,000 |
| CPI | 5.0 (typical) |
| Performance | ~115 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 8/8 |

## Model Files

- `current/sc61860_validated.py` - Active model
- `validation/sc61860_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from sc61860_validated import Sc61860Model

model = Sc61860Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

Custom Sharp CMOS CPU designed for pocket computers. 8-bit accumulator-based
architecture with 96 bytes internal RAM and integrated LCD display controller.
Used in the Sharp PC-1211, PC-1245, and PC-1500 pocket computer series
throughout the 1980s. Ran a built-in BASIC interpreter.
