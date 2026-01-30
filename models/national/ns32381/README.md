# National NS32381

## Quick Reference
| Parameter | Value |
|-----------|-------|
| Year | 1985 |
| Type | Floating-Point Coprocessor |
| Clock | 15 MHz |
| Transistors | ~60,000 |
| Data Width | 32-bit |
| Architecture | NS32000 FPU (slave processor) |
| Predecessor | NS32081 |

## Description
The National NS32381 is a higher-performance floating-point coprocessor for the
NS32000 family, succeeding the NS32081. It operates as a slave processor
communicating with the NS32032 or NS32332 CPU via the slave bus protocol.
It features pipelined FP execution with operations ranging from 4 cycles
(compare) to 35 cycles (square root).

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.5%
- **Model CPI**: 8.042 (target: 8.0)
- **Last Validated**: 2026-01-29

## Instruction Categories
| Category | Base Cycles | Memory Cycles | Total | Description |
|----------|-------------|---------------|-------|-------------|
| FP Add | 5.0 | 1.5 | 6.5 | Add/subtract |
| FP Multiply | 7.0 | 1.5 | 8.5 | Multiply |
| FP Divide | 25.0 | 1.5 | 26.5 | Divide |
| FP Sqrt | 35.0 | 1.5 | 36.5 | Square root |
| FP Compare | 4.0 | 1.5 | 5.5 | Compare |
| Data Transfer | 2.0 | 2.0 | 4.0 | FP load/store |
| Format Convert | 4.0 | 1.5 | 5.5 | Format conversion |
