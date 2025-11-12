#!/bin/bash
# setup_venv.sh
# Script Bash para configurar ambiente virtual

set -e

echo "=== BIOS Documentation Automation - Setup ==="
echo ""

# Verificar Python
echo "[1/4] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "  ERRO: Python3 nao encontrado!"
    echo "  Instale Python 3.8+ usando seu gerenciador de pacotes"
    exit 1
fi
python3 --version
echo "  OK: Python encontrado"

# Criar venv
echo "[2/4] Criando ambiente virtual..."
if [ -d "venv" ]; then
    echo "  Ambiente virtual ja existe, pulando criacao"
else
python3 -m venv venv
    echo "  OK: Ambiente virtual criado"
fi

# Ativar venv
echo "[3/4] Ativando ambiente virtual..."
source venv/bin/activate
echo "  OK: Ambiente virtual ativado"

# Instalar dependências
echo "[4/4] Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt
echo "  OK: Dependencias instaladas"

# Instalar navegador Chromium
echo ""
echo "[EXTRA] Instalando navegador Chromium para Playwright..."
playwright install chromium
echo "  OK: Chromium instalado"

echo ""
echo "=== Setup concluido! ==="
echo ""
echo "Para usar:"
echo "  1. Ative o ambiente: source venv/bin/activate"
echo "  2. Execute: python analyze_google_ai.py"
echo ""
