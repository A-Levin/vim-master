#!/bin/bash

# Test runner script for VimMaster
set -e

echo "🧪 Running VimMaster tests..."

# Create scripts directory if it doesn't exist
mkdir -p scripts

# Change to project root
cd "$(dirname "$0")/.."

# Run tests with coverage
echo "📊 Running tests with coverage..."
uv run pytest app/tests/ \
    --cov=app \
    --cov-report=html \
    --cov-report=term-missing \
    --verbose \
    --tb=short

echo "✅ Tests completed!"
echo "📈 Coverage report generated in htmlcov/"

# Optional: Open coverage report in browser
if command -v xdg-open &> /dev/null; then
    echo "🌐 Opening coverage report in browser..."
    xdg-open htmlcov/index.html
fi