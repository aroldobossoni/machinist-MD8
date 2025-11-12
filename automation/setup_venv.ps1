# setup_venv.ps1
# Script PowerShell para configurar ambiente virtual

# Configurar encoding UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

Write-Host "=== BIOS Documentation Automation - Setup ===" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "[1/4] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  OK: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERRO: Python nao encontrado!" -ForegroundColor Red
    Write-Host "  Instale Python 3.8+ de https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Criar venv
Write-Host "[2/4] Criando ambiente virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  Ambiente virtual ja existe, pulando criacao" -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "  OK: Ambiente virtual criado" -ForegroundColor Green
}

# Ativar venv
Write-Host "[3/4] Ativando ambiente virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "  OK: Ambiente virtual ativado" -ForegroundColor Green

# Instalar dependências
Write-Host "[4/4] Instalando dependencias..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "  OK: Dependencias instaladas" -ForegroundColor Green

# Instalar navegador Chromium
Write-Host ""
Write-Host "[EXTRA] Instalando navegador Chromium para Playwright..." -ForegroundColor Yellow
playwright install chromium
Write-Host "  OK: Chromium instalado" -ForegroundColor Green

Write-Host ""
Write-Host "=== Setup concluido! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Para usar:" -ForegroundColor Cyan
Write-Host "  1. Ative o ambiente: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  2. Execute: python analyze_google_ai.py" -ForegroundColor White
Write-Host ""
