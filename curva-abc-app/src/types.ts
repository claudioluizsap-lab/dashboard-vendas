export interface ProductData {
  codigo: string;
  descricao: string;
  quantidade: number;
  valorUnitario: number;
  valorTotal: number;
}

export interface ProductAnalysis extends ProductData {
  percentualValor: number;
  percentualAcumulado: number;
  classificacao: 'A' | 'B' | 'C';
}

export interface CurvaABCResult {
  produtos: ProductAnalysis[];
  totais: {
    quantidadeTotal: number;
    valorTotal: number;
  };
  categorias: {
    A: { quantidade: number; percentual: number; valorTotal: number };
    B: { quantidade: number; percentual: number; valorTotal: number };
    C: { quantidade: number; percentual: number; valorTotal: number };
  };
}
