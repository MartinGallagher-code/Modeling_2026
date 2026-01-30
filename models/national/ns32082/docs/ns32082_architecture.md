# National NS32082 Architecture Document

## Overview

| Property | Value |
|----------|-------|
| **Full Name** | National Semiconductor NS32082 Memory Management Unit |
| **Manufacturer** | National Semiconductor |
| **Year** | 1983 |
| **Process** | 3 um CMOS |
| **Transistors** | ~60,000 |
| **Clock Speed** | 10 MHz |
| **Data Width** | 32-bit |
| **Address Width** | 32-bit |
| **Package** | 48-pin DIP |

## Architecture Description

The NS32082 was the memory management unit for National Semiconductor's NS32000 processor family. It provided demand-paged virtual memory with hardware page table walking and a translation cache for address mapping.

### Execution Model

- **Type**: Sequential address translation coprocessor
- **Pipeline**: None
- **Translation Cache**: On-chip for recent address mappings
- **Page Size**: Fixed 512-byte pages

### Instruction Categories

| Category | Base Cycles | Description |
|----------|-------------|-------------|
| translate | 4 | Address translation on TLB hit |
| page_fault | 20 | Page fault exception handling setup |
| table_walk | 15 | Page table walk on TLB miss |
| cache_op | 3 | Translation cache operations |
| control | 5 | MMU control and status operations |

### Address Translation

1. Virtual address presented by NS32016/NS32032
2. Translation cache lookup (4 cycles on hit)
3. On cache miss: two-level page table walk (15+ cycles)
4. On page not present: page fault exception (20 cycles)
5. Physical address output

### Key Features

- 32-bit virtual address space
- Demand-paged virtual memory
- Two-level page table structure
- Hardware page table walker
- Translation cache for fast lookups
- Protection and access control mechanisms
- Part of NS32000 chipset family

## References

- National Semiconductor NS32082 MMU Data Sheet (1983)
- NS32000 Family Reference Manual
- Wikipedia: NS32000
