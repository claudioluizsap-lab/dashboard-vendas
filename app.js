let workbookData = null;
let inventoryData = [];
let filteredData = [];
let currentFilter = 'all';
let currentEditIndex = null;
let currentQuickIndex = null;

const fileInput       = document.getElementById('fileInput');
const fileName        = document.getElementById('fileName');
const uploadScreen    = document.getElementById('uploadScreen');
const appScreen       = document.getElementById('appScreen');
const bottomNav       = document.getElementById('bottomNav');
const inventoryBody   = document.getElementById('inventoryBody');
const exportBtn       = document.getElementById('exportBtn');
const resetBtn        = document.getElementById('resetBtn');
const themeToggle     = document.getElementById('themeToggle');
const reportBtn       = document.getElementById('reportBtn');
const reportModal     = document.getElementById('reportModal');
const closeReport     = document.getElementById('closeReport');
const closeReportBtn  = document.getElementById('closeReportBtn');
const printReportBtn  = document.getElementById('printReportBtn');
const exportReportBtn = document.getElementById('exportReportBtn');
const searchCodigoInput = document.getElementById('searchCodigo');
const searchProdutoInput = document.getElementById('searchProduto');
const searchFormBtn   = document.getElementById('searchFormBtn');
const clearFormBtn    = document.getElementById('clearFormBtn');
const searchFormInfo  = document.getElementById('searchFormInfo');

fileInput.addEventListener('change', handleFileUpload);
exportBtn.addEventListener('click', exportToExcel);
resetBtn.addEventListener('click', resetCounts);
themeToggle.addEventListener('click', toggleTheme);
reportBtn.addEventListener('click', generateReport);
closeReport.addEventListener('click', closeReportModal);
closeReportBtn.addEventListener('click', closeReportModal);
printReportBtn.addEventListener('click', printReport);
exportReportBtn.addEventListener('click', exportReportPDF);
searchFormBtn.addEventListener('click', handleFormSearch);
clearFormBtn.addEventListener('click', clearFormSearch);
searchCodigoInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') handleFormSearch(); });
searchProdutoInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') handleFormSearch(); });

document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => switchPanel(btn.dataset.panel));
});

document.querySelectorAll('.mbtn-filter').forEach(btn => {
    btn.addEventListener('click', (e) => {
        document.querySelectorAll('.mbtn-filter').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        currentFilter = e.target.dataset.filter;
        applyFilter();
    });
});

document.getElementById('inlineSaveBtn').addEventListener('click', saveInlineCount);
document.getElementById('inlineCountClose').addEventListener('click', closeInlineCard);
document.getElementById('qtyMinus').addEventListener('click', () => changeQty(-1));
document.getElementById('qtyPlus').addEventListener('click', () => changeQty(1));
document.getElementById('inlinePrevBtn').addEventListener('click', () => navigateItem(-1));
document.getElementById('inlineNextBtn').addEventListener('click', () => navigateItem(1));

window.addEventListener('click', (e) => {
    if (e.target === reportModal) closeReportModal();
});

function switchPanel(panel) {
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    document.querySelector(`.nav-btn[data-panel="${panel}"]`).classList.add('active');
    document.getElementById(`panel-${panel}`).classList.add('active');
}

function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

function loadTheme() {
    if (localStorage.getItem('darkMode') === 'true') document.body.classList.add('dark-mode');
}
loadTheme();

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    fileName.textContent = `✅ ${file.name}`;
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, { type: 'array' });
            workbookData = workbook;
            const ws = workbook.Sheets[workbook.SheetNames[0]];
            processInventoryData(XLSX.utils.sheet_to_json(ws));
            uploadScreen.classList.remove('active');
            appScreen.classList.add('active');
            bottomNav.style.display = 'flex';
            renderInventory();
            renderQuickList(inventoryData);
            updateStats();
        } catch (error) {
            alert('Erro ao processar o arquivo: ' + error.message);
        }
    };
    reader.readAsArrayBuffer(file);
}

function processInventoryData(data) {
    inventoryData = data.map((row, index) => {
        const keys = Object.keys(row);
        return {
            id: index,
            codigo: row[keys[0]] || `ITEM-${index + 1}`,
            produto: row[keys[1]] || 'Produto sem nome',
            qtdSistema: parseFloat(row[keys[2]]) || 0,
            qtdContada: null,
            diferenca: null,
            status: 'pending'
        };
    });
    filteredData = [...inventoryData];
}

function normalizeText(text) {
    return text.toString().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

function handleFormSearch() {
    const codigoTerm = normalizeText(searchCodigoInput.value.trim());
    const produtoTerm = normalizeText(searchProdutoInput.value.trim());

    if (!codigoTerm && !produtoTerm) {
        applyFilter();
        renderQuickList(filteredData);
        searchFormInfo.style.display = 'none';
        return;
    }

    filteredData = inventoryData.filter(item => {
        const matchCodigo = codigoTerm ? normalizeText(item.codigo).includes(codigoTerm) : true;
        const matchProduto = produtoTerm ? produtoTerm.split(/\s+/).every(t => normalizeText(item.produto).includes(t)) : true;
        return matchCodigo && matchProduto && matchesFilter(item);
    });

    renderInventory();
    renderQuickList(filteredData);

    const found = filteredData.length;
    searchFormInfo.textContent = found === 0
        ? '⚠️ Nenhum item encontrado.'
        : `✅ ${found} de ${inventoryData.length} item${found !== 1 ? 's' : ''} encontrado${found !== 1 ? 's' : ''}.`;
    searchFormInfo.style.display = 'block';

    if (found === 1) openInlineCard(filteredData[0].id);
}

function clearFormSearch() {
    searchCodigoInput.value = '';
    searchProdutoInput.value = '';
    searchFormInfo.style.display = 'none';
    closeInlineCard();
    applyFilter();
    renderQuickList(inventoryData);
}

function renderQuickList(data) {
    const body = document.getElementById('quickListBody');
    const hint = document.querySelector('.quick-list-hint');
    body.innerHTML = '';

    if (data.length === 0) {
        body.innerHTML = '<div class="quick-empty">Nenhum item encontrado</div>';
        return;
    }

    if (hint) hint.textContent = `${data.length} item${data.length !== 1 ? 's' : ''} — toque para contar`;

    data.forEach(item => {
        const card = document.createElement('div');
        card.className = `quick-item quick-item-${item.status}`;
        card.onclick = () => openInlineCard(item.id);
        card.innerHTML = `
            <div class="quick-item-left">
                <div class="quick-item-codigo">${item.codigo}</div>
                <div class="quick-item-produto">${item.produto}</div>
            </div>
            <div class="quick-item-right">
                <span class="quick-item-qty">${item.qtdContada !== null ? item.qtdContada : '—'}</span>
                <span class="quick-item-dot dot-${item.status}"></span>
            </div>
        `;
        body.appendChild(card);
    });
}

function openInlineCard(id) {
    const item = inventoryData.find(i => i.id === id);
    if (!item) return;
    currentEditIndex = id;
    currentQuickIndex = filteredData.findIndex(i => i.id === id);

    const statusMap = { pending: 'Pendente', counted: 'Contado', difference: 'Com Diferença' };
    document.getElementById('inlineCountStatus').textContent = statusMap[item.status];
    document.getElementById('inlineCountStatus').className = `inline-count-badge badge-${item.status}`;
    document.getElementById('inlineCountCodigo').textContent = item.codigo;
    document.getElementById('inlineCountProduto').textContent = item.produto;
    document.getElementById('inlineCountSistema').textContent = item.qtdSistema;
    document.getElementById('inlineCountAtual').textContent = item.qtdContada !== null ? item.qtdContada : '—';

    const diff = item.diferenca;
    const diffEl = document.getElementById('inlineCountDiff');
    diffEl.textContent = diff !== null ? (diff > 0 ? `+${diff}` : diff) : '—';
    diffEl.className = `count-num-val ${diff > 0 ? 'positive' : diff < 0 ? 'negative' : ''}`;

    document.getElementById('inlineQtyInput').value = item.qtdContada !== null ? item.qtdContada : '';
    document.getElementById('inlineCountCard').style.display = 'block';
    document.getElementById('inlineQtyInput').focus();

    document.getElementById('inlinePrevBtn').disabled = currentQuickIndex <= 0;
    document.getElementById('inlineNextBtn').disabled = currentQuickIndex >= filteredData.length - 1;
}

function closeInlineCard() {
    document.getElementById('inlineCountCard').style.display = 'none';
    currentEditIndex = null;
    currentQuickIndex = null;
}

function changeQty(delta) {
    const input = document.getElementById('inlineQtyInput');
    const current = parseFloat(input.value) || 0;
    input.value = Math.max(0, current + delta);
}

function saveInlineCount() {
    if (currentEditIndex === null) return;
    const qty = parseFloat(document.getElementById('inlineQtyInput').value);
    if (isNaN(qty) || qty < 0) { alert('Insira uma quantidade válida.'); return; }

    const item = inventoryData.find(i => i.id === currentEditIndex);
    item.qtdContada = qty;
    item.diferenca = qty - item.qtdSistema;
    item.status = item.diferenca === 0 ? 'counted' : 'difference';

    updateStats();
    renderQuickList(filteredData.length > 0 ? filteredData : inventoryData);
    renderInventory();
    openInlineCard(item.id);

    if (currentQuickIndex < filteredData.length - 1) {
        setTimeout(() => navigateItem(1), 400);
    }
}

function navigateItem(dir) {
    const newIndex = currentQuickIndex + dir;
    if (newIndex < 0 || newIndex >= filteredData.length) return;
    openInlineCard(filteredData[newIndex].id);
}

function renderInventory() {
    const fragment = document.createDocumentFragment();
    const statusTextMap = { pending: 'Pendente', counted: 'Contado', difference: 'Com Diferença' };
    filteredData.forEach(item => {
        const row = document.createElement('tr');
        row.className = getRowClass(item);
        const diff = item.diferenca !== null ? item.diferenca : '-';
        const diffClass = item.diferenca !== null ? (item.diferenca > 0 ? 'positive' : item.diferenca < 0 ? 'negative' : 'neutral') : '';
        row.innerHTML = `
            <td>${item.codigo}</td>
            <td>${item.produto}</td>
            <td>${item.qtdSistema}</td>
            <td>${item.qtdContada !== null ? item.qtdContada : '-'}</td>
            <td class="${diffClass}">${diff}</td>
            <td><span class="status-badge status-${item.status}">${statusTextMap[item.status]}</span></td>
            <td><button class="btn btn-count" onclick="openInlineCard(${item.id}); switchPanel('count')">Contar</button></td>
        `;
        fragment.appendChild(row);
    });
    inventoryBody.innerHTML = '';
    inventoryBody.appendChild(fragment);
}

function getRowClass(item) {
    if (item.status === 'difference') return 'row-difference';
    if (item.status === 'counted') return 'row-counted';
    return '';
}

function applyFilter() {
    filteredData = inventoryData.filter(item => matchesFilter(item));
    renderInventory();
    renderQuickList(filteredData);
}

function matchesFilter(item) {
    if (currentFilter === 'all') return true;
    return item.status === currentFilter;
}

function updateStats() {
    document.getElementById('totalItems').textContent = inventoryData.length;
    document.getElementById('countedItems').textContent = inventoryData.filter(i => i.status === 'counted').length;
    document.getElementById('pendingItems').textContent = inventoryData.filter(i => i.status === 'pending').length;
    document.getElementById('differenceItems').textContent = inventoryData.filter(i => i.status === 'difference').length;
}

function exportToExcel() {
    const exportData = inventoryData.map(item => ({
        'Código': item.codigo, 'Produto': item.produto,
        'Qtd. Sistema': item.qtdSistema,
        'Qtd. Contada': item.qtdContada !== null ? item.qtdContada : '',
        'Diferença': item.diferenca !== null ? item.diferenca : '',
        'Status': { pending: 'Pendente', counted: 'Contado', difference: 'Com Diferença' }[item.status]
    }));
    const ws = XLSX.utils.json_to_sheet(exportData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Contagem de Estoque');
    const d = new Date();
    XLSX.writeFile(wb, `Contagem_Estoque_${d.getDate()}-${d.getMonth()+1}-${d.getFullYear()}.xlsx`);
}

function resetCounts() {
    if (!confirm('Limpar todas as contagens?')) return;
    inventoryData.forEach(item => { item.qtdContada = null; item.diferenca = null; item.status = 'pending'; });
    closeInlineCard();
    applyFilter();
    updateStats();
}

function generateReport() {
    if (!inventoryData.length) { alert('Carregue uma planilha primeiro.'); return; }
    const now = new Date();
    document.getElementById('reportDate').textContent = now.toLocaleDateString('pt-BR');
    document.getElementById('reportTime').textContent = now.toLocaleTimeString('pt-BR');
    const total = inventoryData.length;
    const counted = inventoryData.filter(i => i.qtdContada !== null).length;
    const pending = inventoryData.filter(i => i.status === 'pending').length;
    const withDiff = inventoryData.filter(i => i.status === 'difference').length;
    const progress = total > 0 ? Math.round((counted / total) * 100) : 0;
    document.getElementById('reportTotal').textContent = total;
    document.getElementById('reportCounted').textContent = counted;
    document.getElementById('reportPending').textContent = pending;
    document.getElementById('reportProgress').textContent = progress + '%';
    document.getElementById('progressBar').style.width = progress + '%';
    const pos = inventoryData.filter(i => i.diferenca !== null && i.diferenca > 0);
    const neg = inventoryData.filter(i => i.diferenca !== null && i.diferenca < 0);
    const totalDiff = inventoryData.reduce((s, i) => s + (i.diferenca !== null ? Math.abs(i.diferenca) : 0), 0);
    document.getElementById('reportDifference').textContent = withDiff;
    document.getElementById('reportPositive').textContent = pos.length;
    document.getElementById('reportNegative').textContent = neg.length;
    document.getElementById('reportTotalDiff').textContent = totalDiff;
    const critical = inventoryData.filter(i => i.diferenca !== null && i.diferenca !== 0).sort((a,b) => Math.abs(b.diferenca)-Math.abs(a.diferenca)).slice(0,10);
    const criticalSection = document.getElementById('criticalSection');
    const criticalBody = document.getElementById('criticalItemsBody');
    if (critical.length > 0) {
        criticalSection.style.display = 'block';
        criticalBody.innerHTML = '';
        critical.forEach((item, i) => {
            const diffClass = item.diferenca > 0 ? 'positive' : 'negative';
            const abs = Math.abs(item.diferenca);
            const badgeClass = abs >= 20 ? 'high' : abs >= 10 ? 'medium' : 'low';
            const rank = i===0?'🥇':i===1?'🥈':i===2?'🥉':`${i+1}º`;
            const row = document.createElement('tr');
            row.innerHTML = `<td><strong>${rank}</strong> ${item.codigo}</td><td>${item.produto}</td><td>${item.qtdSistema}</td><td>${item.qtdContada}</td>
            <td><span class="${diffClass}" style="font-weight:700">${item.diferenca>0?'+':''}${item.diferenca}</span>
            <span class="critical-badge ${badgeClass}">${badgeClass==='high'?'CRÍTICO':badgeClass==='medium'?'MÉDIO':'BAIXO'}</span></td>`;
            criticalBody.appendChild(row);
        });
    } else { criticalSection.style.display = 'none'; }
    reportModal.style.display = 'flex';
}

function closeReportModal() { reportModal.style.display = 'none'; }
function printReport() { window.print(); }

function exportReportPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    const now = new Date();
    const dateStr = now.toLocaleDateString('pt-BR');
    const timeStr = now.toLocaleTimeString('pt-BR');
    const total = inventoryData.length;
    const counted = inventoryData.filter(i => i.qtdContada !== null).length;
    const pending = inventoryData.filter(i => i.status === 'pending').length;
    const withDiff = inventoryData.filter(i => i.status === 'difference').length;
    const progress = total > 0 ? Math.round((counted / total) * 100) : 0;
    const pos = inventoryData.filter(i => i.diferenca !== null && i.diferenca > 0);
    const neg = inventoryData.filter(i => i.diferenca !== null && i.diferenca < 0);
    const totalDiff = inventoryData.reduce((s, i) => s + (i.diferenca !== null ? Math.abs(i.diferenca) : 0), 0);
    doc.setFontSize(18); doc.setFont(undefined, 'bold');
    doc.text('RELATÓRIO DE CONTAGEM DE ESTOQUE', 105, 20, { align: 'center' });
    doc.setFontSize(10); doc.setFont(undefined, 'normal');
    doc.text(`Data: ${dateStr}`, 20, 35); doc.text(`Hora: ${timeStr}`, 20, 41);
    doc.setFontSize(12); doc.setFont(undefined, 'bold'); doc.text('RESUMO GERAL', 20, 55);
    doc.autoTable({ startY: 60, head: [], body: [['Total de Itens:', total.toString()],['Itens Contados:', counted.toString()],['Itens Pendentes:', pending.toString()],['Progresso:', `${progress}%`]], theme: 'grid', styles: { fontSize: 10 }, columnStyles: { 0: { fontStyle: 'bold', cellWidth: 50 }, 1: { cellWidth: 30 } } });
    let cy = doc.lastAutoTable.finalY + 10;
    doc.setFontSize(12); doc.setFont(undefined, 'bold'); doc.text('ANÁLISE DE DIFERENÇAS', 20, cy);
    doc.autoTable({ startY: cy + 5, head: [], body: [['Itens com Diferença:', withDiff.toString()],['Itens com Sobra:', pos.length.toString()],['Itens com Falta:', neg.length.toString()],['Total da Diferença:', totalDiff.toString()]], theme: 'grid', styles: { fontSize: 10 }, columnStyles: { 0: { fontStyle: 'bold', cellWidth: 50 }, 1: { cellWidth: 30 } } });
    const critical = inventoryData.filter(i => i.diferenca !== null && i.diferenca !== 0).sort((a,b) => Math.abs(b.diferenca)-Math.abs(a.diferenca)).slice(0,10);
    if (critical.length > 0) {
        cy = doc.lastAutoTable.finalY + 10;
        doc.setFontSize(12); doc.setFont(undefined, 'bold'); doc.text('ITENS CRÍTICOS', 20, cy);
        doc.autoTable({ startY: cy+5, head:[['#','Código','Produto','Sistema','Contado','Diferença','Nível']], body: critical.map((item,i) => { const abs=Math.abs(item.diferenca); return [`${i+1}º`,item.codigo,item.produto,item.qtdSistema.toString(),item.qtdContada.toString(),(item.diferenca>0?'+':'')+item.diferenca.toString(),abs>=20?'CRÍTICO':abs>=10?'MÉDIO':'BAIXO']; }), theme:'striped', styles:{fontSize:8}, headStyles:{fillColor:[102,126,234],fontStyle:'bold'} });
    }
    cy = doc.lastAutoTable ? doc.lastAutoTable.finalY + 15 : 280;
    doc.setFontSize(8); doc.setFont(undefined,'italic');
    doc.text('Relatório gerado automaticamente pelo Sistema de Contagem de Estoque', 105, cy, { align: 'center' });
    doc.save(`Relatorio_Contagem_${dateStr.replace(/\//g,'-')}.pdf`);
}
