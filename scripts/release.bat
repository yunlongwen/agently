@echo off
REM Release script for publishing new versions to PyPI (Windows)
REM Usage: scripts\release.bat [version] [message]
REM Example: scripts\release.bat 0.2.0 "Add new features and bug fixes"

setlocal enabledelayedexpansion

if "%~1"=="" (
    echo [91m❌ Error: Version number required[0m
    echo Usage: scripts\release.bat [version] [message]
    echo Example: scripts\release.bat 0.2.0 "Add new features"
    exit /b 1
)

set "VERSION=%~1"
set "MESSAGE=%~2"
if "%MESSAGE%"=="" set "MESSAGE=Release version %VERSION%"

echo [92m🚀 Agently Release Script[0m
echo ======================================
echo [94mVersion:[0m %VERSION%
echo [94mMessage:[0m %MESSAGE%
echo.

REM Validate version format (basic check)
echo %VERSION% | findstr /R "^[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*$" >nul
if %errorlevel% neq 0 (
    echo [91m❌ Error: Invalid version format[0m
    echo Version must follow semantic versioning: MAJOR.MINOR.PATCH
    echo Examples: 0.1.0, 0.2.0, 1.0.0
    exit /b 1
)

REM Check if we're in the right directory
if not exist "pyproject.toml" (
    echo [91m❌ Error: pyproject.toml not found[0m
    echo Please run this script from the project root
    exit /b 1
)

REM Check if version already exists
git rev-parse "v%VERSION%" >nul 2>&1
if %errorlevel% equ 0 (
    echo [91m❌ Error: Tag v%VERSION% already exists[0m
    echo Please use a different version number
    exit /b 1
)

REM Step 1: Update version in __init__.py
echo [93m📝 Step 1/6: Updating version...[0m
powershell -Command "(Get-Content src\agently\__init__.py) -replace '__version__ = \".*\"', '__version__ = \"%VERSION%\"' | Set-Content src\agently\__init__.py"
echo [92m✓ Version updated to %VERSION%[0m

REM Step 2: Run tests
echo [93m🧪 Step 2/6: Running tests...[0m
make test >nul 2>&1
if %errorlevel% neq 0 (
    echo [91m❌ Error: Tests failed[0m
    echo Please fix failing tests before releasing
    exit /b 1
)
echo [92m✓ All tests passed[0m

REM Step 3: Run linting
echo [93m🔍 Step 3/6: Running linting...[0m
make lint >nul 2>&1
if %errorlevel% neq 0 (
    echo [91m❌ Error: Linting failed[0m
    echo Please fix linting errors before releasing
    exit /b 1
)
echo [92m✓ Linting passed[0m

REM Step 4: Run type checking
echo [93m🔍 Step 4/6: Running type checking...[0m
make type-check >nul 2>&1
if %errorlevel% neq 0 (
    echo [91m❌ Error: Type checking failed[0m
    echo Please fix type errors before releasing
    exit /b 1
)
echo [92m✓ Type checking passed[0m

REM Step 5: Commit changes
echo [93m💾 Step 5/6: Committing changes...[0m
git add src\agently\__init__.py
git commit -m "chore: bump version to %VERSION%" --no-verify
if %errorlevel% neq 0 (
    echo [91m❌ Error: Failed to commit changes[0m
    exit /b 1
)
echo [92m✓ Changes committed[0m

REM Step 6: Create and push tag
echo [93m🏷️  Step 6/6: Creating and pushing tag...[0m
git tag -a "v%VERSION%" -m "%MESSAGE%"
git push origin master
if %errorlevel% neq 0 (
    echo [91m❌ Error: Failed to push to master[0m
    exit /b 1
)
git push origin "v%VERSION%"
if %errorlevel% neq 0 (
    echo [91m❌ Error: Failed to push tag[0m
    exit /b 1
)
echo [92m✓ Tag v%VERSION% pushed[0m

echo.
echo [92m✅ Release preparation complete![0m
echo.
echo [94mNext steps:[0m
echo 1. Visit https://github.com/yunlongwen/agently/releases/new
echo 2. Select tag: v%VERSION%
echo 3. Add release notes
echo 4. Click 'Publish release'
echo.
echo [93m⚠️  After publishing the release:[0m
echo    - GitHub Actions will automatically publish to PyPI
echo    - Binary packages will be built and uploaded
echo    - Users can install with: pip install agently==%VERSION%
echo.
echo [94m📊 PyPI URL:[0m https://pypi.org/project/agently/
echo [94m📦 Release URL:[0m https://github.com/yunlongwen/agently/releases/tag/v%VERSION%

endlocal
