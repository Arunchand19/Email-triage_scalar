#!/usr/bin/env bash
# run_mock_inference.sh - Run inference in mock mode (no API key needed)

set -e

echo "=========================================="
echo "  Email Triage Environment - Mock Test"
echo "=========================================="
echo ""

echo "Testing EASY task..."
EMAIL_TRIAGE_TASK=easy python inference.py --mock
echo ""

echo "Testing MEDIUM task..."
EMAIL_TRIAGE_TASK=medium python inference.py --mock
echo ""

echo "Testing HARD task..."
EMAIL_TRIAGE_TASK=hard python inference.py --mock
echo ""

echo "=========================================="
echo "  All tests complete!"
echo "=========================================="
