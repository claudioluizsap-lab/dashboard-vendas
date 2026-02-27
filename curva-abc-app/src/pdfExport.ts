import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import html2canvas from 'html2canvas';
import { CurvaABCResult } from './types';

export const exportToPDF = async (resultado: CurvaABCResult) => {
  const doc = new jsPDF('p', 'mm', 'a4');
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  let currentY = 20;

  doc.setFontSize(20);
  doc.setFont('helvetica', 'bold');
  doc.text('Análise Curva ABC - Estoque', pageWidth / 2, currentY, { align: 'center' });
  
  currentY += 10;
  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  doc.text(`Data: ${new Date().toLocaleDateString('pt-BR')}`, pageWidth / 2, currentY, { align: 'center' });

  currentY += 15;
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.text('Resumo Geral', 14, currentY);

  currentY += 10;
  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');

  const resumoData = [
    ['Total de Produtos', resultado.totais.quantidadeTotal.toString()],
    ['Valor Total do Estoque', resultado.totais.valorTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })],
    ['', ''],
    ['Classe A - Quantidade', `${resultado.categorias.A.quantidade} produtos`],
    ['Classe A - Valor', resultado.categorias.A.valorTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })],
    ['Classe A - Percentual', `${resultado.categorias.A.percentual.toFixed(2)}%`],
    ['', ''],
    ['Classe B - Quantidade', `${resultado.categorias.B.quantidade} produtos`],
    ['Classe B - Valor', resultado.categorias.B.valorTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })],
    ['Classe B - Percentual', `${resultado.categorias.B.percentual.toFixed(2)}%`],
    ['', ''],
    ['Classe C - Quantidade', `${resultado.categorias.C.quantidade} produtos`],
    ['Classe C - Valor', resultado.categorias.C.valorTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })],
    ['Classe C - Percentual', `${resultado.categorias.C.percentual.toFixed(2)}%`],
  ];

  autoTable(doc, {
    startY: currentY,
    head: [],
    body: resumoData,
    theme: 'grid',
    styles: { fontSize: 9, cellPadding: 3 },
    columnStyles: {
      0: { fontStyle: 'bold', cellWidth: 60 },
      1: { cellWidth: 'auto' }
    }
  });

  currentY = (doc as any).lastAutoTable.finalY + 15;

  if (currentY > pageHeight - 40) {
    doc.addPage();
    currentY = 20;
  }

  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.text('Detalhamento por Produto', 14, currentY);
  currentY += 7;

  const produtosData = resultado.produtos.map(p => [
    p.codigo,
    p.descricao.length > 30 ? p.descricao.substring(0, 30) + '...' : p.descricao,
    p.quantidade.toString(),
    p.valorUnitario.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }),
    p.valorTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }),
    `${p.percentualValor.toFixed(2)}%`,
    `${p.percentualAcumulado.toFixed(2)}%`,
    p.classificacao
  ]);

  autoTable(doc, {
    startY: currentY,
    head: [['Código', 'Descrição', 'Qtd', 'Valor Unit.', 'Valor Total', '% Valor', '% Acum.', 'Classe']],
    body: produtosData,
    theme: 'striped',
    styles: { fontSize: 7, cellPadding: 2 },
    headStyles: { fillColor: [79, 70, 229], fontStyle: 'bold' },
    columnStyles: {
      0: { cellWidth: 18 },
      1: { cellWidth: 45 },
      2: { cellWidth: 12, halign: 'right' },
      3: { cellWidth: 20, halign: 'right' },
      4: { cellWidth: 22, halign: 'right' },
      5: { cellWidth: 16, halign: 'right' },
      6: { cellWidth: 16, halign: 'right' },
      7: { cellWidth: 12, halign: 'center' }
    },
    didParseCell: (data) => {
      if (data.section === 'body' && data.column.index === 7) {
        const classe = data.cell.raw as string;
        if (classe === 'A') {
          data.cell.styles.fillColor = [220, 252, 231];
          data.cell.styles.textColor = [22, 101, 52];
          data.cell.styles.fontStyle = 'bold';
        } else if (classe === 'B') {
          data.cell.styles.fillColor = [254, 252, 232];
          data.cell.styles.textColor = [133, 77, 14];
          data.cell.styles.fontStyle = 'bold';
        } else if (classe === 'C') {
          data.cell.styles.fillColor = [254, 226, 226];
          data.cell.styles.textColor = [153, 27, 27];
          data.cell.styles.fontStyle = 'bold';
        }
      }
    }
  });

  const totalPages = (doc as any).internal.pages.length - 1;
  for (let i = 1; i <= totalPages; i++) {
    doc.setPage(i);
    doc.setFontSize(8);
    doc.setFont('helvetica', 'normal');
    doc.text(
      `Página ${i} de ${totalPages}`,
      pageWidth / 2,
      pageHeight - 10,
      { align: 'center' }
    );
  }

  doc.save(`curva-abc-${new Date().toISOString().split('T')[0]}.pdf`);
};

export const exportChartsAndTableToPDF = async (resultado: CurvaABCResult) => {
  const doc = new jsPDF('p', 'mm', 'a4');
  const pageWidth = doc.internal.pageSize.getWidth();
  let currentY = 20;

  doc.setFontSize(20);
  doc.setFont('helvetica', 'bold');
  doc.text('Análise Curva ABC - Estoque', pageWidth / 2, currentY, { align: 'center' });
  
  currentY += 10;
  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  doc.text(`Data: ${new Date().toLocaleDateString('pt-BR')}`, pageWidth / 2, currentY, { align: 'center' });
  currentY += 15;

  try {
    const chartsContainer = document.querySelector('.charts-container') as HTMLElement;
    if (chartsContainer) {
      const canvas = await html2canvas(chartsContainer, { 
        scale: 2,
        backgroundColor: '#ffffff'
      });
      const imgData = canvas.toDataURL('image/png');
      const imgWidth = pageWidth - 28;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      
      doc.addImage(imgData, 'PNG', 14, currentY, imgWidth, imgHeight);
      currentY += imgHeight + 10;
    }
  } catch (error) {
    console.error('Erro ao capturar gráficos:', error);
  }

  doc.addPage();
  currentY = 20;

  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.text('Detalhamento por Produto', 14, currentY);
  currentY += 7;

  const produtosData = resultado.produtos.map(p => [
    p.codigo,
    p.descricao.length > 30 ? p.descricao.substring(0, 30) + '...' : p.descricao,
    p.quantidade.toString(),
    p.valorUnitario.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }),
    p.valorTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }),
    `${p.percentualValor.toFixed(2)}%`,
    `${p.percentualAcumulado.toFixed(2)}%`,
    p.classificacao
  ]);

  autoTable(doc, {
    startY: currentY,
    head: [['Código', 'Descrição', 'Qtd', 'Valor Unit.', 'Valor Total', '% Valor', '% Acum.', 'Classe']],
    body: produtosData,
    theme: 'striped',
    styles: { fontSize: 7, cellPadding: 2 },
    headStyles: { fillColor: [79, 70, 229], fontStyle: 'bold' },
    columnStyles: {
      0: { cellWidth: 18 },
      1: { cellWidth: 45 },
      2: { cellWidth: 12, halign: 'right' },
      3: { cellWidth: 20, halign: 'right' },
      4: { cellWidth: 22, halign: 'right' },
      5: { cellWidth: 16, halign: 'right' },
      6: { cellWidth: 16, halign: 'right' },
      7: { cellWidth: 12, halign: 'center' }
    },
    didParseCell: (data) => {
      if (data.section === 'body' && data.column.index === 7) {
        const classe = data.cell.raw as string;
        if (classe === 'A') {
          data.cell.styles.fillColor = [220, 252, 231];
          data.cell.styles.textColor = [22, 101, 52];
          data.cell.styles.fontStyle = 'bold';
        } else if (classe === 'B') {
          data.cell.styles.fillColor = [254, 252, 232];
          data.cell.styles.textColor = [133, 77, 14];
          data.cell.styles.fontStyle = 'bold';
        } else if (classe === 'C') {
          data.cell.styles.fillColor = [254, 226, 226];
          data.cell.styles.textColor = [153, 27, 27];
          data.cell.styles.fontStyle = 'bold';
        }
      }
    }
  });

  const totalPages = (doc as any).internal.pages.length - 1;
  const pageHeight = doc.internal.pageSize.getHeight();
  for (let i = 1; i <= totalPages; i++) {
    doc.setPage(i);
    doc.setFontSize(8);
    doc.setFont('helvetica', 'normal');
    doc.text(
      `Página ${i} de ${totalPages}`,
      pageWidth / 2,
      pageHeight - 10,
      { align: 'center' }
    );
  }

  doc.save(`curva-abc-completo-${new Date().toISOString().split('T')[0]}.pdf`);
};
