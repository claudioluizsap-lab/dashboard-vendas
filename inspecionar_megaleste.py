import asyncio
from playwright.async_api import async_playwright

async def inspecionar():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        )
        await page.goto("https://www.megaleste.com.br", timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

        await page.evaluate("document.querySelector('button') && document.querySelector('button').click()")
        await page.wait_for_timeout(1000)

        for sel in ['a:has-text("entrar")', 'button:has-text("entrar")', '[href*="login"]', '[class*="login"]']:
            try:
                el = await page.query_selector(sel)
                if el:
                    await el.evaluate("e => e.click()")
                    print(f"Clicou via JS em: {sel}")
                    await page.wait_for_timeout(2000)
                    break
            except Exception:
                continue

        inputs = await page.query_selector_all("input")
        print(f"\n{len(inputs)} input(s) encontrado(s):\n")
        for inp in inputs:
            tipo = await inp.get_attribute("type") or ""
            nome = await inp.get_attribute("name") or ""
            id_  = await inp.get_attribute("id") or ""
            ph   = await inp.get_attribute("placeholder") or ""
            cls  = await inp.get_attribute("class") or ""
            vis  = await inp.is_visible()
            print(f"  type={tipo!r:12} name={nome!r:20} id={id_!r:20} placeholder={ph!r:25} visible={vis}")

        await browser.close()

asyncio.run(inspecionar())
