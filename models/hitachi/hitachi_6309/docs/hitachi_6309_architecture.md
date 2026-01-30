# Hitachi 6309 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s enhanced 8-bit microprocessors
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Enhanced Motorola 6809 with additional registers and instructions
- "The best 8-bit CPU ever made"
- Two operating modes: Native (full 6309 features) and Emulation (6809-compatible)
- Two 8-bit accumulators (A, B) combinable as 16-bit D register
- Additional registers: E, F (combinable as 16-bit W), V, zero register, MD
- Q = D:W forms a 32-bit accumulator
- Two index registers (X, Y), two stack pointers (S, U)
- Hardware 16x16 multiply (MULD) and 32/16 divide (DIVD, DIVQ)
- Block transfer instructions (TFM)
- Bit manipulation instructions (BAND, BOR, BEOR, etc.)
- Inter-register arithmetic (ADDR, SUBR, etc.)
- Position-independent code support
- Runs 6809 code ~10% faster in emulation mode; native mode even faster

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Hitachi |
| Year | 1982 |
| Clock | 2.0 MHz (supports 1-3.5 MHz) |
| Transistors | ~12,000 |
| Data Width | 8-bit |
| Address Width | 16-bit |

## Queueing Model Architecture

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  FETCH  │──►│ DECODE  │──►│ EXECUTE │──►│ MEMORY  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘
    │              │              │              │
    ▼              ▼              ▼              ▼
  M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue

CPI = Fetch + Decode + Execute + Memory (serial sum)
```

## Instruction Categories (Native Mode)

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU (8-bit) | 1.9 | ADDA imm @2, 1 cycle faster than 6809 |
| ALU (16-bit) | 2.8 | ADDD @3, native mode optimized |
| Data Transfer | 2.3 | LDA imm @2, LDD imm @3, LDW imm @4 |
| Memory | 3.3 | LDA dir @3, STA dir @3 (1 cycle faster) |
| Control | 3.0 | JMP @3, BEQ @3, JSR @7, RTS @4 |
| Stack | 4.2 | PSHS/PULS @4+ (faster) |
| Multiply 8x8 | 10.0 | MUL @10 (6809-compatible) |
| Multiply 16x16 | 26.0 | MULD @25-28 (native mode only) |
| Divide | 28.0 | DIVD @25, DIVQ @34 |
| Block Transfer | 9.0 | TFM @6+3n, ~9 avg for small blocks |
| Bit Manipulation | 5.0 | BAND, BOR, BEOR, etc. |

## Instruction Categories (Emulation Mode)

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 2.2 | ~10% faster than 6809 |
| Data Transfer | 2.5 | LDA imm @2, LDD imm @3 |
| Memory | 3.9 | LDA dir @4, ~10% faster than 6809 |
| Control | 3.7 | JMP @4, BEQ @3, JSR @7, RTS @5 |
| Stack | 4.9 | PSHS/PULS @5+, ~10% faster |
| Multiply | 10.0 | MUL @10 (slightly faster than 6809's 11) |

## 6309-Specific Register Set

| Register | Width | Description |
|----------|-------|-------------|
| E | 8-bit | Additional accumulator (native mode) |
| F | 8-bit | Additional accumulator (native mode) |
| W | 16-bit | Combined E:F (native mode) |
| Q | 32-bit | Combined D:W (native mode) |
| V | 16-bit | General register (native mode) |
| 0 | 16-bit | Zero register, always reads 0 (native mode) |
| MD | 8-bit | Mode/error register (native mode) |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The model supports both native and emulation modes with separate timing tables
   - Native mode target CPI is ~3.0 (15% faster than 6809's ~3.5)
   - Emulation mode target CPI is ~3.15 (~10% faster than 6809)
   - Expensive operations (MULD @26, DIVQ @28) are rare in typical code (<1% weight)
   - The 32-bit Q accumulator enables efficient 32-bit arithmetic on an 8-bit bus
   - Block transfer (TFM) is highly efficient for memory copy operations
   - The zero register eliminates the need for explicit zero-loading instructions

## Validation Approach

- Compare against community-measured 6309 cycle counts
- Validate speedup over Motorola 6809 (>= 1.10x in native mode)
- Cross-reference with Tandy Color Computer 3 benchmark data
- Verify native mode instruction categories exist (multiply_16x16, divide, block_transfer)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/hitachi/6309)
- [Wikipedia - Hitachi 6309](https://en.wikipedia.org/wiki/Hitachi_6309)

---
Generated: 2026-01-29
