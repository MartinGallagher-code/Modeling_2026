# Hitachi 6309 - Quick Start

## Best 8-Bit Ever (1982, documented 1988)

Secret enhanced 6809 with native mode!

| Feature | 6809 | 6309 |
|---------|------|------|
| Registers | 9 | **15** |
| HW Divide | No | **Yes** |
| Block Xfer | No | **TFM** |
| 32-bit math | No | **Q register** |
| IPC | 0.11 | **0.18** |

## New Registers
- E, F (8-bit) → W (16-bit)
- D + W = Q (32-bit!)
- V, MD

## Native Mode
```asm
LDMD #$01  ; Enable 2× speed!
```

**Secret features discovered 6 years after release!**
