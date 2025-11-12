# populate_bios_docs.py
# Script principal para popular documentação BIOS usando Google AI Mode
# -*- coding: utf-8 -*-

import json
import sys
import io
import time
import random
import re
import argparse

# Configurar encoding UTF-8 para stdout/stderr no Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from urllib.parse import quote_plus
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# Configurações
PROMPT_TEMPLATE = 'Explique de forma objetiva em 40 palavras a opção "{option}" em "{menu}" na BIOS da placa mãe Machinist MD8 X99 em tópicos: DESCRIÇÃO(para que serve, o que faz):, RISCO:(se pode causar travamento de POST e o GRAU DE RISCO:(NEHUM, BAIXO, MÉDIO, ALTO, CERTAMENTE))'

DELAY_MIN = 3
DELAY_MAX = 8
BATCH_SIZE = 20
BATCH_PAUSE_MIN = 60
BATCH_PAUSE_MAX = 90

# Caminhos relativos ao diretório raiz do projeto (um nível acima de automation/)
BASE_DIR = Path(__file__).parent.parent
JSON_FILES = [
    BASE_DIR / 'docs/data/main.json',
    BASE_DIR / 'docs/data/advanced.json',
    BASE_DIR / 'docs/data/intelrcsetup.json',
    BASE_DIR / 'docs/data/security.json',
    BASE_DIR / 'docs/data/boot.json',
    BASE_DIR / 'docs/data/saveexit.json'
]

AUTOMATION_DIR = Path(__file__).parent
PROGRESS_FILE = AUTOMATION_DIR / 'progress.json'
ERROR_LOG = AUTOMATION_DIR / 'errors.log'
RAW_RESPONSES_DIR = AUTOMATION_DIR / 'raw_responses'
ERROR_SCREENSHOTS_DIR = AUTOMATION_DIR / 'error_screenshots'

# Criar diretórios se não existirem
RAW_RESPONSES_DIR.mkdir(exist_ok=True)
ERROR_SCREENSHOTS_DIR.mkdir(exist_ok=True)


def load_hierarchical_json(file_path):
    """Carrega JSON hierárquico"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_options_from_hierarchy(node, menu="", submenu="", path=[], file=""):
    """Extrai todas as opções com description vazio da árvore hierárquica"""
    options = []
    
    if node.get('type') == 'option' and node.get('description') == '':
        options.append({
            'file': file,
            'menu': menu,
            'submenu': submenu,
            'option': node.get('name', ''),
            'json_path': path.copy()
        })
    
    # Recursão em filhos
    children = node.get('children', [])
    for idx, child in enumerate(children):
        new_path = path + ['children', str(idx)]
        
        if child.get('type') == 'submenu':
            new_submenu = f"{submenu} > {child.get('name')}" if submenu else child.get('name')
            options.extend(extract_options_from_hierarchy(child, menu, new_submenu, new_path, file))
        elif child.get('type') == 'section':
            # Sections não alteram submenu path
            options.extend(extract_options_from_hierarchy(child, menu, submenu, new_path, file))
        else:
            options.extend(extract_options_from_hierarchy(child, menu, submenu, new_path, file))
    
    return options


def fetch_google_ai_response(prompt, page, retry_count=3):
    """Busca resposta do Google AI Mode"""
    url = f"https://www.google.com/search?q={quote_plus(prompt)}&udm=50"
    
    for attempt in range(retry_count):
        try:
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Aguardar resposta carregar - verificar múltiplas vezes
            max_wait = 120  # Máximo 120 segundos (aumentado para dar tempo após CAPTCHA)
            wait_interval = 2  # Verificar a cada 2 segundos
            waited = 0
            response_ready = False
            captcha_resolved = False
            
            while waited < max_wait and not response_ready:
                time.sleep(wait_interval)
                waited += wait_interval
                
                current_url = page.url
                html = page.content()
                
                # Verificar CAPTCHA primeiro
                if 'captcha' in html.lower() or 'unusual traffic' in html.lower() or 'recaptcha' in html.lower():
                    if not captcha_resolved:
                        screenshot_path = ERROR_SCREENSHOTS_DIR / f'captcha_{int(time.time())}.png'
                        page.screenshot(path=str(screenshot_path))
                        print(f"\n⚠️  CAPTCHA detectado! Screenshot: {screenshot_path}")
                        print(f"[INFO] Resolva o CAPTCHA no navegador e aguarde a resposta aparecer...")
                        print(f"[INFO] O script continuara verificando automaticamente apos resolver")
                        input("Quando a resposta da IA aparecer, pressione ENTER para continuar verificacao...")
                    captcha_resolved = True
                    time.sleep(3)  # Aguardar após resolver
                    # Continuar verificando
                    continue
                
                # Se estava em CAPTCHA e agora não está mais, foi resolvido
                if captcha_resolved == False and 'captcha' not in html.lower():
                    captcha_resolved = True
                    print(f"[OK] CAPTCHA resolvido! Aguardando redirecionamento e resposta...")
                    time.sleep(5)  # Aguardar redirecionamento
                    continue
                
                # Verificar se URL mudou (redirecionamento após CAPTCHA) ou se já está na página de busca
                if 'search' in current_url.lower() and 'udm=50' in current_url:
                    # Verificar se resposta apareceu (buscar por marcadores esperados)
                    if ('DESCRIÇÃO' in html or 'descrição' in html.lower() or 
                        'RISCO' in html or 'GRAU DE RISCO' in html or
                        'AI Overview' in html or 'Generative AI' in html or
                        len(html) > 50000):  # Resposta geralmente tem muito HTML
                        # Aguardar mais 5 segundos para garantir que está completo
                        print(f"[OK] Resposta detectada! Aguardando finalizacao...")
                        time.sleep(5)
                        # Verificar novamente
                        html = page.content()
                        if 'DESCRIÇÃO' in html or 'descrição' in html.lower() or 'RISCO' in html:
                            print(f"[OK] Resposta confirmada!")
                            response_ready = True
                            break
            
            if not response_ready:
                print(f"[AVISO] Timeout aguardando resposta (esperado {max_wait}s)")
                if attempt < retry_count - 1:
                    continue
            
            # Extrair texto da resposta
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Estratégia de extração:
            # 1. Buscar por elementos com texto longo que contenham marcadores esperados
            # 2. Nota: Seletores específicos devem ser atualizados após analyze_google_ai.py
            
            response_text = ""
            sources = []
            
            # Buscar por marcadores esperados na resposta
            has_markers = 'DESCRIÇÃO' in html or 'descrição' in html.lower() or 'RISCO' in html
            
            if has_markers:
                # Tentar encontrar container principal da resposta
                # Estratégias múltiplas:
                
                # 1. Buscar por divs com muito texto
                main_containers = soup.find_all(['div', 'section', 'article'], 
                                                class_=lambda x: x and ('answer' in str(x).lower() or 
                                                                       'response' in str(x).lower() or
                                                                       'ai' in str(x).lower()))
                
                if not main_containers:
                    # 2. Buscar por elementos com texto que contém marcadores
                    for element in soup.find_all(['p', 'div', 'span', 'li']):
                        text = element.get_text(separator=' ', strip=True)
                        if text and len(text) > 100:
                            if 'DESCRIÇÃO' in text or 'descrição' in text.lower() or 'RISCO' in text:
                                response_text += text + "\n\n"
                
                # 3. Se ainda não encontrou, pegar todo texto visível da página
                if not response_text:
                    # Remover scripts e styles
                    for script in soup(["script", "style", "nav", "header", "footer"]):
                        script.decompose()
                    
                    # Pegar texto principal
                    body = soup.find('body')
                    if body:
                        response_text = body.get_text(separator='\n', strip=True)
                
                # Buscar links de referência (fontes)
                for link in soup.find_all('a', href=True):
                    href = link.get('href', '')
                    # Filtrar links do Google e manter apenas externos
                    if (href.startswith('http') and 
                        'google.com' not in href and 
                        'youtube.com' not in href and
                        len(href) < 200):  # Evitar URLs muito longas
                        sources.append(href)
            
            if response_text:
                # Limpar texto extraído
                lines = [line.strip() for line in response_text.split('\n') if line.strip()]
                response_text = '\n'.join(lines)
                
                return {
                    'full_text': response_text.strip(),
                    'sources': list(set(sources))[:5]  # Limitar a 5 fontes únicas
                }
            
            # Se não encontrou resposta, tentar novamente
            if attempt < retry_count - 1:
                delay = [5, 10, 20][attempt]
                print(f"[RETRY] Tentativa {attempt + 1}/{retry_count}, resposta nao encontrada, aguardando {delay}s...")
                time.sleep(delay)
            else:
                print(f"[ERRO] Resposta nao encontrada apos {retry_count} tentativas")
        
        except Exception as e:
            if attempt < retry_count - 1:
                delay = [5, 10, 20][attempt]
                print(f"[ERRO] {e}, retry em {delay}s...")
                time.sleep(delay)
            else:
                print(f"[ERRO] Falha apos {retry_count} tentativas: {e}")
                raise
    
    return None


def parse_ai_response(full_text):
    """Parse da resposta da IA extraindo DESCRIÇÃO e RISCO+GRAU"""
    if not full_text:
        return None
    
    # Limpar texto: remover textos da UI do Google
    text = full_text
    
    # Remover textos antes da resposta real (tudo antes de "DESCRIÇÃO")
    desc_start = text.find('DESCRIÇÃO')
    if desc_start == -1:
        desc_start = text.lower().find('descrição')
    
    if desc_start != -1:
        text = text[desc_start:]
    
    # Remover textos após a resposta (texto de rodapé do Google)
    end_markers = [
        'A IA pode cometer erros',
        'Agradecemos a colaboração',
        ' sites BIOS',  # Quando começa a aparecer links
        'Mostrar tudo',
        'Dispensar'
    ]
    
    for marker in end_markers:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
            break
    
    # Normalizar: remover bullets (•) e normalizar espaços
    text = text.replace('•', '')
    text = ' '.join(text.split())
    
    # Extrair DESCRIÇÃO - captura até encontrar "RISCO"
    # Padrão: DESCRIÇÃO (texto dentro de parênteses): CONTEÚDO_AQUI RISCO
    desc_pattern = r'DESCRIÇÃO\s*\([^)]+\)\s*:\s*(.+?)(?=\s+RISCO\s*\(|$)'
    desc_match = re.search(desc_pattern, text, re.IGNORECASE)
    
    if not desc_match:
        print(f"[DEBUG] Nao encontrou DESCRIÇAO no texto limpo")
        print(f"[DEBUG] Primeiros 200 chars: {text[:200]}")
        return None
    
    description = desc_match.group(1).strip()
    
    # Extrair RISCO - captura até encontrar "GRAU DE RISCO"
    risk_pattern = r'RISCO\s*\([^)]+\)\s*:\s*(.+?)(?=\s+GRAU\s+DE\s+RISCO|$)'
    risk_match = re.search(risk_pattern, text, re.IGNORECASE)
    
    risk_text = ""
    if risk_match:
        risk_text = risk_match.group(1).strip()
    
    # Extrair GRAU DE RISCO - pode ter dois formatos:
    # 1. "GRAU DE RISCO: BAIXO (explicação)"
    # 2. "GRAU DE RISCO: BAIXO"
    grade_pattern = r'GRAU\s+DE\s+RISCO\s*:\s*(\w+)(?:\s*\(([^)]+)\))?'
    grade_match = re.search(grade_pattern, text, re.IGNORECASE)
    
    grade_text = ""
    if grade_match:
        # Pegar o grau (BAIXO, MÉDIO, ALTO, etc)
        grade_level = grade_match.group(1).strip().upper()
        # Pegar explicação opcional entre parênteses
        grade_explanation = grade_match.group(2).strip() if grade_match.group(2) else ""
        
        if grade_explanation:
            grade_text = f"{grade_level} ({grade_explanation})"
        else:
            grade_text = grade_level
    
    # Combinar GRAU DE RISCO e RISCO em riskReason
    risk_reason = ""
    if grade_text:
        risk_reason = f"GRAU DE RISCO: {grade_text}"
        if risk_text:
            risk_reason += f". RISCO: {risk_text}"
    elif risk_text:
        risk_reason = f"RISCO: {risk_text}"
    
    # Limpar espaços extras e normalizar
    description = ' '.join(description.split())
    risk_reason = ' '.join(risk_reason.split())
    
    # Limitar tamanho se necessário (remover se ficar muito longo)
    if len(description) > 500:
        description = description[:497] + '...'
    
    return {
        'description': description,
        'risk_reason': risk_reason
    }


def update_json_option(json_tree, json_path, updates):
    """Atualiza uma opção específica na árvore JSON"""
    current = json_tree
    
    # Navegar até o nó usando json_path
    for key in json_path:
        if isinstance(current, dict):
            if key in current:
                current = current[key]
            elif key.isdigit() and 'children' in current:
                idx = int(key)
                if idx < len(current['children']):
                    current = current['children'][idx]
                else:
                    return json_tree  # Path inválido
            else:
                return json_tree  # Path inválido
        elif isinstance(current, list):
            if key.isdigit():
                idx = int(key)
                if idx < len(current):
                    current = current[idx]
                else:
                    return json_tree
            else:
                return json_tree
    
    # Atualizar campos do nó option
    if isinstance(current, dict) and current.get('type') == 'option':
        if 'description' in updates:
            current['description'] = updates['description']
        if 'risk_reason' in updates:
            current['riskReason'] = updates['risk_reason']
        if 'sources' in updates:
            current['sources'] = updates['sources']
    
    return json_tree


def save_json_files(all_jsons):
    """Salva todos os JSONs modificados"""
    for file_path_str, json_data in all_jsons.items():
        file_path = Path(file_path_str)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"[OK] Salvo: {file_path.relative_to(BASE_DIR)}")


def save_progress(data):
    """Salva progresso"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_progress():
    """Carrega progresso salvo"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def log_error(message, option_info=None):
    """Registra erro no log"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(ERROR_LOG, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")
        if option_info:
            f.write(f"  Opção: {option_info}\n")


def save_raw_response(option_name, text):
    """Salva resposta bruta para debug"""
    safe_name = re.sub(r'[^\w\-_]', '_', option_name)
    file_path = RAW_RESPONSES_DIR / f"{safe_name}.txt"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return file_path


def main():
    parser = argparse.ArgumentParser(description='Popular documentação BIOS com Google AI')
    parser.add_argument('--test', action='store_true', help='Processar apenas 1 opção')
    parser.add_argument('--supervised', action='store_true', help='Modo supervisão (confirma cada opção)')
    parser.add_argument('--limit', type=int, help='Limitar número de opções')
    parser.add_argument('--resume', action='store_true', help='Retomar do progresso salvo')
    args = parser.parse_args()
    
    print("=" * 60)
    print("BIOS Documentation Automation")
    print("=" * 60)
    
    # Carregar todos os JSONs
    print("\n[1/8] Carregando JSONs hierárquicos...")
    all_jsons = {}
    for json_file in JSON_FILES:
        file_path = Path(json_file)
        if file_path.exists():
            all_jsons[str(json_file)] = load_hierarchical_json(file_path)
            print(f"  [OK] {file_path.relative_to(BASE_DIR)}")
        else:
            print(f"  [ERRO] {file_path.relative_to(BASE_DIR)} (nao encontrado)")
    
    # Extrair opções pendentes
    print("\n[2/8] Extraindo opções com description vazio...")
    all_options = []
    for json_file, json_data in all_jsons.items():
        menu_name = json_data.get('name', '')
        file_options = extract_options_from_hierarchy(json_data, menu=menu_name, file=json_file)
        all_options.extend(file_options)
        print(f"  {json_file}: {len(file_options)} opções")
    
    print(f"\nTotal de opções pendentes: {len(all_options)}")
    
    # Carregar progresso
    print("\n[3/8] Verificando progresso...")
    progress = load_progress()
    processed = set()
    if progress and args.resume:
        last = progress.get('last_processed', {})
        if last:
            print(f"  Retomando de: {last.get('file')} > {last.get('option')}")
            # Filtrar opções já processadas
            found_last = False
            for opt in all_options:
                processed.add((opt['file'], opt['option']))
                if opt['file'] == last.get('file') and opt['option'] == last.get('option'):
                    found_last = True
                    break
            
            if not found_last:
                print(f"  [AVISO] Opcao '{last.get('option')}' nao encontrada na lista atual")
                print(f"  [AVISO] Progresso pode estar desatualizado ou arquivos foram modificados")
                choice = input("  Continuar do inicio? [S]im / [N]ao (sair): ").lower()
                if choice == 's' or choice == 'sim':
                    processed = set()
                    print(f"  [INFO] Progresso resetado, iniciando do zero")
                else:
                    print(f"  [INFO] Operacao cancelada")
                    return
    
    # Filtrar opções já processadas
    pending_options = [opt for opt in all_options if (opt['file'], opt['option']) not in processed]
    
    if args.test:
        pending_options = pending_options[:1]
        print(f"\n[MODO TESTE] Processando apenas 1 opção")
    elif args.limit:
        pending_options = pending_options[:args.limit]
        print(f"\n[LIMITE] Processando {args.limit} opções")
    
    if not pending_options:
        print("\n[INFO] Nenhuma opção pendente!")
        return
    
    print(f"\n[4/8] Processando {len(pending_options)} opções...")
    
    # Abrir browser
    print("\n[5/8] Iniciando browser Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        total_processed = progress.get('total_processed', 0) if progress else 0
        errors = progress.get('errors', []) if progress else []
        
        try:
            for idx, option in enumerate(pending_options, 1):
                print("\n" + "=" * 60)
                print(f"OPÇÃO #{idx}/{len(pending_options)}: {option['option']}")
                print("=" * 60)
                print(f"Arquivo: {option['file']}")
                print(f"Menu: {option['menu']}")
                if option['submenu']:
                    print(f"Submenu: {option['submenu']}")
                
                # Gerar prompt
                menu_path = f"{option['menu']} > {option['submenu']}" if option['submenu'] else option['menu']
                prompt = PROMPT_TEMPLATE.format(option=option['option'], menu=menu_path)
                
                print(f"\n[FETCH] Buscando resposta no Google AI...")
                response = fetch_google_ai_response(prompt, page)
                
                if not response:
                    error_msg = f"Falha ao buscar resposta para {option['option']}"
                    print(f"[ERRO] {error_msg}")
                    log_error(error_msg, option)
                    errors.append(option['option'])
                    
                    choice = input("[r]etry / [s]kip / [q]uit: ").lower()
                    if choice == 'r':
                        response = fetch_google_ai_response(prompt, page)
                        if not response:
                            print(f"[ERRO] Retry também falhou")
                            continue
                    elif choice == 'q':
                        break
                    else:
                        continue
                
                # Mostrar resposta completa
                print("\n" + "-" * 60)
                print("RESPOSTA COMPLETA DA IA:")
                print("-" * 60)
                print(response['full_text'])
                print("-" * 60)
                
                # Parse
                print("\n[PARSE] Extraindo dados...")
                parsed = parse_ai_response(response['full_text'])
                
                if not parsed:
                    print("[ERRO] Falha no parsing!")
                    raw_file = save_raw_response(option['option'], response['full_text'])
                    print(f"[INFO] Resposta bruta salva em: {raw_file}")
                    
                    choice = input("[r]etry fetch / [m]anual edit / [s]kip / [q]uit: ").lower()
                    if choice == 'r':
                        continue
                    elif choice == 'm':
                        description = input("DESCRIÇÃO: ")
                        risk_reason = input("RISCO+GRAU: ")
                        parsed = {'description': description, 'risk_reason': risk_reason}
                    elif choice == 'q':
                        break
                    else:
                        continue
                
                # Mostrar parsing
                print("\n" + "-" * 60)
                print("PARSING EXTRAÍDO:")
                print("-" * 60)
                print(f"description:\n  {parsed['description']}")
                print(f"\nriskReason:\n  {parsed['risk_reason']}")
                print(f"\nsources: {len(response.get('sources', []))} URLs")
                for src in response.get('sources', [])[:3]:
                    print(f"  - {src}")
                
                # Modo supervisão
                if args.supervised:
                    print("\n" + "-" * 60)
                    choice = input("[s]alvar / [p]ular / [e]ditar / [q]uit: ").lower()
                    
                    if choice == 'e':
                        parsed['description'] = input("Nova DESCRIÇÃO: ") or parsed['description']
                        parsed['risk_reason'] = input("Novo RISCO+GRAU: ") or parsed['risk_reason']
                        choice = 's'
                    
                    if choice == 'q':
                        break
                    elif choice != 's':
                        continue
                
                # Atualizar JSON
                print("\n[UPDATE] Atualizando JSON...")
                updates = {
                    'description': parsed['description'],
                    'risk_reason': parsed['risk_reason'],
                    'sources': response.get('sources', [])
                }
                all_jsons[option['file']] = update_json_option(
                    all_jsons[option['file']],
                    option['json_path'],
                    updates
                )
                
                # Salvar progresso
                total_processed += 1
                progress_data = {
                    'last_processed': {
                        'file': option['file'],
                        'option': option['option']
                    },
                    'total_processed': total_processed,
                    'errors': errors,
                    'timestamp': datetime.now().isoformat()
                }
                save_progress(progress_data)
                
                print(f"[OK] Opção #{total_processed} processada!")
                
                # Delay aleatório
                if idx < len(pending_options):
                    delay = random.randint(DELAY_MIN, DELAY_MAX)
                    print(f"\n[DELAY] Aguardando {delay}s (resposta visível acima)...")
                    time.sleep(delay)
                
                # Pausa a cada batch
                if idx % BATCH_SIZE == 0 and idx < len(pending_options):
                    pause_time = random.randint(BATCH_PAUSE_MIN, BATCH_PAUSE_MAX)
                    print(f"\n[PAUSA] Processadas {idx} opções. Pausa de {pause_time}s...")
                    time.sleep(pause_time)
        
        finally:
            browser.close()
    
    # Salvar todos os JSONs
    print("\n[6/8] Salvando JSONs modificados...")
    save_json_files(all_jsons)
    
    # Relatório final
    print("\n" + "=" * 60)
    print("RELATÓRIO FINAL")
    print("=" * 60)
    print(f"Total processado: {total_processed}")
    print(f"Erros: {len(errors)}")
    if errors:
        print(f"Opções com erro: {', '.join(errors[:5])}")
    print("=" * 60)


if __name__ == '__main__':
    main()

