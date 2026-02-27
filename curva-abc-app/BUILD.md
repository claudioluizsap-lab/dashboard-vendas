# Análise Curva ABC - Build de Produção

## ✅ Build Concluído com Sucesso!

A aplicação foi compilada e otimizada para produção na pasta `dist/`.

## 📦 Arquivos Gerados

```
dist/
├── index.html (0.74 KB)
├── assets/
│   ├── index-Dvzi0-yc.css (16.80 KB) - Estilos
│   ├── vendor-react-*.js (0.04 KB) - React loader
│   ├── purify.es-*.js (21.98 KB) - Sanitização
│   ├── index-*.js (25.19 KB) - Código da aplicação
│   ├── index.es-*.js (150.52 KB) - Utilitários
│   ├── vendor-excel-*.js (332.45 KB) - Processamento Excel (xlsx)
│   ├── vendor-charts-*.js (541.55 KB) - Gráficos (Recharts)
│   └── vendor-pdf-*.js (600.46 KB) - Exportação PDF (jspdf)
```

**Total:** ~1.61 MB (gzipped: ~464 KB)

### Otimizações Aplicadas

✅ **Code splitting implementado** - Bibliotecas separadas em chunks independentes  
✅ **Tree shaking** - Código não utilizado removido automaticamente  
✅ **Minificação** - CSS e JavaScript otimizados  
✅ **Cache-busting** - Hashes nos nomes dos arquivos para cache eficiente  
✅ **Compressão Gzip** - Reduz tamanho em ~70% quando servido com gzip

### Benefícios do Code Splitting

- **Cache eficiente**: Bibliotecas raramente mudam, então ficam em cache do navegador
- **Carregamento paralelo**: Chunks são baixados simultaneamente
- **Updates incrementais**: Apenas arquivos alterados precisam ser baixados novamente

## 🚀 Como Usar

### Teste Local

```bash
npm run preview
```

Acessa em: `http://localhost:4173/`

### Deploy em Produção

**📖 Consulte o guia completo de deploy:** [DEPLOY.md](./DEPLOY.md)

O arquivo `DEPLOY.md` contém instruções detalhadas para:
- Vercel (deploy em 1 comando)
- Netlify (alternativa ao Vercel)
- GitHub Pages (hospedagem grátis)
- Servidores próprios (Apache, Nginx, IIS)
- Docker (containerização)
- Configurações de segurança e performance

## 📊 Estatísticas do Build

- **Tempo de build:** 9.52s
- **Tamanho total:** 1.61 MB
- **Tamanho gzipped:** ~464 KB
- **Módulos transformados:** 1,196
- **Chunks gerados:** 9

## 📈 Distribuição de Tamanho

| Chunk | Tamanho | Comprimido | Conteúdo |
|-------|---------|------------|----------|
| vendor-pdf | 600 KB | 179 KB | jspdf + autotable + html2canvas |
| vendor-charts | 541 KB | 154 KB | Recharts (visualizações) |
| vendor-excel | 332 KB | 114 KB | xlsx (processamento Excel) |
| index.es | 150 KB | 51 KB | Utilitários e dependências |
| Outros | ~37 KB | ~13 KB | App + CSS + React |

## 🔧 Scripts Úteis

```bash
# Desenvolvimento
npm run dev

# Build de produção
npm run build

# Preview do build
npm run preview

# Build limpo (Windows)
build-prod.bat

# Build limpo (Linux/Mac)
./build-prod.sh
```

## 📱 Compatibilidade

- ✅ Chrome/Edge (últimas 2 versões)
- ✅ Firefox (últimas 2 versões)
- ✅ Safari (últimas 2 versões)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🎯 Funcionalidades Incluídas

- ✅ Upload e processamento de Excel (.xls, .xlsx)
- ✅ Análise de Curva ABC com limites configuráveis
- ✅ Gráficos interativos (pizza e barras)
- ✅ Tabela responsiva com filtros por classe (A, B, C)
- ✅ Exportação para PDF (simples e com gráficos)
- ✅ Modo escuro/claro (salva preferência)
- ✅ Design responsivo (mobile-first)
- ✅ PWA ready (pode ser instalado como app)

## 🔍 Verificação da Build

Para verificar a integridade dos arquivos gerados:

```bash
# Windows
dir dist /s

# Linux/Mac
ls -lhR dist/
```

## ⚠️ Notas Importantes

1. **Tamanho dos chunks**: Os chunks maiores (PDF, Charts, Excel) são carregados apenas quando necessários
2. **Compressão**: Configure gzip/brotli no servidor para reduzir o tamanho em ~70%
3. **Cache**: Com os hashes nos nomes, configure cache agressivo (1 ano) para arquivos estáticos
4. **HTTPS**: Sempre use HTTPS em produção para segurança

## 🐛 Troubleshooting

### Build falha com erro de memória
```bash
# Aumente o limite de memória do Node
set NODE_OPTIONS=--max-old-space-size=4096
npm run build
```

### Arquivos muito grandes
O tamanho é esperado devido às bibliotecas incluídas. Com gzip habilitado no servidor, o tamanho real de download é ~464 KB.

### Erro ao fazer preview
```bash
# Pare processos anteriores e tente novamente
npm run build
npm run preview
```

---

**Data do build:** 2026-02-16  
**Versão:** 1.0.0  
**Node version:** 18+  
**Build tool:** Vite 5.4.21
