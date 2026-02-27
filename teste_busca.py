import requests

session = requests.Session()

print("1. Carregando nova planilha (10 sites)...")
r = session.post(
    "http://127.0.0.1:5000/carregar-planilha",
    files={"planilha": open("planilha_exemplo.xlsx", "rb")}
)
dados = r.json()
if dados.get("erro"):
    print("ERRO:", dados["erro"])
    exit()
print(f"OK — {dados['total_sites']} sites carregados: {', '.join(dados['sites'])}")

print("\n2. Buscando produto 'notebook'...\n")
r = session.post(
    "http://127.0.0.1:5000/buscar",
    json={"produto": "notebook"}
)
data = r.json()

if data.get("erro"):
    print("ERRO:", data["erro"])
else:
    encontrados = 0
    sem_resultado = []
    for site in data["resultados"]:
        if site["produtos"]:
            encontrados += 1
            print(f"[OK] {site['site']} — {len(site['produtos'])} produto(s) encontrado(s)")
            for p in site["produtos"][:2]:
                print(f"       Produto : {p['produto'][:60]}")
                print(f"       Preco   : {p['preco']}")
        else:
            sem_resultado.append(site["site"])
            print(f"[--] {site['site']} — {site['status']}")

    print(f"\nResumo: {encontrados} site(s) com precos | {len(sem_resultado)} sem resultado")
