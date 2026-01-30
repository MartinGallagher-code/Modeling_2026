# AMD Am29116

## Quick Reference
| Parameter | Value |
|-----------|-------|
| Year | 1983 |
| Type | 16-bit Microprogrammable CPU |
| Clock | 10 MHz |
| Transistors | ~20,000 |
| Process | Bipolar |
| Data Bus | 16-bit |
| Architecture | Microprogrammable |

## Description
The Am29116 is a single-chip 16-bit microprogrammable CPU that combines the
functionality of the Am2901 bit-slice ALU into one device. It features a 16-bit
data path, 16x16-bit register file, and on-chip microinstruction decoder.
Most operations execute in 1 cycle; memory accesses and multiply steps take
2-3 cycles.

## Validation Status
- **Status**: PASSED
- **CPI Error**: 2.4%
- **Model CPI**: 1.536 (target: 1.5)
- **Last Validated**: 2026-01-29

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 1 | ADD, SUB, AND, OR, XOR |
| Register Transfer | 1 | Reg-to-reg moves |
| Shift | 1 | Shift and rotate |
| Memory Read | 3 | External memory read (with wait state) |
| Memory Write | 2 | External memory write |
| Multiply Step | 3 | Shift-and-add multiply step |
| Status Test | 1 | Flag/condition testing |
| I/O Operation | 2 | I/O port access |
