import pandas as pd

# Simular exatamente o que o JavaScript faz
df = pd.read_excel('planilha-teste-estoque.xlsx')

print('SIMULAÇÃO DO PROCESSAMENTO JAVASCRIPT')
print('='*60)

# Processar como o JS faz
produtos = []
for i, row in df.iterrows():
    quantidade = float(row['Quantidade'])
    valorUnitario = float(row['Valor Unitário'])
    valorTotal = quantidade * valorUnitario
    
    produto = {
        'codigo': str(row['Código']),
        'descricao': str(row['Descrição']),
        'quantidade': quantidade,
        'valorUnitario': valorUnitario,
        'valorTotal': valorTotal
    }
    produtos.append(produto)
    
    if i < 3:
        print(f'\nProduto {i+1}:')
        print(f'  Código: {produto["codigo"]}')
        print(f'  Descrição: {produto["descricao"]}')
        print(f'  Quantidade: {produto["quantidade"]}')
        print(f'  Valor Unit: R$ {produto["valorUnitario"]:,.2f}')
        print(f'  Valor Total: R$ {produto["valorTotal"]:,.2f}')

print(f'\n✅ Total de produtos processados: {len(produtos)}')

valor_total_geral = sum(p["valorTotal"] for p in produtos)
print(f'💰 Valor total do estoque: R$ {valor_total_geral:,.2f}')

# Ordenar
produtos.sort(key=lambda x: x['valorTotal'], reverse=True)

print(f'\n🥇 Produto mais valioso: {produtos[0]["descricao"]} - R$ {produtos[0]["valorTotal"]:,.2f}')
print(f'🥈 Segundo mais valioso: {produtos[1]["descricao"]} - R$ {produtos[1]["valorTotal"]:,.2f}')

# Calcular Curva ABC
print('\n' + '='*60)
print('CÁLCULO DA CURVA ABC')
print('='*60)

acumulado = 0
for i, produto in enumerate(produtos):
    percentual_valor = (produto['valorTotal'] / valor_total_geral) * 100
    acumulado_anterior = acumulado
    acumulado += percentual_valor
    
    if acumulado_anterior < 80:
        classe = 'A'
    elif acumulado_anterior < 95:
        classe = 'B'
    else:
        classe = 'C'
    
    produto['percentualValor'] = percentual_valor
    produto['percentualAcumulado'] = acumulado
    produto['classificacao'] = classe
    
    if i < 5:
        print(f'\n{i+1}. {produto["descricao"][:30]}')
        print(f'   Valor Total: R$ {produto["valorTotal"]:,.2f}')
        print(f'   % Valor: {percentual_valor:.2f}%')
        print(f'   % Acum: {acumulado:.2f}%')
        print(f'   Classe: {classe}')

# Contar por classe
classe_a = sum(1 for p in produtos if p['classificacao'] == 'A')
classe_b = sum(1 for p in produtos if p['classificacao'] == 'B')
classe_c = sum(1 for p in produtos if p['classificacao'] == 'C')

print(f'\n' + '='*60)
print('DISTRIBUIÇÃO POR CLASSE')
print('='*60)
print(f'Classe A: {classe_a} produtos')
print(f'Classe B: {classe_b} produtos')
print(f'Classe C: {classe_c} produtos')
print(f'Total: {classe_a + classe_b + classe_c} produtos')

if classe_a + classe_b + classe_c == len(produtos):
    print('\n✅ CÁLCULO CORRETO!')
else:
    print('\n❌ ERRO NO CÁLCULO!')
