import json
import openpyxl

PLANILHA = r"D:\Users\Claudio\OneDrive\Nova pasta\Bd_curva abc\curva abc.xlsx"
ABA = "Produtos mais vendidos"

wb = openpyxl.load_workbook(PLANILHA, read_only=True, data_only=True)
ws = wb[ABA]
rows = list(ws.iter_rows(values_only=True))
wb.close()

headers = [str(h).strip().lower() if h else "" for h in rows[0]]

def find_col(keywords):
    for i, h in enumerate(headers):
        for kw in keywords:
            if kw in h:
                return i
    return -1

idx_cod  = find_col(["cod"])
idx_desc = find_col(["desc"])
idx_qtd  = find_col(["quant", "qtd"])
idx_vunt = find_col(["unit"])
idx_vtot = find_col(["valor"])

produtos = []
for row in rows[1:]:
    if not any(row):
        continue
    try:
        qtd  = float(row[idx_qtd]  or 0) if idx_qtd  >= 0 else 0
        vunt = float(row[idx_vunt] or 0) if idx_vunt >= 0 else 0
        vtot = float(row[idx_vtot] or 0) if idx_vtot >= 0 else 0
        if vunt == 0 and qtd > 0 and vtot > 0:
            vunt = vtot / qtd
        if qtd == 0 and vtot == 0:
            continue
        produtos.append({
            "codigo":        str(row[idx_cod]  or "") if idx_cod  >= 0 else "",
            "descricao":     str(row[idx_desc] or "") if idx_desc >= 0 else "",
            "quantidade":    qtd,
            "valorUnitario": round(vunt, 4),
        })
    except:
        continue

with open("dist/dados.json", "w", encoding="utf-8") as f:
    json.dump(produtos, f, ensure_ascii=False)

print(f"OK! {len(produtos)} produtos carregados.")
