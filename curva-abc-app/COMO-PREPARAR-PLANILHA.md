# 📊 GUIA: Como Preparar Planilha para Análise Curva ABC

## ✅ ESTRUTURA OBRIGATÓRIA

A planilha Excel deve ter **4 colunas** com os seguintes nomes (exatamente):

| Código | Descrição | Quantidade | Valor Unitário |
|--------|-----------|------------|----------------|
| P001   | Produto A | 10         | 100.00         |
| P002   | Produto B | 25         | 50.00          |

### 📋 Descrição das Colunas:

1. **Código** (texto)
   - Identificador único do produto
   - Pode ser: P001, SKU123, COD-A, etc.
   - Aceita letras e números

2. **Descrição** (texto)
   - Nome/descrição do produto
   - Pode ter qualquer tamanho
   - Exemplo: "Notebook Dell Inspiron 15"

3. **Quantidade** (número)
   - Quantidade em estoque
   - Deve ser número inteiro ou decimal
   - Exemplo: 10, 25.5, 100

4. **Valor Unitário** (número)
   - Preço unitário do produto
   - Pode usar ponto ou vírgula decimal
   - Exemplo: 100.00, 1500.50

---

## ⚠️ NOMES ACEITOS PARA AS COLUNAS

O aplicativo aceita variações dos nomes das colunas:

### Coluna 1 - Código:
- ✅ Código
- ✅ Codigo
- ✅ código
- ✅ CÓDIGO

### Coluna 2 - Descrição:
- ✅ Descrição
- ✅ Descricao
- ✅ descrição
- ✅ DESCRIÇÃO
- ✅ Produto
- ✅ produto

### Coluna 3 - Quantidade:
- ✅ Quantidade
- ✅ quantidade
- ✅ QUANTIDADE
- ✅ Qtd
- ✅ qtd

### Coluna 4 - Valor Unitário:
- ✅ Valor Unitário
- ✅ Valor Unitario
- ✅ valor_unitario
- ✅ ValorUnitario
- ✅ Preço
- ✅ Preco
- ✅ preco

---

## 📝 EXEMPLOS PRÁTICOS

### ✅ Exemplo 1 - Informática (CORRETO)

| Código | Descrição              | Quantidade | Valor Unitário |
|--------|------------------------|------------|----------------|
| P001   | Notebook Dell          | 15         | 3500.00        |
| P002   | Mouse Logitech         | 150        | 45.00          |
| P003   | Teclado Mecânico       | 80         | 250.00         |
| P004   | Monitor 24"            | 25         | 890.00         |

**Resultado Esperado:**
- Valor Total P001: R$ 52.500,00 (15 × 3.500)
- Valor Total P002: R$ 6.750,00 (150 × 45)
- Classificação: P001 provavelmente será Classe A

---

### ✅ Exemplo 2 - Roupas (CORRETO)

| Codigo | Produto        | Qtd | Preco |
|--------|----------------|-----|-------|
| R001   | Camiseta P     | 100 | 35.00 |
| R002   | Calça Jeans M  | 50  | 120.00|
| R003   | Tênis Esportivo| 30  | 250.00|

**Resultado Esperado:**
- Valor Total R001: R$ 3.500,00
- Valor Total R002: R$ 6.000,00
- Valor Total R003: R$ 7.500,00
- Classificação: R003 será Classe A (maior valor)

---

### ❌ Exemplo 3 - ERRADO (Faltam Colunas)

| Produto        | Quantidade |
|----------------|------------|
| Notebook       | 10         |

**Problema:** Falta "Código" e "Valor Unitário"

---

### ❌ Exemplo 4 - ERRADO (Nomes Diferentes)

| ID  | Nome do Produto | Estoque | Preço Unit |
|-----|-----------------|---------|------------|
| 001 | Notebook        | 10      | 3500       |

**Problema:** Nomes das colunas não são reconhecidos
**Solução:** Renomeie para: Código, Descrição, Quantidade, Valor Unitário

---

## 🎯 DICAS IMPORTANTES

### 1️⃣ Primeira Linha DEVE ser o Cabeçalho
```
Linha 1: Código | Descrição | Quantidade | Valor Unitário  ← CABEÇALHO
Linha 2: P001   | Produto A | 10         | 100.00          ← DADOS
Linha 3: P002   | Produto B | 25         | 50.00           ← DADOS
```

### 2️⃣ Não deixe linhas vazias no meio
❌ ERRADO:
```
P001 | Produto A | 10  | 100
     |           |     |        ← Linha vazia
P002 | Produto B | 25  | 50
```

✅ CORRETO:
```
P001 | Produto A | 10  | 100
P002 | Produto B | 25  | 50
P003 | Produto C | 15  | 75
```

### 3️⃣ Valores Numéricos
- ✅ Use ponto OU vírgula: 1500.50 ou 1500,50
- ✅ Pode ter decimais: 125.75
- ❌ Não use símbolos: R$ 100 (use apenas 100)
- ❌ Não use separador de milhares: 1.500 (use 1500)

### 4️⃣ Códigos Únicos
- Cada produto deve ter um código diferente
- Evite repetir códigos

---

## 📊 COMO O CÁLCULO FUNCIONA

### Fórmula:
```
Valor Total do Produto = Quantidade × Valor Unitário
```

### Classificação ABC:
1. **Produtos ordenados** por Valor Total (maior → menor)
2. **Calcula percentual** de cada produto sobre o total
3. **Acumula percentuais** em ordem decrescente
4. **Classifica:**
   - **Classe A**: Produtos que juntos somam até 80% do valor total
   - **Classe B**: Produtos que somam de 80% a 95%
   - **Classe C**: Produtos que somam de 95% a 100%

### Exemplo Visual:
```
Produto       Valor      % Valor   % Acum.  Classe
Notebook      52.500     44,2%     44,2%    A
Monitor       22.250     18,7%     62,9%    A
Teclado       20.000     16,8%     79,7%    A  ← Até 80%
Impressora    14.400     12,1%     91,8%    B
Cadeira       14.400     12,1%    103,9%    B  ← Até 95%
Mouse          6.750      5,7%    109,6%    C  ← Resto
...
```

---

## 🎨 FORMATAÇÃO OPCIONAL

Você pode deixar a planilha mais bonita (não é obrigatório):

- ✅ Negrito no cabeçalho
- ✅ Cores nas células
- ✅ Bordas
- ✅ Formatação de moeda (R$ 100,00)

**O aplicativo vai funcionar de qualquer forma!**

---

## 📥 ARQUIVOS DE EXEMPLO CRIADOS

Verifique na pasta `curva-abc-app`:

1. **EXEMPLO-PLANILHA-MODELO.xlsx**
   - 20 produtos de informática
   - Modelo completo e formatado

2. **EXEMPLO-ELETRONICOS.xlsx**
   - 10 produtos eletrônicos
   - Exemplo alternativo

3. **exemplo-estoque.xlsx**
   - Mesmo conteúdo do modelo
   - Pronto para usar

---

## ✅ CHECKLIST ANTES DE USAR

Antes de fazer upload, verifique:

- [ ] Arquivo é .xlsx ou .xls (não pode ser .csv direto)
- [ ] Primeira linha tem os nomes das colunas
- [ ] As 4 colunas existem (Código, Descrição, Quantidade, Valor)
- [ ] Não há linhas vazias no meio dos dados
- [ ] Valores numéricos estão sem símbolos (R$, %)
- [ ] Cada produto tem um código único

---

## 🚀 COMO USAR NO APLICATIVO

1. Prepare sua planilha seguindo este guia
2. Salve como .xlsx
3. Abra o aplicativo: http://localhost:5173
4. Arraste o arquivo para a área de upload
5. Veja a análise ABC automática!

---

## ❓ PROBLEMAS COMUNS

### "Erro ao processar o arquivo"
- Verifique se é .xlsx (não .csv ou .txt)
- Confirme que as colunas têm os nomes corretos
- Veja se há dados válidos (não vazio)

### "Nenhum produto encontrado"
- Verifique se a primeira linha é o cabeçalho
- Confirme que há dados abaixo do cabeçalho

### "Valores zerados"
- Confirme que Quantidade e Valor são números
- Não use vírgulas como separador de milhares

---

## 📞 SUPORTE

Se tiver dúvidas, abra o Console (F12) e veja as mensagens de erro detalhadas!
