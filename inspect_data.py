import msoffcrypto, io, openpyxl, warnings, datetime
warnings.filterwarnings('ignore')

with open('2025_temp.xlsx','rb') as f:
    of = msoffcrypto.OfficeFile(f)
    of.load_key(password='1515')
    dec = io.BytesIO()
    of.decrypt(dec)

dec.seek(0)
wb = openpyxl.load_workbook(dec, data_only=True)
ws = wb['CALCULOS ']

header = [c.value for c in list(ws.iter_rows(min_row=1, max_row=1))[0]]
datas  = [c for c in header if isinstance(c, datetime.datetime)]

cats = []; rows_data = []
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0] and str(row[0]).strip():
        cats.append(str(row[0]).strip())
        rows_data.append(row)

print('Categorias:', len(cats), cats[:20])
print('Meses:', len(datas), datas[0].strftime('%m/%Y'), '->', datas[-1].strftime('%m/%Y'))

# totais por categoria
for cat, row in list(zip(cats, rows_data))[:5]:
    total = sum(v for v in row[2:] if isinstance(v,(int,float)) and v)
    print(f'  {cat}: R$ {total:,.2f}')
