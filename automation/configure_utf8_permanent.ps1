# configure_utf8_permanent.ps1
# Script para configurar encoding UTF-8 permanentemente no PowerShell

Write-Host "=== Configuracao Permanente de UTF-8 no PowerShell ===" -ForegroundColor Cyan
Write-Host ""

# Verificar se o perfil PowerShell existe
$profilePath = $PROFILE.CurrentUserAllHosts
$profileDir = Split-Path -Parent $profilePath

Write-Host "[1/3] Verificando perfil PowerShell..." -ForegroundColor Yellow
Write-Host "  Perfil: $profilePath" -ForegroundColor Gray

# Criar diretório do perfil se não existir
if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    Write-Host "  OK: Diretorio criado" -ForegroundColor Green
}

# Configuração UTF-8 para adicionar ao perfil
$utf8Config = @"

# Configuracao UTF-8 para scripts Python
# Adicionado automaticamente por configure_utf8_permanent.ps1
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
`$OutputEncoding = [System.Text.Encoding]::UTF8
`$PSDefaultParameterValues['*:Encoding'] = 'utf8'
`$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'

# Configurar chcp para UTF-8 (codigo de pagina 65001)
chcp 65001 | Out-Null

"@

# Verificar se já existe configuração UTF-8 no perfil
Write-Host "[2/3] Verificando configuracoes existentes..." -ForegroundColor Yellow
$needsUpdate = $true

if (Test-Path $profilePath) {
    $profileContent = Get-Content $profilePath -Raw -ErrorAction SilentlyContinue
    if ($profileContent -and $profileContent -match "Configuracao UTF-8 para scripts Python") {
        Write-Host "  Configuracao UTF-8 ja existe no perfil" -ForegroundColor Yellow
        $response = Read-Host "  Deseja atualizar? (S/N)"
        if ($response -ne "S" -and $response -ne "s") {
            $needsUpdate = $false
        }
    }
}

if ($needsUpdate) {
    Write-Host "[3/3] Adicionando configuracao UTF-8 ao perfil..." -ForegroundColor Yellow
    
    # Adicionar ao perfil
    if (Test-Path $profilePath) {
        # Verificar se já tem a configuração
        $currentContent = Get-Content $profilePath -Raw
        if ($currentContent -notmatch "Configuracao UTF-8 para scripts Python") {
            Add-Content -Path $profilePath -Value "`n$utf8Config" -Encoding UTF8
            Write-Host "  OK: Configuracao adicionada ao perfil existente" -ForegroundColor Green
        } else {
            Write-Host "  Configuracao ja existe, pulando..." -ForegroundColor Yellow
        }
    } else {
        # Criar novo perfil
        Set-Content -Path $profilePath -Value $utf8Config -Encoding UTF8
        Write-Host "  OK: Perfil criado com configuracao UTF-8" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "=== Configuracao concluida! ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Para aplicar as mudancas:" -ForegroundColor Cyan
    Write-Host "  1. Feche e reabra o PowerShell" -ForegroundColor White
    Write-Host "  OU" -ForegroundColor White
    Write-Host "  2. Execute: . `$PROFILE" -ForegroundColor White
    Write-Host ""
    Write-Host "Perfil localizado em: $profilePath" -ForegroundColor Gray
} else {
    Write-Host "  Nenhuma alteracao realizada" -ForegroundColor Yellow
}

