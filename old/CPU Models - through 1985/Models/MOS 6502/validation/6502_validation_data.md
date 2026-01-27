# MOS 6502 Validation Data Compilation

## Executive Summary

This document compiles validation data for the MOS 6502 processor from multiple authoritative sources including datasheets, cycle-accurate emulators, published benchmarks, and hardware measurements.

---

## 1. Instruction Cycle Timing (from Datasheets)

### Source: MCS6500 Family Hardware Manual (MOS Technology, 1976)
### Cross-referenced: NESdev Wiki, masswerk.at 6502 reference

| Addressing Mode | Typical Cycles | Notes |
|-----------------|----------------|-------|
| Implied | 2 | Minimum instruction time |
| Immediate | 2 | LDA #$nn |
| Zero Page | 3 | LDA $nn |
| Zero Page,X | 4 | LDA $nn,X |
| Zero Page,Y | 4 | LDX $nn,Y |
| Absolute | 4 | LDA $nnnn |
| Absolute,X | 4+ | +1 if page boundary crossed |
| Absolute,Y | 4+ | +1 if page boundary crossed |
| (Indirect,X) | 6 | LDA ($nn,X) |
| (Indirect),Y | 5+ | +1 if page boundary crossed |
| Indirect | 5 | JMP only |

### Complete Instruction Timing Table (Datasheet Reference)

| Instruction | IMP | IMM | ZP | ZP,X | ZP,Y | ABS | ABS,X | ABS,Y | IND | (IND,X) | (IND),Y |
|-------------|-----|-----|----|----- |------|-----|-------|-------|-----|---------|---------|
| ADC | - | 2 | 3 | 4 | - | 4 | 4+ | 4+ | - | 6 | 5+ |
| AND | - | 2 | 3 | 4 | - | 4 | 4+ | 4+ | - | 6 | 5+ |
| ASL | - | - | 5 | 6 | - | 6 | 7 | - | - | - | - |
| BCC/BCS/etc | 2** | - | - | - | - | - | - | - | - | - | - |
| BIT | - | - | 3 | - | - | 4 | - | - | - | - | - |
| BRK | 7 | - | - | - | - | - | - | - | - | - | - |
| CMP | - | 2 | 3 | 4 | - | 4 | 4+ | 4+ | - | 6 | 5+ |
| CPX/CPY | - | 2 | 3 | - | - | 4 | - | - | - | - | - |
| DEC | - | - | 5 | 6 | - | 6 | 7 | - | - | - | - |
| DEX/DEY | 2 | - | - | - | - | - | - | - | - | - | - |
| EOR | - | 2 | 3 | 4 | - | 4 | 4+ | 4+ | - | 6 | 5+ |
| INC | - | - | 5 | 6 | - | 6 | 7 | - | - | - | - |
| INX/INY | 2 | - | - | - | - | - | - | - | - | - | - |
| JMP | - | - | - | - | - | 3 | - | - | 5 | - | - |
| JSR | - | - | - | - | - | 6 | - | - | - | - | - |
| LDA | - | 2 | 3 | 4 | - | 4 | 4+ | 4+ | - | 6 | 5+ |
| LDX | - | 2 | 3 | - | 4 | 4 | - | 4+ | - | - | - |
| LDY | - | 2 | 3 | 4 | - | 4 | 4+ | - | - | - | - |
| LSR | 2 | - | 5 | 6 | - | 6 | 7 | - | - | - | - |
| NOP | 2 | - | - | - | - | - | - | - | - | - | - |
| ORA | - | 2 | 3 | 4 | - | 4 | 4+ | 4+ | - | 6 | 5+ |
| PHA/PHP | 3 | - | - | - | - | - | - | - | - | - | - |
| PLA/PLP | 4 | - | - | - | - | - | - | - | - | - | - |
| ROL/ROR | 2 | - | 5 | 6 | - | 6 | 7 | - | - | - | - |
| RTI | 6 | - | - | - | - | - | - | - | - | - | - |
| RTS | 6 | - | - | - | - | - | - | - | - | - | - |
| SBC | - | 2 | 3 | 4 | - | 4 | 4+ | 4+ | - | 6 | 5+ |
| SEC/CLC/etc | 2 | - | - | - | - | - | - | - | - | - | - |
| STA | - | - | 3 | 4 | - | 4 | 5 | 5 | - | 6 | 6 |
| STX | - | - | 3 | - | 4 | 4 | - | - | - | - | - |
| STY | - | - | 3 | 4 | - | 4 | - | - | - | - | - |
| TAX/TXA/etc | 2 | - | - | - | - | - | - | - | - | - | - |

**Notes:**
- `+` = Add 1 cycle if page boundary crossed
- `**` = Branch: 2 cycles (not taken), 3 cycles (taken, same page), 4 cycles (taken, page cross)

---

## 2. Performance Metrics

### 2.1 MIPS Ratings (Multiple Sources)

| Source | Clock | MIPS | IPC | Notes |
|--------|-------|------|-----|-------|
| Wikipedia IPS | 1 MHz | 0.43 | 0.43 | Generally cited value |
| Low End Mac | 1 MHz | 0.43 | 0.43 | Comparison table |
| HIARCS Chess Forums | 1 MHz | 0.32 | 0.32 | Chess computer analysis |
| Lemon64 Forum | 1 MHz | 0.31 | 0.31 | "Normal code" estimate |
| WDC Datasheet | 1 MHz | 0.50 | 0.50 | Peak (2-cycle instructions only) |
| Apple II Analysis | 1.023 MHz | 0.146-0.51 | 0.14-0.50 | Range based on instruction mix |

### 2.2 Calculated CPI Values

| Workload Type | Estimated CPI | IPC | Source/Method |
|---------------|---------------|-----|---------------|
| Peak (all 2-cycle) | 2.0 | 0.50 | Theoretical minimum |
| Tight loop | 2.5-3.0 | 0.33-0.40 | Emulator measurements |
| Typical code | 3.0-3.5 | 0.29-0.33 | Mixed instruction analysis |
| Memory-heavy | 4.0-5.0 | 0.20-0.25 | Lots of indirect addressing |
| Control-heavy | 3.5-4.0 | 0.25-0.29 | Many branches |

### 2.3 Apple II Specific (1.023 MHz)

From Apple II timing analysis:
- CPU cycles per second: ~1,020,000
- Minimum instructions/second: 145,700 (all 7-cycle instructions)
- Maximum instructions/second: 510,000 (all 2-cycle instructions)
- Typical instructions/second: ~300,000-350,000

---

## 3. Benchmark Results

### 3.1 BYTE Sieve Benchmark (BYTE Magazine, 1981-1983)

| System | CPU | Clock | Time (10 iter) | Language |
|--------|-----|-------|----------------|----------|
| Apple II | 6502 | 1.023 MHz | 2806 sec | Applesoft BASIC |
| Apple II | 6502 | 1.023 MHz | 160 sec | Pascal |
| Apple II | 6502 | 1.023 MHz | 13.9 sec | Assembly (OSI) |
| Apple II | 6502 | 1.023 MHz | 7.4 sec | Optimized assembly |
| Apple II | 6502 | 1.023 MHz | 3.3 sec | Putney optimized |
| Apple II | 6502 | 1.023 MHz | 1.83 sec | Brightwell optimized |

### 3.2 Rugg/Feldman Benchmarks (1977)

- Apple II with Integer BASIC was fastest of all tested systems
- 6502 @ 1 MHz outperformed Z80 @ 4 MHz in many tests
- Confirmed high cycles-per-instruction efficiency

---

## 4. Emulator Validation Sources

### 4.1 VICE Emulator
- Source: VICE-emu.sourceforge.io
- Claim: Cycle-accurate 6502/6510 emulation
- Validation: Wolfgang Lorenz test suite
- All documented and undocumented opcodes emulated
- Used as reference for C64/VIC-20 timing

### 4.2 Visual 6502 (visual6502.org)
- Source: Transistor-level simulation
- Type: Gate-level accurate
- Used to verify: Cycle-by-cycle behavior, undocumented opcodes
- Can compare against for exact timing verification

### 4.3 Klaus Dormann's Test Suite
- Source: github.com/Klaus2m5/6502_65C02_functional_tests
- Tests: All legal opcodes, decimal mode, interrupts
- Used by many emulator developers
- 6502_functional_test takes 77,759,251 cycles to complete

### 4.4 Perfect6502
- C port of Visual 6502 transistor simulation
- Allows cycle-by-cycle state comparison
- Gold standard for cycle accuracy

---

## 5. Architectural Characteristics

### 5.1 Key Timing Behaviors

**Page Boundary Crossing (+1 cycle):**
- Occurs when: Low byte + index overflows into high byte
- Affects: Absolute,X; Absolute,Y; (Indirect),Y (read operations)
- Does NOT affect: Store operations (STA abs,X always 5 cycles)

**Read-Modify-Write Behavior (NMOS only):**
- Double-write: Unmodified value written before modified value
- Affects: ASL, LSR, ROL, ROR, INC, DEC (memory modes)
- Important for hardware that triggers on any write

**Branch Timing:**
- Not taken: 2 cycles
- Taken, same page: 3 cycles
- Taken, page cross: 4 cycles

### 5.2 Memory Access Pattern

Every cycle accesses memory (no "idle" cycles):
- Opcode fetch
- Operand fetch(es)
- Data read/write
- "Dummy" reads for pipeline effect

---

## 6. Validation Case Definitions

### Case 1: Instruction Timing Verification
```
ID: 6502_datasheet_timing
Processor: MOS 6502
Source: MCS6500 Hardware Manual
Threshold: 0% (exact match required)

Tests:
- LDA #$nn = 2 cycles
- LDA $nn = 3 cycles  
- LDA $nnnn = 4 cycles
- LDA $nnnn,X (no cross) = 4 cycles
- LDA $nnnn,X (page cross) = 5 cycles
- JSR $nnnn = 6 cycles
- BRK = 7 cycles
```

### Case 2: Page Crossing Penalty
```
ID: 6502_page_cross
Processor: MOS 6502
Source: Datasheet + emulator verification
Threshold: 0%

Tests:
- LDA $10F0,X with X=$05 = 4 cycles (no cross)
- LDA $10F0,X with X=$20 = 5 cycles (page cross)
```

### Case 3: CPI Benchmark
```
ID: 6502_cpi_typical
Processor: MOS 6502
Source: Multiple (Wikipedia, forum analysis)
Threshold: 15%

Expected CPI: 2.3-3.2 for typical workloads
Expected IPC: 0.31-0.43
Expected MIPS @ 1 MHz: 0.31-0.43
```

### Case 4: Sieve Benchmark
```
ID: 6502_apple2_sieve
Processor: MOS 6502
System: Apple II (1.023 MHz)
Source: BYTE Magazine / Apple Assembly Line
Threshold: 20%

Assembly version: 7.4 seconds (10 iterations)
Optimized: 1.83 seconds (10 iterations)
```

### Case 5: VICE Emulator Verification
```
ID: 6502_vice_cycles
Processor: MOS 6502
Source: VICE emulator test suite
Threshold: 5%

Verification: Run tight loop, count cycles
Expected: Matches datasheet timings exactly
```

---

## 7. Instruction Mix Analysis

### Typical 6502 Code Instruction Distribution

Based on analysis of Apple II and C64 software:

| Instruction Type | Percentage | Avg Cycles |
|------------------|------------|------------|
| Load/Store | 35% | 3.5 |
| Branch | 15% | 2.8 |
| Arithmetic/Logic | 20% | 3.0 |
| Register Transfer | 10% | 2.0 |
| Stack Operations | 5% | 3.5 |
| Compare | 10% | 3.0 |
| Jump/Call | 5% | 5.0 |

**Weighted Average CPI: ~3.1**
**Corresponding IPC: ~0.32**
**MIPS @ 1 MHz: ~0.32**

---

## 8. Summary of Key Validation Metrics

| Metric | Value | Confidence | Source |
|--------|-------|------------|--------|
| Min instruction cycles | 2 | High | Datasheet |
| Max instruction cycles | 7 | High | Datasheet |
| Average CPI (typical) | 3.0-3.2 | Medium | Analysis |
| IPC (typical) | 0.31-0.33 | Medium | Analysis |
| MIPS @ 1 MHz | 0.31-0.43 | Medium | Multiple |
| Sieve benchmark | 7.4s (asm) | High | BYTE Magazine |

---

## 9. References

1. MCS6500 Microcomputer Family Hardware Manual, MOS Technology, 1976
2. W65C02S Datasheet, Western Design Center, 2018
3. NESdev Wiki - 6502 cycle times: https://www.nesdev.org/wiki/6502_cycle_times
4. masswerk.at 6502 Instruction Set: https://www.masswerk.at/6502/6502_instruction_set.html
5. VICE Emulator: https://vice-emu.sourceforge.io/
6. Klaus Dormann's 6502 Test Suite: https://github.com/Klaus2m5/6502_65C02_functional_tests
7. Visual 6502: http://visual6502.org/
8. BYTE Magazine Sieve Benchmark, September 1981
9. Apple Assembly Line, September 1985
10. Wikipedia - Instructions per second: https://en.wikipedia.org/wiki/Instructions_per_second

---

**Document Version:** 1.0  
**Date:** January 25, 2026  
**Purpose:** Validation data for MOS 6502 performance modeling
