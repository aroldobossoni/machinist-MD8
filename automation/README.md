# BIOS Documentation Automation

Script Python para popular automaticamente campos `description`, `riskReason` e `sources` nos JSONs hierárquicos usando Google AI Mode (udm=50).

## Setup

### Configurar encoding UTF-8 (importante para Windows)

**Opção 1: Configuração temporária (apenas para sessão atual)**

```powershell
cd automation
.\set_utf8.ps1
```

**Opção 2: Configuração permanente no PowerShell**

Adiciona UTF-8 ao perfil do PowerShell para aplicar automaticamente em todas as sessões:

```powershell
cd automation
.\configure_utf8_permanent.ps1
```

Depois, feche e reabra o PowerShell ou execute: `. $PROFILE`

**Opção 3: Configuração no sistema operacional (requer admin)**

Configura UTF-8 como codificação padrão do Windows (recomendado para desenvolvimento):

```powershell
# Execute PowerShell como Administrador
cd automation
.\configure_windows_utf8.ps1
```

**Nota:** A opção 3 requer reinicialização do Windows para aplicar completamente. As opções 1 e 2 são suficientes para uso dos scripts Python.

### Criar ambiente virtual (recomendado)

**Opção 1: Usar script de setup automático**

```bash
cd automation

# Linux/WSL:
bash setup_venv.sh

# Windows PowerShell:
.\setup_venv.ps1

# Windows CMD:
setup_venv.bat
```

**Opção 2: Setup manual**

```bash
cd automation

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
.\venv\Scripts\activate.bat
# Linux/WSL:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Instalar navegador Chromium para Playwright
playwright install chromium
```

### Instalação direta no sistema (não recomendado)

```bash
pip install playwright beautifulsoup4
playwright install chromium
```

## Uso

### 1. Análise inicial da estrutura HTML

```bash
cd automation
python analyze_google_ai.py
```

Isso vai gerar:
- `test_response.html` - HTML completo da página
- `test_screenshot.png` - Screenshot visual
- Documentar seletores em `AI_SELECTORS.md`

### 2. Teste com supervisão (recomendado primeiro)

```bash
python populate_bios_docs.py --test --supervised
```

Processa apenas 1 opção com confirmação manual.

### 3. Execução completa

```bash
# Primeiras 20 opções com supervisão (recomendado)
python populate_bios_docs.py --supervised --limit 20

# Modo automático completo
python populate_bios_docs.py

# Retomar do progresso salvo
python populate_bios_docs.py --resume
```

## Estrutura de Arquivos

- `progress.json`: Progresso salvo (gerado automaticamente)
- `errors.log`: Log de erros (gerado automaticamente)
- `raw_responses/`: Respostas brutas para debug (gerado)
- `error_screenshots/`: Screenshots de erros (gerado)
- `AI_SELECTORS.md`: Documentação de seletores CSS

## Tempo Estimado

- ~396 opções no total
- ~5-8 segundos por opção (delay + fetch)
- Pausas de 60-90s a cada 20 opções
- **Total: 6-8 horas** para completar todos

## Parâmetros

- `--test`: Processa apenas 1 opção
- `--supervised`: Modo supervisão (confirma cada opção)
- `--limit N`: Limita a N opções
- `--resume`: Retoma do progresso salvo

## Tratamento de Erros

- **Timeout**: Retry automático 3x, depois pausa para intervenção
- **CAPTCHA**: Detecta e pausa para resolução manual
- **Parse falhou**: Salva resposta bruta para análise manual

## Formato dos Dados

Os campos são populados assim:

```json
{
  "description": "Texto da DESCRIÇÃO extraído",
  "riskReason": "RISCO: ... GRAU DE RISCO: ...",
  "sources": ["url1", "url2"]
}
```

O campo `risk` não é alterado (mantém valor existente).

