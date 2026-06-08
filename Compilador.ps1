$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "=== Compilador AutoMatch Accept ===" -ForegroundColor Cyan

python -m PyInstaller --version 2>$null
if (-not $?) {
    Write-Host "PyInstaller no encontrado. Instalando..." -ForegroundColor Yellow
    python -m pip install pyinstaller
    if (-not $?) { Write-Host "Fallo instalando PyInstaller." -ForegroundColor Red; exit 1 }
}

Write-Host "Limpiando build/ y dist/..." -ForegroundColor Yellow
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

Write-Host "Compilando..." -ForegroundColor Yellow
python -m PyInstaller --clean LoLAcceptButton.spec
if (-not $?) { Write-Host "Compilacion fallo." -ForegroundColor Red; exit 1 }

$exe = Join-Path $PSScriptRoot "dist\AutoMatch Accept.exe"
if (Test-Path $exe) {
    Write-Host "Listo: $exe" -ForegroundColor Green
} else {
    Write-Host "No se genero el .exe esperado." -ForegroundColor Red
    exit 1
}
