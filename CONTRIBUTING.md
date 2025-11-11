# 🤝 Guia de Contribuição

Obrigado pelo interesse em contribuir para o projeto Machinist MD8 BIOS Wiki!

## 📋 Como Contribuir

### 1. Melhorar Descrições de Opções da BIOS

As descrições devem seguir o padrão técnico definido:

**Estrutura de uma boa descrição:**
- O que é a opção (definição técnica)
- Para que serve (função específica)
- Impacto de alterar o valor
- Casos de uso (quando aplicável)

**Exemplo:**
```json
{
  "option": "Above 4G Decoding",
  "description": "Permite que dispositivos PCIe sejam mapeados acima do limite de 4GB de endereçamento, necessário para GPUs modernas com >4GB VRAM e para sistemas com muitos dispositivos PCIe. Requer SO 64-bit e suporte UEFI. Essencial para GPU passthrough em virtualização. Incompatível com boot legacy/MBR.",
  "risk": "high",
  "riskReason": "Incompatível com boot legacy/MBR; habilitar em sistema legacy pode impedir boot"
}
```

### 2. Classificação de Risco

Use critérios rigorosos baseados no impacto real:

#### Risk: "none"
**USO RESTRITO** - Apenas para:
- Idioma da BIOS
- Data/hora do sistema

#### Risk: "low"
- Afeta compatibilidade com hardware/software específico
- Pode degradar performance em casos particulares
- Reversível sem impedir boot
- Não causa danos permanentes

Exemplos:
- Serial Port (pode afetar console de debug)
- Smart Fan (configuração errada → superaquecimento)
- USB Mass Storage Driver (desabilitar → pen drives não funcionam)

#### Risk: "high"
Aplique quando a opção:
1. ❌ Pode impedir boot do sistema
2. 🔒 Remove proteção de segurança
3. 💻 Quebra VMs/containers/virtualização
4. ⚡ Pode danificar hardware
5. 🔧 É difícil reverter (requer CMOS clear)

Exemplos:
- CSM Support (pode impedir boot)
- Execute Disable Bit (remove proteção DEP)
- VMX/VT-x (quebra virtualização)
- Memory Frequency (pode causar danos ou instabilidade)
- Boot Order (pode impedir acesso ao sistema)

### 3. Editando os Arquivos JSON

Os dados estão em `docs/data/`:
- `main.json` - Menu Main
- `advanced.json` - Menu Advanced
- `intelrcsetup.json` - IntelRCSetup
- `security.json` - Security
- `boot.json` - Boot

**Estrutura de cada entrada:**
```json
{
  "menu": "Advanced",
  "submenu": "PCI Subsystem Settings",
  "option": "Above 4G Decoding",
  "defaultValue": "[Disabled]",
  "description": "Descrição técnica completa...",
  "risk": "high",
  "riskReason": "Explicação do risco específico (se risk != none)"
}
```

### 4. Adicionando Novas Opções

Se encontrou uma opção da BIOS que não está documentada:

1. Verifique em `BIOS_MENU_MAP.md` se a opção existe
2. Adicione no arquivo JSON correspondente ao menu
3. Siga o padrão de descrição e classificação de risco
4. Mantenha ordem alfabética dentro de cada submenu (se possível)
5. Valide o JSON após editar

### 5. Correções e Melhorias

**Tipos de contribuições bem-vindas:**
- ✅ Corrigir erros técnicos nas descrições
- ✅ Adicionar informações técnicas mais detalhadas
- ✅ Reclassificar riscos baseado em evidências
- ✅ Melhorar tradução e clareza
- ✅ Adicionar casos de uso práticos
- ✅ Corrigir valores padrão incorretos
- ✅ Melhorias na interface web (UI/UX)
- ✅ Melhorias de responsividade mobile

**NÃO contribua:**
- ❌ Informações especulativas ou não verificadas
- ❌ Opiniões pessoais sem base técnica
- ❌ Mudanças de formatação desnecessárias
- ❌ Dados sensíveis (MACs, IPs, etc.)

### 6. Processo de Pull Request

1. **Fork** o repositório
2. **Clone** seu fork localmente
3. **Crie um branch** para sua mudança:
   ```bash
   git checkout -b improve-description-vt-d
   ```
4. **Faça suas alterações** nos arquivos JSON
5. **Valide o JSON**: Use um linter JSON ou validador online
6. **Teste localmente**:
   ```bash
   cd docs
   python -m http.server 8000
   ```
   Acesse `http://localhost:8000` e verifique se as mudanças aparecem corretamente

7. **Commit** com mensagem descritiva:
   ```bash
   git commit -m "docs: improve Above 4G Decoding description and reclassify risk"
   ```

8. **Push** para seu fork:
   ```bash
   git push origin improve-description-vt-d
   ```

9. **Abra um Pull Request** com:
   - Título claro
   - Descrição do que foi alterado
   - Justificativa técnica para mudanças de risco
   - Fontes de referência (se aplicável)

### 7. Padrão de Mensagens de Commit

Use conventional commits:

- `docs:` - Melhorias de documentação
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bugs
- `style:` - Mudanças de estilo/formatação
- `refactor:` - Refatoração de código
- `test:` - Adição de testes

Exemplos:
```
docs: improve VMX description and reclassify to high risk
fix: correct default value for Memory Frequency
feat: add missing BIOS option for VT-d interrupt remapping
style: improve mobile responsiveness on option cards
```

### 8. Fontes de Referência Técnica

Para garantir precisão técnica, consulte:

**Documentação Oficial:**
- [Intel Xeon E5 v3/v4 Datasheets](https://www.intel.com/content/www/us/en/products/docs/processors/xeon/xeon-e5-v3-spec-update.html)
- [Intel C610 Chipset Documentation](https://www.intel.com/content/www/us/en/products/docs/chipsets/server-chipsets/c610-chipset-datasheet.html)
- [ACPI Specification](https://uefi.org/specifications)
- [UEFI Specification](https://uefi.org/specifications)
- [PCIe Base Specification](https://pcisig.com/specifications)

**Comunidades:**
- [r/homelab](https://reddit.com/r/homelab) - Discussões sobre hardware de servidor
- [ServeTheHome Forums](https://forums.servethehome.com/) - Comunidade técnica

### 9. Validação de JSON

Antes de fazer commit, valide o JSON:

**Online:**
- [JSONLint](https://jsonlint.com/)
- [JSON Formatter](https://jsonformatter.curiousconcept.com/)

**Linha de comando:**
```bash
python -m json.tool docs/data/advanced.json > /dev/null
```

Se houver erro, será exibido. Se não houver saída, o JSON é válido.

### 10. Código de Conduta

- 🤝 Seja respeitoso e profissional
- 📚 Baseie contribuições em fatos técnicos, não opiniões
- 🔍 Verifique informações antes de submeter
- 💬 Comunique-se claramente em Pull Requests
- 🎯 Mantenha foco em melhorar a qualidade técnica
- ⚡ Responda a feedback de forma construtiva

### 11. Dúvidas e Suporte

**Antes de abrir uma issue:**
- Verifique se já existe issue similar
- Leia a documentação em `README.md` e `AGENTS.md`
- Tente reproduzir o problema localmente

**Issues bem-vindas:**
- 🐛 Bugs na interface web
- 📝 Erros técnicos nas descrições
- 💡 Sugestões de melhorias
- ❓ Dúvidas sobre opções específicas da BIOS
- 🔧 Problemas de responsividade ou compatibilidade

### 12. Agradecimentos

Toda contribuição é valiosa! Seja uma correção de typo, uma descrição melhorada, ou uma nova funcionalidade, seu trabalho ajuda a comunidade a configurar hardware de servidor com mais segurança e eficiência.

---

## 🚀 Quick Start para Contribuidores

1. Fork e clone o repositório
2. Edite os arquivos JSON em `docs/data/`
3. Valide o JSON com linter
4. Teste localmente com `python -m http.server 8000` em `docs/`
5. Commit com mensagem descritiva
6. Abra Pull Request com justificativa técnica

**Qualquer dúvida, abra uma issue!** 💬

---

**Última atualização:** 2024-11-11

