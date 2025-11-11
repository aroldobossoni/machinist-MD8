# Machinist MD8 - BIOS Documentation

## Visão Geral

Este repositório contém documentação completa da BIOS da placa mãe Machinist MD8, incluindo mapeamento detalhado de todos os menus, submenus e opções disponíveis.

## Conteúdo

- **BIOS_MENU_MAP.md** - Árvore completa de menus da BIOS
- **fotos/** - Screenshots originais da BIOS (78 imagens)

## Estrutura da BIOS

A BIOS da Machinist MD8 está organizada em 6 menus principais:

1. **Main** - Informações do sistema, data/hora, configuração SATA
2. **Advanced** - Configurações avançadas de CPU, USB, rede, serial port, TPM
3. **Chipset** - Configurações do chipset, gráficos, PCH-IO
4. **Boot** - Ordem de boot e prioridades
5. **Security** - Senhas e Secure Boot
6. **Save & Exit** - Salvar/descartar alterações

## Como Usar

### Navegação na BIOS

- **F1** - Ajuda geral
- **F2** - Valores anteriores
- **F5** - Descartar alterações e sair
- **F9** - Restaurar padrões
- **F10** - Salvar alterações e sair
- **↑↓** - Navegar entre itens
- **←→** - Alterar valores
- **Enter** - Entrar em submenu
- **ESC** - Sair/Voltar

### Acessar a BIOS

1. Pressione **DEL** ou **F2** durante o POST (Power-On Self-Test)
2. Use as teclas de navegação para percorrer os menus
3. Sempre salve as alterações antes de sair (F10)

## Especificações Suportadas

### Hardware
- **Processador:** Intel multi-core com Hyper-Threading
- **Memória:** DDR3/DDR4
- **Armazenamento:** SATA (múltiplas portas), NVMe
- **Expansão:** PCI Express (Gen1/2/3)
- **Conectividade:** USB 2.0/3.0, Ethernet
- **Áudio:** HD Audio integrado

### Recursos
- Intel Virtualization Technology (VT-x)
- Intel VT-d Technology
- Intel Turbo Boost
- C-States e gerenciamento de energia
- SMART Self Test
- TPM 2.0 (PTT/dTPM)
- Secure Boot
- ME (Management Engine)

## Configurações Importantes

### CPU
- Hyper-Threading
- Virtualization (VT-x/VT-d)
- Power Management (C-States)
- Core Count

### Boot
- Boot Mode: UEFI/Legacy
- Secure Boot
- Boot Order

### Storage
- SATA Mode: AHCI/IDE
- NVMe Support

## Avisos

⚠️ **ATENÇÃO:**
- Alterações incorretas na BIOS podem causar instabilidade do sistema
- Mantenha backup das configurações funcionais
- Use "Restore Defaults" (F9) se houver problemas
- Algumas opções requerem hardware específico

## Documentação Adicional

Para informações detalhadas sobre cada opção e submenu, consulte:
- [BIOS_MENU_MAP.md](BIOS_MENU_MAP.md) - Mapa completo com todas as opções

## Licença

Este projeto é mantido para fins de documentação e referência.

## Contribuições

Para contribuir com a documentação:
1. Verifique a precisão das informações
2. Adicione screenshots se necessário
3. Mantenha a estrutura organizada
4. Documente todas as alterações

---

**Última Atualização:** 09/11/2025
**Versão da Documentação:** 1.0
**Fonte:** Screenshots da BIOS (78 imagens)

