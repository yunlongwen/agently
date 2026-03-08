@echo off
REM Local development runner for Agently (Windows)
REM Usage: scripts\run-local.bat [command] [args...]

setlocal enabledelayedexpansion

echo [92m🚀 Agently Local Development Runner[0m
echo ======================================

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."

REM Check if we're in the right directory
if not exist "%PROJECT_DIR%\pyproject.toml" (
    echo [91m❌ Error: Cannot find pyproject.toml[0m
    echo Please run this script from the project root or scripts directory
    exit /b 1
)

cd /d "%PROJECT_DIR%"

REM Check Python installation
echo [93m📋 Checking Python installation...[0m
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [91m❌ Error: Python is not installed or not in PATH[0m
    echo Please install Python 3.9 or higher from https://python.org
    exit /b 1
)

for /f "tokens=2" %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
echo [92m✓ Python found: %PYTHON_VERSION%[0m

REM Check if package is installed in development mode
echo [93m📦 Checking package installation...[0m
python -c "import agently" >nul 2>&1
if %errorlevel% neq 0 (
    echo [93m⚠️  Package not installed, installing in development mode...[0m
    python -m pip install -e "%PROJECT_DIR%"
    if %errorlevel% neq 0 (
        echo [91m❌ Error: Failed to install package[0m
        exit /b 1
    )
    echo [92m✓ Package installed[0m
) else (
    echo [92m✓ Package already installed[0m
)

REM Find agently executable
echo [93m🔍 Locating agently executable...[0m
set "AGENTLY_CMD="

REM Check if agently is in PATH
where agently >nul 2>&1
if %errorlevel% equ 0 (
    set "AGENTLY_CMD=agently"
    goto :found
)

REM Check common locations
if exist "%LOCALAPPDATA%\Programs\Python\Python39\Scripts\agently.exe" (
    set "AGENTLY_CMD=%LOCALAPPDATA%\Programs\Python\Python39\Scripts\agently.exe"
    goto :found
)

if exist "%LOCALAPPDATA%\Programs\Python\Python310\Scripts\agently.exe" (
    set "AGENTLY_CMD=%LOCALAPPDATA%\Programs\Python\Python310\Scripts\agently.exe"
    goto :found
)

if exist "%LOCALAPPDATA%\Programs\Python\Python311\Scripts\agently.exe" (
    set "AGENTLY_CMD=%LOCALAPPDATA%\Programs\Python\Python311\Scripts\agently.exe"
    goto :found
)

if exist "%APPDATA%\Python\Python39\Scripts\agently.exe" (
    set "AGENTLY_CMD=%APPDATA%\Python\Python39\Scripts\agently.exe"
    goto :found
)

if exist "%APPDATA%\Python\Scripts\agently.exe" (
    set "AGENTLY_CMD=%APPDATA%\Python\Scripts\agently.exe"
    goto :found
)

REM Try to find in Python's script directory
for /f "delims=" %%a in ('python -c "import sys; print(sys.exec_prefix)"') do (
    if exist "%%a\Scripts\agently.exe" (
        set "AGENTLY_CMD=%%a\Scripts\agently.exe"
        goto :found
    )
)

:found
if "!AGENTLY_CMD!"=="" (
    echo [93m⚠️  agently command not found in PATH, trying module execution...[0m
    set "AGENTLY_CMD=python -m agently.cli"
)

echo [92m✓ Using: !AGENTLY_CMD![0m
echo.

REM Run agently with provided arguments
if "%~1"=="" (
    echo [92m🎯 Running: agently[0m
    echo ======================================
    !AGENTLY_CMD!
) else (
    echo [92m🎯 Running: agently %*[0m
    echo ======================================
    !AGENTLY_CMD! %*
)

endlocal
