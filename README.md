# Buscador de Precos

App web para buscar precos de produtos em multiplos sites automaticamente, utilizando credenciais de login armazenadas em uma planilha Excel.

---

## Funcionalidades

- Carrega sites, usuarios e senhas a partir de uma planilha `.xlsx`
- Faz login automatico em cada site usando as credenciais fornecidas
- Busca precos de qualquer produto nos sites cadastrados
- Exibe os resultados em tabela com nome do produto, preco e link direto
- Suporte a 10+ sites de e-commerce brasileiros
- Modulo dedicado para login na Megaleste com deteccao automatica de modal

---

## Estrutura do Projeto

```
new-project/
├── app.py                    # Servidor Flask (backend)
├── scraper.py                # Automacao Playwright (login + busca de precos)
├── excel_reader.py           # Leitura da planilha .xlsx
├── abrir_megaleste.py        # Abre e faz login na Megaleste via planilha
├── requirements.txt          # Dependencias Python
├── gerar_modelo.py           # Gera a planilha modelo formatada
├── criar_planilha_exemplo.py # Gera planilha de exemplo
├── planilha_modelo.xlsx      # Planilha modelo para preencher
├── planilha_exemplo.xlsx     # Planilha de exemplo pre-preenchida
├── uploads/                  # Pasta onde planilhas enviadas sao salvas
└── templates/
    └── index.html            # Interface web
```

---

## Instalacao

### 1. Instalar dependencias Python

```powershell
pip install flask openpyxl playwright werkzeug beautifulsoup4 requests
```

### 2. Instalar o navegador Chromium

```powershell
python -m playwright install chromium
```

---

## Como Usar

### Interface Web (Buscador de Precos)

**1. Iniciar o servidor:**
```powershell
cd "D:\Users\Claudio\Documents\verdent-projects\new-project"
python app.py
```

**2. Abrir no navegador:**
```
http://127.0.0.1:5000
```

**3. Fluxo de uso:**
- Clique na area de upload e selecione sua planilha `.xlsx`
- Os sites da planilha aparecem listados como badges azuis
- Digite o nome do produto no campo de busca
- Clique em **Buscar**
- Aguarde — o app acessa cada site, faz login e coleta os precos
- Os resultados aparecem em tabela com produto, preco e link

---

### Abrir Megaleste com Login Automatico

```powershell
python abrir_megaleste.py planilha_modelo.xlsx
```

O script:
1. Le a planilha e localiza a linha do `megaleste.com.br`
2. Abre o navegador (modo visivel)
3. Acessa `www.megaleste.com.br`
4. Clica em **entrar** para abrir o modal de login
5. Preenche usuario e senha automaticamente
6. Clica em **submit** para entrar
7. Mantem o navegador aberto para navegacao

---

## Planilha Excel

### Formato obrigatorio

| SITE | USUARIO | SENHA |
|------|---------|-------|
| mercadolivre.com.br | email@email.com | senha123 |
| amazon.com.br | email@email.com | senha123 |
| megaleste.com.br | email@email.com | senha123 |
| pontofrio.com.br | | |

**Regras:**
- Primeira linha deve ter os cabecalhos: `SITE`, `USUARIO`, `SENHA`
- Se o site nao precisar de login, deixe `USUARIO` e `SENHA` em branco
- O campo `SITE` aceita com ou sem `https://`
- Pode adicionar quantas linhas quiser

### Gerar planilha modelo

```powershell
python gerar_modelo.py
```

Gera o arquivo `planilha_modelo.xlsx` formatado e pronto para preencher.

---

## Sites Suportados

| Site | Seletores Especificos | Observacao |
|------|-----------------------|------------|
| mercadolivre.com.br | Sim | Funciona sem login |
| amazon.com.br | Sim | Funciona sem login |
| americanas.com.br | Sim | Funciona sem login |
| magazineluiza.com.br | Sim | Funciona sem login |
| kabum.com.br | Sim | Funciona sem login |
| submarino.com.br | Sim | Funciona sem login |
| megaleste.com.br | Sim (modal) | Requer login |
| casasbahia.com.br | Parcial | Protecao anti-bot |
| shopee.com.br | Parcial | Protecao anti-bot |
| extra.com.br | Parcial | Protecao anti-bot |
| Outros sites | Genericos | Depende da estrutura do site |

---

## Dependencias

| Pacote | Versao | Uso |
|--------|--------|-----|
| flask | 3.x | Servidor web |
| openpyxl | 3.x | Leitura de planilhas .xlsx |
| playwright | 1.x | Automacao de navegador |
| werkzeug | 3.x | Upload de arquivos |
| beautifulsoup4 | 4.x | Parsing HTML |
| requests | 2.x | Requisicoes HTTP |

---

## Observacoes

- Sites com protecao Cloudflare ou CAPTCHA podem bloquear a automacao
- Para login na Megaleste o navegador abre em modo visivel (nao headless)
- A busca de precos nos outros sites roda em modo headless (invisivel)
- Credenciais ficam salvas apenas localmente na planilha Excel
