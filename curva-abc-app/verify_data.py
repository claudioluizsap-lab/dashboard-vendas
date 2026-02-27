import pandas as pd
import sys

file_path = sys.argv[1] if len(sys.argv) > 1 else 'planilha-teste-estoque.xlsx'

try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Erro: Arquivo '{file_path}' não encontrado!")
    sys.exit(1)
except Exception as e:
    print(f"Erro ao ler arquivo: {e}")
    sys.exit(1)

df['Valor Total'] = df['Quantidade'] * df['Valor Unitário']
df = df.sort_values('Valor Total', ascending=False)

valor_total_geral = df['Valor Total'].sum()
df['percentualValor'] = (df['Valor Total'] / valor_total_geral) * 100
df['percentualAcumulado'] = df['percentualValor'].cumsum()

print(f'VERIFICACAO DOS DADOS: {file_path}')
print()
print('Primeiros 3 produtos:')
print()
for i, row in df.head(3).iterrows():
    print(f"Codigo: {row['Código']}")
    print(f"Descricao: {row['Descrição']}")
    print(f"Quantidade: {row['Quantidade']}")
    print(f"Valor Unit: R$ {row['Valor Unitário']:.2f}")
    print(f"Valor Total: R$ {row['Valor Total']:.2f}")
    print(f"% Valor: {df.loc[i, 'percentualValor']:.2f}%")
    print(f"% Acumulado: {df.loc[i, 'percentualAcumulado']:.2f}%")
    print()
