import pandas as pd

print("="*60)
print("VERIFICAÇÃO DETALHADA DA PLANILHA")
print("="*60)

try:
    # Ler planilha
    df = pd.read_excel('planilha-teste-estoque.xlsx')
    
    print(f"\n✅ Planilha carregada com sucesso!")
    print(f"📊 Total de linhas: {len(df)}")
    print(f"📋 Colunas: {list(df.columns)}")
    
    print("\n" + "="*60)
    print("PRIMEIROS 5 PRODUTOS")
    print("="*60)
    
    for i in range(min(5, len(df))):
        row = df.iloc[i]
        print(f"\n🔹 Produto {i + 1}:")
        print(f"   Código: {row['Código']}")
        print(f"   Descrição: {row['Descrição']}")
        print(f"   Quantidade: {row['Quantidade']} (tipo: {type(row['Quantidade'])})")
        print(f"   Valor Unitário: R$ {row['Valor Unitário']:,.2f} (tipo: {type(row['Valor Unitário'])})")
        print(f"   Valor Total: R$ {row['Quantidade'] * row['Valor Unitário']:,.2f}")
    
    print("\n" + "="*60)
    print("ESTATÍSTICAS DAS COLUNAS")
    print("="*60)
    
    print(f"\n📈 Quantidade:")
    print(f"   Mínimo: {df['Quantidade'].min()}")
    print(f"   Máximo: {df['Quantidade'].max()}")
    print(f"   Média: {df['Quantidade'].mean():.2f}")
    print(f"   Tipo de dados: {df['Quantidade'].dtype}")
    
    print(f"\n💰 Valor Unitário:")
    print(f"   Mínimo: R$ {df['Valor Unitário'].min():,.2f}")
    print(f"   Máximo: R$ {df['Valor Unitário'].max():,.2f}")
    print(f"   Média: R$ {df['Valor Unitário'].mean():,.2f}")
    print(f"   Tipo de dados: {df['Valor Unitário'].dtype}")
    
    # Calcular valor total
    df['Valor Total'] = df['Quantidade'] * df['Valor Unitário']
    
    print(f"\n💵 Valor Total Calculado:")
    print(f"   Mínimo: R$ {df['Valor Total'].min():,.2f}")
    print(f"   Máximo: R$ {df['Valor Total'].max():,.2f}")
    print(f"   Soma: R$ {df['Valor Total'].sum():,.2f}")
    
    # Verificar valores nulos
    print(f"\n🔍 Verificação de Valores Nulos:")
    nulls = df.isnull().sum()
    if nulls.sum() == 0:
        print("   ✅ Nenhum valor nulo encontrado")
    else:
        for col, count in nulls.items():
            if count > 0:
                print(f"   ⚠️ {col}: {count} valores nulos")
    
    # Verificar zeros
    print(f"\n🔍 Verificação de Zeros:")
    zeros_qtd = (df['Quantidade'] == 0).sum()
    zeros_val = (df['Valor Unitário'] == 0).sum()
    
    if zeros_qtd == 0 and zeros_val == 0:
        print("   ✅ Nenhum zero encontrado")
    else:
        if zeros_qtd > 0:
            print(f"   ⚠️ Quantidade: {zeros_qtd} zeros")
        if zeros_val > 0:
            print(f"   ⚠️ Valor Unitário: {zeros_val} zeros")
    
    print("\n" + "="*60)
    print("✅ VERIFICAÇÃO COMPLETA!")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()
