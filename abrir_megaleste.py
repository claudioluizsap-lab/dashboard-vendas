import asyncio
import sys
import glob as glob_mod
from playwright.async_api import async_playwright
from excel_reader import ler_credenciais


async def abrir_megaleste(caminho_planilha):
    credenciais = ler_credenciais(caminho_planilha)

    entrada = None
    for c in credenciais:
        if "megaleste" in c["site"].lower():
            entrada = c
            break

    if not entrada:
        print("ERRO: 'megaleste' nao encontrado na planilha.")
        print("Sites encontrados:", [c["site"] for c in credenciais])
        return

    site_url = entrada["site"]
    if not site_url.startswith("http"):
        site_url = "https://" + site_url

    usuario = entrada["usuario"]
    senha = entrada["senha"]

    print(f"Site   : {site_url}")
    print(f"Usuario: {usuario}")
    print(f"Senha  : {'*' * len(senha) if senha else '(vazio)'}")
    print("\nAbrindo navegador...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        context = await browser.new_context(
            no_viewport=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            locale="pt-BR"
        )
        page = await context.new_page()

        await page.goto(site_url, timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

        logado = False
        if usuario and senha:
            print("Abrindo formulario de login...")

            BOTOES_ABRIR_LOGIN = [
                'button:has-text("entrar")',
                'a:has-text("entrar")',
                'a:has-text("Entrar")',
                'button:has-text("Entrar")',
                '[class*="login"]',
                '[href*="login"]',
                '[href*="entrar"]',
            ]

            for sel in BOTOES_ABRIR_LOGIN:
                try:
                    el = await page.query_selector(sel)
                    if el:
                        await el.evaluate("e => e.click()")
                        print(f"  Clicou em '{sel}' para abrir login")
                        await page.wait_for_timeout(2500)
                        break
                except Exception:
                    continue

            SELETORES_USUARIO = [
                'input[name="user"]',
                'input[placeholder="login" i]',
                'input[name="login"]',
                'input[name="email"]',
                'input[name="username"]',
                'input[name="usuario"]',
                'input[type="email"]',
                'input[id="login"]',
                'input[id="email"]',
                'input[id*="login"]',
                'input[placeholder*="login" i]',
                'input[placeholder*="usuario" i]',
                'input[placeholder*="e-mail" i]',
                'input[placeholder*="cpf" i]',
            ]
            SELETORES_SENHA = [
                'input[name="pass"]',
                'input[placeholder="senha" i]',
                'input[type="password"]',
                'input[name="password"]',
                'input[name="senha"]',
                'input[id="senha"]',
                'input[id="password"]',
            ]
            SELETORES_SUBMIT = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Entrar")',
                'button:has-text("entrar")',
                'button:has-text("Acessar")',
                'button:has-text("Login")',
                'a:has-text("Entrar")',
            ]

            campo_usuario = None
            for sel in SELETORES_USUARIO:
                try:
                    el = await page.wait_for_selector(sel, timeout=2000)
                    if el:
                        campo_usuario = sel
                        print(f"  Campo usuario encontrado: {sel}")
                        break
                except Exception:
                    continue

            campo_senha = None
            for sel in SELETORES_SENHA:
                try:
                    el = await page.wait_for_selector(sel, timeout=2000)
                    if el:
                        campo_senha = sel
                        print(f"  Campo senha encontrado: {sel}")
                        break
                except Exception:
                    continue

            if campo_usuario and campo_senha:
                await page.evaluate(f"document.querySelector('{campo_usuario}').value = ''")
                await page.type(campo_usuario, usuario, delay=60)
                await page.wait_for_timeout(400)
                await page.evaluate(f"document.querySelector('{campo_senha}').value = ''")
                await page.type(campo_senha, senha, delay=60)
                await page.wait_for_timeout(400)
                print("  Credenciais preenchidas.")

                enviou = False
                for sel in SELETORES_SUBMIT:
                    try:
                        botao = await page.query_selector(sel)
                        if botao:
                            await botao.click()
                            print(f"  Clicou em '{sel}'")
                            await page.wait_for_load_state("networkidle", timeout=10000)
                            enviou = True
                            logado = True
                            break
                    except Exception:
                        continue

                if not enviou:
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(3000)
                    logado = True

                print("LOGIN REALIZADO!" if logado else "Nao foi possivel confirmar o login.")
            else:
                print("  Campos nao encontrados automaticamente.")
                print("  Preencha o login manualmente no navegador.")
        else:
            print("Sem credenciais na planilha — abrindo sem login.")

        print("\nNavegador aberto. Feche a janela quando terminar.")
        await page.wait_for_event("close", timeout=0)
        await browser.close()


def encontrar_planilha():
    arquivos = glob_mod.glob("*.xlsx")
    if not arquivos:
        print("Nenhuma planilha .xlsx encontrada na pasta.")
        sys.exit(1)
    for a in arquivos:
        try:
            creds = ler_credenciais(a)
            if any("megaleste" in c["site"].lower() for c in creds):
                return a
        except Exception:
            continue
    return arquivos[0]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        planilha = sys.argv[1]
    else:
        planilha = encontrar_planilha()

    print(f"Planilha: {planilha}\n")
    asyncio.run(abrir_megaleste(planilha))
