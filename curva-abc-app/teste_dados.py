import json

# Simular exatamente o que o JavaScript xlsx faz
print('TESTE: Simulando XLSX.utils.sheet_to_json()')
print('='*60)

# Dados simulados como viriam do Excel
row = {
    'Código': 'P001',
    'Descrição': 'Notebook Dell Inspiron 15',
    'Quantidade': 25,
    'Valor Unitário': 3500
}

print('📋 Linha do Excel (como JSON):')
print(json.dumps(row, indent=2, ensure_ascii=False))

# Processar como o código faz
quantidade = float(row.get('Quantidade') or row.get('quantidade') or row.get('Qtd') or 0)
valorUnitario = float(row.get('Valor Unitário') or row.get('Valor Unitario') or row.get('Preço') or 0)
valorTotal = quantidade * valorUnitario

print('\n✅ Valores processados:')
print(f'   quantidade: {quantidade} (tipo: {type(quantidade).__name__})')
print(f'   valorUnitario: {valorUnitario} (tipo: {type(valorUnitario).__name__})')
print(f'   valorTotal: {valorTotal} (tipo: {type(valorTotal).__name__})')

# Criar objeto produto
produto = {
    'codigo': str(row['Código']),
    'descricao': str(row['Descrição']),
    'quantidade': quantidade,
    'valorUnitario': valorUnitario,
    'valorTotal': valorTotal
}

print('\n📦 Objeto produto criado:')
print(json.dumps(produto, indent=2, ensure_ascii=False))

# Verificar se campos existem
print('\n🔍 Verificação de campos:')
print(f'   produto.quantidade existe? {"quantidade" in produto}')
print(f'   produto.valorUnitario existe? {"valorUnitario" in produto}')
print(f'   produto.valorTotal existe? {"valorTotal" in produto}')
print(f'   produto.quantidade tem valor? {produto["quantidade"] != 0}')
print(f'   produto.valorUnitario tem valor? {produto["valorUnitario"] != 0}')
print(f'   produto.valorTotal tem valor? {produto["valorTotal"] != 0}')

print('\n' + '='*60)
print('✅ Se todos os testes acima passaram, o problema NÃO é o código!')
print('   O problema deve estar no navegador ou no React!')
print('='*60)
