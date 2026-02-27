import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from datetime import datetime

df = pd.read_csv('exemplo_estoque.csv')
doc = SimpleDocTemplate('Listagem_Estoque.pdf', pagesize=A4)
styles = getSampleStyleSheet()
elementos = []

elementos.append(Paragraph('<b>LISTAGEM DE ESTOQUE</b>', styles['Title']))
elementos.append(Spacer(1, 0.2*inch))
elementos.append(Paragraph(f'<i>Gerado em: {datetime.now().strftime("%d/%m/%Y às %H:%M")}</i>', styles['Normal']))
elementos.append(Spacer(1, 0.3*inch))

dados = [['Código', 'Produto', 'Quantidade']]
for _, row in df.iterrows():
    dados.append([row['Código'], row['Produto'], f"{row['Quantidade']:,}"])

tabela = Table(dados, colWidths=[1*inch, 4*inch, 1.2*inch])
tabela.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
]))

elementos.append(tabela)
elementos.append(Spacer(1, 0.3*inch))
elementos.append(Paragraph(f'<b>Total: {df["Quantidade"].sum():,} unidades</b>', styles['Normal']))

doc.build(elementos)
print('✓ PDF simples gerado: Listagem_Estoque.pdf')
