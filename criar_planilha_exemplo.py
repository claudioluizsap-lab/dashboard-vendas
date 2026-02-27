import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Credenciais"

ws.append(["SITE", "USUARIO", "SENHA"])
ws.append(["mercadolivre.com.br",   "seu_email@email.com", "sua_senha"])
ws.append(["amazon.com.br",         "seu_email@email.com", "sua_senha"])
ws.append(["americanas.com.br",     "seu_email@email.com", "sua_senha"])
ws.append(["magazineluiza.com.br",  "seu_email@email.com", "sua_senha"])
ws.append(["casasbahia.com.br",     "seu_email@email.com", "sua_senha"])
ws.append(["shopee.com.br",         "seu_email@email.com", "sua_senha"])
ws.append(["kabum.com.br",          "seu_email@email.com", "sua_senha"])
ws.append(["extra.com.br",          "seu_email@email.com", "sua_senha"])
ws.append(["pontofrio.com.br",      "",                    ""])
ws.append(["submarino.com.br",      "",                    ""])

for col in ws.columns:
    ws.column_dimensions[col[0].column_letter].width = 30

wb.save("planilha_exemplo.xlsx")
print("Planilha de exemplo criada: planilha_exemplo.xlsx")
