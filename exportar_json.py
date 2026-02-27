import pandas as pd
import json

caminho = r'D:\Users\Claudio\OneDrive\Nova pasta\Bd_curva abc\curva abc.xlsx'
df = pd.read_excel(caminho, sheet_name='Produtos mais vendidos')

print(f"Total de produtos: {len(df)}")
print("Colunas:", list(df.columns))
print("\nPrimeiros 5:")
print(df.head())
print("\nÚltimos 5:")
print(df.tail())

dados = []
for _, row in df.iterrows():
    codigo       = str(row.get('Codigo', '')).strip()
    descricao    = str(row.get('Descrição', '')).strip()
    quantidade   = float(row.get('Quant.',   0) or 0)
    valor_unit   = float(row.get('valor unit.', 0) or 0)
    valor_total  = float(row.get('Valor',    0) or 0)

    if not valor_unit and quantidade and valor_total:
        valor_unit = round(valor_total / quantidade, 6) if quantidade else 0

    if descricao and (quantidade > 0 or valor_total > 0):
        dados.append({
            "codigo":        codigo,
            "descricao":     descricao,
            "quantidade":    round(quantidade, 4),
            "valorUnitario": round(valor_unit, 4),
        })

print(f"\nProdutos válidos: {len(dados)}")
print("Primeiro:", dados[0] if dados else "N/A")
print("Último:",  dados[-1] if dados else "N/A")

total_valor = sum(d['quantidade'] * d['valorUnitario'] for d in dados)
print(f"\nValor total do estoque: R$ {total_valor:,.2f}")

with open('curva-abc-app/public/dados.json', 'w', encoding='utf-8') as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print("\n✅ dados.json atualizado com sucesso!")
