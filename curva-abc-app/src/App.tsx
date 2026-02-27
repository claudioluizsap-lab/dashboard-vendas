import { useState, useEffect } from 'react';
import { calcularCurvaABC, processExcelFile, CurvaABCThresholds } from './utils';
import { CurvaABCResult } from './types';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { exportToPDF, exportChartsAndTableToPDF } from './pdfExport';
function App() {
  const [resultado, setResultado] = useState<CurvaABCResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [atualizando, setAtualizando] = useState(false);
  const [ultimaAtualizacao, setUltimaAtualizacao] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [filtroCategoria, setFiltroCategoria] = useState<'Todas' | 'A' | 'B' | 'C'>('Todas');
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode');
    return saved ? JSON.parse(saved) : false;
  });
  const [thresholds, setThresholds] = useState<CurvaABCThresholds>(() => {
    const saved = localStorage.getItem('curvaABCThresholds');
    return saved ? JSON.parse(saved) : { limiteA: 80, limiteB: 95 };
  });
  const [showConfig, setShowConfig] = useState(false);
  const [tempThresholds, setTempThresholds] = useState(thresholds);

  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const API_BASE = 'http://localhost:8080';

  const carregarDados = async (mostrarSpinner = false) => {
    if (mostrarSpinner) setAtualizando(true);
    setError(null);
    try {
      if (mostrarSpinner) {
        const apiResp = await fetch(`${API_BASE}/api/atualizar`);
        const apiJson = await apiResp.json();
        if (!apiResp.ok) {
          setError(apiJson.erro || 'Erro ao atualizar dados da planilha.');
          return;
        }
      }
      const resp = await fetch(`${API_BASE}/dados.json?t=${Date.now()}`);
      if (!resp.ok) throw new Error('Servidor não encontrado em localhost:8080');
      const dados = await resp.json();
      if (!dados || dados.length === 0) throw new Error('Nenhum dado retornado pelo servidor.');
      const produtos = dados.map((p: { codigo: string; descricao: string; quantidade: number; valorUnitario: number }) => ({
        ...p,
        valorTotal: p.quantidade * p.valorUnitario,
      }));
      const result = calcularCurvaABC(produtos, thresholds);
      setResultado(result);
      setError(null);
      const agora = new Date().toLocaleString('pt-BR');
      setUltimaAtualizacao(agora);
    } catch (err: any) {
      setError(`Erro ao atualizar: ${err.message || 'Verifique se o servidor está rodando.'}`);
    } finally {
      if (mostrarSpinner) setAtualizando(false);
    }
  };

  useEffect(() => {
    carregarDados();
  }, []);

  useEffect(() => {
    localStorage.setItem('curvaABCThresholds', JSON.stringify(thresholds));
  }, [thresholds]);

  const handleSaveThresholds = () => {
    if (tempThresholds.limiteA >= tempThresholds.limiteB) {
      alert('Erro: O limite da Classe A deve ser menor que o limite da Classe B!');
      return;
    }
    if (tempThresholds.limiteA < 0 || tempThresholds.limiteB > 100) {
      alert('Erro: Os limites devem estar entre 0 e 100!');
      return;
    }
    setThresholds(tempThresholds);
    setShowConfig(false);
    if (resultado) {
      window.location.reload();
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await processExcelFile(file, thresholds);
      
      if (!result || !result.produtos || result.produtos.length === 0) {
        setError('Nenhum produto encontrado na planilha.');
        return;
      }
      
      setResultado(result);
      
    } catch (err) {
      console.error('Erro ao processar arquivo:', err);
      setError('Erro ao processar o arquivo. Verifique se o formato está correto.');
    } finally {
      setLoading(false);
    }
  };

  const handleExportPDF = () => {
    if (resultado) {
      exportToPDF(resultado);
    }
  };

  const handleExportFullPDF = () => {
    if (resultado) {
      exportChartsAndTableToPDF(resultado);
    }
  };

  const COLORS = {
    A: '#22c55e',
    B: '#eab308',
    C: '#ef4444',
  };

  const produtosFiltrados = resultado?.produtos.filter(p => 
    filtroCategoria === 'Todas' || p.classificacao === filtroCategoria
  ) || [];

  const chartData = resultado ? [
    { name: 'Classe A', value: resultado.categorias.A.quantidade, percentual: resultado.categorias.A.percentual },
    { name: 'Classe B', value: resultado.categorias.B.quantidade, percentual: resultado.categorias.B.percentual },
    { name: 'Classe C', value: resultado.categorias.C.quantidade, percentual: resultado.categorias.C.percentual },
  ] : [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 transition-colors duration-300">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8 relative">
          <div className="absolute right-0 top-0 flex gap-2 items-center">
            {ultimaAtualizacao && (
              <span className="text-xs text-gray-500 dark:text-gray-400 hidden md:block">
                Atualizado: {ultimaAtualizacao}
              </span>
            )}
            <button
              onClick={() => carregarDados(true)}
              disabled={atualizando}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-green-500 hover:bg-green-600 disabled:bg-green-300 text-white shadow-lg hover:shadow-xl transition-all duration-300 font-medium text-sm"
              title="Recarregar dados da planilha"
            >
              <svg className={`w-4 h-4 ${atualizando ? 'animate-spin' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              {atualizando ? 'Atualizando...' : 'Atualizar Dados'}
            </button>
            <button
              onClick={() => setShowConfig(!showConfig)}
              className="p-3 rounded-lg bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300"
              aria-label="Configurações"
              title="Configurar limites da Curva ABC"
            >
              <svg className="w-6 h-6 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-3 rounded-lg bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300"
              aria-label="Toggle Dark Mode"
            >
              {darkMode ? (
                <svg className="w-6 h-6 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              ) : (
                <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
              )}
            </button>
          </div>
          <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-2">Análise Curva ABC</h1>
          <p className="text-gray-600 dark:text-gray-300">Gestão de Estoque e Inventário</p>
        </div>

        {showConfig && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8 transition-colors duration-300">
            <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">⚙️ Configuração dos Limites</h2>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              Defina os percentuais acumulados que delimitam cada classe. Valores padrão: A=80%, B=95%
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Limite Classe A (%)
                </label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={tempThresholds.limiteA}
                  onChange={(e) => setTempThresholds({ ...tempThresholds, limiteA: parseFloat(e.target.value) })}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500"
                />
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  Produtos até este percentual acumulado serão Classe A
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Limite Classe B (%)
                </label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={tempThresholds.limiteB}
                  onChange={(e) => setTempThresholds({ ...tempThresholds, limiteB: parseFloat(e.target.value) })}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500"
                />
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  Produtos acima de A e até este percentual serão Classe B. Acima deste será Classe C
                </p>
              </div>
            </div>
            <div className="flex gap-3">
              <button
                onClick={handleSaveThresholds}
                className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-medium"
              >
                Salvar Configuração
              </button>
              <button
                onClick={() => {
                  setTempThresholds(thresholds);
                  setShowConfig(false);
                }}
                className="px-6 py-2 bg-gray-300 dark:bg-gray-600 text-gray-800 dark:text-white rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500 transition font-medium"
              >
                Cancelar
              </button>
              <button
                onClick={() => {
                  setTempThresholds({ limiteA: 80, limiteB: 95 });
                }}
                className="px-6 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition font-medium"
              >
                Restaurar Padrão
              </button>
            </div>
          </div>
        )}

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8 transition-colors duration-300">
          <div className="flex flex-col items-center">
            <label className="w-full max-w-md">
              <div className="flex items-center justify-center w-full h-32 px-4 transition bg-white dark:bg-gray-700 border-2 border-gray-300 dark:border-gray-600 border-dashed rounded-lg appearance-none cursor-pointer hover:border-indigo-400 dark:hover:border-indigo-500 focus:outline-none">
                <div className="flex flex-col items-center space-y-2">
                  <svg className="w-12 h-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  <span className="font-medium text-gray-600 dark:text-gray-300">
                    {loading ? 'Processando...' : 'Clique para enviar planilha Excel'}
                  </span>
                  <span className="text-xs text-gray-500 dark:text-gray-400">XLS ou XLSX</span>
                </div>
              </div>
              <input
                type="file"
                className="hidden"
                accept=".xlsx,.xls"
                onChange={handleFileUpload}
                disabled={loading}
              />
            </label>
            {error && (
              <div className="mt-4 p-4 bg-red-100 dark:bg-red-900/30 border border-red-400 dark:border-red-800 text-red-700 dark:text-red-300 rounded">
                {error}
              </div>
            )}
          </div>
        </div>

        {resultado && (
          <>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8 transition-colors duration-300">
              <div className="flex flex-wrap gap-3 justify-center">
                <button
                  onClick={handleExportPDF}
                  className="flex items-center gap-2 px-6 py-3 bg-indigo-600 dark:bg-indigo-500 text-white rounded-lg hover:bg-indigo-700 dark:hover:bg-indigo-600 transition font-medium shadow-md"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Exportar Relatório PDF
                </button>
                <button
                  onClick={handleExportFullPDF}
                  className="flex items-center gap-2 px-6 py-3 bg-green-600 dark:bg-green-500 text-white rounded-lg hover:bg-green-700 dark:hover:bg-green-600 transition font-medium shadow-md"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Exportar PDF com Gráficos
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 transition-colors duration-300">
                <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Total de Produtos</div>
                <div className="text-3xl font-bold text-gray-800 dark:text-white">{resultado.totais.quantidadeTotal}</div>
              </div>
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 transition-colors duration-300">
                <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Valor Total</div>
                <div className="text-3xl font-bold text-gray-800 dark:text-white">
                  {resultado.totais.valorTotal.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
                </div>
              </div>
              <div className="bg-green-500 rounded-lg shadow p-6 text-white">
                <div className="text-sm mb-1">Classe A (até {thresholds.limiteA}%)</div>
                <div className="text-2xl font-bold">{resultado.categorias.A.quantidade} produtos</div>
                <div className="text-xs mt-1">{resultado.categorias.A.percentual.toFixed(1)}% do valor</div>
              </div>
              <div className="bg-yellow-500 rounded-lg shadow p-6 text-white">
                <div className="text-sm mb-1">Classe B ({thresholds.limiteA}-{thresholds.limiteB}%)</div>
                <div className="text-2xl font-bold">{resultado.categorias.B.quantidade} produtos</div>
                <div className="text-xs mt-1">{resultado.categorias.B.percentual.toFixed(1)}% do valor</div>
              </div>
              <div className="bg-red-500 rounded-lg shadow p-6 text-white md:col-span-2 lg:col-span-1">
                <div className="text-sm mb-1">Classe C (acima de {thresholds.limiteB}%)</div>
                <div className="text-2xl font-bold">{resultado.categorias.C.quantidade} produtos</div>
                <div className="text-xs mt-1">{resultado.categorias.C.percentual.toFixed(1)}% do valor</div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8 charts-container">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 transition-colors duration-300">
                <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">Distribuição por Categoria</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={chartData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percentual }) => `${name}: ${percentual.toFixed(1)}%`}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {chartData.map((_entry, index) => (
                        <Cell key={`cell-${index}`} fill={Object.values(COLORS)[index]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 transition-colors duration-300">
                <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">Quantidade por Classe</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="value" fill="#3b82f6" name="Quantidade de Produtos" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 transition-colors duration-300">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-gray-800 dark:text-white">Produtos Analisados</h2>
                <div className="flex gap-2">
                  <button
                    onClick={() => setFiltroCategoria('Todas')}
                    className={`px-4 py-2 rounded ${filtroCategoria === 'Todas' ? 'bg-indigo-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'}`}
                  >
                    Todas
                  </button>
                  <button
                    onClick={() => setFiltroCategoria('A')}
                    className={`px-4 py-2 rounded ${filtroCategoria === 'A' ? 'bg-green-500 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'}`}
                  >
                    A
                  </button>
                  <button
                    onClick={() => setFiltroCategoria('B')}
                    className={`px-4 py-2 rounded ${filtroCategoria === 'B' ? 'bg-yellow-500 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'}`}
                  >
                    B
                  </button>
                  <button
                    onClick={() => setFiltroCategoria('C')}
                    className={`px-4 py-2 rounded ${filtroCategoria === 'C' ? 'bg-red-500 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'}`}
                  >
                    C
                  </button>
                </div>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Código</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Descrição</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Qtd</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Valor Unit.</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Valor Total</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">% Valor</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">% Acum.</th>
                      <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Classe</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                    {produtosFiltrados.map((produto, index) => (
                      <tr key={index} className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                        <td className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100">{produto.codigo || '-'}</td>
                        <td className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100">{produto.descricao || '-'}</td>
                        <td className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100 text-right">{produto.quantidade || 0}</td>
                        <td className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100 text-right">
                          {produto.valorUnitario ? 
                            `R$ ${produto.valorUnitario.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}` : 
                            'R$ 0,00'
                          }
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100 text-right font-medium">
                          {produto.valorTotal ? 
                            `R$ ${produto.valorTotal.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}` : 
                            'R$ 0,00'
                          }
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100 text-right font-semibold">
                          {Number.isFinite(produto.percentualValor) ? produto.percentualValor.toFixed(2) + '%' : '0.00%'}
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-900 dark:text-gray-100 text-right font-semibold">
                          {Number.isFinite(produto.percentualAcumulado) ? produto.percentualAcumulado.toFixed(2) + '%' : '0.00%'}
                        </td>
                        <td className="px-4 py-3 text-center">
                          <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
                            produto.classificacao === 'A' ? 'bg-green-100 text-green-800' :
                            produto.classificacao === 'B' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {produto.classificacao}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
