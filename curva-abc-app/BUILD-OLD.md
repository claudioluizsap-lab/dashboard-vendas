# Curva ABC - Build de Produção

## ✅ Build Concluído com Sucesso!

A aplicação foi compilada e está pronta para produção na pasta `dist/`.

## 📦 Arquivos Gerados

```
dist/
├── index.html
├── assets/
│   ├── index-Dvzi0-yc.css (16.80 kB)
│   ├── purify.es-C_uT9hQ1.js (21.98 kB)
│   ├── index.es-CCUYsRPP.js (150.47 kB)
│   └── index-B_f6wYbw.js (1.5 MB)
```

## 🚀 Como Usar

### Opção 1: Preview Local (Recomendado para Testes)

```bash
npm run preview
```

Isso iniciará um servidor local em `http://localhost:4173/`

### Opção 2: Servidor Web Simples (Python)

```bash
cd dist
python -m http.server 8000
```

Acesse: `http://localhost:8000`

### Opção 3: Deploy em Servidor Web

Copie todo o conteúdo da pasta `dist/` para seu servidor web (Apache, Nginx, IIS, etc.).

**Configuração necessária:**
- A pasta `dist/` deve ser a raiz do servidor ou configurar o caminho base
- Para SPAs, configure redirecionamento para `index.html`

## 🌐 Deploy em Serviços de Hosting

### Vercel
```bash
npm install -g vercel
vercel --prod
```

### Netlify
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

### GitHub Pages
1. Crie um repositório no GitHub
2. Configure GitHub Pages para usar a branch `gh-pages`
3. Use o pacote `gh-pages`:
```bash
npm install -g gh-pages
gh-pages -d dist
```

### Servidor Apache (.htaccess)
Crie um arquivo `.htaccess` na pasta `dist/`:
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

### Nginx
```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    root /caminho/para/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## 📊 Estatísticas do Build

- **Tempo de build:** 10.23s
- **Tamanho total:** ~1.7 MB
- **Tamanho gzipped:** ~464 KB
- **Módulos transformados:** 1196

## ⚠️ Nota sobre Tamanho

O bundle principal é de 1.5 MB devido às bibliotecas:
- **React & React-DOM**: ~140 KB
- **Recharts**: ~600 KB (visualizações)
- **xlsx**: ~500 KB (processamento Excel)
- **jspdf + autotable**: ~200 KB (exportação PDF)

Para otimizar:
1. Considere lazy loading dos componentes de gráficos
2. Use code splitting para exportação PDF
3. Implemente cache agressivo no servidor

## 🔧 Scripts Úteis

```bash
# Desenvolvimento
npm run dev

# Build de produção
npm run build

# Preview do build
npm run preview

# Limpar e rebuildar
rm -rf dist && npm run build
```

## 📱 Compatibilidade

- ✅ Chrome/Edge (últimas 2 versões)
- ✅ Firefox (últimas 2 versões)
- ✅ Safari (últimas 2 versões)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🎯 Funcionalidades Incluídas

- ✅ Upload e processamento de Excel
- ✅ Análise de Curva ABC configurável
- ✅ Gráficos interativos (pizza e barras)
- ✅ Tabela com filtros por classe
- ✅ Exportação para PDF
- ✅ Modo escuro/claro
- ✅ Design responsivo
- ✅ PWA ready (pode ser instalado como app)

---

**Data do build:** 2026-02-16
**Versão:** 1.0.0
