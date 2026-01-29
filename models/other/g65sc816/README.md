# GTE G65SC816

**WDC 65C816 second-source, full 16-bit mode (1985)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1985 |
| Data Width | 8/16-bit |
| Clock | 4 MHz |
| CPI | ~3.8 cycles |
| Performance | ~1.05 MIPS |
| Address Space | 16 MB (24-bit) |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 1.32% |
| Tests Passing | 7/7 |

## Model Files

- `current/g65sc816_validated.py` - Active model
- `validation/g65sc816_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from g65sc816_validated import G65sc816Model

model = G65sc816Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi} cycles, IPS: {result.ips:,.0f}")
```

## Notes

The G65SC816 was GTE Microcircuits' second-source of the WDC 65C816 with
the full 65816 pinout. It provided 24-bit addressing (16MB) through
address/data bus multiplexing. Used in the Apple IIGS and other systems
requiring more than 64KB of address space with 6502-family compatibility.
The full native mode supported 16-bit accumulator and index registers.
