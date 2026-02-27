# Deploy para Netlify (Método 1 - Mais Fácil)

## Via Interface Web (RECOMENDADO)

1. Acesse: https://app.netlify.com/
2. Faça login (pode usar GitHub, GitLab ou email)
3. Clique em "Add new site" → "Deploy manually"
4. Arraste a pasta `dist` para o campo de upload
5. Aguarde o deploy (30-60 segundos)
6. Sua aplicação estará online!

**URL gerada:** netlify fornecerá um link como `nome-aleatorio.netlify.app`

---

# Deploy para Vercel (Método 2)

## Via Interface Web

1. Acesse: https://vercel.com/
2. Faça login com GitHub
3. Clique em "Add New..." → "Project"
4. Importe o repositório (ou faça upload da pasta)
5. Configure:
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. Clique em "Deploy"

**URL gerada:** vercel fornecerá um link como `nome-projeto.vercel.app`

---

# Deploy para GitHub Pages (Método 3)

## Passo a Passo

### 1. Criar repositório no GitHub

```bash
cd curva-abc-app
git init
git add .
git commit -m "Initial commit - Curva ABC App"
```

### 2. No GitHub:
- Crie um novo repositório
- Copie a URL do repositório

### 3. Conectar e fazer push:

```bash
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
git branch -M main
git push -u origin main
```

### 4. Instalar gh-pages:

```bash
npm install --save-dev gh-pages
```

### 5. Adicionar scripts no package.json:

Adicione estas linhas em "scripts":
```json
"predeploy": "npm run build",
"deploy": "gh-pages -d dist"
```

### 6. Configurar vite.config.ts:

Adicione a propriedade `base`:
```typescript
export default defineConfig({
  base: '/SEU-REPOSITORIO/',
  // ... resto da configuração
})
```

### 7. Fazer deploy:

```bash
npm run deploy
```

### 8. Configurar GitHub Pages:
- Vá em Settings → Pages
- Source: Deploy from a branch
- Branch: gh-pages / root
- Save

**URL final:** `https://SEU-USUARIO.github.io/SEU-REPOSITORIO/`

---

# Deploy para Render (Método 4)

1. Acesse: https://render.com/
2. Crie uma conta
3. "New" → "Static Site"
4. Conecte seu repositório GitHub ou faça upload
5. Configure:
   - Build Command: `npm run build`
   - Publish Directory: `dist`
6. "Create Static Site"

**URL gerada:** `nome-projeto.onrender.com`

---

# Comparação Rápida

| Plataforma | Velocidade | Facilidade | URL Customizado | Limite |
|------------|-----------|------------|-----------------|---------|
| **Netlify** | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | Sim (grátis) | 100GB/mês |
| **Vercel** | ⚡⚡⚡ | ⭐⭐⭐⭐ | Sim (grátis) | 100GB/mês |
| **GitHub Pages** | ⚡⚡ | ⭐⭐⭐ | Sim (domínio próprio) | 1GB |
| **Render** | ⚡⚡ | ⭐⭐⭐⭐ | Sim (pago) | 100GB/mês |

---

# Recomendação

**Para iniciantes:** Use **Netlify** (Método 1)
- Mais simples
- Apenas arrastar e soltar
- Grátis
- Rápido

Basta arrastar a pasta `dist` no site do Netlify e pronto! ✅
