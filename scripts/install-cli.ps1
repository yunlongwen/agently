#!/usr/bin/env pwsh
# Install agently CLI to system PATH (PowerShell - Cross-platform)
# Usage: .\scripts\install-cli.ps1

$ErrorActionPreference = "Stop"

# Colors for output
$Green = "`e[32m"
$Yellow = "`e[33m"
$Red = "`e[31m"
$Blue = "`e[34m"
$NC = "`e[0m" # No Color

Write-Host "${Green}🚀 Agently CLI Installer${NC}"
Write-Host "======================================"

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

Set-Location $ProjectDir

# Check Python installation
Write-Host "${Yellow}📋 Checking Python installation...${NC}"
$PythonCmd = $null

if (Get-Command python3 -ErrorAction SilentlyContinue) {
    $PythonCmd = "python3"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonCmd = "python"
} else {
    Write-Host "${Red}❌ Error: Python is not installed${NC}"
    exit 1
}

$PythonVersion = & $PythonCmd --version 2>&1
Write-Host "${Green}✓ Python found: $PythonVersion${NC}"

# Install package in development mode
Write-Host "${Yellow}📦 Installing agently package...${NC}"
& $PythonCmd -m pip install -e "$ProjectDir" --Quiet
Write-Host "${Green}✓ Package installed${NC}"

# Find where agently was installed
Write-Host "${Yellow}🔍 Locating agently executable...${NC}"
$AgentlyPath = $null

# Get Python's script directory
$PythonPrefix = & $PythonCmd -c "import sys; print(sys.exec_prefix)"
$PossiblePaths = @(
    "$PythonPrefix\Scripts\agently.exe"
    "$PythonPrefix\bin\agently"
    "$env:LOCALAPPDATA\Programs\Python\Python39\Scripts\agently.exe"
    "$env:LOCALAPPDATA\Programs\Python\Python310\Scripts\agently.exe"
    "$env:LOCALAPPDATA\Programs\Python\Python311\Scripts\agently.exe"
    "$env:LOCALAPPDATA\Programs\Python\Python312\Scripts\agently.exe"
    "$env:APPDATA\Python\Python39\Scripts\agently.exe"
    "$env:APPDATA\Python\Scripts\agently.exe"
    "$HOME/.local/bin/agently"
)

foreach ($Path in $PossiblePaths) {
    if (Test-Path $Path) {
        $AgentlyPath = $Path
        break
    }
}

if (-not $AgentlyPath) {
    Write-Host "${Red}❌ Error: Could not find agently executable${NC}"
    exit 1
}

Write-Host "${Green}✓ Found agently at: $AgentlyPath${NC}"

# Check if agently is in PATH
if (Get-Command agently -ErrorAction SilentlyContinue) {
    Write-Host "${Green}✓ agently is already in PATH${NC}"
    Write-Host ""
    Write-Host "${Blue}🎉 Installation complete! You can now use:${NC}"
    Write-Host "   agently          - Show logo and help"
    Write-Host "   agently chat     - Start interactive chat"
    Write-Host "   agently version  - Show version"
    exit 0
}

# Add to PATH
Write-Host "${Yellow}⚠️  agently is not in PATH${NC}"
Write-Host ""

# Get the directory containing agently
$AgentlyDir = Split-Path -Parent $AgentlyPath

Write-Host "${Yellow}🔧 Adding agently to PATH...${NC}"
Write-Host "   Adding: $AgentlyDir"
Write-Host ""

# Add to user PATH
$CurrentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($CurrentPath -notlike "*$AgentlyDir*") {
    [Environment]::SetEnvironmentVariable("PATH", "$CurrentPath;$AgentlyDir", "User")
    Write-Host "${Green}✓ PATH updated${NC}"
} else {
    Write-Host "${Green}✓ PATH already contains agently directory${NC}"
}

Write-Host ""
Write-Host "${Blue}🎉 Installation complete!${NC}"
Write-Host ""
Write-Host "${Yellow}⚠️  Please restart your terminal to apply changes${NC}"
Write-Host ""
Write-Host "${Blue}Then you can use:${NC}"
Write-Host "   agently          - Show logo and help"
Write-Host "   agently chat     - Start interactive chat"
Write-Host "   agently version  - Show version"
