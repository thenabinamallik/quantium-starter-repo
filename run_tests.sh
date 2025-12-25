#!/usr/bin/env bash

# Exit immediately if a command fails
set -e

# -----------------------------
# Activate virtual environment
# -----------------------------
if [ -d "venv" ]; then
  source venv/Scripts/activate
else
  echo "❌ Virtual environment not found"
  exit 1
fi

# -----------------------------
# Run test suite
# -----------------------------
pytest

# -----------------------------
# If we reach here, tests passed
# -----------------------------
echo "✅ All tests passed"
exit 0
