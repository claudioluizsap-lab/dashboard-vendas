# Análise Curva ABC - Estoque

Aplicativo web moderno para análise de Curva ABC de estoque baseado em planilhas Excel.

## Funcionalidades

- Upload de planilhas Excel (XLS/XLSX)
- Cálculo automático da Curva ABC
- Classificação em categorias A, B e C
- Visualizações gráficas (pizza e barras)
- Tabela interativa com filtros
- Interface responsiva e moderna

## Tecnologias

- React 18
- TypeScript
- Vite
- Tailwind CSS
- Recharts (gráficos)
- XLSX (processamento Excel)

## Formato da Planilha

O aplicativo aceita planilhas com as seguintes colunas (nomes flexíveis):

- **Código/Codigo**: Código do produto
- **Descrição/Descricao/Produto**: Nome/descrição do produto
- **Quantidade/Qtd**: Quantidade em estoque
- **Valor Unitário/Preço**: Valor unitário do produto

## Como Usar

### Instalação

```bash
cd curva-abc-app
npm install
```

### Desenvolvimento

```bash
npm run dev
```

### Build para Produção

```bash
npm run build
```

## Sobre a Curva ABC

A Curva ABC é uma ferramenta de gestão que classifica itens de estoque em três categorias:

- **Classe A**: 80% do valor total (itens mais importantes)
- **Classe B**: 15% do valor total (itens intermediários)
- **Classe C**: 5% do valor total (itens menos importantes)

Isso permite priorizar a gestão dos itens mais relevantes financeiramente.
