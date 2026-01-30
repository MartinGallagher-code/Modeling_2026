# Intel 82730 Architecture

## Overview
The Intel 82730 (1983) is a 16-bit text display coprocessor providing hardware character rendering, smooth scrolling, and DMA-based display list processing.

## Key Features
- 16-bit data bus, 20-bit address bus
- 5 MHz clock frequency
- ~25,000 NMOS transistors
- Hardware character rendering with font ROM support
- Row-based display processing
- Smooth pixel-level scrolling
- Cursor blink and shape control
- DMA display list fetch

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| Char Render | 3 | Character-to-pixel rendering |
| Row Process | 5 | Row descriptor processing |
| Scroll | 6 | Smooth scrolling operations |
| Cursor | 3 | Cursor position and blink |
| DMA | 4 | Display list DMA fetch |

## Application
Text display acceleration:
- High-performance terminals
- Text editor workstations
- Industrial display panels

## Related Processors
- Intel 82720 (graphics display controller)
- Intel 82786 (graphics coprocessor successor)
