# Toshiba TLCS-870

**8-bit Proprietary Microcontroller (1985)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1985 |
| Data Width | 8-bit |
| Clock | 8 MHz |
| CPI | ~4.5 |
| Performance | ~1.78 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 1.33% |
| Tests Passing | 8/8 |

## Model Files

- `current/tlcs870_validated.py` - Active model
- `validation/tlcs870_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from tlcs870_validated import Tlcs870Model

model = Tlcs870Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The TLCS-870 was Toshiba's proprietary 8-bit MCU with a unique instruction
set (not Z80 or 6502 compatible). Features efficient bit manipulation
instructions, making it well-suited for embedded I/O control applications.
On-chip ROM, RAM, timer, UART, and I/O peripherals.
