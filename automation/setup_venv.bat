@echo off
REM setup_venv.bat
REM Script CMD para configurar ambiente virtual

echo === BIOS Documentation Automation - Setup ===
echo.

REM Verificar Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo   ERRO: Python nao encontrado!
    echo   Instale Python 3.8+ de https://www.python.org/
    pause
    exit /b 1
)
python --version
echo   OK: Python encontrado

REM Criar venv
echo [2/4] Criando ambiente virtual...
if exist venv (
    echo   Ambiente virtual ja existe, pulando criacao
) else (
    python -m venv venv
    echo   OK: Ambiente virtual criado
)

REM Ativar venv
echo [3/4] Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo   OK: Ambiente virtual ativado

REM Instalar dependências
echo [4/4] Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo   OK: Dependencias instaladas

REM Instalar navegador Chromium
echo.
echo [EXTRA] Instalando navegador Chromium para Playwright...
playwright install chromium
echo   OK: Chromium instalado

echo.
echo === Setup concluido! ===
echo.
echo Para usar:
echo   1. Ative o ambiente: venv\Scripts\activate.bat
echo   2. Execute: python analyze_google_ai.py
echo.
pause
