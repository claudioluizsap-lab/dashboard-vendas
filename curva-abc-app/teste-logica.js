// TESTE MANUAL DA LÓGICA DE CLASSIFICAÇÃO

console.log('🧪 TESTE DA LÓGICA ABC\n');

// Simular dados
const produtos = [
  { codigo: 'P001', descricao: 'Produto A', valorTotal: 50000 }, // 50%
  { codigo: 'P002', descricao: 'Produto B', valorTotal: 30000 }, // 30%
  { codigo: 'P003', descricao: 'Produto C', valorTotal: 15000 }, // 15%
  { codigo: 'P004', descricao: 'Produto D', valorTotal: 5000 },  // 5%
];

const valorTotal = produtos.reduce((sum, p) => sum + p.valorTotal, 0);
console.log(`💰 Valor Total: R$ ${valorTotal.toFixed(2)}\n`);

let acumulado = 0;

produtos.forEach((produto, index) => {
  const percentualValor = (produto.valorTotal / valorTotal) * 100;
  const acumuladoAnterior = acumulado;
  acumulado += percentualValor;

  let classificacao;
  
  // LÓGICA ATUAL
  if (acumuladoAnterior < 80) {
    classificacao = 'A';
  } else if (acumuladoAnterior < 95) {
    classificacao = 'B';
  } else {
    classificacao = 'C';
  }

  console.log(`${index + 1}º: ${produto.descricao}`);
  console.log(`   Valor: R$ ${produto.valorTotal.toFixed(2)}`);
  console.log(`   % Valor: ${percentualValor.toFixed(2)}%`);
  console.log(`   Acum Anterior: ${acumuladoAnterior.toFixed(2)}%`);
  console.log(`   Acum Atual: ${acumulado.toFixed(2)}%`);
  console.log(`   ➡️  CLASSE: ${classificacao}\n`);
});

console.log('\n📊 RESULTADO ESPERADO:');
console.log('Produto A (50%) → Acum 0% → Classe A ✅');
console.log('Produto B (30%) → Acum 50% → Classe A ✅');
console.log('Produto C (15%) → Acum 80% → Classe B ✅');
console.log('Produto D (5%) → Acum 95% → Classe C ✅');
