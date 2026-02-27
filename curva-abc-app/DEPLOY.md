# 🚀 Guia de Deploy - Aplicativo Curva ABC

## ✅ Build Concluído!

**Tamanho total:** 1.61 MB (9 arquivos)  
**Chunks otimizados:** Separação por funcionalidade para melhor cache

## 📦 Estrutura do Build

```
dist/
├── index.html (0.74 KB)
├── assets/
│   ├── index-Dvzi0-yc.css (16.80 KB)
│   ├── vendor-react-*.js (0.04 KB) - React loader
│   ├── purify.es-*.js (21.98 KB) - Sanitização
│   ├── index-*.js (25.19 KB) - Código da aplicação
│   ├── index.es-*.js (150.52 KB) - Utilitários
│   ├── vendor-excel-*.js (332.45 KB) - Processamento Excel
│   ├── vendor-charts-*.js (541.55 KB) - Gráficos
│   └── vendor-pdf-*.js (600.46 KB) - Exportação PDF
```

## 🌐 Opções de Deploy

### 1️⃣ Teste Local (Rápido)

```bash
npm run preview
```
Acesse: http://localhost:4173

---

### 2️⃣ Vercel (Recomendado - Grátis)

**Setup único:**
```bash
npm install -g vercel
vercel login
```

**Deploy:**
```bash
vercel --prod
```

✅ **Vantagens:**
- CDN global automático
- HTTPS gratuito
- Deploy em segundos
- Domínio personalizado grátis

---

### 3️⃣ Netlify (Alternativa Grátis)

**Setup único:**
```bash
npm install -g netlify-cli
netlify login
```

**Deploy:**
```bash
netlify deploy --prod --dir=dist
```

✅ **Vantagens:**
- Formulários integrados
- Functions serverless
- Split testing A/B

---

### 4️⃣ GitHub Pages (Grátis)

1. Crie repositório no GitHub
2. Instale gh-pages:
```bash
npm install --save-dev gh-pages
```

3. Adicione ao `package.json`:
```json
{
  "homepage": "https://SEU-USUARIO.github.io/curva-abc-app",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d dist"
  }
}
```

4. Deploy:
```bash
npm run deploy
```

---

### 5️⃣ Servidor Web Próprio

#### Apache

1. Copie `dist/*` para `/var/www/html/curva-abc/`

2. Crie `.htaccess`:
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /curva-abc/
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /curva-abc/index.html [L]
</IfModule>

# Cache estático por 1 ano
<FilesMatch "\.(js|css|woff2|woff|ttf|eot)$">
  Header set Cache-Control "max-age=31536000, public, immutable"
</FilesMatch>

# Cache HTML por 1 hora
<FilesMatch "\.(html)$">
  Header set Cache-Control "max-age=3600, must-revalidate"
</FilesMatch>

# Compressão Gzip
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript
</IfModule>
```

#### Nginx

```nginx
server {
    listen 80;
    server_name curva-abc.exemplo.com;
    root /var/www/curva-abc;
    index index.html;

    # Gzip
    gzip on;
    gzip_types text/css application/javascript application/json;
    gzip_min_length 1000;

    # Cache estático
    location ~* \.(js|css|woff2|woff|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "max-age=3600, must-revalidate";
    }
}
```

#### IIS (Windows Server)

1. Instale URL Rewrite Module
2. Copie `dist/*` para `C:\inetpub\wwwroot\curva-abc\`
3. Crie `web.config`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <rewrite>
      <rules>
        <rule name="SPA Routes" stopProcessing="true">
          <match url=".*" />
          <conditions logicalGrouping="MatchAll">
            <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" />
            <add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" />
          </conditions>
          <action type="Rewrite" url="/" />
        </rule>
      </rules>
    </rewrite>
    <staticContent>
      <clientCache cacheControlMode="UseMaxAge" cacheControlMaxAge="365.00:00:00" />
    </staticContent>
  </system.webServer>
</configuration>
```

---

### 6️⃣ Docker

**Dockerfile:**
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**nginx.conf:**
```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    gzip on;
    gzip_types text/css application/javascript;
}
```

**Build e run:**
```bash
docker build -t curva-abc .
docker run -p 8080:80 curva-abc
```

---

## 🔒 Checklist de Segurança

- [ ] HTTPS habilitado
- [ ] Headers de segurança configurados:
  ```
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  ```
- [ ] CSP (Content Security Policy) configurado
- [ ] Upload de arquivos validado no frontend

---

## ⚡ Otimizações de Performance

### Cache Strategy

| Tipo | Cache | Motivo |
|------|-------|--------|
| HTML | 1 hora | Permite atualizações rápidas |
| CSS/JS | 1 ano | Hash no nome do arquivo |
| Fontes | 1 ano | Raramente mudam |
| API | No-cache | Dados dinâmicos |

### CDN Recomendados

- **Cloudflare** (Grátis): https://cloudflare.com
- **Vercel Edge** (Incluído no Vercel)
- **Netlify CDN** (Incluído no Netlify)

---

## 📊 Monitoramento

### Google Analytics (Opcional)

Adicione ao `index.html` antes de `</head>`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 🐛 Troubleshooting

### Problema: Página branca após deploy
**Solução:** Verifique a configuração de SPA routing no servidor

### Problema: Erro 404 em rotas
**Solução:** Configure fallback para `index.html`

### Problema: Assets não carregam
**Solução:** Verifique o `base` no `vite.config.ts`

### Problema: Erro CORS
**Solução:** Configure CORS headers no servidor

---

## 📞 Suporte

- **Email**: seu-email@exemplo.com
- **Issues**: GitHub Issues
- **Documentação**: README.md

---

**Build criado em:** 2026-02-16  
**Versão:** 1.0.0  
**Build time:** 9.52s
