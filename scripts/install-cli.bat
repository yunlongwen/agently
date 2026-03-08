@echo off
REM Install agently CLI to system PATH (Windows)
REM Usage: scripts\install-cli.bat

setlocal enabledelayedexpansion

echo [92m🚀 Agently CLI Installer[0m
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
    echo Please install Python 3.9 or higher from https://python.org
    exit /b 1
)

for /f "tokens=2" %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
echo [92m✓ Python found: %PYTHON_VERSION%[0m

REM Install package in development mode
echo [93m📦 Installing agently package...[0m
python -m pip install -e "%PROJECT_DIR%" --quiet
if %errorlevel% neq 0 (
    echo [91m❌ Error: Failed to install package[0m
    exit /b 1
)
echo [92m✓ Package installed[0m

REM Find where agently was installed
echo [93m🔍 Locating agently executable...[0m
set "AGENTLY_PATH="

REM Check common locations
for %%p in (
    "%LOCALAPPDATA%\Programs\Python\Python39\Scripts\agently.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\Scripts\agently.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\Scripts\agently.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\Scripts\agently.exe"
    "%APPDATA%\Python\Python39\Scripts\agently.exe"
    "%APPDATA%\Python\Scripts\agently.exe"
) do (
    if exist "%%~p" (
        set "AGENTLY_PATH=%%~p"
        goto :found
    )
)

REM Try to find in Python's script directory
for /f "delims=" %%a in ('python -c "import sys; print(sys.exec_prefix)"') do (
    if exist "%%a\Scripts\agently.exe" (
        set "AGENTLY_PATH=%%a\Scripts\agently.exe"
        goto :found
    )
)

:found
if "!AGENTLY_PATH!"=="" (
    echo [91m❌ Error: Could not find agently executable[0m
    exit /b 1
)

echo [92m✓ Found agently at: !AGENTLY_PATH![0m

REM Check if agently is in PATH
where agently >nul 2>&1
if %errorlevel% equ 0 (
    echo [92m✓ agently is already in PATH[0m
    echo.
    echo [94m🎉 Installation complete! You can now use:[0m
    echo    agently          - Show logo and help
    echo    agently chat     - Start interactive chat
    echo    agently version  - Show version
    exit /b 0
)

REM Add to PATH
echo [93m⚠️  agently is not in PATH[0m
echo.

REM Get the directory containing agently
for %%F in ("!AGENTLY_PATH!") do set "AGENTLY_DIR=%%~dpF"

REM Remove trailing backslash
if "!AGENTLY_DIR:~-1!"=="\" set "AGENTLY_DIR=!AGENTLY_DIR:~0,-1!"

echo [93m🔧 Adding agently to PATH...[0m
echo    Adding: !AGENTLY_DIR!
echo.

REM Add to user PATH using setx
setx PATH "%PATH%;!AGENTLY_DIR!" >nul 2>&1
if %errorlevel% neq 0 (
    echo [91m❌ Error: Failed to update PATH. Please run as Administrator.[0m
    echo.
    echo [93mManual installation:[0m
    echo 1. Open System Properties ^> Advanced ^> Environment Variables
    echo 2. Edit "Path" variable under User variables
    echo 3. Add: !AGENTLY_DIR!
    echo 4. Click OK and restart your terminal
    exit /b 1
)

echo [92m✓ PATH updated[0m
echo.
echo [94m🎉 Installation complete![0m
echo.
echo [93m⚠️  Please restart your terminal to apply changes[0m
echo.
echo [94mThen you can use:[0m
echo    agently          - Show logo and help
echo    agently chat     - Start interactive chat
echo    agently version  - Show version

endlocal
