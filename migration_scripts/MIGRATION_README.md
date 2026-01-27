# Modeling_2026 Migration Scripts

This package contains scripts to migrate processors from the legacy `old/` directory structure to the new standardized main repository structure.

## Quick Start

```bash
# 1. Copy all scripts to your repository root
cp migrate_old_to_main.py /path/to/Modeling_2026/
cp run_migration.sh /path/to/Modeling_2026/
cp validate_migration.py /path/to/Modeling_2026/

# 2. Make shell script executable
chmod +x /path/to/Modeling_2026/run_migration.sh

# 3. Preview what will be migrated (dry run)
cd /path/to/Modeling_2026
./run_migration.sh

# 4. Perform the actual migration
./run_migration.sh --execute

# 5. Validate the results
python3 validate_migration.py --verbose

# 6. Commit and push
git add .
git commit -m "Migrate processors from old/ to main structure"
git push origin main
```

## Scripts Included

### 1. `migrate_old_to_main.py`

The main migration script. Handles:
- Discovering processors in `old/` that aren't in main directories
- Converting old naming conventions to standardized names
- Restructuring files into `current/`, `archive/`, `validation/`, `docs/` folders
- Generating README files for migrated processors
- Preserving historical documentation
- Updating `index.json`

**Usage:**
```bash
# Dry run (preview only)
python3 migrate_old_to_main.py --dry-run

# Execute migration
python3 migrate_old_to_main.py

# Force overwrite existing processors
python3 migrate_old_to_main.py --force

# Migrate only specific processors
python3 migrate_old_to_main.py --only pentium i80486 alpha21064
```

### 2. `run_migration.sh`

Shell wrapper for easy execution:
```bash
./run_migration.sh              # Dry run
./run_migration.sh --execute    # Actual migration
./run_migration.sh --force -e   # Migration with overwrite
./run_migration.sh --help       # Show help
```

### 3. `validate_migration.py`

Post-migration validation script. Checks:
- Directory structure is correct
- All expected subdirectories exist
- Python files have valid syntax
- JSON files are parseable
- `index.json` is complete and accurate

**Usage:**
```bash
# Validate only
python3 validate_migration.py

# Validate with verbose output
python3 validate_migration.py --verbose

# Validate and fix issues
python3 validate_migration.py --fix
```

## What Gets Migrated

### From Old Structure:
```
old/
├── CPU Models - through 1985/
│   ├── Intel 8080/
│   │   ├── intel_8080_model.py
│   │   ├── intel_8080_model.json
│   │   └── README.md
│   └── ...
└── CPU Models - after 1985/
    ├── Intel Pentium/
    └── DEC Alpha 21064/
```

### To New Structure:
```
intel/
├── i8080/
│   ├── README.md
│   ├── current/
│   │   └── i8080_validated.py
│   ├── archive/
│   ├── validation/
│   │   └── i8080_validation.json
│   └── docs/
│       └── [original documentation]
└── pentium/
    └── [same structure]

other/
└── alpha21064/
    └── [same structure]
```

## Processor Name Mapping

| Old Name | New Name | Family |
|----------|----------|--------|
| Intel 80486 | i80486 | intel |
| Intel Pentium | pentium | intel |
| Intel i860 | i860 | intel |
| Motorola 68030 | m68030 | motorola |
| Motorola 68040 | m68040 | motorola |
| Motorola 68060 | m68060 | motorola |
| DEC Alpha 21064 | alpha21064 | other |
| AIM PPC 601 | ppc601 | other |
| ARM2 | arm2 | other |
| ARM3 | arm3 | other |
| ARM6 | arm6 | other |
| Sun SPARC | sparc | other |
| HP PA-RISC | pa_risc | other |
| Transputer | t414 | other |

## Historical Documentation

The following files from `old/` are preserved to `docs/historical/`:
- `Modeling_2026_Master_Prompt.docx`
- `Modeling_2026_Recreation_Guide_v2.docx`
- `Pre1986_CPU_Modeling_Lessons_Learned.docx`
- `METHODOLOGY.md`
- `PROCESSOR_EVOLUTION_1971-1985.md`
- `PROJECT_STATUS.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- Any `.zip` archives

## After Migration

### Recommended Steps:

1. **Review migrated files:**
   ```bash
   git status
   git diff --stat
   ```

2. **Run validation:**
   ```bash
   python3 validate_migration.py --verbose
   ```

3. **Test a few models:**
   ```bash
   cd intel/pentium/current
   python3 -c "import pentium_validated; print('OK')"
   ```

4. **Commit changes:**
   ```bash
   git add .
   git commit -m "Migrate processors from old/ to main structure"
   ```

5. **Consider archiving old/:**
   - Keep as-is (current approach)
   - Move to separate branch: `git checkout -b archive-old && git push`
   - Delete after confirming migration: `rm -rf old/` (not recommended until verified)

## Troubleshooting

### "old directory not found"
Make sure you're running from the repository root where `old/` exists.

### "Permission denied"
Make the shell script executable: `chmod +x run_migration.sh`

### "Processor already exists"
Use `--force` to overwrite, or manually merge the files.

### "Syntax error in migrated file"
The original file had issues. Check `old/` for the original and fix manually.

## Requirements

- Python 3.6+
- No external dependencies (uses only stdlib)
- Git (for committing changes)
- Bash (for shell wrapper, optional)

## License

Part of the Modeling_2026 project - Research and Educational Use
