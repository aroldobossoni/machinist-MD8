# parse_bios_tree.py

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class BIOSTreeParser:
    def __init__(self, md_file: str = "BIOS_MENU_MAP.md"):
        self.md_file = md_file
        self.tree_lines = []
        self.menus = {}
        
    def read_tree_section(self):
        """Extrai apenas a seção da árvore ASCII do arquivo MD"""
        with open(self.md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Encontra o bloco de código entre ```
        tree_match = re.search(r'```\n(.*?)\n```', content, re.DOTALL)
        if tree_match:
            tree_content = tree_match.group(1)
            self.tree_lines = tree_content.split('\n')
            # Remove primeira linha "Aptio Setup Utility"
            if self.tree_lines and 'Aptio Setup Utility' in self.tree_lines[0]:
                self.tree_lines = self.tree_lines[1:]
        else:
            raise ValueError("Árvore ASCII não encontrada no arquivo MD")
    
    def get_indent_level(self, line: str) -> int:
        """Calcula nível de indentação baseado em caracteres ASCII"""
        # Conta ocorrências de │ (vertical bar) que indicam níveis de profundidade
        vertical_bars = line.count('│')
        return vertical_bars
    
    def parse_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parseia uma linha e retorna dict com tipo e conteúdo"""
        if not line.strip() or line.strip() == '│':
            return None
        
        # Remove caracteres de árvore ASCII
        clean = re.sub(r'^[│├└\s─]+', '', line).strip()
        
        if not clean:
            return None
        
        # Identifica tipo de item
        item = {'raw': clean}
        
        # Submenu (termina com >)
        if clean.endswith('>'):
            item['type'] = 'submenu'
            item['name'] = clean[:-1].strip()
            return item
        
        # Item configurável (começa com -)
        if clean.startswith('-'):
            item['type'] = 'option'
            content = clean[1:].strip()
            
            # Extrai nome e valor
            if ':' in content:
                name, value_part = content.split(':', 1)
                item['name'] = name.strip()
                
                # Extrai valor padrão
                value_part = value_part.strip()
                
                # Ignora valores entre parênteses
                if value_part.startswith('(') and value_part.endswith(')'):
                    item['value'] = None
                # Valor entre colchetes (mantém os colchetes para consistência)
                elif '[' in value_part and ']' in value_part:
                    match = re.search(r'(\[[^\]]+\])', value_part)
                    if match:
                        item['value'] = match.group(1)
                # Valor numérico direto
                elif value_part and not value_part.startswith('('):
                    item['value'] = value_part
                else:
                    item['value'] = None
            else:
                item['name'] = content
                item['value'] = None
            
            return item
        
        # Item informativo (começa com •)
        if clean.startswith('•'):
            item['type'] = 'info'
            item['content'] = clean[1:].strip()
            return item
        
        # Seção descritiva (texto simples)
        item['type'] = 'section'
        item['name'] = clean
        return item
    
    def build_hierarchy(self) -> Dict[str, Any]:
        """Constrói estrutura hierárquica da árvore"""
        root = {'type': 'root', 'children': []}
        stack = [(0, root)]  # (indent_level, node)
        
        for line in self.tree_lines:
            if not line.strip():
                continue
            
            indent = self.get_indent_level(line)
            item = self.parse_line(line)
            
            if not item:
                continue
            
            # Encontra o pai correto baseado na indentação
            while len(stack) > 1 and stack[-1][0] >= indent:
                stack.pop()
            
            parent = stack[-1][1]
            
            # Cria nó
            node = {
                'type': item['type'],
                'name': item.get('name') or item.get('content', ''),
            }
            
            if item['type'] == 'option' and 'value' in item:
                node['defaultValue'] = item['value']
                # Adiciona campos para documentação futura
                node['description'] = ''
                node['risk'] = 'none'
                node['riskReason'] = ''
                node['sources'] = []
            
            if item['type'] == 'info':
                node['content'] = item['content']
            
            if item['type'] in ['submenu', 'section']:
                node['children'] = []
            
            # Adiciona ao pai
            if 'children' not in parent:
                parent['children'] = []
            parent['children'].append(node)
            
            # Adiciona à pilha se pode ter filhos
            if item['type'] in ['submenu', 'section']:
                stack.append((indent, node))
        
        return root
    
    def split_by_main_menus(self, root: Dict[str, Any]) -> Dict[str, Any]:
        """Divide árvore em menus principais"""
        menus = {}
        menu_names = {
            'Main': 'main',
            'Advanced': 'advanced',
            'IntelRCSetup': 'intelrcsetup',
            'Security': 'security',
            'Boot': 'boot',
            'Save & Exit': 'saveexit'
        }
        
        for child in root.get('children', []):
            name = child.get('name', '')
            # Identifica menu principal (pode ser type='section' ou type='submenu')
            for full_name, short_name in menu_names.items():
                if name == full_name or name.startswith(full_name):
                    # Converte section para submenu para manter consistência
                    if child.get('type') == 'section':
                        child['type'] = 'submenu'
                    menus[short_name] = child
                    break
        
        return menus
    
    def save_json_files(self, output_dir: str = "docs/data"):
        """Salva cada menu em arquivo JSON separado"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        self.read_tree_section()
        root = self.build_hierarchy()
        menus = self.split_by_main_menus(root)
        
        for menu_name, menu_data in menus.items():
            # Gera arquivos sem prefixo "map-"
            output_file = Path(output_dir) / f"{menu_name}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(menu_data, f, ensure_ascii=False, indent=2)
            print(f"[OK] Gerado: {output_file}")
        
        print(f"\n[INFO] Total de arquivos gerados: {len(menus)}")
        return menus


def main():
    """Gera arquivos JSON hierárquicos a partir do BIOS_MENU_MAP.md"""
    parser = BIOSTreeParser()
    parser.save_json_files()
    print("\n[INFO] Arquivos JSON hierarquicos gerados com sucesso!")
    print("[INFO] Cada opcao inclui campos: description, risk, riskReason (vazios para preenchimento futuro)")


if __name__ == "__main__":
    main()
