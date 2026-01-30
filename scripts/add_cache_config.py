#!/usr/bin/env python3
"""
Script to add CacheConfig to post-1985 processor models.

This script:
1. Adds CacheConfig import/fallback definition to each model file
2. Adds cache_config and memory_categories to __init__
3. Adds cache penalty computation in analyze() before CPI sum

Usage:
    python scripts/add_cache_config.py [--dry-run] [--single PATH]
"""

import re
import sys
import os
import json
from pathlib import Path

# Models and their years + cache characteristics
# We'll detect these from the source files themselves

ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT / "models"


def get_year_from_source(content: str) -> int:
    """Extract year from model source."""
    m = re.search(r'self\.year\s*=\s*(\d{4})', content)
    if m:
        return int(m.group(1))
    m = re.search(r'year\s*=\s*(\d{4})', content)
    if m:
        return int(m.group(1))
    return 0


def get_clock_mhz_from_source(content: str) -> float:
    """Extract clock_mhz from model source."""
    m = re.search(r'self\.clock_mhz\s*=\s*([\d.]+)', content)
    if m:
        return float(m.group(1))
    m = re.search(r'clock_mhz\s*=\s*([\d.]+)', content)
    if m:
        return float(m.group(1))
    return 1.0


def get_memory_categories(content: str) -> list:
    """Detect which instruction categories deal with memory access."""
    # Look at instruction_categories dict for memory-related names
    memory_cats = []
    # Find all category names defined in instruction_categories
    cat_pattern = re.compile(r"'(\w+)':\s*InstructionCategory\(\s*'(\w+)'")
    for m in cat_pattern.finditer(content):
        cat_name = m.group(1)
        if cat_name in ('memory', 'load', 'store', 'load_store', 'mem_read', 'mem_write',
                         'memory_read', 'memory_write', 'data_memory', 'mem'):
            memory_cats.append(cat_name)
    if not memory_cats:
        # Fallback: check for 'memory' category
        if "'memory'" in content:
            memory_cats = ['memory']
    return memory_cats


def estimate_cache_config(year: int, clock_mhz: float, name_lower: str) -> dict:
    """Estimate appropriate cache parameters based on processor characteristics."""
    # Default: simple L1-only cache
    config = {
        'has_cache': True,
        'l1_latency': 1.0,
        'l1_hit_rate': 0.93,
        'has_l2': False,
        'l2_latency': 10.0,
        'l2_hit_rate': 0.90,
        'dram_latency': 30.0,
    }

    # DSP processors typically don't have traditional caches
    if any(k in name_lower for k in ('dsp', 'tms320', 'adsp', 'dsp56', 'dsp96',
                                      'att_dsp', 'ym', 'sn76', 'upd7759',
                                      'sid', '8580', 'ensoniq', 'otto',
                                      'ay3_8910', 'sp0256')):
        config['has_cache'] = False
        return config

    # GPU/VDP processors - no traditional cache
    if any(k in name_lower for k in ('vdp', 'v9938', 'ppu', 'vic', 'ted',
                                      'antic', 'pokey', 'et4000', 's3_86c',
                                      'ati_mach', 'weitek_p9000', 'ct65545',
                                      'iit_agx', 'sega_315', 'snk_lspc',
                                      'huc6280', 'sm83', '82596', '82586',
                                      '82730', '82557', 'fd1094', 'fd1089',
                                      'hd63484', 'rp2c', 'ricoh_2a03',
                                      'ricoh_5a22', '8580_sid',
                                      'am79c970', 'sega_svp')):
        config['has_cache'] = False
        return config

    # Simple 8/16-bit embedded - typically no cache
    if any(k in name_lower for k in ('h8_300', 'h8_500', 'm68hc', 'z8s180',
                                      'z380', 'z80000', 'k580', 'k1810',
                                      'kr1858', 'elbrus_el90', 'k580ik51',
                                      'mos8580', 'rp2c07')):
        config['has_cache'] = False
        return config

    # Estimate DRAM latency based on era and clock speed
    # Rule of thumb: DRAM ~100-200ns access time throughout this era
    # At higher clock rates, this translates to more cycles
    dram_ns = 120.0  # typical DRAM access time
    if year >= 1993:
        dram_ns = 100.0  # faster DRAM in mid-90s
    if year >= 1995:
        dram_ns = 80.0

    config['dram_latency'] = max(8.0, round(clock_mhz * dram_ns / 1000.0, 1))

    # Early cached processors (1986-1988): small caches, lower hit rates
    if year <= 1988:
        config['l1_hit_rate'] = 0.90
        config['dram_latency'] = max(8.0, config['dram_latency'])

    # i486 class (1989-1991): 8KB unified cache
    elif year <= 1991:
        config['l1_hit_rate'] = 0.93

    # Pentium class (1992-1993): separate I/D caches
    elif year <= 1993:
        config['l1_hit_rate'] = 0.94

    # Late processors (1994-1995): larger caches
    else:
        config['l1_hit_rate'] = 0.95

    # Specific processors with L2 caches
    if any(k in name_lower for k in ('pentium', 'alpha', 'power1', 'power2',
                                      'ppc601', 'ppc603', 'ppc604', 'ppc620',
                                      'pa_risc', 'pa7100', 'pa7200',
                                      'ultrasparc', 'sparc64', 'supersparc',
                                      'r4000', 'r4400', 'r4600', 'r8000', 'r10000',
                                      'm68040', 'm68060', 'i860',
                                      'cx5x86', 'am5x86', 'nx586',
                                      'umc_u5s', 'hypersparc',
                                      'ibm_rs64', 'ibm_486slc2',
                                      'microsparc_ii', 'microsparc',
                                      'i960ca', 'i960cf',
                                      'm88110', 'coldfire')):
        config['has_l2'] = True
        config['l2_hit_rate'] = 0.90
        # L2 latency depends on era
        if year >= 1993:
            config['l2_latency'] = max(5.0, round(clock_mhz * 15.0 / 1000.0 * 10, 1))
            config['l2_latency'] = min(config['l2_latency'], 25.0)
            config['l2_latency'] = max(config['l2_latency'], 5.0)
        else:
            config['l2_latency'] = 8.0

    # Specific overrides for well-known processors
    if 'i80486' in name_lower or 'i486' in name_lower:
        config['l1_hit_rate'] = 0.93
        config['has_l2'] = False
        config['dram_latency'] = 12.0  # 25MHz * ~480ns

    elif 'pentium' in name_lower:
        config['l1_hit_rate'] = 0.94
        config['has_l2'] = True
        config['l2_latency'] = 8.0
        config['l2_hit_rate'] = 0.92
        config['dram_latency'] = 18.0  # 60MHz * ~300ns

    elif 'alpha21064' in name_lower or 'alpha_21064' in name_lower:
        config['l1_hit_rate'] = 0.95
        config['has_l2'] = True
        config['l2_latency'] = 8.0
        config['l2_hit_rate'] = 0.93
        config['dram_latency'] = 30.0  # 150MHz * ~200ns

    elif 'alpha_21066' in name_lower:
        config['l1_hit_rate'] = 0.94
        config['has_l2'] = True
        config['l2_latency'] = 10.0
        config['l2_hit_rate'] = 0.90
        config['dram_latency'] = 20.0

    return config


def has_cache_config_already(content: str) -> bool:
    """Check if cache_config is already present."""
    return 'cache_config' in content


def has_try_except_import(content: str) -> bool:
    """Check if the file uses try/except ImportError pattern."""
    return 'except ImportError:' in content


def has_top_level_inline_classes(content: str) -> bool:
    """Check if the file defines InstructionCategory at top level (no indentation)."""
    return bool(re.search(r'^@dataclass\nclass InstructionCategory:', content, re.MULTILINE))


CACHE_CONFIG_INLINE = '''@dataclass
class CacheConfig:
    has_cache: bool = False
    l1_latency: float = 1.0
    l1_hit_rate: float = 0.95
    l2_latency: float = 10.0
    l2_hit_rate: float = 0.90
    has_l2: bool = False
    dram_latency: float = 50.0
    def effective_memory_penalty(self):
        if not self.has_cache: return 0.0
        l1_miss = 1.0 - self.l1_hit_rate
        if self.has_l2:
            l2_miss = 1.0 - self.l2_hit_rate
            return l1_miss * (self.l2_hit_rate * (self.l2_latency - self.l1_latency) + l2_miss * (self.dram_latency - self.l1_latency))
        return l1_miss * (self.dram_latency - self.l1_latency)

'''

CACHE_CONFIG_INDENTED = '''
    @dataclass
    class CacheConfig:
        has_cache: bool = False
        l1_latency: float = 1.0
        l1_hit_rate: float = 0.95
        l2_latency: float = 10.0
        l2_hit_rate: float = 0.90
        has_l2: bool = False
        dram_latency: float = 50.0
        def effective_memory_penalty(self):
            if not self.has_cache: return 0.0
            l1_miss = 1.0 - self.l1_hit_rate
            if self.has_l2:
                l2_miss = 1.0 - self.l2_hit_rate
                return l1_miss * (self.l2_hit_rate * (self.l2_latency - self.l1_latency) + l2_miss * (self.dram_latency - self.l1_latency))
            return l1_miss * (self.dram_latency - self.l1_latency)

'''


def add_cache_config_import(content: str) -> str:
    """Add CacheConfig to the import line (try/except pattern)."""
    # Pattern: from common.base_model import BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult
    pattern = r'(from common\.base_model import\s+)(BaseProcessorModel,\s*InstructionCategory,\s*WorkloadProfile,\s*AnalysisResult)'
    replacement = r'\1BaseProcessorModel, InstructionCategory, WorkloadProfile, AnalysisResult, CacheConfig'
    new_content = re.sub(pattern, replacement, content)
    return new_content


def add_cache_config_class_inline(content: str) -> str:
    """Add CacheConfig class at top level after InstructionCategory (inline pattern).

    Insert before the WorkloadProfile class definition.
    """
    # Find the @dataclass before WorkloadProfile at top level
    pattern = r'\n(@dataclass\nclass WorkloadProfile:)'
    match = re.search(pattern, content)
    if match:
        insert_pos = match.start() + 1  # after the newline
        content = content[:insert_pos] + CACHE_CONFIG_INLINE + '\n' + content[insert_pos:]
    return content


def add_cache_config_fallback(content: str) -> str:
    """Add CacheConfig fallback class in the except ImportError block.

    Insert before the indented WorkloadProfile class definition.
    """
    # Find the indented @dataclass before WorkloadProfile in the except block
    pattern = r'\n(    @dataclass\n    class WorkloadProfile:)'
    match = re.search(pattern, content)
    if match:
        insert_pos = match.start() + 1  # after the newline
        content = content[:insert_pos] + CACHE_CONFIG_INDENTED + '\n' + content[insert_pos:]
    return content


def add_cache_to_init(content: str, config: dict, memory_cats: list) -> str:
    """Add cache_config and memory_categories to __init__."""
    # Find the end of self.corrections = { ... } block
    # We'll insert after the corrections block

    # Pattern: find the corrections dict closing brace
    corrections_pattern = re.compile(
        r"(        self\.corrections\s*=\s*\{[^}]*\})",
        re.DOTALL
    )
    match = corrections_pattern.search(content)
    if not match:
        # Try alternative: corrections defined inline
        corrections_pattern = re.compile(
            r"(        self\.corrections\s*=\s*\{.*?\n        \})",
            re.DOTALL
        )
        match = corrections_pattern.search(content)

    if match:
        insert_pos = match.end()
        # Build the cache config code
        if config['has_cache']:
            mem_cats_str = repr(memory_cats) if memory_cats else "['memory']"
            if config['has_l2']:
                cache_code = f"""

        # Cache configuration for memory hierarchy modeling
        self.cache_config = CacheConfig(
            has_cache=True,
            l1_latency={config['l1_latency']},
            l1_hit_rate={config['l1_hit_rate']},
            has_l2=True,
            l2_latency={config['l2_latency']},
            l2_hit_rate={config['l2_hit_rate']},
            dram_latency={config['dram_latency']},
        )
        self.memory_categories = {mem_cats_str}"""
            else:
                cache_code = f"""

        # Cache configuration for memory hierarchy modeling
        self.cache_config = CacheConfig(
            has_cache=True,
            l1_latency={config['l1_latency']},
            l1_hit_rate={config['l1_hit_rate']},
            dram_latency={config['dram_latency']},
        )
        self.memory_categories = {mem_cats_str}"""
        else:
            cache_code = """

        # No cache on this processor
        self.cache_config = None
        self.memory_categories = []"""

        content = content[:insert_pos] + cache_code + content[insert_pos:]
    else:
        print(f"  WARNING: Could not find corrections block in __init__")

    return content


def add_cache_penalty_to_analyze(content: str) -> str:
    """Add cache penalty computation at the start of analyze()."""
    # Find the analyze method and add cache penalty after profile lookup
    # Pattern: look for the profile = self.workload_profiles.get(...) line
    # and add cache penalty computation after it

    # Find the profile assignment line
    pattern = re.compile(
        r"(        profile = self\.workload_profiles\.get\([^)]+\))\n",
    )
    match = pattern.search(content)
    if not match:
        # Try alternate pattern
        pattern = re.compile(
            r"(        profile = self\.workload_profiles\[workload\])\n",
        )
        match = pattern.search(content)
    if not match:
        # Try another alternate
        pattern = re.compile(
            r"(        profile = self\.workload_profiles\.get\(workload,\s*self\.workload_profiles\['typical'\]\))\n",
        )
        match = pattern.search(content)

    if match:
        insert_pos = match.end()
        cache_penalty_code = """
        # Apply cache miss penalty to memory-accessing categories
        if hasattr(self, 'cache_config') and self.cache_config and self.cache_config.has_cache:
            penalty = self.cache_config.effective_memory_penalty()
            for cat_name in getattr(self, 'memory_categories', []):
                if cat_name in self.instruction_categories:
                    self.instruction_categories[cat_name].memory_cycles = penalty

"""
        content = content[:insert_pos] + cache_penalty_code + content[insert_pos:]
    else:
        print(f"  WARNING: Could not find profile assignment in analyze()")

    return content


def process_model_file(filepath: Path, dry_run: bool = False) -> bool:
    """Process a single model file."""
    content = filepath.read_text()

    # Skip if already has cache_config
    if has_cache_config_already(content):
        print(f"  SKIP (already has cache_config): {filepath}")
        return False

    year = get_year_from_source(content)
    if year <= 1985:
        return False

    clock_mhz = get_clock_mhz_from_source(content)
    name_lower = filepath.stem.replace('_validated', '').lower()
    memory_cats = get_memory_categories(content)
    config = estimate_cache_config(year, clock_mhz, name_lower)

    try:
        display_path = filepath.relative_to(ROOT)
    except ValueError:
        display_path = filepath
    print(f"  Processing: {display_path}")
    print(f"    Year: {year}, Clock: {clock_mhz} MHz, Memory cats: {memory_cats}")
    print(f"    Cache: has_cache={config['has_cache']}, L1 hit={config.get('l1_hit_rate', 'N/A')}, "
          f"has_L2={config.get('has_l2', False)}, DRAM={config.get('dram_latency', 'N/A')}")

    # Step 1: Add CacheConfig class/import based on file pattern
    if has_try_except_import(content):
        # Pattern A: try/except ImportError — add to import + add fallback
        new_content = add_cache_config_import(content)
        new_content = add_cache_config_fallback(new_content)
    elif has_top_level_inline_classes(content):
        # Pattern B: Top-level inline class definitions
        new_content = add_cache_config_class_inline(content)
    else:
        print(f"    WARNING: Unknown file pattern, skipping")
        return False

    # Step 3: Add cache_config to __init__
    new_content = add_cache_to_init(new_content, config, memory_cats)

    # Step 4: Add cache penalty to analyze()
    if config['has_cache'] and memory_cats:
        new_content = add_cache_penalty_to_analyze(new_content)

    if not dry_run:
        filepath.write_text(new_content)
        print(f"    UPDATED")
    else:
        print(f"    DRY RUN - would update")

    return True


def find_all_validated_files():
    """Find all *_validated.py files."""
    return sorted(MODELS_DIR.rglob("*_validated.py"))


def main():
    dry_run = '--dry-run' in sys.argv
    single = None
    if '--single' in sys.argv:
        idx = sys.argv.index('--single')
        single = Path(sys.argv[idx + 1])

    if single:
        files = [single]
    else:
        files = find_all_validated_files()

    print(f"Found {len(files)} model files")
    updated = 0
    skipped = 0

    for f in files:
        content = f.read_text()
        year = get_year_from_source(content)
        if year <= 1985:
            continue
        if process_model_file(f, dry_run):
            updated += 1
        else:
            skipped += 1

    print(f"\nDone: {updated} updated, {skipped} skipped")


if __name__ == '__main__':
    main()
