# Motorola 68851 Architecture Document

## Overview

| Property | Value |
|----------|-------|
| **Full Name** | Motorola 68851 Paged Memory Management Unit |
| **Manufacturer** | Motorola |
| **Year** | 1984 |
| **Process** | 2 um HCMOS |
| **Transistors** | ~190,000 |
| **Clock Speed** | 10 MHz |
| **Data Width** | 32-bit |
| **Address Width** | 32-bit |
| **Package** | 132-pin PGA |

## Architecture Description

The Motorola 68851 was a dedicated PMMU designed to work with the MC68020 processor. It provided full demand-paged virtual memory management with hardware page table walking, a translation lookaside buffer, and comprehensive protection mechanisms.

### Execution Model

- **Type**: Sequential address translation coprocessor
- **Pipeline**: None
- **TLB**: On-chip translation lookaside buffer
- **Page Sizes**: Multiple configurable page sizes

### Instruction Categories

| Category | Base Cycles | Description |
|----------|-------------|-------------|
| translate | 3 | TLB hit address translation |
| table_walk | 12 | Hardware page table walk on TLB miss |
| flush | 8 | TLB flush operations |
| load_descriptor | 6 | Page/segment descriptor load |
| validate | 4 | Address validation and protection check |

### Address Translation Pipeline

1. Virtual address presented by MC68020
2. TLB lookup (3 cycles on hit)
3. On TLB miss: hardware table walk (12+ cycles)
4. Protection check and physical address output
5. Access control validation

### Key Features

- 32-bit virtual and physical address spaces
- Hardware page table walker (reduces software overhead)
- Translation lookaside buffer for fast translations
- Multiple page size support
- Access level protection (supervisor/user)
- MC68020 coprocessor interface protocol
- 190,000 transistors - highly complex for its era

## References

- Motorola MC68851 PMMU User's Manual (1984)
- Motorola MC68020/68851 Technical Summary
- Wikipedia: Motorola 68851
