# configure_windows_utf8.ps1
# Script para configurar UTF-8 como codificacao padrao do Windows
# REQUER ELEVACAO DE PRIVILEGIOS (Execute como Administrador)

Write-Host "=== Configuracao UTF-8 no Windows (Sistema Operacional) ===" -ForegroundColor Cyan
Write-Host ""

# Verificar se está executando como administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERRO: Este script requer privilegios de administrador!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Para executar como administrador:" -ForegroundColor Yellow
    Write-Host "  1. Clique com botao direito no PowerShell" -ForegroundColor White
    Write-Host "  2. Selecione 'Executar como administrador'" -ForegroundColor White
    Write-Host "  3. Execute este script novamente" -ForegroundColor White
    Write-Host ""
    Write-Host "OU execute no PowerShell como admin:" -ForegroundColor Yellow
    Write-Host "  Start-Process powershell -Verb RunAs -ArgumentList '-File', '$(Resolve-Path $PSCommandPath)'" -ForegroundColor White
    exit 1
}

Write-Host "[OK] Executando como administrador" -ForegroundColor Green
Write-Host ""

# Configurar UTF-8 como codificação padrão do sistema
Write-Host "[1/2] Configurando UTF-8 como codificacao padrao do Windows..." -ForegroundColor Yellow

try {
    # Habilitar UTF-8 como código de página padrão (Windows 10 1903+)
    # Isso requer reinicialização para ter efeito completo
    $regPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Nls\CodePage"
    $regValue = "ACP"
    
    $currentACP = Get-ItemProperty -Path $regPath -Name $regValue -ErrorAction SilentlyContinue
    
    if ($currentACP.ACP -ne "65001") {
        Write-Host "  Configurando ACP (Active Code Page) para UTF-8 (65001)..." -ForegroundColor Gray
        Set-ItemProperty -Path $regPath -Name $regValue -Value "65001" -Type String
        Write-Host "  OK: ACP configurado para UTF-8" -ForegroundColor Green
        Write-Host "  AVISO: Reinicie o Windows para aplicar completamente" -ForegroundColor Yellow
    } else {
        Write-Host "  ACP ja esta configurado para UTF-8" -ForegroundColor Green
    }
    
    # Configurar OEMCP também
    $regValueOEM = "OEMCP"
    $currentOEMCP = Get-ItemProperty -Path $regPath -Name $regValueOEM -ErrorAction SilentlyContinue
    
    if ($currentOEMCP.OEMCP -ne "65001") {
        Write-Host "  Configurando OEMCP (OEM Code Page) para UTF-8 (65001)..." -ForegroundColor Gray
        Set-ItemProperty -Path $regPath -Name $regValueOEM -Value "65001" -Type String
        Write-Host "  OK: OEMCP configurado para UTF-8" -ForegroundColor Green
    } else {
        Write-Host "  OEMCP ja esta configurado para UTF-8" -ForegroundColor Green
    }
    
} catch {
    Write-Host "  ERRO: Falha ao configurar registro do Windows" -ForegroundColor Red
    Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Configurar variáveis de ambiente do usuário
Write-Host ""
Write-Host "[2/2] Configurando variaveis de ambiente..." -ForegroundColor Yellow

try {
    # Configurar PYTHONIOENCODING para UTF-8
    [Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
    Write-Host "  OK: PYTHONIOENCODING configurado" -ForegroundColor Green
    
    # Configurar PYTHONUTF8 (Python 3.7+)
    [Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User")
    Write-Host "  OK: PYTHONUTF8 configurado" -ForegroundColor Green
    
} catch {
    Write-Host "  ERRO: Falha ao configurar variaveis de ambiente" -ForegroundColor Red
    Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Configuracao concluida! ===" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANTE:" -ForegroundColor Yellow
Write-Host "  - Reinicie o Windows para aplicar mudancas no registro" -ForegroundColor White
Write-Host "  - Ou feche e reabra todas as janelas do PowerShell" -ForegroundColor White
Write-Host ""
Write-Host "Variaveis de ambiente configuradas:" -ForegroundColor Cyan
Write-Host "  PYTHONIOENCODING=utf-8" -ForegroundColor White
Write-Host "  PYTHONUTF8=1" -ForegroundColor White
Write-Host ""

