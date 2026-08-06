# PocketRelay One-Tap Installer for Windows
# Usage in PowerShell:
# iwr -useb https://raw.githubusercontent.com/Anasukun/Pocket-Relay/main/install.ps1 | iex

$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   📱 PocketRelay One-Tap Installer (Windows)    " -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check for uv
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "[1/3] 'uv' package manager not found. Installing uv..." -ForegroundColor Yellow
    try {
        Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "User") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    } catch {
        Write-Host "Failed to install 'uv' automatically. Please ensure PowerShell execution policy allows scripts." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[1/3] 'uv' found!" -ForegroundColor Green
}

Write-Host "[2/3] Installing PocketRelay globally..." -ForegroundColor Yellow
try {
    uv tool install git+https://github.com/Anasukun/Pocket-Relay.git --force
} catch {
    Write-Host "Failed to install PocketRelay via uv tool install." -ForegroundColor Red
    exit 1
}

# Ensure user PATH includes uv bin path
$uvBinDir = "$env:USERPROFILE\.local\bin"
if (Test-Path $uvBinDir) {
    if ($env:Path -notlike "*$uvBinDir*") {
        $env:Path += ";$uvBinDir"
    }
}

Write-Host "[3/3] PocketRelay installed successfully! 🎉" -ForegroundColor Green
Write-Host ""
Write-Host "Starting PocketRelay Setup Wizard..." -ForegroundColor Cyan
Write-Host ""

if (Get-Command pocketrelay -ErrorAction SilentlyContinue) {
    pocketrelay init
} else {
    uv run pocketrelay init
}
