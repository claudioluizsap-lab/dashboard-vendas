# 🔍 INSTRUÇÕES PARA VERIFICAR O CONSOLE

## ❗ PROBLEMA ATUAL
Os valores de **Valor Unit.** e **Valor Total** não aparecem na tabela (mostram "R$ 0,00").

## ✅ DIAGNÓSTICO NECESSÁRIO

### PASSO 1: ABRIR O CONSOLE DO NAVEGADOR

1. Abra a aplicação: http://localhost:4173
2. **Pressione F12** (ou clique com botão direito → "Inspecionar")
3. **Clique na aba "Console"** no topo das ferramentas de desenvolvedor

### PASSO 2: FAZER UPLOAD DA PLANILHA

1. Clique no botão de **"Upload Excel"**
2. Selecione a planilha de teste

### PASSO 3: VERIFICAR AS MENSAGENS NO CONSOLE

Você verá várias mensagens de log. **Procure especificamente por estas:**

#### 🔍 Log 1: "DEBUG TABELA - Primeiro produto filtrado"
```
🔍 DEBUG TABELA - Primeiro produto filtrado:
   codigo: [código do produto]
   descricao: [descrição]
   quantidade: [número]
   valorUnitario: [aqui deve aparecer um número ou undefined]
   valorTotal: [aqui deve aparecer um número ou undefined]
```

#### 🚨 Log 2: "RENDER TABELA - Produto sendo renderizado"
```
🚨 RENDER TABELA - Produto sendo renderizado:
   produto completo: {objeto completo}
   produto.quantidade: [número] tipo: number
   produto.valorUnitario: [número ou undefined] tipo: [tipo]
   produto.valorTotal: [número ou undefined] tipo: [tipo]
   produto.valorUnitario existe? true/false
   produto.valorTotal existe? true/false
```

## 📋 O QUE COPIAR E ENVIAR

**Copie EXATAMENTE estas duas seções do console e me envie:**

1. A seção que começa com "🔍 DEBUG TABELA"
2. A seção que começa com "🚨 RENDER TABELA"

## 🎯 O QUE ESTAMOS PROCURANDO

- **Se `valorUnitario: undefined`** → problema está no processamento do Excel
- **Se `valorUnitario: 3500` (ou qualquer número)** → problema está na renderização React

## 📸 ALTERNATIVA

Se preferir, tire uma **captura de tela do console** e descreva o que vê nas linhas:
- `produto.valorUnitario:`
- `produto.valorTotal:`
