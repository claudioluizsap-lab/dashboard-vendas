import pandas as pd

# Carregar dados da planilha
df = pd.read_excel('curva-abc-app/EXEMPLO-PLANILHA-MODELO.xlsx')

print("=" * 80)
print("📊 ANÁLISE CURVA ABC - SIMULAÇÃO DO CÁLCULO")
print("=" * 80)

# Calcular valor total
df['Valor Total'] = df['Quantidade'] * df['Valor Unitário']

# Ordenar por valor total (decrescente)
df = df.sort_values('Valor Total', ascending=False).reset_index(drop=True)

# Calcular percentuais
valor_total_estoque = df['Valor Total'].sum()
df['% Valor'] = (df['Valor Total'] / valor_total_estoque) * 100
df['% Acumulado'] = df['% Valor'].cumsum()

print(f"\n💰 VALOR TOTAL DO ESTOQUE: R$ {valor_total_estoque:,.2f}")
print(f"📦 TOTAL DE PRODUTOS: {len(df)}")

# Classificar
def classificar(acum_anterior):
    if acum_anterior < 80:
        return 'A'
    elif acum_anterior < 95:
        return 'B'
    else:
        return 'C'

# Adicionar acumulado anterior
df['Acum Anterior'] = df['% Acumulado'].shift(1).fillna(0)
df['Classe'] = df['Acum Anterior'].apply(classificar)

print("\n" + "=" * 80)
print("📈 TOP 10 PRODUTOS (ordenados por valor)")
print("=" * 80)

for idx, row in df.head(10).iterrows():
    print(f"\n{idx + 1}º: {row['Descrição']}")
    print(f"   Código: {row['Código']}")
    print(f"   Quantidade: {row['Quantidade']}")
    print(f"   Valor Unitário: R$ {row['Valor Unitário']:,.2f}")
    print(f"   Valor Total: R$ {row['Valor Total']:,.2f}")
    print(f"   % do Valor: {row['% Valor']:.2f}%")
    print(f"   % Acumulado Anterior: {row['Acum Anterior']:.2f}%")
    print(f"   % Acumulado Atual: {row['% Acumulado']:.2f}%")
    print(f"   ➡️  CLASSE: {row['Classe']}")

print("\n" + "=" * 80)
print("📊 DISTRIBUIÇÃO POR CLASSE")
print("=" * 80)

for classe in ['A', 'B', 'C']:
    produtos_classe = df[df['Classe'] == classe]
    qtd = len(produtos_classe)
    valor_classe = produtos_classe['Valor Total'].sum()
    perc_classe = (valor_classe / valor_total_estoque) * 100
    
    print(f"\n{'🟢' if classe == 'A' else '🟡' if classe == 'B' else '🔴'} CLASSE {classe}:")
    print(f"   Quantidade de Produtos: {qtd}")
    print(f"   Valor Total: R$ {valor_classe:,.2f}")
    print(f"   Percentual do Estoque: {perc_classe:.2f}%")
    print(f"   Produtos:")
    for _, p in produtos_classe.iterrows():
        print(f"      • {p['Descrição']} (R$ {p['Valor Total']:,.2f})")

print("\n" + "=" * 80)
print("✅ RESULTADO ESPERADO NO APLICATIVO:")
print("=" * 80)

classe_a = df[df['Classe'] == 'A']
classe_b = df[df['Classe'] == 'B']
classe_c = df[df['Classe'] == 'C']

print(f"\n📊 Dashboard deve mostrar:")
print(f"   • Total de Produtos: {len(df)}")
print(f"   • Valor Total: R$ {valor_total_estoque:,.2f}")
print(f"   • Classe A: {len(classe_a)} produtos ({(classe_a['Valor Total'].sum()/valor_total_estoque*100):.1f}%)")
print(f"   • Classe B: {len(classe_b)} produtos ({(classe_b['Valor Total'].sum()/valor_total_estoque*100):.1f}%)")
print(f"   • Classe C: {len(classe_c)} produtos ({(classe_c['Valor Total'].sum()/valor_total_estoque*100):.1f}%)")

print("\n" + "=" * 80)
print("🔍 VERIFICAÇÃO DA LÓGICA:")
print("=" * 80)
print("\nCritério de classificação:")
print("   • Classe A: Produtos onde % Acum. ANTERIOR < 80%")
print("   • Classe B: Produtos onde 80% ≤ % Acum. ANTERIOR < 95%")
print("   • Classe C: Produtos onde % Acum. ANTERIOR ≥ 95%")

print("\n✅ CÁLCULO CONCLUÍDO!")
