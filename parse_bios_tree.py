# parse_bios_tree.py

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import random
import time

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
            output_file = Path(output_dir) / f"map-{menu_name}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(menu_data, f, ensure_ascii=False, indent=2)
            print(f"[OK] Gerado: {output_file}")
        
        print(f"\n[INFO] Total de arquivos gerados: {len(menus)}")
        return menus


class BIOSValidator:
    def __init__(self, map_dir: str = "docs/data"):
        self.map_dir = Path(map_dir)
        self.existing_jsons = []
        self.map_jsons = []
        
    def load_jsons(self):
        """Carrega JSONs existentes e map-*.json"""
        # JSONs existentes (flat)
        for json_file in ['main.json', 'advanced.json', 'intelrcsetup.json', 
                          'security.json', 'boot.json']:
            path = self.map_dir / json_file
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    self.existing_jsons.append({
                        'file': json_file,
                        'data': json.load(f)
                    })
        
        # map-*.json (hierárquico)
        for json_file in self.map_dir.glob('map-*.json'):
            with open(json_file, 'r', encoding='utf-8') as f:
                self.map_jsons.append({
                    'file': json_file.name,
                    'data': json.load(f)
                })
    
    def flatten_hierarchy(self, node: Dict, menu: str = "", submenu: str = "") -> List[Dict]:
        """Converte estrutura hierárquica em lista flat"""
        items = []
        
        if node.get('type') == 'option':
            items.append({
                'menu': menu,
                'submenu': submenu if submenu else None,
                'option': node.get('name', ''),
                'defaultValue': node.get('defaultValue')
            })
        
        # Recursão em filhos
        for child in node.get('children', []):
            if child.get('type') == 'submenu':
                # Atualiza submenu path
                new_submenu = f"{submenu} > {child.get('name')}" if submenu else child.get('name')
                items.extend(self.flatten_hierarchy(child, menu, new_submenu))
            else:
                items.extend(self.flatten_hierarchy(child, menu, submenu))
        
        return items
    
    def compare_random_samples(self, num_samples: int = 10, delay: float = 2.0):
        """Compara amostras aleatórias lado a lado"""
        self.load_jsons()
        
        if not self.existing_jsons or not self.map_jsons:
            print("[ERRO] JSONs nao encontrados")
            return
        
        print("[INFO] Iniciando validacao por amostragem aleatoria...\n")
        time.sleep(1)
        
        for i in range(num_samples):
            # Escolhe JSON aleatório
            existing = random.choice(self.existing_jsons)
            
            # Encontra map-*.json correspondente
            map_name = existing['file'].replace('.json', '')
            map_json = next((m for m in self.map_jsons if f"map-{map_name}" in m['file']), None)
            
            if not map_json:
                continue
            
            # Escolhe item aleatório do JSON flat
            if not existing['data']:
                continue
            flat_item = random.choice(existing['data'])
            
            # Flatten do map-*.json para comparar
            menu_name = map_json['data'].get('name', '')
            map_flat = self.flatten_hierarchy(map_json['data'], menu=menu_name)
            
            # Busca item correspondente
            map_item = next((m for m in map_flat if m['option'] == flat_item['option']), None)
            
            # Exibe comparação
            print(f"================================================================")
            print(f"[SAMPLE] Amostra {i+1}/{num_samples}")
            print(f"================================================================")
            print(f"\n[FILE] Arquivo: {existing['file']} vs {map_json['file']}")
            print(f"\n{'FLAT JSON (existente)':<50} | {'MAP JSON (gerado)':<50}")
            print(f"{'-'*50} | {'-'*50}")
            
            # Garantir que None seja convertido para 'N/A'
            flat_menu = flat_item.get('menu') or 'N/A'
            flat_submenu = flat_item.get('submenu') or 'N/A'
            flat_option = flat_item.get('option') or 'N/A'
            flat_value = flat_item.get('defaultValue') or 'N/A'
            
            map_menu = (map_item.get('menu') if map_item else None) or 'N/A'
            map_submenu = (map_item.get('submenu') if map_item else None) or 'N/A'
            map_option = (map_item.get('option') if map_item else None) or 'N/A'
            map_value = (map_item.get('defaultValue') if map_item else None) or 'N/A'
            
            print(f"Menu: {flat_menu:<42} | Menu: {map_menu:<42}")
            print(f"Submenu: {flat_submenu:<39} | Submenu: {map_submenu:<39}")
            print(f"Option: {flat_option:<40} | Option: {map_option:<40}")
            print(f"Value: {flat_value:<41} | Value: {map_value:<41}")
            
            # Status de correspondência
            if map_item:
                match = (
                    flat_item.get('option') == map_item.get('option') and
                    flat_item.get('defaultValue') == map_item.get('defaultValue')
                )
                status = "[OK] MATCH" if match else "[WARN] DIFF"
            else:
                status = "[ERROR] NOT FOUND IN MAP"
            
            print(f"\n{status}\n")
            
            # Pausa entre amostras
            time.sleep(delay)


def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'validate':
        # Modo validação
        validator = BIOSValidator()
        num_samples = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        delay = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
        validator.compare_random_samples(num_samples, delay)
    else:
        # Modo geração
        parser = BIOSTreeParser()
        parser.save_json_files()
        print("\n[INFO] Para validar: python parse_bios_tree.py validate [num_samples] [delay]")


if __name__ == "__main__":
    main()

