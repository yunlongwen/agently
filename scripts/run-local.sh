#!/bin/bash
# Local development runner for Agently (macOS/Linux)
# Usage: ./scripts/run-local.sh [command] [args...]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${GREEN}🚀 Agently Local Development Runner${NC}"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "$PROJECT_DIR/pyproject.toml" ]; then
    echo -e "${RED}❌ Error: Cannot find pyproject.toml${NC}"
    echo "Please run this script from the project root or scripts directory"
    exit 1
fi

cd "$PROJECT_DIR"

# Check Python installation
echo -e "${YELLOW}📋 Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Error: Python is not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"

# Check if package is installed in development mode
echo -e "${YELLOW}📦 Checking package installation...${NC}"
if ! $PYTHON_CMD -c "import agently" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Package not installed, installing in development mode...${NC}"
    $PYTHON_CMD -m pip install -e "$PROJECT_DIR"
    echo -e "${GREEN}✓ Package installed${NC}"
else
    echo -e "${GREEN}✓ Package already installed${NC}"
fi

# Find agently executable
echo -e "${YELLOW}🔍 Locating agently executable...${NC}"
AGENTLY_CMD=""

# Check common locations
if command -v agently &> /dev/null; then
    AGENTLY_CMD="agently"
elif [ -f "$HOME/.local/bin/agently" ]; then
    AGENTLY_CMD="$HOME/.local/bin/agently"
elif [ -f "/usr/local/bin/agently" ]; then
    AGENTLY_CMD="/usr/local/bin/agently"
else
    # Try to find in Python's script directory
    PYTHON_BIN_DIR=$($PYTHON_CMD -c "import sys; print(sys.exec_prefix)")/bin
    if [ -f "$PYTHON_BIN_DIR/agently" ]; then
        AGENTLY_CMD="$PYTHON_BIN_DIR/agently"
    fi
fi

if [ -z "$AGENTLY_CMD" ]; then
    echo -e "${YELLOW}⚠️  agently command not found in PATH, trying module execution...${NC}"
    AGENTLY_CMD="$PYTHON_CMD -m agently.cli"
fi

echo -e "${GREEN}✓ Using: $AGENTLY_CMD${NC}"
echo ""

# Run agently with provided arguments
if [ $# -eq 0 ]; then
    echo -e "${GREEN}🎯 Running: agently${NC}"
    echo "======================================"
    $AGENTLY_CMD
else
    echo -e "${GREEN}🎯 Running: agently $*${NC}"
    echo "======================================"
    $AGENTLY_CMD "$@"
fi
