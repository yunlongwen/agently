#!/bin/bash
# Build Agently binary locally using PyInstaller
# Usage: ./scripts/build-binary.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Agently Binary Builder${NC}"
echo "======================================"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

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

# Check if PyInstaller is installed
echo -e "${YELLOW}📦 Checking PyInstaller...${NC}"
if ! $PYTHON_CMD -c "import PyInstaller" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  PyInstaller not found, installing...${NC}"
    $PYTHON_CMD -m pip install pyinstaller
fi
echo -e "${GREEN}✓ PyInstaller is available${NC}"

# Install package in development mode
echo -e "${YELLOW}📦 Installing agently package...${NC}"
$PYTHON_CMD -m pip install -e "$PROJECT_DIR" --quiet
echo -e "${GREEN}✓ Package installed${NC}"

# Detect platform
echo -e "${YELLOW}🔍 Detecting platform...${NC}"
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

# Normalize architecture names
case $ARCH in
    x86_64)
        ARCH="x64"
        ;;
    arm64|aarch64)
        ARCH="arm64"
        ;;
esac

echo -e "${GREEN}✓ Platform: $OS-$ARCH${NC}"

# Build binary
echo -e "${YELLOW}🔨 Building binary...${NC}"
echo "   This may take a few minutes..."
echo ""

OUTPUT_NAME="agently-$OS-$ARCH"

$PYTHON_CMD -m PyInstaller \
    --onefile \
    --name "$OUTPUT_NAME" \
    --add-data "src/agently:agently" \
    --hidden-import agently.cli \
    --hidden-import agently.cli.main \
    --hidden-import agently.cli.interactive \
    --hidden-import agently.cli.logo \
    --hidden-import prompt_toolkit \
    --hidden-import click \
    --hidden-import pydantic \
    --hidden-import structlog \
    --console \
    src/agently/cli/__main__.py

# Check if build succeeded
if [ -f "dist/$OUTPUT_NAME" ]; then
    echo ""
    echo -e "${GREEN}✅ Build successful!${NC}"
    echo ""
    echo -e "${BLUE}📁 Binary location:${NC}"
    echo "   $(pwd)/dist/$OUTPUT_NAME"
    echo ""
    echo -e "${BLUE}📊 Binary size:${NC}"
    ls -lh "dist/$OUTPUT_NAME" | awk '{print "   " $5}'
    echo ""
    echo -e "${BLUE}🚀 You can now run:${NC}"
    echo "   ./dist/$OUTPUT_NAME"
    echo ""
    echo -e "${YELLOW}💡 To install system-wide (optional):${NC}"
    echo "   sudo cp dist/$OUTPUT_NAME /usr/local/bin/agently"
else
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi
