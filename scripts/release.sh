#!/bin/bash
# Release script for publishing new versions to PyPI
# Usage: ./scripts/release.sh [version] [message]
# Example: ./scripts/release.sh 0.2.0 "Add new features and bug fixes"

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

if [ $# -lt 1 ]; then
    echo -e "${RED}❌ Error: Version number required${NC}"
    echo "Usage: ./scripts/release.sh [version] [message]"
    echo "Example: ./scripts/release.sh 0.2.0 'Add new features'"
    exit 1
fi

VERSION=$1
MESSAGE=${2:-"Release version $VERSION"}

echo -e "${GREEN}🚀 Agently Release Script${NC}"
echo "======================================"
echo -e "${BLUE}Version:${NC} $VERSION"
echo -e "${BLUE}Message:${NC} $MESSAGE"
echo ""

# Validate version format
if [[ ! $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9\.]+)?$ ]]; then
    echo -e "${RED}❌ Error: Invalid version format${NC}"
    echo "Version must follow semantic versioning: MAJOR.MINOR.PATCH"
    echo "Examples: 0.1.0, 0.2.0, 1.0.0, 0.2.0a1"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Error: pyproject.toml not found${NC}"
    echo "Please run this script from the project root"
    exit 1
fi

# Check if version already exists
if git rev-parse "v$VERSION" >/dev/null 2>&1; then
    echo -e "${RED}❌ Error: Tag v$VERSION already exists${NC}"
    echo "Please use a different version number"
    exit 1
fi

# Step 1: Update version in __init__.py
echo -e "${YELLOW}📝 Step 1/6: Updating version...${NC}"
sed -i.bak "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" src/agently/__init__.py
rm -f src/agently/__init__.py.bak
echo -e "${GREEN}✓ Version updated to $VERSION${NC}"

# Step 2: Run tests
echo -e "${YELLOW}🧪 Step 2/6: Running tests...${NC}"
if ! make test > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Tests failed${NC}"
    echo "Please fix failing tests before releasing"
    exit 1
fi
echo -e "${GREEN}✓ All tests passed${NC}"

# Step 3: Run linting
echo -e "${YELLOW}🔍 Step 3/6: Running linting...${NC}"
if ! make lint > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Linting failed${NC}"
    echo "Please fix linting errors before releasing"
    exit 1
fi
echo -e "${GREEN}✓ Linting passed${NC}"

# Step 4: Run type checking
echo -e "${YELLOW}🔍 Step 4/6: Running type checking...${NC}"
if ! make type-check > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Type checking failed${NC}"
    echo "Please fix type errors before releasing"
    exit 1
fi
echo -e "${GREEN}✓ Type checking passed${NC}"

# Step 5: Commit changes
echo -e "${YELLOW}💾 Step 5/6: Committing changes...${NC}"
git add src/agently/__init__.py
git commit -m "chore: bump version to $VERSION" --no-verify
echo -e "${GREEN}✓ Changes committed${NC}"

# Step 6: Create and push tag
echo -e "${YELLOW}🏷️  Step 6/6: Creating and pushing tag...${NC}"
git tag -a "v$VERSION" -m "$MESSAGE"
git push origin master
git push origin "v$VERSION"
echo -e "${GREEN}✓ Tag v$VERSION pushed${NC}"

echo ""
echo -e "${GREEN}✅ Release preparation complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Visit https://github.com/yunlongwen/agently/releases/new"
echo "2. Select tag: v$VERSION"
echo "3. Add release notes"
echo "4. Click 'Publish release'"
echo ""
echo -e "${YELLOW}⚠️  After publishing the release:${NC}"
echo "   - GitHub Actions will automatically publish to PyPI"
echo "   - Binary packages will be built and uploaded"
echo "   - Users can install with: pip install agently==$VERSION"
echo ""
echo -e "${BLUE}📊 PyPI URL:${NC} https://pypi.org/project/agently/"
echo -e "${BLUE}📦 Release URL:${NC} https://github.com/yunlongwen/agently/releases/tag/v$VERSION"
