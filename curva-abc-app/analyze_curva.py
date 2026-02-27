import pandas as pd
from openpyxl import load_workbook

df = pd.read_excel('planilha-teste-estoque.xlsx')

df['Valor Total'] = df['Quantidade'] * df['Valor Unitário']

df = df.sort_values('Valor Total', ascending=False)

valor_total_geral = df['Valor Total'].sum()
df['% Valor'] = (df['Valor Total'] / valor_total_geral) * 100
df['% Acumulado'] = df['% Valor'].cumsum()

df['Classe'] = df['% Acumulado'].apply(
    lambda x: 'A' if x <= 80 else ('B' if x <= 95 else 'C')
)

print('=' * 100)
print('ANÁLISE CURVA ABC - RESULTADOS')
print('=' * 100)
print()

print('📊 RESUMO GERAL:')
print(f'   Total de Produtos: {len(df)}')
print(f'   Valor Total do Estoque: R$ {valor_total_geral:,.2f}')
print()

print('📈 DISTRIBUIÇÃO POR CLASSE:')
print()
for classe in ['A', 'B', 'C']:
    classe_df = df[df['Classe'] == classe]
    qtd = len(classe_df)
    valor = classe_df['Valor Total'].sum()
    perc_qtd = (qtd / len(df)) * 100
    perc_valor = (valor / valor_total_geral) * 100
    
    print(f'   Classe {classe}:')
    print(f'      Produtos: {qtd} ({perc_qtd:.1f}% do total)')
    print(f'      Valor: R$ {valor:,.2f} ({perc_valor:.1f}% do valor total)')
    print()

print('🏆 TOP 10 PRODUTOS POR VALOR:')
print()
print(f"{'#':<4} {'Código':<10} {'Descrição':<35} {'Valor Total':>15} {'% Acum':>10} {'Classe':>8}")
print('-' * 100)

for i, (idx, row) in enumerate(df.head(10).iterrows(), 1):
    desc = row['Descrição'][:33]
    print(f"{i:<4} {row['Código']:<10} {desc:<35} R$ {row['Valor Total']:>11,.2f} {row['% Acumulado']:>8.2f}% {row['Classe']:>8}")

print()
print('=' * 100)
print()
print('💡 INTERPRETAÇÃO:')
print('   • Classe A: Itens críticos que representam 80% do valor - alta prioridade de gestão')
print('   • Classe B: Itens intermediários que representam 15% do valor - média prioridade')
print('   • Classe C: Itens de baixo impacto que representam 5% do valor - baixa prioridade')
