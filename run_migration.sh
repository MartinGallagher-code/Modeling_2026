#!/bin/bash
#
# Modeling_2026 Migration Runner
# ==============================
# Easy-to-use wrapper for the migration script
#
# Usage:
#   ./run_migration.sh              # Dry run (preview changes)
#   ./run_migration.sh --execute    # Actually perform migration
#   ./run_migration.sh --help       # Show help
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}   Modeling_2026 Migration Tool${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Check Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: python3 is required but not found${NC}"
    exit 1
fi

# Parse arguments
EXECUTE=false
FORCE=false
HELP=false
ONLY=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --execute|-e)
            EXECUTE=true
            shift
            ;;
        --force|-f)
            FORCE=true
            shift
            ;;
        --only)
            ONLY="$2"
            shift 2
            ;;
        --help|-h)
            HELP=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            HELP=true
            shift
            ;;
    esac
done

if [ "$HELP" = true ]; then
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --execute, -e    Actually perform the migration (default is dry-run)"
    echo "  --force, -f      Overwrite existing processors"
    echo "  --only NAME      Only migrate specific processor(s)"
    echo "  --help, -h       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                           # Preview what will be migrated"
    echo "  $0 --execute                 # Perform the migration"
    echo "  $0 --execute --force         # Migrate and overwrite existing"
    echo "  $0 --only pentium --execute  # Only migrate Pentium"
    echo ""
    exit 0
fi

# Build command
CMD="python3 ${SCRIPT_DIR}/migrate_old_to_main.py --repo-path ${REPO_ROOT}"

if [ "$EXECUTE" = false ]; then
    echo -e "${YELLOW}Running in DRY-RUN mode (no changes will be made)${NC}"
    echo -e "${YELLOW}Use --execute to perform actual migration${NC}"
    echo ""
    CMD="${CMD} --dry-run"
else
    echo -e "${GREEN}Running in EXECUTE mode (changes will be made)${NC}"
    echo ""
fi

if [ "$FORCE" = true ]; then
    CMD="${CMD} --force"
fi

if [ -n "$ONLY" ]; then
    CMD="${CMD} --only ${ONLY}"
fi

# Run the migration
echo -e "${BLUE}Running: ${CMD}${NC}"
echo ""

eval ${CMD}

# Post-migration steps
if [ "$EXECUTE" = true ]; then
    echo ""
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}   Post-Migration Steps${NC}"
    echo -e "${GREEN}============================================${NC}"
    echo ""
    echo "1. Review the changes:"
    echo "   git status"
    echo "   git diff --stat"
    echo ""
    echo "2. Run validation (if available):"
    echo "   python3 validate_migration.py"
    echo ""
    echo "3. Commit the changes:"
    echo "   git add ."
    echo "   git commit -m 'Migrate processors from old/ to main structure'"
    echo ""
    echo "4. Push to GitHub:"
    echo "   git push origin main"
    echo ""
fi
