# Architectural Guide

## Understanding Microprocessor Design Evolution (1971-1985)

This guide explains the key architectural concepts and how they evolved across the processors in this collection.

---

## Table of Contents

1. [Fundamental Concepts](#fundamental-concepts)
2. [Data Width Evolution](#data-width-evolution)
3. [Memory Addressing](#memory-addressing)
4. [Register Architectures](#register-architectures)
5. [Instruction Set Design](#instruction-set-design)
6. [Pipeline Evolution](#pipeline-evolution)
7. [Memory Hierarchy](#memory-hierarchy)
8. [Peripheral Integration](#peripheral-integration)

---

## Fundamental Concepts

### What is a Microprocessor?

A microprocessor is a complete CPU on a single integrated circuit. Before the Intel 4004 (1971), CPUs required multiple chips or entire boards.

```
Before 4004 (1960s):                After 4004 (1971+):
┌─────────────────────────┐         ┌─────────────────────────┐
│  ALU Board              │         │                         │
├─────────────────────────┤         │    Single Chip CPU      │
│  Register Board         │         │    (Microprocessor)     │
├─────────────────────────┤         │                         │
│  Control Logic Board    │         │    4004: 2,300          │
├─────────────────────────┤         │    transistors          │
│  Timing Board           │         │                         │
└─────────────────────────┘         └─────────────────────────┘
    Hundreds of chips                    ONE chip
```

### CPU vs MCU (Microcontroller)

| Aspect | CPU (Microprocessor) | MCU (Microcontroller) |
|--------|---------------------|----------------------|
| Contains | CPU only | CPU + ROM + RAM + I/O |
| Needs | External memory, I/O | Minimal external parts |
| Examples | 8080, Z80, 68000 | 8051, PIC, 8096 |
| Use case | General computing | Embedded systems |

---

## Data Width Evolution

### 4-Bit Era (1971-1974)

The first microprocessors were 4-bit, designed for calculators and simple control.

```
4-bit data path:
┌───┬───┬───┬───┐
│ 3 │ 2 │ 1 │ 0 │  = 0-15 (one BCD digit)
└───┴───┴───┴───┘

Perfect for: Calculators (0-9 digits)
Examples: 4004, 4040, TMS1000
```

### 8-Bit Era (1972-1979)

Eight bits became the standard for practical computing.

```
8-bit data path:
┌───┬───┬───┬───┬───┬───┬───┬───┐
│ 7 │ 6 │ 5 │ 4 │ 3 │ 2 │ 1 │ 0 │  = 0-255
└───┴───┴───┴───┴───┴───┴───┴───┘

Perfect for: ASCII text (0-127), small numbers
Examples: 8080, 6502, Z80, 6809
```

### 16-Bit Era (1978-1985)

Sixteen bits enabled larger numbers and memory.

```
16-bit data path:
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│15 │14 │13 │12 │11 │10 │ 9 │ 8 │ 7 │ 6 │ 5 │ 4 │ 3 │ 2 │ 1 │ 0 │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
= 0-65,535

Perfect for: Memory addresses, larger calculations
Examples: 8086, 68000, Z8000
```

### 32-Bit Era (1984-1985)

Thirty-two bits enabled modern computing.

```
32-bit data path:
= 0 to 4,294,967,295
= 4 GB direct addressing

Perfect for: Large memory, complex calculations
Examples: 80386, 68020, ARM1, MIPS R2000
```

### Hybrid Architectures

Some processors had different internal and external widths:

| Processor | Internal | External | Reason |
|-----------|----------|----------|--------|
| 68000 | 32-bit | 16-bit | Cost reduction |
| 68008 | 32-bit | 8-bit | Even cheaper |
| 8088 | 16-bit | 8-bit | Use 8-bit boards |

---

## Memory Addressing

### Linear Addressing

Most processors used simple linear addressing:

```
6502 (16-bit address):
$0000 ┌─────────────────────┐
      │   Zero Page         │ ← Fast access
$0100 ├─────────────────────┤
      │   Stack             │
$0200 ├─────────────────────┤
      │                     │
      │   RAM/ROM           │
      │                     │
$FFFF └─────────────────────┘
      
Total: 64 KB addressable
```

### Segmented Addressing (8086)

Intel chose segmentation to address more than 64 KB:

```
8086 Segmented Memory:

Physical Address = (Segment × 16) + Offset

Segment Register (16-bit): 0x1234
                           × 16 = 0x12340
Offset (16-bit):                  + 0x5678
                                  ─────────
Physical (20-bit):                 0x179B8

Result: 1 MB addressable with 16-bit registers
```

**Problem:** Same physical address can have multiple segment:offset combinations. This caused compatibility headaches for decades.

### Linear 24/32-Bit (68000, 80386)

Modern approach: just use more address bits.

```
68000 (24-bit address):
$000000 ┌─────────────────────┐
        │                     │
        │   16 MB Linear      │
        │   Address Space     │
        │                     │
$FFFFFF └─────────────────────┘

Much cleaner than segmentation!
```

### Virtual Memory

80286 introduced protected mode; 80386 added paging:

```
80386 Paging:

Virtual Address        Physical Address
┌─────────────┐       ┌─────────────┐
│   Process A │       │             │
│   sees 4 GB │──┐    │   Actual    │
└─────────────┘  │    │    RAM      │
                 ├───►│   (maybe    │
┌─────────────┐  │    │   16 MB)    │
│   Process B │──┘    │             │
│   sees 4 GB │       └─────────────┘
└─────────────┘
                Page tables translate
                virtual → physical
```

---

## Register Architectures

### Accumulator Architecture (8080, 6800)

One special register for arithmetic:

```
8080 Registers:
┌─────────────┐
│     A       │ ← Accumulator (all ALU ops)
├─────────────┤
│  B  │  C    │ ← General purpose pairs
├─────────────┤
│  D  │  E    │
├─────────────┤
│  H  │  L    │ ← Also memory pointer
└─────────────┘

ADD B    ; A = A + B (A is implicit)
```

**Limitation:** Everything flows through A, creating bottleneck.

### Zero-Page Architecture (6502)

First 256 bytes of RAM act as pseudo-registers:

```
6502 Memory Map:
$00-$FF  ┌─────────────────────┐
         │   Zero Page         │ ← Fast as registers!
         │   (256 "registers") │    Single-byte address
$100     └─────────────────────┘

LDA $50    ; Load from zero page (2 bytes, fast)
LDA $1050  ; Load from memory (3 bytes, slower)
```

**Clever:** Minimal on-chip registers, but zero-page provides similar speed.

### Orthogonal Architecture (68000)

Any register can do anything:

```
68000 Registers:
D0-D7: 8 × 32-bit Data registers
A0-A7: 8 × 32-bit Address registers

ADD.W D3,D5    ; Add any D to any D
MOVE.L (A2),D4 ; Load from any A pointer
LEA (A1,D2),A3 ; Complex addressing

No special accumulator - any register works!
```

**Advantage:** Compiler-friendly, more efficient code.

### Register File (TMS9900, 8096)

Registers live in RAM:

```
TMS9900 Workspace:
                           RAM:
Workspace Pointer ─────►  ┌─────────┐
                          │   R0    │
                          │   R1    │
                          │   ...   │
                          │   R15   │
                          └─────────┘
                          
Context switch = change pointer (FAST!)
```

**Trade-off:** Register access is memory access (slower), but context switches are instant.

### RISC Registers (ARM, MIPS)

Many uniform registers:

```
MIPS R2000:
$0:  Always zero (hardwired)
$1:  Assembler temporary
$2-$3: Return values
$4-$7: Arguments
$8-$15: Temporaries
$16-$23: Saved
$24-$25: More temporaries
$26-$27: OS reserved
$28: Global pointer
$29: Stack pointer
$30: Frame pointer
$31: Return address

32 registers, all 32-bit, all general-purpose
```

**RISC philosophy:** More registers = fewer memory accesses = faster.

---

## Instruction Set Design

### CISC (Complex Instruction Set)

Many specialized instructions:

```
8086 CISC Example:
REP MOVSB    ; Repeat move string byte
             ; One instruction does entire block copy!
             
Microcode implements complex operation.
```

### RISC (Reduced Instruction Set)

Few simple instructions:

```
MIPS RISC Example:
loop:
    LB   $t0, ($a0)    ; Load byte
    SB   $t0, ($a1)    ; Store byte
    ADDI $a0, $a0, 1   ; Increment source
    ADDI $a1, $a1, 1   ; Increment dest
    BNE  $t0, $zero, loop  ; Loop if not zero
    
Five simple instructions instead of one complex one.
But each completes in one cycle!
```

### Instruction Encoding

**Variable Length (CISC):**
```
8086:
NOP           ; 1 byte:  90
MOV AX, BX    ; 2 bytes: 89 D8
MOV AX, [BX+1234] ; 4 bytes: 8B 87 34 12
```

**Fixed Length (RISC):**
```
MIPS:
Every instruction is exactly 32 bits.
┌────────┬─────┬─────┬─────┬─────┬────────┐
│ opcode │ rs  │ rt  │ rd  │shamt│ funct  │
│ 6 bits │5 bit│5 bit│5 bit│5 bit│ 6 bits │
└────────┴─────┴─────┴─────┴─────┴────────┘
```

---

## Pipeline Evolution

### No Pipeline (8080, 6502, Z80)

```
Cycle: 1    2    3    4    5    6    7    8
       ├────┼────┼────┼────┼────┼────┼────┼────
Inst1: [  Fetch  ][  Execute  ]
Inst2:                         [  Fetch  ][  Execute  ]

One instruction at a time.
```

### Prefetch Buffer (8086)

```
8086 Prefetch:
┌────────────────────────────────────────┐
│ EU (Execution Unit)                    │
│   Executes instructions                │
├────────────────────────────────────────┤
│ BIU (Bus Interface Unit)               │
│   Fetches bytes into 6-byte queue      │
└────────────────────────────────────────┘

BIU fills queue while EU executes.
Overlap increases throughput.
```

### True Pipeline (ARM, MIPS)

```
MIPS 5-Stage Pipeline:

Cycle:    1     2     3     4     5     6     7
          ├─────┼─────┼─────┼─────┼─────┼─────┼─────
Inst 1:   IF    ID    EX    MEM   WB
Inst 2:         IF    ID    EX    MEM   WB
Inst 3:               IF    ID    EX    MEM   WB
Inst 4:                     IF    ID    EX    MEM   WB
Inst 5:                           IF    ID    EX    MEM

IF  = Instruction Fetch
ID  = Instruction Decode
EX  = Execute
MEM = Memory Access
WB  = Write Back

One instruction completes per cycle (ideally)!
```

---

## Memory Hierarchy

### Single-Level (Early Processors)

```
8080 Memory:
CPU ◄────────► RAM/ROM (same speed)

All memory accesses take the same time.
```

### On-Chip RAM (MCUs)

```
8051 Memory:
┌─────────────────────────────────────┐
│              8051                    │
│  ┌─────────┐     ┌─────────────┐    │
│  │  CPU    │◄───►│  128B RAM   │    │ Fast
│  └────┬────┘     └─────────────┘    │
│       │                              │
└───────┼──────────────────────────────┘
        │
        ▼ (External bus)
   External Memory                       Slow
```

### Cache Memory (68020, 80386)

```
68020 with Cache:
┌─────────────────────────────────────┐
│              68020                   │
│  ┌─────────┐     ┌─────────────┐    │
│  │  CPU    │◄───►│  256B Cache │    │ Very fast
│  └────┬────┘     └─────────────┘    │
│       │                              │
└───────┼──────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│            Main Memory               │ Slower
└─────────────────────────────────────┘

Cache holds recently-used instructions.
```

---

## Peripheral Integration

### External Peripherals (8080 Era)

```
8080 System:
┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐
│ 8080 │───│ RAM  │───│ 8255 │───│ 8253 │
│ CPU  │   │      │   │ PIO  │   │Timer │
└──────┘   └──────┘   └──────┘   └──────┘
    │          │          │          │
    └──────────┴──────────┴──────────┘
              System Bus
              
Multiple chips needed for basic system.
```

### Microcontroller Integration (8051)

```
8051 Single-Chip:
┌────────────────────────────────────────┐
│                 8051                    │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌───────┐  │
│  │ CPU │  │ RAM │  │Timer│  │ UART  │  │
│  └─────┘  └─────┘  └─────┘  └───────┘  │
│  ┌─────┐  ┌─────┐  ┌─────────────────┐ │
│  │ ROM │  │ I/O │  │   Interrupts    │ │
│  └─────┘  └─────┘  └─────────────────┘ │
└────────────────────────────────────────┘

Complete system on one chip!
```

### Domain-Specific Integration (8096)

```
8096 Automotive MCU:
┌────────────────────────────────────────────┐
│                  8096                       │
│  ┌─────┐  ┌─────┐  ┌──────┐  ┌──────────┐  │
│  │ CPU │  │ RAM │  │ A/D  │  │   HSI    │  │ Sensors
│  │16-bit│ │232B │  │10-bit│  │(capture) │  │
│  └─────┘  └─────┘  └──────┘  └──────────┘  │
│  ┌─────┐  ┌─────┐  ┌──────┐  ┌──────────┐  │
│  │ ROM │  │Timer│  │ PWM  │  │   HSO    │  │ Actuators
│  │ 8KB │  │     │  │      │  │(compare) │  │
│  └─────┘  └─────┘  └──────┘  └──────────┘  │
└────────────────────────────────────────────┘

Peripherals specifically designed for engine control!
```

---

## Key Architectural Lessons

### 1. Simplicity Can Win

ARM1's 25,000 transistors outperformed the 80286's 134,000 transistors. Simple designs can run faster and use less power.

### 2. Compatibility Constrains Evolution

x86 still carries baggage from 1978 segmented memory design. The 68000's clean architecture couldn't overcome x86's compatibility advantage.

### 3. Integration Reduces Cost

The 6502's simple design (3,510 transistors) enabled $25 pricing, making personal computers affordable.

### 4. The Right Peripherals Matter

The 8096's specialized HSI/HSO peripherals made it dominant in automotive, while generic CPUs struggled.

### 5. Memory Architecture Defines Capability

Linear addressing (68000) vs. segmentation (8086) created decades of software differences.

---

**Document Version:** 1.0  
**Last Updated:** January 25, 2026
