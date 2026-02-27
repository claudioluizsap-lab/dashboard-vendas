import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

def exportar_relatorio_completo():
    """Exporta o relatório ABC completo com gráficos para PDF"""
    
    print("=" * 70)
    print("  EXPORTAÇÃO PARA PDF - RELATÓRIO ABC DE MERCADORIAS")
    print("=" * 70)
    
    # Carregar dados
    try:
        df = pd.read_csv('exemplo_estoque.csv')
        print("✓ Dados carregados: exemplo_estoque.csv")
    except:
        print("❌ Erro ao carregar planilha!")
        return
    
    # Calcular análise ABC
    df = df.sort_values('Quantidade', ascending=False).reset_index(drop=True)
    df['Percentual'] = (df['Quantidade'] / df['Quantidade'].sum()) * 100
    df['Percentual Acumulado'] = df['Percentual'].cumsum()
    
    def classificar_abc(percentual_acum):
        if percentual_acum <= 80:
            return 'A'
        elif percentual_acum <= 95:
            return 'B'
        else:
            return 'C'
    
    df['Classe ABC'] = df['Percentual Acumulado'].apply(classificar_abc)
    
    # Criar PDF
    arquivo_pdf = 'Relatorio_ABC_Mercadorias.pdf'
    doc = SimpleDocTemplate(
        arquivo_pdf,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1F4788'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#4472C4'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12
    )
    
    # Elementos do PDF
    elementos = []
    
    # Título
    titulo = Paragraph("RELATÓRIO DE ANÁLISE ABC DE MERCADORIAS", title_style)
    elementos.append(titulo)
    
    # Data
    data_atual = datetime.now().strftime("%d/%m/%Y às %H:%M")
    data_texto = Paragraph(f"<i>Gerado em: {data_atual}</i>", normal_style)
    elementos.append(data_texto)
    elementos.append(Spacer(1, 0.3*inch))
    
    # Resumo executivo
    resumo_classe = df.groupby('Classe ABC').agg(
        Qtd_Itens=('Código', 'count'),
        Qtd_Total=('Quantidade', 'sum')
    ).reset_index()
    
    resumo_texto = f"""
    <b>RESUMO EXECUTIVO</b><br/>
    <br/>
    Total de itens analisados: <b>{len(df)}</b><br/>
    Quantidade total em estoque: <b>{df['Quantidade'].sum():,}</b> unidades<br/>
    <br/>
    <b>Distribuição por Classe ABC:</b><br/>
    """
    
    for _, row in resumo_classe.iterrows():
        perc = (row['Qtd_Total'] / df['Quantidade'].sum()) * 100
        resumo_texto += f"• Classe {row['Classe ABC']}: {row['Qtd_Itens']} itens ({row['Qtd_Total']:,} unidades - {perc:.1f}%)<br/>"
    
    elementos.append(Paragraph(resumo_texto, normal_style))
    elementos.append(Spacer(1, 0.3*inch))
    
    # Tabela completa
    elementos.append(Paragraph("TABELA DETALHADA - ANÁLISE ABC", subtitle_style))
    
    # Preparar dados da tabela
    dados_tabela = [['Código', 'Produto', 'Quantidade', '%', '% Acum.', 'Classe']]
    
    for _, row in df.iterrows():
        dados_tabela.append([
            row['Código'],
            row['Produto'][:40],  # Limitar tamanho do nome
            f"{row['Quantidade']:,}",
            f"{row['Percentual']:.2f}%",
            f"{row['Percentual Acumulado']:.2f}%",
            row['Classe ABC']
        ])
    
    # Criar tabela
    tabela = Table(dados_tabela, colWidths=[0.8*inch, 3.5*inch, 1.2*inch, 0.8*inch, 1*inch, 0.8*inch])
    
    # Estilo da tabela
    estilo_tabela = TableStyle([
        # Cabeçalho
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Dados
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Código
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Produto
        ('ALIGN', (2, 1), (-1, -1), 'CENTER'), # Resto
        
        # Bordas
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#4472C4')),
        
        # Zebra striping
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F2F2F2')])
    ])
    
    # Colorir classes ABC
    for i, row in enumerate(df.iterrows(), start=1):
        classe = row[1]['Classe ABC']
        if classe == 'A':
            cor = colors.HexColor('#00B050')
        elif classe == 'B':
            cor = colors.HexColor('#FFC000')
        else:
            cor = colors.HexColor('#FF0000')
        
        estilo_tabela.add('BACKGROUND', (5, i), (5, i), cor)
        estilo_tabela.add('TEXTCOLOR', (5, i), (5, i), colors.whitesmoke)
        estilo_tabela.add('FONTNAME', (5, i), (5, i), 'Helvetica-Bold')
    
    tabela.setStyle(estilo_tabela)
    elementos.append(tabela)
    elementos.append(Spacer(1, 0.3*inch))
    
    # Adicionar nova página para gráficos (se existirem)
    if os.path.exists('graficos/distribuicao_classe_abc.png'):
        elementos.append(PageBreak())
        elementos.append(Paragraph("ANÁLISE VISUAL", subtitle_style))
        elementos.append(Spacer(1, 0.2*inch))
        
        # Gráfico de distribuição
        if os.path.exists('graficos/distribuicao_classe_abc.png'):
            img = Image('graficos/distribuicao_classe_abc.png', width=4.5*inch, height=3.6*inch)
            elementos.append(img)
            elementos.append(Spacer(1, 0.2*inch))
        
        # Gráfico top 15
        if os.path.exists('graficos/top15_produtos.png'):
            elementos.append(PageBreak())
            img2 = Image('graficos/top15_produtos.png', width=7*inch, height=5*inch)
            elementos.append(img2)
    
    # Rodapé com legenda
    elementos.append(Spacer(1, 0.3*inch))
    legenda = """
    <b>LEGENDA CLASSE ABC:</b><br/>
    <font color="#00B050"><b>Classe A</b></font>: Itens mais importantes (até 80% do valor acumulado)<br/>
    <font color="#FFC000"><b>Classe B</b></font>: Itens intermediários (80% a 95% do valor acumulado)<br/>
    <font color="#FF0000"><b>Classe C</b></font>: Itens menos importantes (acima de 95% do valor acumulado)
    """
    elementos.append(Paragraph(legenda, normal_style))
    
    # Gerar PDF
    doc.build(elementos)
    
    print(f"✓ PDF gerado com sucesso: {arquivo_pdf}")
    print(f"✓ Total de páginas: {len(elementos) // 10 + 1}")
    print(f"✓ Formato: {landscape(A4)}")
    
    return arquivo_pdf

def exportar_estoque_simples():
    """Exporta listagem simples do estoque para PDF"""
    
    print("\n" + "=" * 70)
    print("  EXPORTAÇÃO SIMPLES PARA PDF")
    print("=" * 70)
    
    # Carregar dados
    try:
        df = pd.read_csv('exemplo_estoque.csv')
    except:
        print("❌ Erro ao carregar planilha!")
        return
    
    arquivo_pdf = 'Listagem_Estoque.pdf'
    doc = SimpleDocTemplate(arquivo_pdf, pagesize=A4)
    
    styles = getSampleStyleSheet()
    elementos = []
    
    # Título
    titulo = Paragraph("<b>LISTAGEM DE ESTOQUE</b>", styles['Title'])
    elementos.append(titulo)
    elementos.append(Spacer(1, 0.2*inch))
    
    # Data
    data_atual = datetime.now().strftime("%d/%m/%Y às %H:%M")
    data_p = Paragraph(f"<i>Gerado em: {data_atual}</i>", styles['Normal'])
    elementos.append(data_p)
    elementos.append(Spacer(1, 0.3*inch))
    
    # Tabela
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
    
    # Total
    total = Paragraph(f"<b>Total: {df['Quantidade'].sum():,} unidades</b>", styles['Normal'])
    elementos.append(total)
    
    doc.build(elementos)
    print(f"✓ PDF gerado: {arquivo_pdf}")
    
    return arquivo_pdf

if __name__ == "__main__":
    print("\nEscolha o tipo de exportação:")
    print("1. Relatório ABC Completo (com análise e gráficos)")
    print("2. Listagem Simples de Estoque")
    
    escolha = input("\nOpção (1 ou 2): ").strip()
    
    if escolha == "1":
        arquivo = exportar_relatorio_completo()
    elif escolha == "2":
        arquivo = exportar_estoque_simples()
    else:
        print("❌ Opção inválida!")
        exit(1)
    
    print(f"\n✓ Arquivo gerado: {arquivo}")
    print("\n🎉 Exportação concluída com sucesso!")
    
    # Abrir PDF automaticamente
    import subprocess
    try:
        subprocess.run(['start', '', arquivo], shell=True, check=True)
        print(f"✓ Abrindo {arquivo}...")
    except:
        print(f"⚠️ Abra manualmente o arquivo: {arquivo}")
