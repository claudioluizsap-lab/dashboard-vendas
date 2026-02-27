# 🔍 GUIA DE TROUBLESHOOTING - Curva ABC

## ❌ Problema Relatado: "Não está calculando os resultados"

### ✅ Verificações Realizadas

1. **Planilha está correta** ✅
   - 30 produtos com quantidades
   - Todas as colunas presentes
   - Sem valores nulos ou zeros

2. **Lógica de cálculo está correta** ✅
   - Simulação Python confirmou o cálculo
   - Distribuição: 17 A, 9 B, 4 C
   - Valor total: R$ 1.032.550,00

3. **Logs de debug adicionados** ✅
   - Mostra chaves da planilha
   - Mostra primeiros 3 produtos
   - Mostra resultado final
   - Mostra atualização do estado React

---

## 🧪 Como Verificar no Navegador

### Passo 1: Abrir o Aplicativo
```
URL: http://localhost:4177
```

### Passo 2: Abrir o Console
```
Pressione F12
Clique na aba "Console"
```

### Passo 3: Fazer Upload da Planilha
```
Clique em "Escolher arquivo"
Selecione: planilha-teste-estoque.xlsx
```

### Passo 4: Verificar Logs no Console

Você deve ver esta sequência de logs:

```javascript
📁 Arquivo selecionado: planilha-teste-estoque.xlsx
⏳ Processando arquivo...
🔍 Primeira linha da planilha: {Código: "P001", Descrição: "Notebook Dell...", Quantidade: 25, Valor Unitário: 3500}
🔑 Chaves disponíveis: (4) ["Código", "Descrição", "Quantidade", "Valor Unitário"]
📦 Produto 1: {codigo: "P001", descricao: "Notebook Dell Inspiron 15", quantidade: 25, valorUnitario: 3500, valorTotal: 87500}
📦 Produto 2: {codigo: "P002", descricao: "Mouse Logitech MX Master", quantidade: 150, valorUnitario: 450, valorTotal: 67500}
📦 Produto 3: {codigo: "P003", descricao: "Teclado Mecânico Keychron", quantidade: 80, valorUnitario: 650, valorTotal: 52000}
✅ Resultado recebido: {produtos: Array(30), totais: {…}, categorias: {…}}
📊 Produtos: 30
💰 Valor total: 1032550
🎯 Setando resultado no estado...
✅ Estado atualizado!
🔔 Resultado atualizado no estado!
   Produtos: 30
   Valor total: 1032550
   Classe A: 17
   Classe B: 9
   Classe C: 4
```

---

## 🔍 Diagnósticos

### Cenário 1: Não aparece nenhum log
**Problema:** JavaScript não está carregando  
**Solução:**
```bash
cd curva-abc-app
npm run build
npm run preview
```

### Cenário 2: Logs aparecem mas tabela fica vazia
**Problema:** Render do React não está funcionando  
**O que verificar:**
1. Console mostra "🔔 Resultado atualizado no estado!" ?
2. Quantos produtos aparecem?
3. Há erros de JavaScript no console?

### Cenário 3: Upload não funciona
**Problema:** Input de arquivo não está funcionando  
**O que fazer:**
1. Verificar se o input está visível na tela
2. Tentar arrastar e soltar o arquivo
3. Verificar permissões do navegador

### Cenário 4: "Nenhum produto encontrado"
**Problema:** Planilha não está sendo lida corretamente  
**Verificar nos logs:**
```javascript
🔑 Chaves disponíveis: [...]
```
Se as chaves estiverem diferentes de:
`["Código", "Descrição", "Quantidade", "Valor Unitário"]`

Então o problema é a planilha.

### Cenário 5: Quantidade aparece como 0
**Problema:** Mapeamento de colunas  
**Verificar log:**
```javascript
📦 Produto 1: {quantidade: ???}
```
Se quantidade for 0, mas na planilha tem valor:
- A coluna pode ter nome diferente
- Adicionar variação do nome em utils.ts linha 26

---

## 🐛 Possíveis Problemas e Soluções

### Problema: Colunas com nomes diferentes

Se sua planilha tem colunas com nomes como:
- "Qtde" em vez de "Quantidade"
- "Preço Unit" em vez de "Valor Unitário"
- "Item" em vez de "Código"

**Solução:** Editar `src/utils.ts` linha 24-27:

```typescript
const quantidade = parseFloat(
  row['Quantidade'] || 
  row['quantidade'] || 
  row['QUANTIDADE'] || 
  row['Qtd'] || 
  row['qtd'] ||
  row['Qtde'] ||  // Adicionar variação
  0
);
```

### Problema: Valores não numéricos

Se a planilha tem valores como:
- "R$ 1.500,00" (com símbolo de moeda)
- "1.500" (com ponto de milhar)

**Solução:** Limpar a planilha ou adaptar o parseFloat.

### Problema: Excel antigo (.xls)

Se o arquivo for .xls (Excel 97-2003):
- Converter para .xlsx
- Ou instalar suporte adicional

---

## 📊 Resultados Esperados

Após upload bem-sucedido, você deve ver:

### Cards no topo:
```
Classe A (até 80%)     | Classe B (80-95%)    | Classe C (acima de 95%)
17 produtos            | 9 produtos           | 4 produtos
77.7% do valor         | 16.8% do valor       | 5.4% do valor
```

### Gráficos:
- **Gráfico de Pizza:** 3 fatias (verde=A, amarelo=B, vermelho=C)
- **Gráfico de Barras:** 3 barras mostrando quantidade por classe

### Tabela:
- 30 linhas com todos os produtos
- Colunas: Código, Descrição, Qtd, Valor Unit., Valor Total, % Valor, % Acum., Classe

---

## 🆘 Se Nada Funcionar

1. **Limpar cache do navegador:**
   ```
   Ctrl + Shift + Delete
   Limpar cache e dados de sites
   ```

2. **Rebuild completo:**
   ```bash
   cd curva-abc-app
   Remove-Item dist -Recurse -Force
   npm run build
   npm run preview
   ```

3. **Verificar se não há erro de CORS:**
   - Console não deve mostrar erros de CORS
   - Preview deve estar rodando localmente

4. **Usar navegador diferente:**
   - Testar em Chrome
   - Testar em Edge
   - Testar em Firefox

5. **Enviar print do console:**
   - Fazer upload da planilha
   - Copiar TODOS os logs do console
   - Enviar para análise

---

## 📝 Checklist de Debug

- [ ] Aplicação abre no navegador (http://localhost:4177)
- [ ] Console do navegador está aberto (F12)
- [ ] Upload funciona (botão clicável)
- [ ] Arquivo selecionado aparece no log (📁)
- [ ] Chaves da planilha aparecem (🔑)
- [ ] Produtos aparecem (📦)
- [ ] Resultado recebido (✅)
- [ ] Estado atualizado (🔔)
- [ ] Cards aparecem no topo
- [ ] Gráficos renderizam
- [ ] Tabela mostra dados

Se TODOS os itens estiverem marcados, o aplicativo está funcionando!

---

## 🎯 Teste Rápido

Execute no console do navegador (F12 > Console):

```javascript
// Verificar se React está funcionando
console.log('React version:', React.version);

// Verificar se xlsx está carregado
console.log('XLSX loaded:', typeof XLSX !== 'undefined');

// Verificar estado
// (só funciona se você tiver React DevTools instalado)
```

---

**Atualizado em:** 2026-02-16  
**Versão com logs:** http://localhost:4177  
**Aplicativo:** Curva ABC v1.0.0
