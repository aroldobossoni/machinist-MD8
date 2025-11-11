# BIOS Options Data - Estrutura de Arquivos

## Arquivos JSON (Fonte da verdade)

Todos os dados da documentação da BIOS estão armazenados em arquivos JSON neste diretório:

### `index.json`
Arquivo principal que lista todos os outros arquivos e contém metadados:
- Versão da BIOS
- Data de atualização
- Lista de arquivos de dados
- Descrição de cada menu

### Arquivos por menu:
- `main.json` — Menu Main (data/hora, idioma, SATA)
- `advanced.json` — Menu Advanced (ACPI, USB, CSM, PCI, Network)
- `intelrcsetup.json` — Menu IntelRCSetup (CPU, memória, QPI, IIO, PCH)
- `security.json` — Menu Security (senhas, Secure Boot)
- `boot.json` — Menu Boot (ordem de boot)

## Estrutura de cada opção

```json
{
  "menu": "Advanced",
  "submenu": "ACPI Settings",
  "option": "Enable Hibernation",
  "defaultValue": "[Enabled]",
  "description": "Controla se o sistema operacional pode usar o modo de hibernação (S4)...",
  "risk": "low",
  "riskReason": "Requer espaço em disco; falha pode causar perda de dados"
}
```

### Campos obrigatórios:
- `menu`: Menu principal (Main, Advanced, IntelRCSetup, Security, Boot)
- `submenu`: Submenu (ou `null` se for opção do menu principal)
- `option`: Nome da opção (exatamente como aparece na BIOS)
- `defaultValue`: Valor padrão (formato: `[Value]` ou número)
- `description`: Descrição em português da opção
- `risk`: Nível de risco (`none`, `low`, `high`)
- `riskReason`: Explicação do risco (ou `null` se risk for `none`)

### Campos opcionais (futuro):
- `possibleValues`: Array com valores possíveis
- `warnings`: Array de avisos específicos
- `relatedOptions`: Array de IDs de opções relacionadas
- `tags`: Array de tags para categorização

## Como editar

1. **Edição manual:** Abra o arquivo JSON no editor
2. **Validação:** Use JSON validator online ou no VS Code
3. **Teste:** Recarregue a página para ver mudanças

## Regras importantes

1. ✅ **JSON é a fonte da verdade** — todas as mudanças devem ser feitas aqui
2. ✅ **Um arquivo por menu** — facilita manutenção
3. ✅ **Sintaxe JSON correta** — aspas duplas, vírgulas, sem trailing comma
4. ✅ **Descrições em português** — claras e concisas
5. ✅ **Risk levels consistentes** — `none`, `low`, `high`
6. ✅ **riskReason obrigatório** — `null` para `none`, texto explicativo para `low`/`high`

## Estrutura do diretório

```
docs/data/
├── README.md              # Este arquivo
├── index.json             # Índice e metadados
├── main.json              # Opções do menu Main (~3 opções)
├── advanced.json          # Opções do menu Advanced (~40 opções)
├── intelrcsetup.json      # Opções do menu IntelRCSetup (~50 opções)
├── security.json          # Opções do menu Security (~2 opções)
├── boot.json              # Opções do menu Boot (~3 opções)
└── bios-options.json      # [DEPRECATED] Arquivo único antigo
```

## Próximos passos

1. Expandir todos os arquivos com todas as opções do BIOS_MENU_MAP.md
2. Criar script Python para gerar JSON automaticamente
3. Adicionar validação de schema (JSON Schema)
4. Adicionar campos opcionais (possibleValues, warnings, etc.)

---

**Última atualização:** 2024-11-10  
**Versão:** 1.0

