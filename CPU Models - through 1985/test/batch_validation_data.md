# Process A: Batch Validation Data for Next 6 Processors

## Processors Being Processed (Alphabetically after Intel 4004, MOS 6502)

1. AMD 2901
2. Fairchild F8
3. Intel 4040
4. Intel 8008
5. Intel 80186
6. Intel 80188

---

## 1. AMD 2901 Bit-Slice Processor

### Basic Specifications
| Parameter | Value | Source |
|-----------|-------|--------|
| Release Date | August 1975 | Wikipedia |
| Data Width | 4-bit slice | Datasheet |
| Clock Frequency | 20-40 MHz | Wikipedia |
| Process | Bipolar | Datasheet |
| Package | 40-pin DIP | Datasheet |
| Type | Bit-slice ALU | Datasheet |

### Timing Characteristics
- **Cycle time**: 50-25 ns (at 20-40 MHz)
- **Microinstruction execution**: Single clock cycle per microop
- **Typical system CPI**: 2-5 microinstructions per instruction
- **Performance**: Much faster than contemporary microprocessors (5-10× faster than 8085)

### Performance Metrics
| Configuration | Speed | Notes |
|--------------|-------|-------|
| 4-bit slice | 20-40 MHz | Single chip |
| 8-bit system (2 chips) | 20-40 MHz | Cascaded |
| 16-bit system (4 chips) | 20-40 MHz | Data General Nova 4 |
| 32-bit system (8 chips) | 20-40 MHz | VAX 11/730 |

### Key Facts
- Not a standalone CPU - requires microsequencer (Am2909/2910)
- User-programmable microcode
- 16 × 4-bit register file
- 8 ALU functions, 3 source operand selects

---

## 2. Fairchild F8 (3850)

### Basic Specifications
| Parameter | Value | Source |
|-----------|-------|--------|
| Release Date | 1975 | Wikipedia |
| Data Width | 8-bit | Datasheet |
| Clock Frequency | 1-2 MHz | Datasheet |
| Cycle Time | 2 µs (standard) | Datasheet |
| Transistors | ~6000 | Estimated |
| Process | N-channel NMOS | Datasheet |
| Package | 40-pin DIP | Datasheet |

### Timing Characteristics
- **Short cycle**: 4 φ periods (4 µs at 1 MHz)
- **Long cycle**: 6 φ periods (6 µs at 1 MHz)
- **Cycle time**: 2 µs at 2 MHz (standard F3850)
- **Cycle time**: 1.5 µs (Mostek 3870)

### Instruction Timing (from MAME source code)
| Instruction Type | Cycles (φ periods) |
|-----------------|-------------------|
| Short (cS) | 4 |
| Long (cL) | 6 |

### Performance Metrics
| Metric | Value | Notes |
|--------|-------|-------|
| IPS @ 2 MHz | 250,000-500,000 | Estimated |
| MIPS | 0.25-0.50 | At 2 MHz |
| CPI (short) | 4 | Minimum |
| CPI (long) | 6 | Maximum |
| Typical CPI | 5 | Mixed workload |

### Architecture Notes
- Multi-chip architecture (3850 CPU + 3851 PSU minimum)
- 64-byte on-chip scratchpad RAM
- Two 8-bit I/O ports
- 70+ instructions
- Used in Fairchild Channel F game console

---

## 3. Intel 4040

### Basic Specifications
| Parameter | Value | Source |
|-----------|-------|--------|
| Release Date | 1974 | Wikipedia |
| Data Width | 4-bit | Datasheet |
| Clock Frequency | 500-740 kHz | Wikipedia |
| Transistors | 3,000 | Wikipedia |
| Process | 10 µm PMOS | Datasheet |
| Package | 24-pin DIP | Datasheet |

### Timing Characteristics
- **Machine cycle**: 8 clock cycles = 10.8 µs (at 740 kHz)
- **Same as 4004** for instruction timing
- **1-word instruction**: 10.8 µs (1 machine cycle)
- **2-word instruction**: 21.6 µs (2 machine cycles)

### Instruction Set Enhancements over 4004
| Feature | 4004 | 4040 |
|---------|------|------|
| Total instructions | 46 | 60 |
| Index registers | 16 | 24 (8 in bank 1) |
| Stack depth | 3 | 7 |
| Interrupts | No | Yes |
| New instructions | - | 14 new |

### New Instructions (14 additional)
- HLT (Halt)
- BBS (Branch Back from interrupt, restore registers)
- LCR (Load command register)
- OR4, OR5 (OR register 4, 5 with accumulator)
- AN4, AN5 (AND register 4, 5 with accumulator)
- DB0, DB1 (Designate ROM bank)
- EI, DI (Enable/Disable interrupts)
- RPM (Read program memory)
- PKI (Pop first 4 bits into index register)

### Performance Metrics
| Metric | Value | Notes |
|--------|-------|-------|
| Peak IPS | 92,500 | Same as 4004 |
| Typical IPS | 60,000-77,000 | Same as 4004 |
| kIPS | 60-92 | Range |
| MIPS | 0.060-0.092 | Range |

---

## 4. Intel 8008

### Basic Specifications
| Parameter | Value | Source |
|-----------|-------|--------|
| Release Date | April 1972 | Wikipedia |
| Data Width | 8-bit | Datasheet |
| Clock Frequency | 500 kHz (8008), 800 kHz (8008-1) | Datasheet |
| Transistors | 3,500 | Wikipedia |
| Address Space | 16 KB (14-bit) | Datasheet |
| Process | 10 µm PMOS | Datasheet |
| Package | 18-pin DIP | Datasheet |

### Timing Characteristics
- **T-state**: 2 clock cycles each (unlike 8080)
- **Instructions**: 5-11 T-states (10-22 clock cycles)
- **Machine cycle**: 5 T-states = 20 µs at 500 kHz

### Instruction Timing
| Type | T-states | Clock Cycles | Time @ 500 kHz |
|------|----------|--------------|----------------|
| Fastest | 5 | 10 | 20 µs |
| Average | 7-8 | 14-16 | 28-32 µs |
| Slowest (JMP/CALL) | 11 | 22 | 44 µs |

### Performance Metrics (CPU-World, corrected)
| Metric | 8008 @ 500 kHz | 8008-1 @ 800 kHz |
|--------|----------------|------------------|
| IPS range | 22,500-50,000 | 36,000-80,000 |
| Typical IPS | 32,000 | 50,000 |
| MIPS | 0.032 | 0.050 |

### Key Facts
- First 8-bit microprocessor
- Architecture designed by CTC (Datapoint 2200)
- Slower than 4004 in raw IPS but faster in real-world due to 8-bit data
- Predecessor to 8080 architecture

---

## 5. Intel 80186

### Basic Specifications
| Parameter | Value | Source |
|-----------|-------|--------|
| Release Date | 1982 | Wikipedia |
| Data Width | 16-bit | Datasheet |
| Clock Frequency | 6-25 MHz | Datasheet |
| Transistors | 55,000 | Estimated |
| Address Space | 1 MB (20-bit) | Datasheet |
| Process | HMOS, later CHMOS | Datasheet |
| Package | 68-pin PLCC/PGA | Datasheet |

### Integrated Features (vs 8086)
- Clock generator
- 2 DMA channels
- Programmable interrupt controller
- 3 programmable 16-bit timers
- Chip select logic
- Wait state generator

### Timing Improvements over 8086
| Instruction Type | 8086 Cycles | 80186 Cycles | Improvement |
|-----------------|-------------|--------------|-------------|
| Register+immediate | 4 | 3 | 25% |
| MUL 16-bit | 118-133 | 26-28 | 4-5× |
| DIV 16-bit | 144-162 | 29 | 5× |
| Multi-bit shifts | 8+4n | 5+n | ~4× |

### Performance Metrics
| Clock | Bus Bandwidth | Estimated MIPS |
|-------|--------------|----------------|
| 6 MHz | 3 MB/sec | 0.75-1.0 |
| 8 MHz | 4 MB/sec | 1.0-1.3 |
| 10 MHz | 5 MB/sec | 1.3-1.7 |

### New Instructions (10)
- ENTER, LEAVE (stack frame)
- PUSHA, POPA (push/pop all)
- BOUND (array bounds check)
- INS, OUTS (string I/O)
- PUSH immediate
- IMUL immediate
- Immediate shifts/rotates

---

## 6. Intel 80188

### Basic Specifications
| Parameter | Value | Source |
|-----------|-------|--------|
| Release Date | 1982 | Wikipedia |
| Data Width | 16-bit internal, 8-bit external | Datasheet |
| Clock Frequency | 6-25 MHz | Datasheet |
| Transistors | 55,000 | Same as 80186 |
| Address Space | 1 MB | Datasheet |
| Package | 68-pin | Datasheet |

### Key Differences from 80186
| Feature | 80186 | 80188 |
|---------|-------|-------|
| External data bus | 16-bit | 8-bit |
| Bus cycles for word | 1 | 2 |
| Typical MIPS | 1.0 @ 8 MHz | 0.6-0.7 @ 8 MHz |
| Cost | Higher | Lower |

### Performance Impact of 8-bit Bus
- Word operations require 2 bus cycles instead of 1
- 30-40% slower than 80186 for memory-intensive code
- Similar performance for register-only operations

### Performance Metrics
| Clock | MIPS (estimated) | Notes |
|-------|-----------------|-------|
| 8 MHz | 0.6-0.7 | ~60-70% of 80186 |
| 10 MHz | 0.75-0.9 | Memory-bound |

---

## Summary Table

| Processor | Year | Bits | Clock | Typical MIPS | Category |
|-----------|------|------|-------|--------------|----------|
| AMD 2901 | 1975 | 4-bit slice | 20-40 MHz | N/A (bit-slice) | BIT_SLICE |
| Fairchild F8 | 1975 | 8-bit | 2 MHz | 0.35 | SIMPLE_8BIT |
| Intel 4040 | 1974 | 4-bit | 740 kHz | 0.074 | SIMPLE_4BIT |
| Intel 8008 | 1972 | 8-bit | 500-800 kHz | 0.032-0.050 | SIMPLE_8BIT |
| Intel 80186 | 1982 | 16-bit | 6-10 MHz | 1.0-1.3 | COMPLEX_16BIT |
| Intel 80188 | 1982 | 16-bit/8-bit | 6-10 MHz | 0.6-0.9 | COMPLEX_16BIT |

---

## Validation Sources Summary

1. **Wikipedia** - General specifications, history
2. **WikiChip** - Technical details, performance
3. **CPU-World** - Instruction timing corrections
4. **MAME Source Code** - Cycle-accurate timing (F8)
5. **Original Datasheets** - Pin-level timing
6. **Bitsavers** - Application notes, user manuals
7. **Grokipedia** - Consolidated technical data
