# GTE G65SC802

**WDC 65C816 second-source, 6502 pin-compatible (1985)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1985 |
| Data Width | 8/16-bit |
| Clock | 4 MHz |
| CPI | ~3.5 cycles |
| Performance | ~1.14 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 2.86% |
| Tests Passing | 7/7 |

## Model Files

- `current/g65sc802_validated.py` - Active model
- `validation/g65sc802_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from g65sc802_validated import G65sc802Model

model = G65sc802Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi} cycles, IPS: {result.ips:,.0f}")
```

## Notes

The G65SC802 was GTE Microcircuits' second-source of the WDC 65C816, packaged
in a 6502-compatible 40-pin DIP. It could run 65816 native mode code with
16-bit registers but only had a 16-bit external address bus (24-bit addressing
via bank register multiplexing on the data bus). CMOS technology enabled 4 MHz
operation.

## Comparison with G65SC816

| Feature | G65SC802 | G65SC816 |
|---------|----------|----------|
| Package | 40-pin DIP (6502 compat) | 40-pin DIP (new pinout) |
| Address Bus | 16-bit external | 24-bit (via multiplexing) |
| CPI | 3.5 | 3.8 |
