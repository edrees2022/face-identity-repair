@echo off
echo ==================================================================
echo   CANDIDATE-A PAPER A: OFFLINE REPRODUCIBILITY SMOKE TEST
echo ==================================================================

echo [1/4] Auditing data integrity...
python scripts\verify_data_integrity.py
if errorlevel 1 exit /b 1

echo [2/4] Running Track R1-T1a Analysis Replay...
python scripts\run_tier1a_analysis_replay.py --reps 100
if errorlevel 1 exit /b 1

echo [3/4] Running Track R1-T1b Frozen Summary Verification...
python scripts\run_tier1b_frozen_verification.py
if errorlevel 1 exit /b 1

echo [4/4] Executing test suite...
pytest -q -p no:cacheprovider tests\
if errorlevel 1 exit /b 1

echo ==================================================================
echo   SMOKE TEST RESULT: PASS — ALL CHECKS CONCORDANT
echo ==================================================================
