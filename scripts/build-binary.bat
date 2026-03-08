@echo off
REM Build Agently binary locally using PyInstaller (Windows)
REM Usage: scripts\build-binary.bat

setlocal enabledelayedexpansion

echo [92m🚀 Agently Binary Builder[0m
echo ======================================

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."

cd /d "%PROJECT_DIR%"

REM Check Python installation
echo [93m📋 Checking Python installation...[0m
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [91m❌ Error: Python is not installed or not in PATH[0m
    exit /b 1
)

for /f "tokens=2" %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
echo [92m✓ Python found: %PYTHON_VERSION%[0m

REM Check if PyInstaller is installed
echo [93m📦 Checking PyInstaller...[0m
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo [93m⚠️  PyInstaller not found, installing...[0m
    python -m pip install pyinstaller
)
echo [92m✓ PyInstaller is available[0m

REM Install package in development mode
echo [93m📦 Installing agently package...[0m
python -m pip install -e "%PROJECT_DIR%" --quiet
if %errorlevel% neq 0 (
    echo [91m❌ Error: Failed to install package[0m
    exit /b 1
)
echo [92m✓ Package installed[0m

REM Detect platform
echo [93m🔍 Detecting platform...[0m
set "OS=windows"
set "ARCH=x64"

REM Check if running on ARM64
reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "ARM" >nul && set "ARCH=arm64"

echo [92m✓ Platform: %OS%-%ARCH%[0m

REM Build binary
echo [93m🔨 Building binary...[0m
echo    This may take a few minutes...
echo.

set "OUTPUT_NAME=agently-%OS%-%ARCH%.exe"

python -m PyInstaller ^
    --onefile ^
    --name "%OUTPUT_NAME%" ^
    --add-data "src/agently;agently" ^
    --hidden-import agently.cli ^
    --hidden-import agently.cli.main ^
    --hidden-import agently.cli.interactive ^
    --hidden-import agently.cli.logo ^
    --hidden-import prompt_toolkit ^
    --hidden-import click ^
    --hidden-import pydantic ^
    --hidden-import structlog ^
    --console ^
    src/agently/cli/__main__.py

REM Check if build succeeded
if exist "dist\%OUTPUT_NAME%" (
    echo.
    echo [92m✅ Build successful![0m
    echo.
    echo [94m📁 Binary location:[0m
    echo    %PROJECT_DIR%\dist\%OUTPUT_NAME%
    echo.
    echo [94m📊 Binary size:[0m
    for %%F in ("dist\%OUTPUT_NAME%") do echo    %%~zF bytes
    echo.
    echo [94m🚀 You can now run:[0m
    echo    dist\%OUTPUT_NAME%
    echo.
    echo [93m💡 To add to PATH (optional):[0m
    echo    1. Copy the binary to a folder in your PATH
    echo    2. Or add %PROJECT_DIR%\dist to your PATH
) else (
    echo [91m❌ Build failed![0m
    exit /b 1
)

endlocal
