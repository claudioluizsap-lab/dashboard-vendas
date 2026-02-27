from app import load_data, calcular_projecao
df = load_data()
rows, media = calcular_projecao(df)
print(f'Media diaria base: R$ {media:,.2f}')
print()
for r in rows:
    real_s = f'R$ {r["real"]:,.2f}' if r["real"] else '-'
    print(f'{r["mes"]:12} | {r["status"]:10} | Real: {real_s:>16} | Proj: R$ {r["proj"]:>12,.2f}')
