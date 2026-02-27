import asyncio
import re
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout


SELETORES_LOGIN = {
    "usuario": [
        'input[name="email"]', 'input[name="username"]', 'input[name="user"]',
        'input[name="login"]', 'input[type="email"]', 'input[name="usuario"]',
        'input[id*="email"]', 'input[id*="user"]', 'input[id*="login"]',
        'input[placeholder*="e-mail" i]', 'input[placeholder*="usuario" i]',
        'input[placeholder*="login" i]',
    ],
    "senha": [
        'input[type="password"]',
        'input[name="password"]', 'input[name="senha"]',
        'input[id*="password"]', 'input[id*="senha"]',
    ],
    "botao": [
        'button[type="submit"]', 'input[type="submit"]',
        'button:has-text("Entrar")', 'button:has-text("Login")',
        'button:has-text("Acessar")', 'button:has-text("Sign in")',
        'a:has-text("Entrar")',
    ]
}

SELETORES_BUSCA = [
    'input[name="q"]', 'input[name="search"]', 'input[name="busca"]',
    'input[name="query"]', 'input[type="search"]',
    'input[placeholder*="busca" i]', 'input[placeholder*="pesquis" i]',
    'input[placeholder*="search" i]', 'input[placeholder*="produto" i]',
    'input[id*="search"]', 'input[id*="busca"]',
]

# Seletores especificos por dominio: (seletor_nome, seletor_preco)
SELETORES_POR_SITE = {
    "mercadolivre.com.br": (
        [".poly-component__title", ".ui-search-item__title", "h2.ui-search-item__title"],
        [".andes-money-amount__fraction", ".price-tag-fraction", ".poly-price__current .andes-money-amount__fraction"]
    ),
    "amazon.com.br": (
        ["span.a-size-medium.a-color-base.a-text-normal", "span.a-size-base-plus", "h2 a span"],
        ["span.a-price-whole", ".a-price .a-offscreen", "span.a-color-base.a-text-bold"]
    ),
    "americanas.com.br": (
        ["h3[class*='product']", "span[class*='product-name']", "[data-testid='product-card-name']",
         "h2[class*='Name']", "span[class*='Name']"],
        ["[data-testid='product-card-price']", "span[class*='Price']", "span[class*='price']",
         "[class*='best-price']", "[class*='sales-price']"]
    ),
    "magazineluiza.com.br": (
        ["h2[data-testid='product-title']", "[class*='product-title']", "h2[class*='sc-']",
         "a[data-testid='product-card-link'] h2"],
        ["[data-testid='price-value']", "p[data-testid='price-value']", "[class*='sc-kAyceB']",
         "span[class*='price']", "[class*='Price']"]
    ),
    "casasbahia.com.br": (
        ["h3[class*='product']", "span[class*='product-name']", "[data-testid='product-card-name']",
         "h2[class*='Name']"],
        ["[data-testid='product-card-price']", "span[class*='Price']", "[class*='best-price']",
         "span[class*='price']"]
    ),
    "shopee.com.br": (
        ["div[class*='shopee-search-item-result__item'] span", "._10Wfc2 span", "div[class*='ie3A+n']"],
        ["span[class*='_1xk7ak']", "span[class*='price']", "div[class*='price'] span"]
    ),
    "kabum.com.br": (
        ["span.nameCard", "h2.nameCard", "span[class*='nameCard']", "a[class*='productCard'] span"],
        ["span.priceCard", "b.priceCard", "span[class*='priceCard']", "[class*='price-card']",
         "span[class*='price']", "b[class*='price']"]
    ),
    "extra.com.br": (
        ["h3[class*='product']", "[data-testid='product-card-name']", "h2[class*='Name']",
         "span[class*='product-name']"],
        ["[data-testid='product-card-price']", "span[class*='Price']", "[class*='best-price']",
         "span[class*='price']"]
    ),
    "pontofrio.com.br": (
        ["h3[class*='product']", "[data-testid='product-card-name']", "span[class*='product-name']"],
        ["[data-testid='product-card-price']", "span[class*='Price']", "span[class*='price']"]
    ),
    "submarino.com.br": (
        ["h3[class*='product']", "[data-testid='product-card-name']", "span[class*='product-name']"],
        ["[data-testid='product-card-price']", "span[class*='Price']", "span[class*='price']"]
    ),
}

SELETORES_PRECO_GENERIC = [
    '[class*="price"]', '[class*="preco"]', '[class*="valor"]',
    '[class*="Price"]', '[class*="Preco"]',
    'span[class*="price"]', 'span[class*="preco"]',
    '[itemprop="price"]', '[data-price]',
    '.price', '.preco', '.valor', '.product-price',
]

SELETORES_PRODUTO_GENERIC = [
    '[class*="product-title"]', '[class*="product-name"]',
    '[class*="titulo"]', 'h2[class*="product"]', 'h3[class*="product"]',
    'a[class*="product"]', '[class*="item-title"]',
    '.product-title', '.product-name',
]


def dominio(url):
    url = url.lower().replace("https://", "").replace("http://", "").replace("www.", "")
    return url.split("/")[0]


async def tentar_login(page, usuario, senha):
    try:
        campo_usuario = None
        for seletor in SELETORES_LOGIN["usuario"]:
            try:
                el = await page.wait_for_selector(seletor, timeout=2000, state="visible")
                if el:
                    campo_usuario = seletor
                    break
            except Exception:
                continue

        if not campo_usuario:
            return False

        campo_senha = None
        for seletor in SELETORES_LOGIN["senha"]:
            try:
                el = await page.wait_for_selector(seletor, timeout=2000, state="visible")
                if el:
                    campo_senha = seletor
                    break
            except Exception:
                continue

        if not campo_senha:
            return False

        await page.fill(campo_usuario, usuario)
        await page.fill(campo_senha, senha)

        for seletor in SELETORES_LOGIN["botao"]:
            try:
                botao = await page.query_selector(seletor)
                if botao:
                    await botao.click()
                    await page.wait_for_load_state("networkidle", timeout=10000)
                    return True
            except Exception:
                continue

        await page.keyboard.press("Enter")
        await page.wait_for_load_state("networkidle", timeout=10000)
        return True

    except Exception:
        return False


async def buscar_produto(page, produto, site_key):
    resultados = []

    campo_busca = None
    for seletor in SELETORES_BUSCA:
        try:
            el = await page.wait_for_selector(seletor, timeout=3000, state="visible")
            if el:
                campo_busca = seletor
                break
        except Exception:
            continue

    if not campo_busca:
        return resultados

    try:
        await page.fill(campo_busca, produto)
        await page.keyboard.press("Enter")
        await page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        return resultados

    await page.wait_for_timeout(2500)

    seletores_nome, seletores_preco = SELETORES_POR_SITE.get(
        site_key, (SELETORES_PRODUTO_GENERIC, SELETORES_PRECO_GENERIC)
    )

    nomes_raw = []
    for seletor in seletores_nome:
        try:
            els = await page.query_selector_all(seletor)
            for el in els[:20]:
                texto = (await el.inner_text()).strip()
                if texto and len(texto) > 3:
                    nomes_raw.append(texto[:120])
            if nomes_raw:
                break
        except Exception:
            continue

    if not nomes_raw:
        for seletor in SELETORES_PRODUTO_GENERIC:
            try:
                els = await page.query_selector_all(seletor)
                for el in els[:20]:
                    texto = (await el.inner_text()).strip()
                    if texto and len(texto) > 3:
                        nomes_raw.append(texto[:120])
                if nomes_raw:
                    break
            except Exception:
                continue

    precos_raw = []
    for seletor in seletores_preco:
        try:
            els = await page.query_selector_all(seletor)
            for el in els[:20]:
                texto = (await el.inner_text()).strip().replace("\n", " ")
                if texto and re.search(r"\d", texto):
                    precos_raw.append(texto[:60])
            if precos_raw:
                break
        except Exception:
            continue

    if not precos_raw:
        for seletor in SELETORES_PRECO_GENERIC:
            try:
                els = await page.query_selector_all(seletor)
                for el in els[:20]:
                    texto = (await el.inner_text()).strip().replace("\n", " ")
                    if re.search(r"R\$|[\d]+[,\.]\d{2}", texto):
                        precos_raw.append(texto[:60])
                if precos_raw:
                    break
            except Exception:
                continue

    total = max(len(precos_raw), len(nomes_raw))
    for i in range(min(total, 10)):
        nome = nomes_raw[i] if i < len(nomes_raw) else "Produto"
        preco = precos_raw[i] if i < len(precos_raw) else "N/D"
        resultados.append({
            "produto": nome,
            "preco": preco,
            "url": page.url
        })

    return resultados


async def buscar_em_site(credencial, produto):
    site_url = credencial["site"]
    usuario = credencial["usuario"]
    senha = credencial["senha"]
    site_key = dominio(site_url)

    if not site_url.startswith("http"):
        site_url = "https://" + site_url

    resultado = {
        "site": credencial["site"],
        "status": "",
        "login": False,
        "produtos": []
    }

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
                locale="pt-BR",
                viewport={"width": 1366, "height": 768}
            )
            page = await context.new_page()

            await page.goto(site_url, timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            if usuario and senha:
                logado = await tentar_login(page, usuario, senha)
                resultado["login"] = logado
                resultado["status"] = "Login realizado" if logado else "Login nao realizado / nao necessario"
            else:
                resultado["status"] = "Sem credenciais"

            produtos = await buscar_produto(page, produto, site_key)
            resultado["produtos"] = produtos

            if not produtos:
                resultado["status"] += " | Nenhum resultado encontrado"

            await browser.close()

    except PlaywrightTimeout:
        resultado["status"] = "Timeout ao acessar o site"
    except Exception as e:
        resultado["status"] = f"Erro: {str(e)[:100]}"

    return resultado


async def buscar_em_todos(credenciais, produto):
    tarefas = [buscar_em_site(cred, produto) for cred in credenciais]
    return await asyncio.gather(*tarefas)


def executar_busca(credenciais, produto):
    return asyncio.run(buscar_em_todos(credenciais, produto))
