#!/bin/bash
#
# Convenience wrapper for Cross-Family Consistency Audit
# Usage: ./run_audit.sh [repo_path] [options]
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_PATH="${1:-.}"

# Shift to remove repo_path from args if provided
if [[ "$1" != -* ]] && [[ -n "$1" ]]; then
    shift
fi

echo "=============================================="
echo "Cross-Family Consistency Audit"
echo "=============================================="
echo "Repository: $REPO_PATH"
echo "Options: $@"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found"
    exit 1
fi

# Run the audit
python3 "$SCRIPT_DIR/cross_family_audit.py" "$REPO_PATH" "$@"
AUDIT_EXIT=$?

echo ""
echo "=============================================="

if [ $AUDIT_EXIT -eq 0 ]; then
    echo "✓ Audit completed - No errors found"
else
    echo "✗ Audit completed - Errors found"
    echo ""
    echo "To fix issues, run:"
    echo "  python3 apply_consistency_fixes.py $REPO_PATH --fix-all --dry-run"
    echo ""
    echo "Then to apply fixes:"
    echo "  python3 apply_consistency_fixes.py $REPO_PATH --fix-all"
fi

echo "=============================================="

exit $AUDIT_EXIT
