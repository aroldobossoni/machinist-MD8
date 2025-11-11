# Machinist MD8 BIOS Wiki - GitHub Pages

Documentação interativa da BIOS da placa mãe Machinist MD8 (X99 MD8).

## 🌐 Acesso

**GitHub Pages:** https://aroldobossoni.github.io/selfhost/machinist-MD8/

## 🎯 Funcionalidades

- 📋 **Tabela completa** de todas as opções da BIOS
- 🔍 **Busca e filtros** por menu, opção e nível de risco
- 🎨 **Tema claro/escuro** com detecção automática
- 🔍✨ **Integração com Google Search AI** para explicações
- 📱 **Responsivo** para desktop e mobile
- 🌲 **Hierarquia visual** de menus e submenus

## 📂 Estrutura de arquivos

```
docs/
├── index.html              # Página principal (single-page app)
├── data/                   # Dados da BIOS (fonte da verdade)
│   ├── index.json          # Índice e metadados
│   ├── main.json           # Opções do menu Main
│   ├── advanced.json       # Opções do menu Advanced
│   ├── intelrcsetup.json   # Opções do menu IntelRCSetup
│   ├── security.json       # Opções do menu Security
│   ├── boot.json           # Opções do menu Boot
│   ├── README.md           # Documentação da estrutura de dados
│   └── CHANGELOG.md        # Histórico de mudanças
├── SERVIDOR_LOCAL.md       # Instruções para teste local
└── .nojekyll               # Desabilita processamento Jekyll
```

## 📝 Como editar

### Editar opções da BIOS

1. Abra o arquivo JSON correspondente em `docs/data/`
2. Edite a descrição, risco ou outros campos
3. Salve o arquivo
4. Recarregue a página para ver mudanças

### Adicionar nova opção

Adicione um novo objeto no arquivo JSON apropriado:

```json
{
  "menu": "Advanced",
  "submenu": "USB Configuration",
  "option": "Nova Opção",
  "defaultValue": "[Enabled]",
  "description": "Descrição clara e concisa da opção.",
  "risk": "none"
}
```

### Estrutura de uma opção

- `menu`: Menu principal (Main, Advanced, IntelRCSetup, Security, Boot)
- `submenu`: Submenu ou `null` (use `>` para submenus aninhados)
- `option`: Nome exato da opção na BIOS
- `defaultValue`: Valor padrão entre colchetes `[Value]` ou número
- `description`: Texto em português, claro e objetivo
- `risk`: `none` (verde), `low` (amarelo), `high` (vermelho)

## 🔒 Privacidade

Todas as informações específicas de hardware foram generalizadas:
- Modelos de discos → `[Device Name]`
- Endereços MAC → `XX:XX:XX:XX:XX:XX`
- IDs de CPU → `XXXXXXXX`
- Versões de drivers → `X.XXX`

## 🎨 Temas

O site detecta automaticamente o tema preferido do sistema operacional e permite alternar entre:
- 🌙 **Tema Escuro** (padrão)
- ☀️ **Tema Claro**

A preferência é salva no navegador.

## 🔍 Integração Google Search AI

Cada opção tem um botão "🔍✨ IA" que:
1. Gera automaticamente uma pergunta sobre a opção
2. Abre Google Search AI em popup window
3. Em mobile: popup fullscreen
4. Em desktop: popup lateral (30% da tela)

## 📊 Estatísticas

- **Total de opções documentadas:** ~87 (em expansão)
- **Menus principais:** 5 (Main, Advanced, IntelRCSetup, Security, Boot)
- **Arquivos JSON:** 5 + 1 índice
- **Suporte:** Desktop e Mobile

## 🛠 Tecnologias

- HTML5 puro
- CSS3 com variáveis CSS
- Vanilla JavaScript (sem frameworks)
- JSON para dados
- GitHub Pages para hospedagem

## 📖 Documentação adicional

- `data/README.md` — Estrutura de dados JSON
- `data/CHANGELOG.md` — Histórico de mudanças
- `SERVIDOR_LOCAL.md` — Instruções de desenvolvimento local

---

**Versão:** 1.0  
**Última atualização:** 2024-11-10  
**BIOS:** Machinist MD8 - M94X8 3.00 x64

