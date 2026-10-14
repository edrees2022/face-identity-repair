#!/usr/bin/env bash
set -e
echo "=================================================================="
echo "  CANDIDATE-A PAPER A: OFFLINE REPRODUCIBILITY SMOKE TEST"
echo "=================================================================="

# Detect Python interpreter with required dependencies
if [ -n "$PYTHON" ] && "$PYTHON" -c "import pandas" >/dev/null 2>&1; then
    PY_CMD="$PYTHON"
elif command -v python >/dev/null 2>&1 && python -c "import pandas" >/dev/null 2>&1; then
    PY_CMD="python"
elif [ -f "/home/eds/anaconda3/envs/uniportrait/bin/python" ]; then
    PY_CMD="/home/eds/anaconda3/envs/uniportrait/bin/python"
elif command -v python3 >/dev/null 2>&1 && python3 -c "import pandas" >/dev/null 2>&1; then
    PY_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PY_CMD="python"
elif command -v python3 >/dev/null 2>&1; then
    PY_CMD="python3"
else
    echo "Error: Python interpreter not found." >&2
    exit 1
fi

echo "Using Python interpreter: $PY_CMD"

# 1. Data Integrity Check (all 6 files)
echo ""
echo "[1/4] Auditing data integrity..."
$PY_CMD scripts/verify_data_integrity.py

# 2. Track R1-T1a: Study 2 Paired Analysis Replay & Table S9 Recalculation
echo ""
echo "[2/4] Running Track R1-T1a Analysis Replay (smoke test, 100 reps)..."
$PY_CMD scripts/run_tier1a_analysis_replay.py --reps 100

# 3. Track R1-T1b: Frozen Summary Verification
echo ""
echo "[3/4] Running Track R1-T1b Frozen Summary Verification..."
$PY_CMD scripts/run_tier1b_frozen_verification.py

# 4. Automated Pytest Suite
echo ""
echo "[4/4] Executing test suite..."
$PY_CMD -m pytest -q -p no:cacheprovider tests/

echo ""
echo "=================================================================="
echo "  SMOKE TEST RESULT: PASS — ALL CHECKS CONCORDANT"
echo "=================================================================="
