#!/usr/bin/env pwsh
# Local development runner for Agently (PowerShell - Cross-platform)
# Usage: .\scripts\run-local.ps1 [command] [args...]

$ErrorActionPreference = "Stop"

# Colors for output
$Green = "`e[32m"
$Yellow = "`e[33m"
$Red = "`e[31m"
$NC = "`e[0m" # No Color

Write-Host "${Green}🚀 Agently Local Development Runner${NC}"
Write-Host "======================================"

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

# Check if we're in the right directory
if (-not (Test-Path "$ProjectDir\pyproject.toml")) {
    Write-Host "${Red}❌ Error: Cannot find pyproject.toml${NC}"
    Write-Host "Please run this script from the project root or scripts directory"
    exit 1
}

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

# Check if package is installed in development mode
Write-Host "${Yellow}📦 Checking package installation...${NC}"
try {
    & $PythonCmd -c "import agently" 2>&1 | Out-Null
    Write-Host "${Green}✓ Package already installed${NC}"
} catch {
    Write-Host "${Yellow}⚠️  Package not installed, installing in development mode...${NC}"
    & $PythonCmd -m pip install -e "$ProjectDir"
    Write-Host "${Green}✓ Package installed${NC}"
}

# Find agently executable
Write-Host "${Yellow}🔍 Locating agently executable...${NC}"
$AgentlyCmd = $null

# Check if agently is in PATH
if (Get-Command agently -ErrorAction SilentlyContinue) {
    $AgentlyCmd = "agently"
} else {
    # Try to find in Python's script directory
    $PythonPrefix = & $PythonCmd -c "import sys; print(sys.exec_prefix)"
    $PossiblePaths = @(
        "$PythonPrefix\Scripts\agently.exe"
        "$PythonPrefix\bin\agently"
        "$env:LOCALAPPDATA\Programs\Python\Python39\Scripts\agently.exe"
        "$env:LOCALAPPDATA\Programs\Python\Python310\Scripts\agently.exe"
        "$env:LOCALAPPDATA\Programs\Python\Python311\Scripts\agently.exe"
        "$env:APPDATA\Python\Python39\Scripts\agently.exe"
        "$env:APPDATA\Python\Scripts\agently.exe"
    )
    
    foreach ($Path in $PossiblePaths) {
        if (Test-Path $Path) {
            $AgentlyCmd = $Path
            break
        }
    }
}

if (-not $AgentlyCmd) {
    Write-Host "${Yellow}⚠️  agently command not found in PATH, trying module execution...${NC}"
    $AgentlyCmd = "$PythonCmd -m agently.cli"
}

Write-Host "${Green}✓ Using: $AgentlyCmd${NC}"
Write-Host ""

# Run agently with provided arguments
if ($args.Count -eq 0) {
    Write-Host "${Green}🎯 Running: agently${NC}"
    Write-Host "======================================"
    Invoke-Expression $AgentlyCmd
} else {
    $ArgString = $args -join " "
    Write-Host "${Green}🎯 Running: agently $ArgString${NC}"
    Write-Host "======================================"
    Invoke-Expression "$AgentlyCmd $ArgString"
}
