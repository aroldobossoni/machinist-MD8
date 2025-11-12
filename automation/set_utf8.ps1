# set_utf8.ps1
# Script para configurar encoding UTF-8 no PowerShell
# Execute este script antes de rodar os scripts Python ou adicione ao seu perfil PowerShell

# Configurar encoding UTF-8 para console
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Configurar encoding padrão para cmdlets
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'

# Configurar chcp para UTF-8 (código de página 65001)
chcp 65001 | Out-Null

Write-Host "Encoding UTF-8 configurado!" -ForegroundColor Green
Write-Host "OutputEncoding: $([Console]::OutputEncoding.EncodingName)" -ForegroundColor Cyan
Write-Host "Console CodePage: $([Console]::OutputEncoding.CodePage)" -ForegroundColor Cyan

