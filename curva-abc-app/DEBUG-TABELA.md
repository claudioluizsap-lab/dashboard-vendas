# 🔍 GUIA VISUAL - Verificar Colunas na Tabela

## 🎯 Problema Identificado

As colunas **Valor Unit.**, **Valor Total**, **% Valor** e **% Acum.** não estão aparecendo na tabela.

---

## ✅ TESTE ATUALIZADO

Adicionei logs específicos para verificar se os campos `percentualValor` e `percentualAcumulado` existem.

### 📍 Aplicação Rodando
**URL:** http://localhost:4174

---

## 🧪 Como Testar

### Passo 1: Abrir Console
1. Pressione **F12**
2. Clique na aba **Console**
3. Limpe o console (ícone 🚫 ou Ctrl+L)

### Passo 2: Fazer Upload
1. Clique em "Escolher arquivo"
2. Selecione `planilha-teste-estoque.xlsx`
3. Aguarde o processamento

### Passo 3: Verificar Logs

Procure por estas linhas **ESPECÍFICAS** no console:

```javascript
🔍 DEBUG TABELA - Primeiro produto filtrado:
   codigo: P001
   descricao: Notebook Dell Inspiron 15
   quantidade: 25
   valorUnitario: 3500
   valorTotal: 87500
   percentualValor: 8.474576271186441 (tipo: number)
   percentualAcumulado: 8.474576271186441 (tipo: number)
   classificacao: A
   Number.isFinite(percentualValor)? true
   Number.isFinite(percentualAcumulado)? true
```

---

## 📊 O que Verificar

### ✅ Se os valores aparecem no log:

```
percentualValor: 8.47 (tipo: number)  ✅ OK
percentualAcumulado: 8.47 (tipo: number)  ✅ OK
Number.isFinite(percentualValor)? true  ✅ OK
```

**Significa:** Os cálculos estão corretos! O problema é na renderização da tabela.

---

### ❌ Se aparecer undefined:

```
percentualValor: undefined (tipo: undefined)  ❌ PROBLEMA
percentualAcumulado: undefined (tipo: undefined)  ❌ PROBLEMA
Number.isFinite(percentualValor)? false  ❌ PROBLEMA
```

**Significa:** Os campos não estão sendo calculados ou não estão no objeto.

---

### ❌ Se aparecer NaN:

```
percentualValor: NaN (tipo: number)  ⚠️ PROBLEMA
percentualAcumulado: NaN (tipo: number)  ⚠️ PROBLEMA
Number.isFinite(percentualValor)? false  ❌ PROBLEMA
```

**Significa:** O cálculo está dividindo por zero ou usando valores inválidos.

---

## 🔎 O que Deve Aparecer na Tela

### Cabeçalho da Tabela (deve ter todas estas colunas):

```
┌────────┬─────────────┬─────┬─────────────┬─────────────┬────────┬────────┬────────┐
│ Código │ Descrição   │ Qtd │ Valor Unit. │ Valor Total │ % Valor│ % Acum.│ Classe │
└────────┴─────────────┴─────┴─────────────┴─────────────┴────────┴────────┴────────┘
```

### Primeira Linha de Dados (exemplo):

```
┌────────┬─────────────────────┬─────┬─────────────┬─────────────┬────────┬────────┬────────┐
│ P001   │ Notebook Dell...    │  25 │ R$ 3.500,00 │ R$ 87.500,00│  8,47% │  8,47% │   A    │
└────────┴─────────────────────┴─────┴─────────────┴─────────────┴────────┴────────┴────────┘
```

---

## 🐛 Possíveis Problemas e Soluções

### Problema 1: Colunas vazias (sem dados)

**Sintoma:** Cabeçalho aparece mas células estão vazias

**Causa:** Valores são `undefined` ou `null`

**Verificar no log:**
```javascript
percentualValor: undefined  ❌
```

**Solução:** O cálculo não está sendo feito. Verificar `calcularCurvaABC()`.

---

### Problema 2: Mostra "0.00%" em tudo

**Sintoma:** Todas as linhas mostram 0.00%

**Causa:** Cálculo retorna 0 ou divisão por zero

**Verificar no log:**
```javascript
valorTotal: 0  ❌ ou
percentualValor: 0  ❌
```

**Solução:** Verificar se quantidade e valorUnitario estão sendo lidos.

---

### Problema 3: Colunas não aparecem (nem cabeçalho)

**Sintoma:** Faltam colunas inteiras na tabela

**Causa:** Código do `<th>` ou `<td>` comentado/removido

**Solução:** Verificar `App.tsx` linhas 360-430

---

## 📋 Checklist de Verificação

Após fazer upload, verifique:

- [ ] Console aberto (F12)
- [ ] Log "🔍 DEBUG TABELA" aparece
- [ ] `percentualValor` tem valor numérico (não undefined)
- [ ] `percentualAcumulado` tem valor numérico (não undefined)
- [ ] `Number.isFinite()` retorna `true`
- [ ] Tabela renderiza com todas as colunas
- [ ] Valores aparecem nas células
- [ ] Primeira linha tem: 8.47%, 8.47%, Classe A

---

## 🎯 Próximo Passo

**TIRE UM PRINT DO CONSOLE** mostrando os logs do "🔍 DEBUG TABELA".

Especificamente, eu preciso ver:
1. O valor de `percentualValor`
2. O valor de `percentualAcumulado`
3. O resultado de `Number.isFinite()`

Isso vai me dizer EXATAMENTE onde está o problema!

---

## 📸 Como Tirar o Print

1. Abra http://localhost:4174
2. Pressione F12
3. Faça upload da planilha
4. **Espere os logs aparecerem**
5. Procure por "🔍 DEBUG TABELA"
6. Tire print dessa parte do console
7. Também tire print da tabela na tela

---

**Atualizado:** 2026-02-17  
**Versão:** Com debug específico de tabela  
**URL:** http://localhost:4174
