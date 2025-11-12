# Seletores CSS do Google AI Mode

Este arquivo documenta os seletores CSS identificados para extrair dados do Google AI Mode (`udm=50`).

## Como Atualizar

Se o Google mudar a estrutura HTML:

1. Execute `analyze_google_ai.py`
2. Analise o HTML gerado (`test_response.html`)
3. Atualize os seletores abaixo
4. Teste com `populate_bios_docs.py --test`

## Formato da Resposta (Atualizado 2025-11-12)

O Google AI Mode retorna HTML minificado com a resposta estruturada assim:

### Texto da Resposta
A resposta da IA vem em formato de texto livre dentro do HTML, contendo:
- **DESCRIÇÃO (para que serve, o que faz):** [texto explicativo]
- **RISCO (se pode causar travamento de POST):** [texto sobre riscos]
- **GRAU DE RISCO:** [NENHUM, BAIXO, MÉDIO, ALTO, CERTAMENTE] + explicação adicional

### Links de Fontes/Referências
Aparecem após a resposta da IA, geralmente com:
- Título do site (ex: "Super User", "Reddit")
- Data da publicação
- Snippet do conteúdo

## Estratégia de Extração

### Para o Texto da Resposta
1. Usar BeautifulSoup para extrair todo o texto
2. Procurar por padrões regex:
   - `DESCRIÇÃO.*?:(.*?)(?=RISCO|$)`
   - `RISCO.*?:(.*?)(?=GRAU DE RISCO|$)`
   - `GRAU DE RISCO.*?:(.*?)(?=\n\n|$)`

### Para as Fontes
1. Procurar por links (`<a href=...>`) externos ao Google
2. Filtrar URLs que contenham domínios conhecidos (stackoverflow.com, reddit.com, etc.)
3. Evitar URLs muito longas (>200 caracteres)

## Notas

- O HTML vem minificado em uma única linha ou poucas linhas
- A resposta está em português (pt-BR)
- Os marcadores DESCRIÇÃO, RISCO, GRAU DE RISCO são em maiúsculas
- Caracteres especiais (á, ã, ç, etc.) podem vir codificados em UTF-8
- Às vezes aparece texto extra como "A IA pode cometer erros..."
- Links de referência incluem snippets e datas

