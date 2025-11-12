# analyze_google_ai.py
# Script para analisar estrutura HTML do Google AI Mode

from playwright.sync_api import sync_playwright
import time
from pathlib import Path
from urllib.parse import quote_plus

# Prompt de teste realista
prompt = "Explique de forma objetiva em 40 palavras a opção EHCI Hand-off em Advanced na BIOS da placa mãe Machinist MD8 X99 em tópicos: DESCRIÇÃO(para que serve, o que faz):, RISCO:(se pode causar travamento de POST e o GRAU DE RISCO:(NEHUM, BAIXO, MÉDIO, ALTO, CERTAMENTE))"

# URL com udm=50 (Google AI Mode)
url = f"https://www.google.com/search?q={quote_plus(prompt)}&udm=50"

print(f"[INFO] Abrindo Google AI Mode...")
print(f"[INFO] URL: {url}")
print(f"[INFO] Aguardando resposta carregar (10 segundos)...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Navegar para a página
    page.goto(url)
    
    print(f"[INFO] Aguardando resposta carregar...")
    print(f"[INFO] Se aparecer CAPTCHA, resolva manualmente e aguarde a resposta aparecer")
    
    # Aguardar resposta carregar - verificar múltiplas vezes
    max_wait = 120  # Máximo 120 segundos (aumentado para dar tempo após CAPTCHA)
    wait_interval = 2  # Verificar a cada 2 segundos
    waited = 0
    captcha_resolved = False
    
    while waited < max_wait:
        time.sleep(wait_interval)
        waited += wait_interval
        
        current_url = page.url
        page_html = page.content()
        
        # Verificar CAPTCHA
        if 'captcha' in page_html.lower() or 'unusual traffic' in page_html.lower() or 'recaptcha' in page_html.lower():
            if not captcha_resolved:
                print(f"\n[CAPTCHA] Detectado! Resolva manualmente no navegador...")
                print(f"[INFO] Aguardando resolucao (maximo {max_wait - waited}s restantes)...")
            # Continuar verificando
            continue
        
        # Se estava em CAPTCHA e agora não está mais, foi resolvido
        if captcha_resolved == False and 'captcha' not in page_html.lower():
            captcha_resolved = True
            print(f"[OK] CAPTCHA resolvido! Aguardando redirecionamento e resposta...")
            # Aguardar redirecionamento
            time.sleep(5)
            continue
        
        # Verificar se URL mudou (redirecionamento após CAPTCHA)
        if 'search' in current_url.lower() and 'udm=50' in current_url:
            # Verificar se resposta apareceu (buscar por marcadores esperados)
            # Procurar por elementos comuns da resposta do Google AI
            if ('DESCRIÇÃO' in page_html or 'descrição' in page_html.lower() or 
                'RISCO' in page_html or 'GRAU DE RISCO' in page_html or
                'AI Overview' in page_html or 'Generative AI' in page_html or
                len(page_html) > 50000):  # Resposta geralmente tem muito HTML
                # Verificar mais uma vez após 5 segundos para garantir que está completo
                print(f"[OK] Resposta detectada! Aguardando finalizacao...")
                time.sleep(5)
                # Verificar novamente e capturar
                final_html = page.content()
                if 'DESCRIÇÃO' in final_html or 'descrição' in final_html.lower() or 'RISCO' in final_html:
                    print(f"[OK] Resposta confirmada!")
                    html = final_html  # Capturar o HTML agora que confirmamos
                    break
                else:
                    print(f"[AVISO] Resposta nao confirmada na verificacao final, continuando...")
                    # Continuar verificando
    
    # Se não capturou no loop, capturar agora
    if 'html' not in locals() or not html:
        html = page.content()
    
    # Tirar screenshot
    screenshot_path = Path("test_screenshot.png")
    page.screenshot(path=str(screenshot_path))
    
    # Salvar HTML
    html_path = Path("test_response.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\n[OK] HTML salvo em: {html_path}")
    print(f"[OK] Screenshot salvo em: {screenshot_path}")
    print(f"\n[INFO] Analise o HTML para identificar seletores CSS")
    print(f"[INFO] Atualize automation/AI_SELECTORS.md com os seletores encontrados")
    
    # Manter browser aberto por mais 10 segundos para inspeção visual
    print(f"\n[INFO] Browser ficara aberto por mais 10 segundos para inspecao...")
    time.sleep(10)
    
    browser.close()

print(f"\n[INFO] Analise concluida!")

