# Intel 4004 Validation Data Compilation

## Executive Summary

This document compiles validation data for the Intel 4004 processor from multiple authoritative sources including the original MCS-4 datasheet, instruction set documentation, and performance measurements.

---

## 1. Basic Specifications (from Datasheets)

| Parameter | Value | Source |
|-----------|-------|--------|
| Release Date | November 15, 1971 | Intel |
| Data Width | 4-bit | Datasheet |
| Clock Frequency | 740 kHz (max) | Datasheet |
| Process | 10 µm PMOS | Datasheet |
| Transistors | 2,300 | Datasheet |
| Package | 16-pin DIP | Datasheet |
| Power | 0.5 W | Datasheet |
| Price | $60 (1971) | Intel |

---

## 2. Timing Specifications (from Datasheet)

### Clock and Cycle Timing
| Parameter | Value | Notes |
|-----------|-------|-------|
| Clock frequency | 740 kHz max | Some docs say 0.75 MHz |
| Clock period | 1.35 µs min | At 740 kHz |
| Clock cycles per machine cycle | 8 | Fixed |
| Machine cycle time | 10.8 µs min | 8 × 1.35 µs |
| 1-word instruction time | 10.8 µs | 1 machine cycle |
| 2-word instruction time | 21.6 µs | 2 machine cycles |

### Instruction Execution Speed
| Metric | Value | Calculation |
|--------|-------|-------------|
| Peak IPS (1-word only) | 92,500 | 1 / 10.8 µs |
| Minimum IPS (2-word only) | 46,250 | 1 / 21.6 µs |
| Typical IPS | 60,000-70,000 | Mixed workload |
| kIPS | 60-92 | Range |

---

## 3. Complete Instruction Set Timing

### One-Word Instructions (10.8 µs = 1 machine cycle)

| Mnemonic | Description | Cycles |
|----------|-------------|--------|
| NOP | No operation | 1 |
| INC | Increment register | 1 |
| ADD | Add register to accumulator | 1 |
| SUB | Subtract register from accumulator | 1 |
| LD | Load register to accumulator | 1 |
| XCH | Exchange register and accumulator | 1 |
| BBL | Branch back and load | 1 |
| LDM | Load immediate to accumulator | 1 |
| WRM | Write RAM main memory | 1 |
| WMP | Write RAM port | 1 |
| WRR | Write ROM port | 1 |
| WR0-WR3 | Write status characters | 1 |
| SBM | Subtract from memory | 1 |
| RDM | Read RAM main memory | 1 |
| RDR | Read ROM port | 1 |
| ADM | Add from memory | 1 |
| RD0-RD3 | Read status characters | 1 |
| CLB | Clear both (ACC and CY) | 1 |
| CLC | Clear carry | 1 |
| IAC | Increment accumulator | 1 |
| CMC | Complement carry | 1 |
| CMA | Complement accumulator | 1 |
| RAL | Rotate left | 1 |
| RAR | Rotate right | 1 |
| TCC | Transfer carry and clear | 1 |
| DAC | Decrement accumulator | 1 |
| TCS | Transfer carry subtract | 1 |
| STC | Set carry | 1 |
| DAA | Decimal adjust accumulator | 1 |
| KBP | Keyboard process | 1 |
| DCL | Designate command line | 1 |
| SRC | Send register control | 1 |
| JIN | Jump indirect | 1 |

### Two-Word Instructions (21.6 µs = 2 machine cycles)

| Mnemonic | Description | Cycles |
|----------|-------------|--------|
| JCN | Jump conditional | 2 |
| FIM | Fetch immediate | 2 |
| FIN | Fetch indirect from ROM | 2 |
| JUN | Jump unconditional | 2 |
| JMS | Jump to subroutine | 2 |
| ISZ | Increment and skip if zero | 2 |

### Instruction Count Summary
| Type | Count | Percentage |
|------|-------|------------|
| 1-word (1 cycle) | 40 | 87% |
| 2-word (2 cycles) | 6 | 13% |
| **Total** | **46** | 100% |

---

## 4. Performance Metrics

### 4.1 Published Performance Data

| Source | IPS Value | Notes |
|--------|-----------|-------|
| Wikipedia | 60,000 | Commonly cited |
| WikiChip | 92,000 | Peak (1-word only) |
| Intel Documentation | 46,250-92,500 | Range |
| ACM Queue CPU DB | 60,000 | Stated value |

### 4.2 Calculated Performance

**At 740 kHz clock:**
- Machine cycle = 8 clocks = 10.8 µs
- Peak IPS = 1/10.8µs = 92,593 IPS
- With 2-word instructions (21.6 µs): 46,296 IPS

**Estimated typical workload (80% 1-word, 20% 2-word):**
- Average cycle time = 0.80 × 10.8 + 0.20 × 21.6 = 12.96 µs
- Typical IPS = 1/12.96µs = 77,160 IPS

**More conservative estimate (70% 1-word, 30% 2-word):**
- Average cycle time = 0.70 × 10.8 + 0.30 × 21.6 = 14.04 µs
- Typical IPS = 1/14.04µs = 71,225 IPS

### 4.3 CPI Analysis

| Scenario | CPI | IPC | Notes |
|----------|-----|-----|-------|
| Peak (1-word only) | 8 | 0.125 | Minimum cycles |
| 2-word only | 16 | 0.0625 | Maximum cycles |
| Typical (80/20 mix) | 10.4 | 0.096 | Estimated |
| Typical (70/30 mix) | 11.2 | 0.089 | More conservative |

**Note:** CPI here is in terms of **clock cycles**, not machine cycles.
- 1 machine cycle = 8 clock cycles
- CPI_clocks = machine_cycles × 8

### 4.4 MIPS Rating

At 740 kHz:
- Peak MIPS: 0.0925 (92.5 kIPS)
- Typical MIPS: 0.060-0.077 (60-77 kIPS)
- Published MIPS: 0.060 (commonly cited)

---

## 5. Architectural Characteristics

### 5.1 Registers
| Register | Size | Count | Description |
|----------|------|-------|-------------|
| Accumulator | 4-bit | 1 | Main working register |
| Index Registers | 4-bit | 16 | General purpose (8 pairs) |
| Stack | 12-bit | 3 | Return addresses (3-level) |
| Program Counter | 12-bit | 1 | Instruction pointer |
| Carry | 1-bit | 1 | Carry/link flag |

### 5.2 Memory
| Type | Capacity | Access |
|------|----------|--------|
| Program ROM | 4 KB (4096 × 8) | 12-bit address |
| Data RAM | 640 × 4 bits | Via SRC instruction |

### 5.3 Pipeline
- No pipeline (single-cycle execution model)
- 8-phase clock within each machine cycle
- Sequential instruction fetch and execute

---

## 6. Benchmark Data

### 6.1 BCD Addition Benchmark (from datasheet)
- Task: Add two 8-digit BCD numbers (32 bits each)
- Time: 850 µs
- Machine cycles: ~79
- Clock ticks: ~632
- Rate: 1,176 8-digit additions per second

### 6.2 Original Calculator Application
- Busicom 141-PF printing calculator
- Full calculator functionality
- Real-time keypad scanning and display

---

## 7. Comparison with Later Processors

| Processor | Year | Clock | IPS | Improvement |
|-----------|------|-------|-----|-------------|
| Intel 4004 | 1971 | 740 kHz | 60,000 | Baseline |
| Intel 4040 | 1974 | 740 kHz | 60,000 | 0× (same) |
| Intel 8008 | 1972 | 500 kHz | 50,000 | ~same |
| Intel 8080 | 1974 | 2 MHz | 290,000 | 4.8× |
| Intel 8085 | 1976 | 3 MHz | 370,000 | 6.2× |
| Zilog Z80 | 1976 | 2.5 MHz | 290,000 | 4.8× |

---

## 8. Validation Case Definitions

### Case 1: Instruction Timing Verification
```
ID: 4004_datasheet_timing
Processor: Intel 4004
Source: MCS-4 Users Manual
Threshold: 0% (exact match required)

Tests:
- 1-word instruction = 8 clock cycles = 10.8 µs
- 2-word instruction = 16 clock cycles = 21.6 µs
- NOP = 1 machine cycle
- JUN = 2 machine cycles
- JMS = 2 machine cycles
```

### Case 2: Peak Performance
```
ID: 4004_peak_performance
Processor: Intel 4004
Source: Datasheet calculations
Threshold: 5%

Expected:
- Peak IPS: 92,500
- Peak MIPS: 0.0925
```

### Case 3: Typical Performance
```
ID: 4004_typical_performance  
Processor: Intel 4004
Source: Multiple (Wikipedia, WikiChip)
Threshold: 15%

Expected:
- Typical IPS: 60,000-77,000
- Typical MIPS: 0.060-0.077
```

### Case 4: BCD Addition Benchmark
```
ID: 4004_bcd_benchmark
Processor: Intel 4004
Source: Intel datasheet
Threshold: 10%

Expected:
- 8-digit BCD addition: 850 µs
- Rate: ~1,176 additions/second
```

---

## 9. Summary of Key Validation Metrics

| Metric | Value | Confidence | Source |
|--------|-------|------------|--------|
| Clock frequency | 740 kHz | High | Datasheet |
| Machine cycle | 10.8 µs | High | Datasheet |
| 1-word cycles | 8 clocks | High | Datasheet |
| 2-word cycles | 16 clocks | High | Datasheet |
| Typical IPS | 60,000-77,000 | Medium | Analysis |
| Peak IPS | 92,500 | High | Calculation |
| Typical CPI (clocks) | 10-11 | Medium | Analysis |
| Typical IPC | 0.09-0.10 | Medium | Analysis |

---

## 10. References

1. Intel MCS-4 Micro Computer Set Users Manual, Intel Corporation, 1971
2. Intel 4004 Datasheet, Intel Corporation
3. Wikipedia - Intel 4004: https://en.wikipedia.org/wiki/Intel_4004
4. WikiChip - Intel 4004: https://en.wikichip.org/wiki/intel/mcs-4/4004
5. e4004.szyc.org Instruction Set Reference: http://e4004.szyc.org/iset.html
6. 4004.com - Complete Artwork and Schematics: https://4004.com/
7. CPU DB (Stanford): https://cpudb.stanford.edu
8. ACM Queue - CPU DB Article: https://queue.acm.org/detail.cfm?id=2181798

---

**Document Version:** 1.0  
**Date:** January 25, 2026  
**Purpose:** Validation data for Intel 4004 performance modeling
