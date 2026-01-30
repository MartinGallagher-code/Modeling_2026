# Architectural Guide

## Understanding Microprocessor Design Evolution (1970-1995)

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
9. [Superscalar Architecture](#superscalar-architecture)
10. [Out-of-Order Execution](#out-of-order-execution)
11. [RISC vs CISC Convergence](#risc-vs-cisc-convergence)
12. [DSP Architecture](#dsp-architecture)
13. [Graphics Processor Architecture](#graphics-processor-architecture)

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

### 32-Bit Era (1984-1995)

Thirty-two bits enabled modern computing.

```
32-bit data path:
= 0 to 4,294,967,295
= 4 GB direct addressing

Perfect for: Large memory, complex calculations
Examples: 80386, 68020, ARM1, MIPS R2000
```

### 64-Bit Era (1992-1995)

```
64-bit data path:
= 0 to 18,446,744,073,709,551,615
= Massive address space

Examples: DEC Alpha 21064, MIPS R4000, i860
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

### Register Windows (SPARC)

SPARC introduced overlapping register windows for fast function calls:

```
SPARC Register Windows:

Window N-1 (caller):
┌────────────┬────────────┬────────────┬────────────┐
│  Global    │   Outs     │   Locals   │    Ins     │
│  r0-r7    │  r8-r15    │  r16-r23   │  r24-r31   │
└────────────┴─────┬──────┴────────────┴────────────┘
                   │
              (overlap)
                   │
Window N (callee): ▼
┌────────────┬────────────┬────────────┬────────────┐
│  Global    │   Outs     │   Locals   │    Ins     │
│  r0-r7    │  r8-r15    │  r16-r23   │  r24-r31   │
└────────────┴────────────┴────────────┴────────────┘

Caller's "Outs" become Callee's "Ins" automatically!
No memory access needed for parameter passing.

Typical SPARC: 8 windows × 24 unique registers = 192 physical registers
```

**Advantage:** Function calls and returns avoid stack memory accesses entirely.

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

### Superpipelined (Alpha 21064)

Deeper pipelines allow higher clock speeds by breaking stages into smaller pieces:

```
Alpha 21064 - 7+ Stage Pipeline:

Cycle:    1     2     3     4     5     6     7     8     9
          ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────
Inst 1:   IF0   IF1   ID    ISS   EX0   EX1   MEM   WB
Inst 2:         IF0   IF1   ID    ISS   EX0   EX1   MEM   WB
Inst 3:               IF0   IF1   ID    ISS   EX0   EX1   MEM

IF0/IF1 = Two-stage instruction fetch
ID      = Decode
ISS     = Issue
EX0/EX1 = Two-stage execute
MEM     = Memory access
WB      = Write back

More stages = shorter critical path = higher clock speed.
Alpha 21064 ran at 150-200 MHz when others ran at 50-66 MHz.
Trade-off: Deeper pipeline means larger branch misprediction penalty.
```

### Superscalar (Pentium, 68060, PPC 604)

```
Pentium Dual Pipeline:

Cycle:    1     2     3     4     5
U-pipe:   IF    ID    EX    MEM   WB
V-pipe:   IF    ID    EX    MEM   WB

Two instructions per cycle (when compatible)!

U-pipe handles all instructions.
V-pipe handles "simple" instructions only (no microcode).

Pairing rules determine which instructions can execute together.
Best case: 2 IPC. Typical: ~1.5 IPC on real workloads.
```

### Out-of-Order (MIPS R10000, Alpha 21264)

```
In-Order:  Fetch -> Decode -> Execute -> Writeback
                                 ^ stall if dependency

Out-of-Order: Fetch -> Decode -> Reorder Buffer -> Execute (any order) -> Commit (in order)

Example:
  ADD R1, R2, R3     ; R1 = R2 + R3
  MUL R4, R1, R5     ; R4 = R1 * R5  (depends on ADD)
  SUB R6, R7, R8     ; R6 = R7 - R8  (independent!)

In-Order:   ADD ... MUL stalls waiting for R1 ... SUB waits too
Out-of-Order: ADD issued ... SUB issued immediately ... MUL issued when R1 ready

The reorder buffer tracks dependencies and ensures results
commit in program order even though execution is out of order.
```

---

## Memory Hierarchy

### Single-Level (Early Processors)

```
8080 Memory:
CPU <---------> RAM/ROM (same speed)

All memory accesses take the same time.
```

### On-Chip RAM (MCUs)

```
8051 Memory:
┌─────────────────────────────────────┐
│              8051                    │
│  ┌─────────┐     ┌─────────────┐    │
│  │  CPU    │<--->│  128B RAM   │    │ Fast
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
│  │  CPU    │<--->│  256B Cache │    │ Very fast
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

### Split Cache (80486, Pentium)

Separate instruction and data caches eliminate structural hazards:

```
80486 Unified Cache:
┌─────────────────────────────────────────┐
│               80486                      │
│  ┌─────────┐     ┌─────────────────┐    │
│  │  CPU    │<--->│  8 KB Unified   │    │
│  └─────────┘     │  Cache          │    │
│                   └─────────────────┘    │
└─────────────────────────────────────────┘

Pentium Split Cache:
┌───────────────────────────────────────────────┐
│                  Pentium                       │
│  ┌─────────┐     ┌──────────┐  ┌──────────┐   │
│  │  CPU    │<--->│  8 KB    │  │  8 KB    │   │
│  │         │     │  I-Cache │  │  D-Cache │   │
│  └─────────┘     └──────────┘  └──────────┘   │
└───────────────────────────────────────────────┘

Split cache allows simultaneous instruction fetch
and data read/write -- no contention!
```

### Multi-Level Cache

```
Pentium with External L2 Cache:

┌───────────────────────────────────────────────┐
│                  Pentium                       │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐      │
│  │  CPU    │  │ 8KB I-L1 │  │ 8KB D-L1 │      │ ~1 cycle
│  └─────────┘  └──────────┘  └──────────┘      │
└──────────────────────┬────────────────────────┘
                       │
              ┌────────▼────────┐
              │  256 KB - 1 MB  │
              │   L2 Cache      │                  ~5-10 cycles
              │  (on board)     │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │   Main Memory   │                  ~50-70 cycles
              │   (16-64 MB)    │
              └─────────────────┘

As CPU speed outpaced memory speed, more cache levels
became essential to hide memory latency.
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

## Superscalar Architecture

Superscalar processors issue multiple instructions per clock cycle using multiple execution units:

### Dual-Issue (Pentium, Alpha 21064)

```
Pentium Dual-Issue:
┌──────────────────────────────────────────────────┐
│                    Pentium                        │
│                                                  │
│  ┌───────────────┐        ┌───────────────┐      │
│  │   U Pipeline  │        │   V Pipeline  │      │
│  │  (full)       │        │  (simple)     │      │
│  │               │        │               │      │
│  │  ALU          │        │  ALU          │      │
│  │  FPU          │        │               │      │
│  │  Mem          │        │  Mem          │      │
│  └───────────────┘        └───────────────┘      │
│                                                  │
│  Pairing rules:                                  │
│  - Both must be "simple" or U can be complex     │
│  - No data dependency between paired insts       │
│  - No read-after-write on same register          │
└──────────────────────────────────────────────────┘

Alpha 21064 Dual-Issue:
- One integer + one floating-point per cycle
- Or: one integer + one load/store per cycle
- 150-200 MHz clock (fastest of its era)
```

### Four-Issue (PPC 604)

```
PPC 604 Dispatch:

Each cycle can dispatch up to 4 instructions to:
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│  Integer   │ │  Integer   │ │  FP Unit   │ │  Branch    │
│  Unit 1    │ │  Unit 2    │ │            │ │  Unit      │
└────────────┘ └────────────┘ └────────────┘ └────────────┘
       │              │              │              │
       └──────────────┴──────────────┴──────────────┘
                    Completion Unit
                (retires in order)

With two integer units, FP, and branch prediction,
the PPC 604 achieved high throughput on mixed workloads.
```

### 68060 Superscalar

```
68060 Dual-Issue CISC Superscalar:
┌──────────────────────────────────────────────┐
│                  68060                        │
│                                              │
│  Instruction Fetch -> Decode -> Dispatch     │
│                                    │         │
│                         ┌──────────┴───┐     │
│                         ▼              ▼     │
│                   ┌──────────┐  ┌──────────┐ │
│                   │  pOEP    │  │  sOEP    │ │
│                   │ Primary  │  │Secondary │ │
│                   │Exec Pipe │  │Exec Pipe │ │
│                   └──────────┘  └──────────┘ │
│                                              │
│  Remarkable: CISC superscalar without        │
│  micro-op translation (unlike Pentium Pro)   │
└──────────────────────────────────────────────┘
```

### Concept of Issue Width

```
Issue Width Over Time:

Processor     Year    Issue Width    Peak IPC
─────────────────────────────────────────────
8080          1974    1 (multi-cyc)  ~0.2
68000         1979    1              ~0.3
ARM1          1985    1              ~0.5
i486          1989    1 (pipelined)  ~1.0
Pentium       1993    2              ~2.0
PPC 604       1994    4              ~4.0
Alpha 21164   1995    4              ~4.0

Wider issue = more ILP (instruction-level parallelism) exploited.
Diminishing returns above 4-6 due to dependency limits.
```

---

## Out-of-Order Execution

Out-of-order (OoO) execution allows the processor to execute instructions in whatever order their operands become available, rather than strictly in program order.

### The Problem: In-Order Stalls

```
In-Order Execution:

  LOAD  R1, [mem]      ; Cache miss! 50 cycle wait
  ADD   R2, R1, R3     ; Depends on R1 -- must stall
  SUB   R4, R5, R6     ; Independent, but stalled too!
  MUL   R7, R8, R9     ; Independent, but stalled too!

  50 cycles wasted while three independent instructions wait.
```

### The Solution: Reorder Buffer

```
Out-of-Order Execution:

  LOAD  R1, [mem]      ; Cache miss -- issued to memory
  ADD   R2, R1, R3     ; Queued in reorder buffer, waiting for R1
  SUB   R4, R5, R6     ; Independent -- execute immediately!
  MUL   R7, R8, R9     ; Independent -- execute immediately!

  ┌─────────────────────────────────────────────────────────┐
  │                   Reorder Buffer                        │
  │  ┌─────┬───────────┬────────┬─────────┐                │
  │  │ Seq │ Instruction│ Status │ Result  │                │
  │  ├─────┼───────────┼────────┼─────────┤                │
  │  │  1  │ LOAD R1   │ waiting│   --    │                │
  │  │  2  │ ADD R2    │ waiting│   --    │ depends on #1  │
  │  │  3  │ SUB R4    │  done  │  R4=val │ commit after 1,2│
  │  │  4  │ MUL R7    │  done  │  R7=val │ commit after 3  │
  │  └─────┴───────────┴────────┴─────────┘                │
  │                                                         │
  │  Results commit in original program order (1,2,3,4)     │
  │  even though execution order was (3,4,1,2)              │
  └─────────────────────────────────────────────────────────┘
```

### Key OoO Processors (1990-1995)

```
Processor         Year    OoO Window    Notes
──────────────────────────────────────────────────────
MIPS R10000       1996    32 entries    First MIPS OoO
Alpha 21264       1998    80 entries    Deep OoO
Pentium Pro       1995    40 entries    x86 with RISC micro-ops
PPC 604           1994    Limited       Partial OoO (dispatch)
NexGen Nx586      1994    x86 -> RISC   Pioneered micro-op approach

OoO execution was the defining innovation of mid-1990s CPUs.
It extracts parallelism the programmer never explicitly expressed.
```

---

## RISC vs CISC Convergence

### Phase 1: The RISC Revolution (1985-1990)

```
RISC clearly faster per clock:

                CPI (lower is better)
CISC (68020):   ████████████████████  ~4.0 CPI
CISC (80386):   ██████████████████    ~3.5 CPI
RISC (SPARC):   █████                 ~1.2 CPI
RISC (MIPS):    ████                  ~1.0 CPI
RISC (ARM):     █████                 ~1.1 CPI

RISC advantages:
- Fixed-length instructions: easy to pipeline
- Load/store architecture: simple execution units
- Large register files: fewer memory accesses
- Single-cycle execution: predictable timing
```

### Phase 2: CISC Fights Back (1990-1995)

x86 adopted RISC techniques internally while keeping the CISC ISA:

```
Evolution of x86 Internal Architecture:

8086 (1978):    Microcode → Execute
                Pure CISC, no pipeline

80486 (1989):   IF → ID → EX → MEM → WB
                RISC-style 5-stage pipeline!
                Many simple instructions: 1 CPI

Pentium (1993): Dual Pipeline (U + V)
                Superscalar CISC
                Simple instructions: 0.5 CPI

NexGen Nx586 (1994):
  x86 instruction → translate → RISC micro-ops → execute
  ┌─────────┐    ┌──────────┐    ┌──────────────┐
  │  CISC   │ -> │Translate │ -> │ RISC Engine  │
  │  Fetch  │    │ to RISC  │    │ (OoO, super- │
  │         │    │ micro-ops│    │  scalar)     │
  └─────────┘    └──────────┘    └──────────────┘
  Pioneered the approach later used by AMD K6 and Intel P6.

Pentium Pro (1995):
  Full out-of-order execution with micro-op translation.
  x86 ISA decoded into RISC-like micro-ops internally.
  40-entry reorder buffer, 3-wide dispatch.
  The CISC/RISC distinction became an ISA detail, not a
  microarchitecture distinction.
```

### The Convergence

```
By 1995:
                        RISC                    CISC (x86)
ISA:                    Simple, fixed           Complex, variable
Internal execution:     Pipelined, OoO          Pipelined, OoO
Micro-ops:              N/A (already simple)    Translated from CISC
Performance:            High                    Comparable
Volume/Cost:            Low volume, expensive   Massive volume, cheap

Winner: x86 won on economics (PC volume), while RISC won on
elegance (servers, embedded). Both used the same internal techniques.
```

---

## DSP Architecture

Digital Signal Processors (DSPs) diverged from general-purpose CPUs with architectures optimized for repetitive math on data streams.

### Harvard Architecture

```
Von Neumann (general-purpose CPU):
┌─────────┐     ┌──────────────────┐
│   CPU   │<--->│  Single Memory   │
│         │     │  (code + data)   │
└─────────┘     └──────────────────┘
One bus = fetch instruction OR read data (not both)

Harvard Architecture (DSP):
┌─────────┐     ┌──────────────────┐
│         │<--->│ Program Memory   │  Fetch instruction
│   CPU   │     └──────────────────┘
│         │<--->┌──────────────────┐
│         │     │  Data Memory A   │  Read operand A
│         │<--->┌──────────────────┐
│         │     │  Data Memory B   │  Read operand B
└─────────┘     └──────────────────┘
Multiple buses = fetch + 2 data reads simultaneously!
```

### MAC (Multiply-Accumulate) in Single Cycle

```
The core DSP operation:

Accumulator += Data[i] * Coefficient[i]

General-purpose CPU:
  LOAD  R1, [data+i]      ; 1 cycle
  LOAD  R2, [coeff+i]     ; 1 cycle
  MUL   R3, R1, R2        ; 3-10 cycles
  ADD   ACC, ACC, R3      ; 1 cycle
  Total: 6-13 cycles

DSP (e.g., TMS320C25):
  MAC   *AR0+, *AR1+      ; 1 cycle!
  - Fetches two operands via dual data buses
  - Multiplies in hardware multiplier
  - Adds to 40-bit accumulator
  - Auto-increments two address pointers
  All in a single cycle.
```

### Hardware Loop Counters

```
DSP Hardware Loops:

General-purpose CPU loop:
  loop: ...              ; loop body
        DEC  counter     ; decrement
        BNZ  loop        ; branch (pipeline flush!)

DSP hardware loop:
  RPT  #255              ; Set hardware repeat counter
  MAC  *AR0+, *AR1+      ; Executes 256 times
                         ; Zero overhead: no branch,
                         ; no counter decrement instruction
```

### Key DSPs

```
Processor      Year   Clock    MAC/cycle   Application
──────────────────────────────────────────────────────────
TMS320C10      1983   5 MHz    1           Telecom
TMS320C25      1986   40 MHz   1           Modems, audio
ADSP-2100      1986   12 MHz   1           Audio, control
DSP56001       1987   20 MHz   1           Audio, music
TMS320C30      1988   33 MHz   1 (float)   Scientific
TMS320C50      1991   50 MHz   1           Telecom
DSP56002       1993   66 MHz   1           Multimedia

DSPs dominated real-time signal processing where
general-purpose CPUs could not keep up.
```

---

## Graphics Processor Architecture

As graphical user interfaces (GUIs) became standard in the late 1980s and early 1990s, specialized graphics processors emerged to offload the CPU.

### BitBLT Acceleration (TMS34010)

```
BitBLT = Bit Block Transfer
The fundamental GUI operation: copying rectangular pixel blocks.

Without acceleration (CPU does everything):
  CPU reads source pixels from VRAM
  CPU applies raster operation (AND, OR, XOR)
  CPU writes destination pixels to VRAM
  ... one pixel at a time, through the system bus

With TMS34010 (1986):
┌─────────────────────────────────────────────┐
│              TMS34010                        │
│  ┌──────────────┐    ┌──────────────────┐   │
│  │ Programmable │    │   PIXBLT         │   │
│  │ 32-bit CPU   │    │   Hardware       │   │
│  │ (general     │    │   (BitBLT in     │   │
│  │  purpose)    │    │    hardware)     │   │
│  └──────────────┘    └──────────────────┘   │
│         │                    │               │
│         └────────┬───────────┘               │
│                  ▼                           │
│         ┌──────────────────┐                │
│         │  Video RAM       │                │
│         │  (local, fast)   │                │
│         └──────────────────┘                │
└─────────────────────────────────────────────┘

The TMS34010 was unique: a fully programmable GPU.
It ran its own programs, not just fixed-function operations.
Used in: arcade games, Windows accelerator cards, printers.
```

### Windows GDI Acceleration (S3 86C911)

```
S3 86C911 (1991) - Named after the Porsche 911:

Instead of a programmable CPU, fixed-function hardware
accelerates specific Windows GDI operations:

┌─────────────────────────────────────────────┐
│               S3 86C911                      │
│                                             │
│  ┌───────────────┐  ┌───────────────────┐   │
│  │  Hardware      │  │  Hardware         │   │
│  │  Line Draw     │  │  BitBLT Engine   │   │
│  └───────────────┘  └───────────────────┘   │
│  ┌───────────────┐  ┌───────────────────┐   │
│  │  Hardware      │  │  Hardware         │   │
│  │  Rectangle    │  │  Color Expand    │   │
│  │  Fill          │  │  (text render)   │   │
│  └───────────────┘  └───────────────────┘   │
│                  │                           │
│         ┌────────▼────────┐                 │
│         │   1 MB VRAM     │                 │
│         │   (local bus)   │                 │
│         └─────────────────┘                 │
└─────────────────────────────────────────────┘

Windows 3.1 sent GDI commands directly to the card.
10-100x faster than CPU software rendering.
Launched the "Windows accelerator" market.
```

### Programmable vs Fixed-Function

```
Spectrum of GPU Architecture (1986-1995):

Fully Programmable              Fixed-Function
◄──────────────────────────────────────────────►
│                                              │
TMS34010     TMS34020      S3 86C911      VGA chip
(1986)       (1988)        (1991)         (1987)

- Runs its   - Faster      - HW GDI      - Dumb
  own code     programmable   accel only    framebuffer
- Flexible   - PIXBLT      - Very fast   - CPU does
- Slower for   hardware      for Windows   all work
  fixed ops  - Used in     - Cheap       - Cheapest
- Expensive    CAD, print  - Volume

The market chose fixed-function acceleration for PCs
(cost/performance), while programmable GPUs found
niches in arcade games and professional graphics.

The fully programmable GPU would return years later
with modern shader architectures (late 1990s+).
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

### 6. RISC Principles Eventually Won Everywhere

Even x86 processors use RISC-style execution internally since the Pentium Pro (1995). The RISC philosophy of simple, fast micro-operations proved universally effective regardless of the external instruction set.

### 7. Specialization Matters

DSPs and GPUs diverged from general-purpose CPUs because certain workloads demand dedicated hardware. A DSP's single-cycle MAC is 10x faster than a general-purpose CPU for signal processing. This pattern of specialization continues to this day.

### 8. Memory Wall: Cache Hierarchy Becomes Critical

As clock speeds rose from 5 MHz to 200 MHz (40x), DRAM speed improved only ~2x. The growing gap -- the "memory wall" -- made cache hierarchy the most important architectural feature by 1995. Processors without effective caching were bottlenecked regardless of execution speed.

---

**Document Version:** 2.0
**Last Updated:** January 30, 2026
