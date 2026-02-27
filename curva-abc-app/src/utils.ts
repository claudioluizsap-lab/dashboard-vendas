import * as XLSX from 'xlsx';
import { ProductData, ProductAnalysis, CurvaABCResult } from './types';

export interface CurvaABCThresholds {
  limiteA: number;
  limiteB: number;
}

const normalizar = (str: string): string =>
  str.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

const encontrarColuna = (headers: string[], palavras: string[]): number =>
  headers.findIndex(h => h && palavras.some(p => normalizar(String(h)).includes(p)));

const parseNumero = (valor: any): number => {
  if (valor === null || valor === undefined || valor === '') return 0;
  if (typeof valor === 'number') return valor;
  const str = String(valor).replace(/\./g, '').replace(',', '.').replace(/[^\d.-]/g, '');
  const n = parseFloat(str);
  return isNaN(n) ? 0 : n;
};

export const processExcelFile = (file: File, thresholds?: CurvaABCThresholds): Promise<CurvaABCResult> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const data = e.target?.result;
        const workbook = XLSX.read(data, { type: 'binary' });
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        const rawData = XLSX.utils.sheet_to_json(worksheet, { header: 1 }) as any[][];

        if (!rawData || rawData.length < 2) {
          reject(new Error('Planilha vazia ou sem dados.'));
          return;
        }

        const headers = rawData[0].map((h: any) => String(h || ''));

        const codigoIdx    = encontrarColuna(headers, ['cod']);
        const descricaoIdx = encontrarColuna(headers, ['desc', 'prod', 'nome', 'item']);
        const quantidadeIdx = encontrarColuna(headers, ['quant', 'qtd', 'qt']);
        const valorUnitIdx  = encontrarColuna(headers, ['unit', 'prec', 'vunit', 'valor u']);

        const produtos: ProductData[] = rawData
          .slice(1)
          .filter(row => row && row.some((c: any) => c !== null && c !== undefined && c !== ''))
          .map((row: any[]) => {
            const codigo       = codigoIdx >= 0    ? String(row[codigoIdx] || '') : '';
            const descricao    = descricaoIdx >= 0 ? String(row[descricaoIdx] || '') : '';
            const quantidade   = parseNumero(quantidadeIdx >= 0 ? row[quantidadeIdx] : 0);
            const valorUnitario = parseNumero(valorUnitIdx >= 0  ? row[valorUnitIdx]  : 0);

            return {
              codigo,
              descricao,
              quantidade,
              valorUnitario,
              valorTotal: quantidade * valorUnitario,
            };
          })
          .filter(p => p.descricao !== '' || p.codigo !== '');

        if (produtos.length === 0) {
          reject(new Error('Nenhum produto encontrado. Verifique os cabeçalhos da planilha.'));
          return;
        }

        const result = calcularCurvaABC(produtos, thresholds);
        resolve(result);
      } catch (error) {
        reject(error);
      }
    };

    reader.onerror = () => reject(new Error('Erro ao ler o arquivo.'));
    reader.readAsBinaryString(file);
  });
};

export const calcularCurvaABC = (
  produtos: ProductData[],
  thresholds: CurvaABCThresholds = { limiteA: 80, limiteB: 95 }
): CurvaABCResult => {
  const produtosOrdenados = [...produtos].sort((a, b) => b.valorTotal - a.valorTotal);
  const valorTotal = produtosOrdenados.reduce((sum, p) => sum + p.valorTotal, 0);

  if (valorTotal === 0) {
    return {
      produtos: produtosOrdenados.map(p => ({ ...p, percentualValor: 0, percentualAcumulado: 0, classificacao: 'C' as const })),
      totais: { quantidadeTotal: produtos.length, valorTotal: 0 },
      categorias: {
        A: { quantidade: 0, percentual: 0, valorTotal: 0 },
        B: { quantidade: 0, percentual: 0, valorTotal: 0 },
        C: { quantidade: produtos.length, percentual: 0, valorTotal: 0 },
      },
    };
  }

  let acumulado = 0;
  const produtosAnalisados: ProductAnalysis[] = produtosOrdenados.map((produto) => {
    const percentualValor = (produto.valorTotal / valorTotal) * 100;
    const acumuladoAnterior = acumulado;
    acumulado += percentualValor;

    let classificacao: 'A' | 'B' | 'C';
    if (acumuladoAnterior < thresholds.limiteA) {
      classificacao = 'A';
    } else if (acumuladoAnterior < thresholds.limiteB) {
      classificacao = 'B';
    } else {
      classificacao = 'C';
    }

    return { ...produto, percentualValor, percentualAcumulado: acumulado, classificacao };
  });

  const categorias = {
    A: { quantidade: 0, percentual: 0, valorTotal: 0 },
    B: { quantidade: 0, percentual: 0, valorTotal: 0 },
    C: { quantidade: 0, percentual: 0, valorTotal: 0 },
  };

  produtosAnalisados.forEach(p => {
    categorias[p.classificacao].quantidade++;
    categorias[p.classificacao].valorTotal += p.valorTotal;
  });

  categorias.A.percentual = (categorias.A.valorTotal / valorTotal) * 100;
  categorias.B.percentual = (categorias.B.valorTotal / valorTotal) * 100;
  categorias.C.percentual = (categorias.C.valorTotal / valorTotal) * 100;

  return {
    produtos: produtosAnalisados,
    totais: { quantidadeTotal: produtos.length, valorTotal },
    categorias,
  };
};
