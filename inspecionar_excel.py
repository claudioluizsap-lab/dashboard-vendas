import pandas as pd
import json

caminho = r'D:\Users\Claudio\OneDrive\Nova pasta\Bd_curva abc\21.02 curva abc.xlsx'

xl = pd.ExcelFile(caminho)
print("Planilhas encontradas:", xl.sheet_names)

for sheet in xl.sheet_names:
    df = pd.read_excel(caminho, sheet_name=sheet, nrows=5)
    print(f"\n--- Planilha: {sheet} ---")
    print("Colunas:", list(df.columns))
    print(df.head(3).to_string())
