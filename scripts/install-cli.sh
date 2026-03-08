#!/bin/bash
# Install agently CLI to system PATH (macOS/Linux)
# Usage: ./scripts/install-cli.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Agently CLI Installer${NC}"
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

# Install package in development mode
echo -e "${YELLOW}📦 Installing agently package...${NC}"
$PYTHON_CMD -m pip install -e "$PROJECT_DIR" --quiet
echo -e "${GREEN}✓ Package installed${NC}"

# Find where agently was installed
echo -e "${YELLOW}🔍 Locating agently executable...${NC}"
AGENTLY_PATH=""

# Get Python's user script directory
USER_SCRIPT_DIR=$($PYTHON_CMD -c "import site; print(site.USER_BASE + '/bin')" 2>/dev/null || echo "")
SYSTEM_SCRIPT_DIR=$($PYTHON_CMD -c "import sys; print(sys.exec_prefix + '/bin')" 2>/dev/null || echo "")

# Check possible locations
if [ -f "$USER_SCRIPT_DIR/agently" ]; then
    AGENTLY_PATH="$USER_SCRIPT_DIR/agently"
elif [ -f "$SYSTEM_SCRIPT_DIR/agently" ]; then
    AGENTLY_PATH="$SYSTEM_SCRIPT_DIR/agently"
elif [ -f "$HOME/.local/bin/agently" ]; then
    AGENTLY_PATH="$HOME/.local/bin/agently"
fi

if [ -z "$AGENTLY_PATH" ]; then
    echo -e "${RED}❌ Error: Could not find agently executable${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Found agently at: $AGENTLY_PATH${NC}"

# Check if agently is in PATH
if command -v agently &> /dev/null; then
    echo -e "${GREEN}✓ agently is already in PATH${NC}"
    echo ""
    echo -e "${BLUE}🎉 Installation complete! You can now use:${NC}"
    echo "   agently          - Show logo and help"
    echo "   agently chat     - Start interactive chat"
    echo "   agently version  - Show version"
    exit 0
fi

# Add to PATH
echo -e "${YELLOW}⚠️  agently is not in PATH${NC}"
echo ""

# Determine shell configuration file
SHELL_CONFIG=""
if [ -n "$ZSH_VERSION" ] || [ "$SHELL" = "/bin/zsh" ] || [ "$SHELL" = "/usr/bin/zsh" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ] || [ "$SHELL" = "/bin/bash" ] || [ "$SHELL" = "/usr/bin/bash" ]; then
    if [ -f "$HOME/.bash_profile" ]; then
        SHELL_CONFIG="$HOME/.bash_profile"
    else
        SHELL_CONFIG="$HOME/.bashrc"
    fi
else
    SHELL_CONFIG="$HOME/.profile"
fi

# Get the directory containing agently
AGENTLY_DIR=$(dirname "$AGENTLY_PATH")

echo -e "${YELLOW}🔧 Adding agently to PATH...${NC}"
echo "   Shell config: $SHELL_CONFIG"
echo "   Adding: export PATH=\"$AGENTLY_DIR:\$PATH\""
echo ""

# Add to shell config
echo "" >> "$SHELL_CONFIG"
echo "# Added by agently installer" >> "$SHELL_CONFIG"
echo "export PATH=\"$AGENTLY_DIR:\$PATH\"" >> "$SHELL_CONFIG"

echo -e "${GREEN}✓ PATH updated in $SHELL_CONFIG${NC}"
echo ""
echo -e "${BLUE}🎉 Installation complete!${NC}"
echo ""
echo -e "${YELLOW}⚠️  Please run the following command to apply changes:${NC}"
echo "   source $SHELL_CONFIG"
echo ""
echo -e "${BLUE}Then you can use:${NC}"
echo "   agently          - Show logo and help"
echo "   agently chat     - Start interactive chat"
echo "   agently version  - Show version"
