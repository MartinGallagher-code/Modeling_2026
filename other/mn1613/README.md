# Panafacom MN1613

**Improved MN1610 16-bit processor (1982)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1982 |
| Data Width | 16-bit |
| Clock | 4 MHz |
| CPI | ~4.5 cycles |
| Performance | ~889 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 2.22% |
| Tests Passing | 7/7 |

## Model Files

- `current/mn1613_validated.py` - Active model
- `validation/mn1613_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from mn1613_validated import Mn1613Model

model = Mn1613Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi} cycles, IPS: {result.ips:,.0f}")
```

## Notes

The MN1613 was Panafacom's improved successor to the MN1610, one of Japan's
first 16-bit microprocessors. It featured a 4 MHz clock (double the MN1610),
hardware multiply, and improved execution efficiency. CPI dropped from 8.0
to 4.5, providing roughly 3.5x the throughput of the MN1610.

## Comparison with MN1610

| Feature | MN1610 | MN1613 |
|---------|--------|--------|
| Clock | 2 MHz | 4 MHz |
| CPI | 8.0 | 4.5 |
| Multiply | Software | Hardware |
| Performance | ~250 KIPS | ~889 KIPS |
