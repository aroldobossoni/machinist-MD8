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
import threading

# Import para alerta sonoro
try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

# Configurações
PROMPT_TEMPLATE = 'Explique de forma objetiva em 40 palavras a opção "{option}" em "{menu}" na BIOS da placa mãe Machinist MD8 X99 em tópicos: DESCRIÇÃO(para que serve, o que faz):, RISCO:(se pode causar travamento de POST e o GRAU DE RISCO:(NENHUM, BAIXO, MÉDIO, ALTO, CERTAMENTE))'

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
BROWSER_STATE_FILE = AUTOMATION_DIR / 'browser_state.json'

# User-Agent realista
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Criar diretórios se não existirem
RAW_RESPONSES_DIR.mkdir(exist_ok=True)
ERROR_SCREENSHOTS_DIR.mkdir(exist_ok=True)


def beep_alert():
    """Emite alerta sonoro"""
    if SOUND_AVAILABLE:
        try:
            pattern = [(1400, 700), (900, 500), (1400, 700)]
            for freq, duration in pattern:
                winsound.Beep(freq, duration)
                time.sleep(0.1)
        except Exception:
            print('\a' * 3)
    else:
        print('\a' * 3)


def input_with_timeout(prompt, timeout=10, default='s'):
    """Input com timeout. Retorna default se timeout expirar."""
    result = [None]
    
    def get_input():
        try:
            result[0] = input(prompt)
        except:
            pass
    
    thread = threading.Thread(target=get_input, daemon=True)
    thread.start()
    thread.join(timeout)
    
    if result[0] is None:
        print(f"\n[TIMEOUT] Sem resposta em {timeout}s. Auto-skip.")
        return default
    
    return result[0]


def format_eta(seconds):
    """Formata segundos em string compacta hh:mm:ss."""
    seconds = max(0, int(round(seconds)))
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours > 0:
        return f"{hours:02d}h{minutes:02d}m"
    if minutes > 0:
        return f"{minutes:02d}m{secs:02d}s"
    return f"{secs:02d}s"


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


def fetch_google_ai_response(prompt, context, retry_count=3):
    """Busca resposta do Google AI Mode"""
    url = f"https://www.google.com/search?q={quote_plus(prompt)}&udm=50"

    for attempt in range(retry_count):
        page = None
        try:
            # Criar nova página para cada request
            page = context.new_page()
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Aguardar resposta carregar - verificar múltiplas vezes
            max_wait = 120  # Máximo 120 segundos (aumentado para dar tempo após CAPTCHA)
            wait_interval = 2  # Verificar a cada 2 segundos
            waited = 0
            response_ready = False
            captcha_detected = False
            captcha_start_time = None
            last_beep_time = None
            
            while waited < max_wait and not response_ready:
                time.sleep(wait_interval)
                waited += wait_interval
                
                current_url = page.url
                html = page.content()
                
                # Verificar CAPTCHA primeiro
                if 'captcha' in html.lower() or 'unusual traffic' in html.lower() or 'recaptcha' in html.lower():
                    if not captcha_detected:
                        captcha_detected = True
                        captcha_start_time = time.time()
                        last_beep_time = captcha_start_time
                        screenshot_path = ERROR_SCREENSHOTS_DIR / f'captcha_{int(time.time())}.png'
                        page.screenshot(path=str(screenshot_path))
                        print(f"\n⚠️  CAPTCHA detectado! Screenshot: {screenshot_path}")
                        print(f"[INFO] Resolva o CAPTCHA no navegador")
                        print(f"[INFO] O script aguardara automaticamente a resposta aparecer...")
                    else:
                        # CAPTCHA ainda ativo - verificar se passou 60s desde detecção inicial
                        current_time = time.time()
                        elapsed_since_start = current_time - captcha_start_time
                        
                        # Só emitir beep se já passou 60s desde a detecção inicial
                        if elapsed_since_start >= 60 and (current_time - last_beep_time) >= 60:
                            print(f"\n🔔 ALERTA: CAPTCHA ainda não resolvido ({int(elapsed_since_start)}s aguardando)")
                            beep_alert()
                            last_beep_time = current_time
                    
                    time.sleep(3)
                    # Continuar verificando
                    continue
                
                # Se estava em CAPTCHA e agora não está mais, foi resolvido
                if captcha_detected and 'captcha' not in html.lower():
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
            
            # Extrair texto da resposta usando seletor CSS específico
            response_text = ""
            sources = []
            
            try:
                # Tentar usar seletor CSS para extrair apenas resposta da IA
                ai_container = page.query_selector('.pWvJNd')
                if ai_container:
                    response_text = ai_container.inner_text()
                    print(f"[OK] Resposta extraida via seletor CSS")
                else:
                    print(f"[AVISO] Seletor CSS nao encontrou container, usando fallback")
            except Exception as e:
                print(f"[AVISO] Erro ao usar seletor CSS: {e}, usando fallback")
            
            # Fallback: extrair de todo HTML se seletor CSS falhou
            html = None
            soup = None
            
            if not response_text or len(response_text) < 50:
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Remover scripts e styles
                for script in soup(["script", "style", "nav", "header", "footer"]):
                    script.decompose()
                
                # Pegar texto principal
                body = soup.find('body')
                if body:
                    response_text = body.get_text(separator='\n', strip=True)
                
                print(f"[OK] Resposta extraida via fallback")
            
            # Buscar links de referência (fontes) - reusar html/soup se já existe
            if not html:
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                if (href.startswith('http') and 
                    'google.com' not in href and 
                    'youtube.com' not in href and
                    len(href) < 200):
                    sources.append(href)
            
            if response_text:
                if page:
                    page.close()
                return {
                    'full_text': response_text.strip(),
                    'sources': list(set(sources))[:5]
                }
            
            # Se não encontrou resposta, tentar novamente
            if page:
                page.close()
            if attempt < retry_count - 1:
                delay = [5, 10, 20][attempt]
                print(f"[RETRY] Tentativa {attempt + 1}/{retry_count}, resposta nao encontrada, aguardando {delay}s...")
                time.sleep(delay)
            else:
                print(f"[ERRO] Resposta nao encontrada apos {retry_count} tentativas")
        
        except Exception as e:
            if page:
                page.close()
            if attempt < retry_count - 1:
                delay = [5, 10, 20][attempt]
                print(f"[ERRO] {e}, retry em {delay}s...")
                time.sleep(delay)
            else:
                print(f"[ERRO] Falha apos {retry_count} tentativas: {e}")
                raise

    return None


def parse_ai_response(full_text):
    """Parse da resposta da IA extraindo DESCRIÇÃO e RISCO+GRAU (v2: linha por linha)"""
    if not full_text:
        return None
    
    lines = full_text.split('\n')
    
    description = ""
    risk_text = ""
    grade_text = ""
    
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        # Identifica seções
        if line.startswith('DESCRIÇÃO'):
            current_section = 'description'
            # Pega o texto após os dois pontos
            if ':' in line:
                content = line.split(':', 1)[1].strip()
                description = content
            continue
        
        elif line.startswith('RISCO'):
            current_section = 'risk'
            # Pega o texto após os dois pontos, removendo prompts entre parênteses
            if ':' in line:
                content = line.split(':', 1)[1].strip()
                # Remove parênteses de prompt no início
                content = re.sub(r'^\([^)]+\)\s*', '', content)
                risk_text = content
            continue
        
        elif line.startswith('GRAU DE RISCO') or line.startswith('GRAU'):
            current_section = 'grade'
            # Pega o texto após os dois pontos
            if ':' in line:
                content = line.split(':', 1)[1].strip()
                grade_text = content
            continue
        
        elif line.startswith('A IA pode cometer'):
            # Fim da resposta útil
            break
        
        # Continua acumulando texto da seção atual
        elif current_section and line:
            if current_section == 'description':
                description += ' ' + line
            elif current_section == 'risk':
                # Não acumula linhas adicionais no risk se começarem com parênteses de prompt
                if not line.startswith('('):
                    risk_text += ' ' + line
            elif current_section == 'grade':
                grade_text += ' ' + line
    
    # Limpar textos
    description = ' '.join(description.split()).strip()
    risk_text = ' '.join(risk_text.split()).strip()
    risk_text = risk_text.lstrip(')').lstrip()  # Remove ") " do início (prompt residual)
    risk_text = risk_text.rstrip('.')
    grade_text = ' '.join(grade_text.split()).strip()
    grade_text = grade_text.rstrip('.')
    
    # VALIDAÇÃO: Se não encontrou descrição, retorna None (parsing falhou)
    if not description:
        return None
    
    # Montar riskReason
    if grade_text and risk_text:
        risk_reason = f"{grade_text}. {risk_text}"
    elif grade_text:
        risk_reason = grade_text
    else:
        risk_reason = risk_text
    
    risk_reason = ' '.join(risk_reason.split()).strip()  # Limpa espaços duplos
    
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


def save_json_file(file_path_str, json_data):
    """Salva um único arquivo JSON"""
    file_path = Path(file_path_str)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"[SAVE] {file_path.relative_to(BASE_DIR)}")


def save_json_files(all_jsons):
    """Salva todos os JSONs modificados"""
    for file_path_str, json_data in all_jsons.items():
        save_json_file(file_path_str, json_data)


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

        # Criar context com cookies persistentes e user-agent
        context_options = {'user_agent': USER_AGENT}
        if BROWSER_STATE_FILE.exists():
            context_options['storage_state'] = str(BROWSER_STATE_FILE)
            print(f"[INFO] Cookies carregados")

        context = browser.new_context(**context_options)
        
        total_processed = progress.get('total_processed', 0) if progress else 0
        errors = progress.get('errors', []) if progress else []
        
        try:
            session_start = time.time()
            for idx, option in enumerate(pending_options, 1):
                print("\n" + "=" * 60)
                if idx == 1:
                    eta_label = "[ETA calculando...] "
                else:
                    elapsed = time.time() - session_start
                    avg_time = elapsed / (idx - 1)
                    remaining = len(pending_options) - (idx - 1)
                    eta_seconds = avg_time * remaining
                    eta_label = f"[ETA {format_eta(eta_seconds)}] "
                print(f"{eta_label}OPÇÃO #{idx}/{len(pending_options)}: {option['option']}")
                print("=" * 60)
                print(f"Arquivo: {option['file']}")
                print(f"Menu: {option['menu']}")
                if option['submenu']:
                    print(f"Submenu: {option['submenu']}")
                
                # Gerar prompt
                menu_path = f"{option['menu']} > {option['submenu']}" if option['submenu'] else option['menu']
                prompt = PROMPT_TEMPLATE.format(option=option['option'], menu=menu_path)
                
                print(f"\n[FETCH] Buscando resposta no Google AI...")
                response = fetch_google_ai_response(prompt, context)
                
                if not response:
                    error_msg = f"Falha ao buscar resposta para {option['option']}"
                    print(f"[ERRO] {error_msg}")
                    log_error(error_msg, option)
                    errors.append(option['option'])
                    
                    choice = input("[r]etry / [s]kip / [q]uit: ").lower()
                    if choice == 'r':
                        response = fetch_google_ai_response(prompt, context)
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
                
                # No modo --test, sempre salvar raw response para análise
                if args.test:
                    raw_file = save_raw_response(option['option'], response['full_text'])
                    print(f"[DEBUG] Resposta bruta salva em: {raw_file}")
                
                if not parsed:
                    print("[ERRO] Falha no parsing!")
                    raw_file = save_raw_response(option['option'], response['full_text'])
                    print(f"[INFO] Resposta bruta salva em: {raw_file}")
                    
                    choice = input_with_timeout("[r]etry fetch / [m]anual edit / [s]kip / [q]uit: ", timeout=10, default='s').lower()
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
                
                # Salvar arquivo JSON imediatamente
                save_json_file(option['file'], all_jsons[option['file']])
                
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
            # Salvar cookies para próxima execução
            try:
                context.storage_state(path=str(BROWSER_STATE_FILE))
                print(f"\n[INFO] Cookies salvos")
            except:
                pass
            context.close()
            browser.close()
    
    # JSONs já foram salvos incrementalmente
    print("\n[6/8] JSONs salvos incrementalmente (após cada opção)")
    
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