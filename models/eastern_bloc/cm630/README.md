# CM630

**Bulgarian CMOS 6502 clone - used in Pravetz Apple II clones (1984)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1984 |
| Data Width | 8-bit |
| Clock | 1.0 MHz |
| CPI | ~2.85 |
| Performance | ~0.35 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 14/14 |

## Model Files

- `current/cm630_validated.py` - Active model
- `validation/cm630_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from cm630_validated import CM630Model

model = CM630Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The CM630 is a Bulgarian CMOS clone of the WDC 65C02 processor. It was used
in the Pravetz series of Apple II compatible computers, including the Pravetz
82 and Pravetz 8M. These computers were widely used in Bulgarian schools and
offices during the 1980s. The CMOS design provides lower power consumption
than the original NMOS MOS 6502 while maintaining full compatibility with
the enhanced 65C02 instruction set.
