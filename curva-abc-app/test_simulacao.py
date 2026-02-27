import pandas as pd
import json

# Simular exatamente o que o XLSX JavaScript faz
print("=== SIMULAÇÃO DO PROCESSAMENTO XLSX ===\n")

# Ler a planilha
df = pd.read_excel('planilha-teste-estoque.xlsx')

# Simular a remoção de acentos que o XLSX JavaScript faz
def remove_accents(text):
    # Mapeamento de caracteres com acento para sem acento
    accents = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i',
        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u',
        'ç': 'c',
        'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A',
        'É': 'E', 'È': 'E', 'Ê': 'E',
        'Í': 'I', 'Ì': 'I', 'Î': 'I',
        'Ó': 'O', 'Ò': 'O', 'Õ': 'O', 'Ô': 'O',
        'Ú': 'U', 'Ù': 'U', 'Û': 'U',
        'Ç': 'C'
    }
    result = text
    for char, replacement in accents.items():
        result = result.replace(char, replacement)
    return result

# Renomear colunas removendo acentos
df_no_accent = df.copy()
df_no_accent.columns = [remove_accents(col) for col in df.columns]

print("Colunas originais:", df.columns.tolist())
print("Colunas sem acento:", df_no_accent.columns.tolist())
print()

# Pegar primeira linha
first_row = df_no_accent.iloc[0].to_dict()
print("Primeira linha (como JavaScript vê):")
print(json.dumps(first_row, indent=2, ensure_ascii=False))
print()

# Testar o código de extração
row = first_row
codigo = row.get('Codigo') or row.get('Código') or ''
descricao = row.get('Descricao') or row.get('Descrição') or ''
quantidade = float(row.get('Quantidade') or 0)
valorUnitario = float(row.get('Valor Unitario') or row.get('Valor Unitário') or 0)
valorTotal = quantidade * valorUnitario

print("=== RESULTADO DO PROCESSAMENTO ===")
print(f"codigo: '{codigo}'")
print(f"descricao: '{descricao}'")
print(f"quantidade: {quantidade}")
print(f"valorUnitario: {valorUnitario}")
print(f"valorTotal: {valorTotal}")
print()

# Verificar todas as tentativas
print("=== TESTES DE ACESSO ===")
print(f"row.get('Valor Unitario'): {row.get('Valor Unitario')}")
print(f"row.get('Valor Unitário'): {row.get('Valor Unitário')}")
print(f"'Valor Unitario' in row: {'Valor Unitario' in row}")
print(f"'Valor Unitário' in row: {'Valor Unitário' in row}")
