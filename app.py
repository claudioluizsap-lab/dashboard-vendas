import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif !important; }
.stApp { background: #0A0E1A; }
.block-container { padding: 1rem 1.5rem 2rem 1.5rem; max-width: 100% !important; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0D1117 0%,#0A0E1A 100%) !important;
    border-right: 1px solid #1E2736 !important;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span { color: #8B949E !important; font-size: 12px !important; }
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background: #1C2333 !important; border: 1px solid #30363D !important;
}

/* KPI CARDS */
.kpi-grid { display: grid; grid-template-columns: repeat(6,1fr); gap: 12px; margin-bottom: 20px; }
.kpi-card {
    background: #0D1117;
    border: 1px solid #1E2736;
    border-radius: 16px;
    padding: 18px 16px 14px;
    position: relative; overflow: hidden;
    transition: all .2s ease;
    cursor: default;
}
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    border-radius: 16px 16px 0 0;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.5);
    border-color: #30363D;
}
.kpi-card .icon { font-size: 22px; margin-bottom: 10px; display: block; }
.kpi-card .lbl {
    font-size: 9px; font-weight: 600; letter-spacing: 1.4px;
    text-transform: uppercase; color: #6E7681; margin-bottom: 6px;
}
.kpi-card .val {
    font-size: 20px; font-weight: 700; color: #E6EDF3;
    line-height: 1.1; margin-bottom: 6px; word-break: break-word;
}
.kpi-card .sub { font-size: 10px; color: #6E7681; font-weight: 400; }
.kpi-card .badge {
    display: inline-block; padding: 2px 8px; border-radius: 20px;
    font-size: 9px; font-weight: 600; margin-top: 6px;
}

.kpi-blue::before   { background: linear-gradient(90deg,#388BFD,#79C0FF); }
.kpi-green::before  { background: linear-gradient(90deg,#3FB950,#7EE787); }
.kpi-purple::before { background: linear-gradient(90deg,#BC8CFF,#D2A8FF); }
.kpi-orange::before { background: linear-gradient(90deg,#F78166,#FFA657); }
.kpi-red::before    { background: linear-gradient(90deg,#FF7B72,#FFA198); }
.kpi-teal::before   { background: linear-gradient(90deg,#39D353,#56D364); }

.badge-blue   { background:rgba(56,139,253,.15); color:#388BFD; }
.badge-green  { background:rgba(63,185,80,.15);  color:#3FB950; }
.badge-purple { background:rgba(188,140,255,.15);color:#BC8CFF; }
.badge-orange { background:rgba(247,129,102,.15);color:#F78166; }
.badge-red    { background:rgba(255,123,114,.15); color:#FF7B72; }
.badge-teal   { background:rgba(57,211,83,.15);  color:#39D353; }

/* SECTION HEADER */
.sec-hdr {
    display: flex; align-items: center; gap: 10px;
    margin: 24px 0 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid #1E2736;
}
.sec-hdr .dot {
    width: 10px; height: 10px; border-radius: 50%;
    flex-shrink: 0; box-shadow: 0 0 8px currentColor;
}
.sec-hdr .title {
    font-size: 13px; font-weight: 600; color: #CDD9E5; letter-spacing: .3px;
}
.sec-hdr .pill {
    margin-left: auto; font-size: 9px; font-weight: 600;
    padding: 3px 10px; border-radius: 20px;
    background: #1C2333; color: #8B949E; border: 1px solid #30363D;
}

/* CHART WRAPPER */
.chart-box {
    background: #0D1117;
    border: 1px solid #1E2736;
    border-radius: 14px;
    padding: 4px;
    margin-bottom: 4px;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] { background: #0D1117 !important; border-radius: 10px; padding: 4px; gap: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px !important; color: #6E7681 !important; font-size: 12px !important; padding: 6px 16px !important; }
.stTabs [aria-selected="true"] { background: #1C2333 !important; color: #CDD9E5 !important; }

/* DATAFRAME */
div[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; border: 1px solid #1E2736; }

/* SCROLLBAR */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0D1117; }
::-webkit-scrollbar-thumb { background: #30363D; border-radius: 3px; }

/* FOOTER */
.footer {
    text-align: center; color: #3D444D; font-size: 10px;
    padding: 16px 0 4px; border-top: 1px solid #1E2736;
    margin-top: 32px; letter-spacing: .5px;
}
</style>
""", unsafe_allow_html=True)

XLSX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vendas.xlsx')

COLORS = [
    '#388BFD','#3FB950','#F78166','#BC8CFF','#FFA657',
    '#79C0FF','#56D364','#FF7B72','#D2A8FF','#7EE787',
    '#FFA198','#A5D6FF','#FFD700','#E879F9','#22D3EE',
]

def layout_base(title='', height=380, margin=None, show_unified=True):
    return dict(
        paper_bgcolor='#0D1117',
        plot_bgcolor='#080C14',
        font=dict(family='Inter, sans-serif', color='#CDD9E5', size=11),
        title=dict(text=title, font=dict(size=13, color='#E6EDF3'), x=0.02, xanchor='left'),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#8B949E', size=9),
                    bordercolor='rgba(0,0,0,0)'),
        margin=margin or dict(t=48, b=36, l=8, r=8),
        height=height,
        hovermode='x unified' if show_unified else 'closest',
        hoverlabel=dict(bgcolor='#161B22', font_color='#CDD9E5',
                        bordercolor='#30363D', font_size=11),
        xaxis=dict(gridcolor='#131A26', gridwidth=0.6, linecolor='#1E2736',
                   tickfont=dict(color='#6E7681', size=9), zeroline=False,
                   tickcolor='#1E2736'),
        yaxis=dict(gridcolor='#131A26', gridwidth=0.6, linecolor='#1E2736',
                   tickfont=dict(color='#6E7681', size=9), zeroline=False,
                   tickcolor='#1E2736'),
    )

def ax():
    return dict(gridcolor='#131A26', gridwidth=0.6, linecolor='#1E2736',
                tickfont=dict(color='#6E7681', size=9), zeroline=False)

@st.cache_data(ttl=300)
def load_data():
    df_raw = pd.read_excel(XLSX_PATH, sheet_name='Planilha1', header=None)
    dates = [pd.to_datetime(v) for v in df_raw.iloc[0, 2:] if pd.notna(v)]
    n = len(dates)
    ml = [d.strftime('%b/%Y') for d in dates]
    alias = {
        'JHOYCE':'JHOICE','CHRISTIANE':'CRISTIANE',
        'FRANCISCO ':'FRANCISCO','vendas PAULO ':'PAULO','VENDEDOR':'PAULO',
    }
    def norm(x): return alias.get(str(x).strip(), str(x).strip())
    qtd_rows = df_raw.iloc[3:14].copy()
    qtd_rows = qtd_rows[qtd_rows[0].notna() & (qtd_rows[0] != 0)]
    qtd_data = {
        norm(r[0]): [float(r.iloc[2+i]) if pd.notna(r.iloc[2+i]) else 0. for i in range(n)]
        for _, r in qtd_rows.iterrows()
    }
    setor_rows = df_raw.iloc[17:].copy()
    setor_rows = setor_rows[setor_rows[0].notna() & (setor_rows[0] != 0)]
    setor_data = {}
    for _, row in setor_rows.iterrows():
        rs = str(row[1]).strip()
        if rs.startswith('z') or rs.endswith('**'):
            continue
        setor = rs.rstrip('*').rstrip().strip()
        func = norm(row[0])
        vals = [float(row.iloc[2+i]) if pd.notna(row.iloc[2+i]) else 0. for i in range(n)]
        setor_data.setdefault(func, {}).setdefault(setor, [0.]*n)
        setor_data[func][setor] = [setor_data[func][setor][i]+vals[i] for i in range(n)]
    all_funcs = sorted(set(list(qtd_data.keys()) + list(setor_data.keys())))
    return dates, ml, n, qtd_data, setor_data, all_funcs

dates, ml, n, qtd_data, setor_data, all_funcs = load_data()

setor_global = {}
for fd in setor_data.values():
    for ss, vv in fd.items():
        setor_global[ss] = setor_global.get(ss, 0) + sum(vv)
all_setores = sorted(setor_global.keys())

# ───────────────────────── SIDEBAR ─────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 8px;text-align:center'>
        <div style='font-size:32px'>📊</div>
        <div style='font-size:14px;font-weight:700;color:#CDD9E5;margin-top:4px'>Vendas Dashboard</div>
        <div style='font-size:10px;color:#6E7681;margin-top:2px'>v3.0 · Jan/2025–Dez/2026</div>
    </div>
    <hr style='border-color:#1E2736;margin:8px 0 16px'>
    """, unsafe_allow_html=True)

    anos = sorted(set(d.year for d in dates))
    import datetime as _dt
    ano_atual = _dt.datetime.now().year
    mes_atual = _dt.datetime.now().month
    default_anos = [ano_atual] if ano_atual in anos else anos
    anos_sel = st.multiselect("📅 Ano", anos, default=default_anos)

    nomes_meses = {1:'Janeiro',2:'Fevereiro',3:'Março',4:'Abril',5:'Maio',6:'Junho',
                   7:'Julho',8:'Agosto',9:'Setembro',10:'Outubro',11:'Novembro',12:'Dezembro'}
    meses_disp = sorted(set(d.month for d in dates))
    meses_ano  = sorted(set(d.month for d in dates if d.year in anos_sel)) if anos_sel else meses_disp
    default_meses = [mes_atual] if mes_atual in meses_disp else meses_disp[:1]
    meses_sel = st.multiselect("🗓 Mês", options=meses_disp, default=default_meses,
        format_func=lambda m: nomes_meses[m])

    funcs_sel = st.multiselect("👤 Funcionario", all_funcs, default=all_funcs)
    setores_sel = st.multiselect("🏷 Setor", all_setores, default=all_setores)

    st.markdown("<hr style='border-color:#1E2736;margin:16px 0 12px'>", unsafe_allow_html=True)

    if st.button("🔄 Limpar Filtros", use_container_width=True):
        st.rerun()

    if st.button("⬆ Atualizar Dados", use_container_width=True, type="primary"):
        load_data.clear()
        st.rerun()

    st.markdown("<div style='font-size:10px;color:#6E7681;margin-top:14px;margin-bottom:4px'>📂 CARREGAR PLANILHA</div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("", type=["xlsx"], label_visibility="collapsed")
    if uploaded is not None:
        import shutil
        with open(XLSX_PATH, "wb") as f_out:
            f_out.write(uploaded.getbuffer())
        load_data.clear()
        st.success("Planilha atualizada!")
        st.rerun()

    st.markdown("""
    <div style='text-align:center;margin-top:12px'>
        <div style='font-size:9px;color:#3D444D;letter-spacing:.5px'>FONTE DE DADOS</div>
        <div style='font-size:10px;color:#6E7681;margin-top:2px'>vendas.xlsx</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────── CALCULOS ───────────────────────────
idx_f    = [i for i,d in enumerate(dates) if d.year in anos_sel and d.month in meses_sel]
ml_f     = [ml[i] for i in idx_f]
dates_f  = [dates[i] for i in idx_f]

total_qtd = sum(qtd_data.get(f,[0]*n)[i] for f in funcs_sel for i in idx_f)
total_val = sum(
    setor_data.get(f,{}).get(s,[0]*n)[i]
    for f in funcs_sel for s in setores_sel for i in idx_f
    if s in setor_data.get(f,{})
)
ticket = total_val / total_qtd if total_qtd else 0

qtd_men_f = [sum(qtd_data.get(f,[0]*n)[i] for f in funcs_sel) for i in idx_f]
val_men_f = [
    sum(setor_data.get(f,{}).get(s,[0]*n)[i]
        for f in funcs_sel for s in setores_sel
        if s in setor_data.get(f,{}))
    for i in idx_f
]
func_qtd = {f: sum(qtd_data.get(f,[0]*n)[i] for i in idx_f) for f in funcs_sel}
func_val = {
    f: sum(setor_data.get(f,{}).get(s,[0]*n)[i]
           for s in setores_sel for i in idx_f
           if s in setor_data.get(f,{}))
    for f in funcs_sel
}
setor_vals_f = {
    s: sum(setor_data.get(f,{}).get(s,[0]*n)[i]
           for f in funcs_sel for i in idx_f
           if s in setor_data.get(f,{}))
    for s in setores_sel
}

top_qtd_f   = max(func_qtd, key=lambda f: func_qtd[f]) if funcs_sel else '-'
top_val_f   = max(func_val, key=lambda f: func_val[f])  if funcs_sel else '-'
top_setor_f = max(setor_vals_f, key=lambda s: setor_vals_f[s]) if setores_sel else '-'

# crescimento ultimo mes
cresc_pct = 0.0
cresc_abs = 0
if len(qtd_men_f) >= 2:
    prev = qtd_men_f[-2]
    curr = qtd_men_f[-1]
    cresc_pct = ((curr - prev) / prev * 100) if prev else 0
    cresc_abs = int(curr - prev)

def brl(v):  return "R$ {:,.0f}".format(v).replace(',','X').replace('.',',').replace('X','.')
def nn(v):   return "{:,}".format(int(v)).replace(',','.')
def pct(v):  return f"{v:+.1f}%"

# ─────────────────────── HEADER ─────────────────────────────
now = datetime.now().strftime('%d/%m/%Y %H:%M')
periodo = f"{ml_f[0]} – {ml_f[-1]}" if ml_f else "—"
st.markdown(f"""
<div style='
    background:linear-gradient(135deg,#0D1117 0%,#0F1824 50%,#0A0E1A 100%);
    border:1px solid #1E2736; border-radius:18px;
    padding:22px 28px; margin-bottom:20px;
    display:flex; align-items:center; justify-content:space-between;
    box-shadow:0 8px 32px rgba(0,0,0,0.6);
'>
  <div>
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:6px'>
      <div style='
          background:linear-gradient(135deg,#388BFD,#BC8CFF);
          border-radius:12px;padding:8px 10px;font-size:20px;line-height:1
      '>📊</div>
      <h1 style='color:#E6EDF3;margin:0;font-size:24px;font-weight:700;letter-spacing:-0.5px'>
          Dashboard de Vendas
      </h1>
    </div>
    <p style='color:#6E7681;margin:0;font-size:11px'>
      Periodo: <span style='color:#388BFD;font-weight:500'>{periodo}</span>
      &nbsp;·&nbsp;
      {len(funcs_sel)} funcionario(s)
      &nbsp;·&nbsp;
      {len(setores_sel)} setor(es)
    </p>
  </div>
  <div style='text-align:right'>
    <div style='font-size:10px;color:#3D444D;letter-spacing:.5px;text-transform:uppercase'>Atualizado</div>
    <div style='font-size:12px;color:#6E7681;margin-top:2px'>{now}</div>
    <div style='
        display:inline-block;margin-top:6px;padding:3px 10px;border-radius:20px;
        background:rgba(63,185,80,.12);border:1px solid rgba(63,185,80,.3);
        color:#3FB950;font-size:9px;font-weight:600;letter-spacing:.5px
    '>● ONLINE</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────── KPI CARDS ──────────────────────────
cresc_color = '#3FB950' if cresc_pct >= 0 else '#FF7B72'
cresc_bg    = 'rgba(63,185,80,.12)' if cresc_pct >= 0 else 'rgba(255,123,114,.12)'
cresc_border= 'rgba(63,185,80,.3)' if cresc_pct >= 0 else 'rgba(255,123,114,.3)'

kpis = [
    ("kpi-blue",   "💼", "TOTAL DE VENDAS",  nn(int(total_qtd)),  "unidades acumuladas",      "badge-blue",   nn(int(total_qtd))+" un"),
    ("kpi-green",  "💰", "RECEITA TOTAL",    brl(total_val),      "valor acumulado",          "badge-green",  "acumulado"),
    ("kpi-purple", "🎯", "TICKET MEDIO",     brl(ticket),         "por transacao",            "badge-purple", "por venda"),
    ("kpi-orange", "🏆", "TOP VENDEDOR QTD", top_qtd_f,           nn(int(func_qtd.get(top_qtd_f,0)))+" un", "badge-orange", "lider"),
    ("kpi-red",    "💎", "TOP RECEITA",      top_val_f,           brl(func_val.get(top_val_f,0)),    "badge-red",    "lider"),
    ("kpi-teal",   "📦", "TOP SETOR",        top_setor_f[:14],    brl(setor_vals_f.get(top_setor_f,0)), "badge-teal", "destaque"),
]

cols_kpi = st.columns(6)
for col, (cls, icon, lbl, val, sub, badge_cls, badge_txt) in zip(cols_kpi, kpis):
    col.markdown(f"""
    <div class="kpi-card {cls}">
        <span class="icon">{icon}</span>
        <div class="lbl">{lbl}</div>
        <div class="val">{val}</div>
        <div class="sub">{sub}</div>
        <span class="badge {badge_cls}">{badge_txt}</span>
    </div>
    """, unsafe_allow_html=True)

# mini-card crescimento
st.markdown(f"""
<div style='
    background:#0D1117; border:1px solid #1E2736; border-radius:12px;
    padding:10px 20px; margin:8px 0 4px;
    display:flex; align-items:center; gap:24px;
'>
  <div style='font-size:11px;color:#6E7681;font-weight:600;letter-spacing:.5px;text-transform:uppercase'>
      Crescimento ultimo mes
  </div>
  <div style='
      padding:4px 14px; border-radius:20px;
      background:{cresc_bg}; border:1px solid {cresc_border};
      color:{cresc_color}; font-size:14px; font-weight:700;
  '>{pct(cresc_pct)}</div>
  <div style='font-size:11px;color:#6E7681'>
      {("+" if cresc_abs >= 0 else "")}{nn(cresc_abs)} unidades vs mes anterior
  </div>
  <div style='margin-left:auto;font-size:10px;color:#3D444D'>
      {ml_f[-1] if ml_f else "—"}
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────── HELPER ─────────────────────────────
CFG = {'displayModeBar': True, 'displaylogo': False,
       'modeBarButtonsToRemove': ['lasso2d','select2d','autoScale2d'],
       'toImageButtonOptions': {'format':'png','filename':'grafico_vendas','scale':2}}

def chart(fig):
    try:
        st.plotly_chart(fig, config=CFG, width='stretch')
    except Exception as e:
        st.error(f"Erro ao renderizar gráfico: {e}")

def sec(title, icon, color='#388BFD', pill=''):
    st.markdown(f"""
    <div class="sec-hdr">
        <div class="dot" style='background:{color};color:{color}'></div>
        <span class="title">{icon} {title}</span>
        {'<span class="pill">'+pill+'</span>' if pill else ''}
    </div>""", unsafe_allow_html=True)

# ─────────────────────── TABS PRINCIPAIS ────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈  Evolucao",
    "👥  Ranking",
    "🔥  Analise",
    "📋  Dados",
])

# ═══════════════════════ TAB 1: EVOLUCAO ════════════════════
with tab1:
    col_ev, col_pie = st.columns([3, 2])

    with col_ev:
        sec("Evolucao Mensal — Quantidade e Valor", "📈", '#388BFD',
            f"{len(ml_f)} meses")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=ml_f, y=qtd_men_f, name='Qtd Vendas',
            marker=dict(
                color=[f'rgba(56,139,253,{max(0.35, v/max(qtd_men_f+[1])*0.9+0.1)})' for v in qtd_men_f],
                line=dict(width=0),
                pattern_shape='',
            ),
            hovertemplate='<b>%{x}</b><br>Quantidade: <b>%{y:,.0f}</b><extra></extra>',
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=ml_f, y=val_men_f, name='Valor R$',
            mode='lines+markers',
            line=dict(color='#F78166', width=2.5, shape='spline', smoothing=0.7),
            marker=dict(size=8, color='#F78166',
                        line=dict(color='#080C14', width=2.5),
                        symbol='circle'),
            fill='tozeroy', fillcolor='rgba(247,129,102,0.06)',
            hovertemplate='<b>%{x}</b><br>Valor: <b>R$ %{y:,.0f}</b><extra></extra>',
        ), secondary_y=True)
        L = layout_base(height=360)
        L['legend'] = dict(orientation='h', y=1.1, x=0,
                           bgcolor='rgba(0,0,0,0)', font=dict(color='#8B949E', size=10))
        L['bargap'] = 0.18
        fig.update_layout(**L)
        fig.update_yaxes(title_text='Qtd.', secondary_y=False, **ax())
        fig.update_yaxes(title_text='Valor (R$)', secondary_y=True,
                         **{k:v for k,v in ax().items() if 'grid' not in k}, showgrid=False)
        fig.update_xaxes(tickangle=-40, **ax())
        chart(fig)

    with col_pie:
        sec("Participacao por Setor", "🥧", '#BC8CFF')
        sv = {k: v for k,v in setor_vals_f.items() if v > 0}
        top10 = sorted(sv, key=lambda s: -sv[s])[:10]
        v10   = [sv[s] for s in top10]
        oth   = sum(sv[s] for s in sv if s not in top10)
        if oth > 0: top10.append('Outros'); v10.append(oth)
        fig2 = go.Figure(go.Pie(
            labels=top10, values=v10, hole=0.55,
            marker=dict(colors=COLORS[:len(top10)],
                        line=dict(color='#080C14', width=2)),
            textinfo='percent',
            textfont=dict(size=9, color='white'),
            textposition='inside',
            hovertemplate='<b>%{label}</b><br>R$ %{value:,.0f}<br><b>%{percent}</b><extra></extra>',
            rotation=30,
        ))
        total_sv = sum(v10)
        fig2.add_annotation(
            text=f"<b>R$</b><br><b>{brl(total_sv).replace('R$ ','')}</b>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=11, color='#CDD9E5', family='Inter'),
        )
        L2 = layout_base(height=360, show_unified=False)
        L2['margin'] = dict(t=20,b=10,l=10,r=10)
        L2['legend'] = dict(font=dict(size=8, color='#8B949E'),
                            orientation='v', x=1.01, y=0.5)
        L2['showlegend'] = True
        fig2.update_layout(**L2)
        chart(fig2)

    # linha do tempo por funcionario
    sec("Evolucao por Funcionario (Quantidade)", "👤", '#3FB950',
        "selecione na legenda")
    fig_line = go.Figure()
    for i, func in enumerate(funcs_sel):
        vals = [qtd_data.get(func,[0]*n)[j] for j in idx_f]
        if sum(vals) == 0: continue
        fig_line.add_trace(go.Scatter(
            x=ml_f, y=vals, name=func, mode='lines+markers',
            line=dict(color=COLORS[i % len(COLORS)], width=2, shape='spline', smoothing=0.6),
            marker=dict(size=6, line=dict(color='#080C14', width=1.5)),
            hovertemplate=f'<b>{func}</b><br>%{{x}}<br>Qtd: <b>%{{y:,.0f}}</b><extra></extra>',
        ))
    L3 = layout_base(height=300)
    L3['legend'] = dict(orientation='h', y=-0.2, bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#8B949E', size=9))
    L3['margin'] = dict(t=40, b=60, l=8, r=8)
    fig_line.update_layout(**L3)
    fig_line.update_xaxes(tickangle=-40, **ax())
    fig_line.update_yaxes(**ax())
    chart(fig_line)

    # comparativo anual
    if len(anos_sel) >= 2:
        sec("Comparativo Anual", "📅", '#FFA657')
        comp = []
        for ano in anos_sel:
            ia = [i for i,d in enumerate(dates) if d.year==ano and d.month in meses_sel]
            for func in funcs_sel:
                q = sum(qtd_data.get(func,[0]*n)[i] for i in ia)
                v = sum(setor_data.get(func,{}).get(s,[0]*n)[i]
                        for s in setores_sel for i in ia
                        if s in setor_data.get(func,{}))
                if q > 0:
                    comp.append({'Ano':str(ano),'Funcionario':func,'Qtd':q,'Valor':v})
        if comp:
            df_c = pd.DataFrame(comp)
            yr_colors = {str(a):c for a,c in zip(sorted(anos_sel),
                         ['#388BFD','#3FB950','#F78166','#BC8CFF'])}
            fig_cmp = px.bar(df_c, x='Funcionario', y='Qtd', color='Ano',
                barmode='group', color_discrete_map=yr_colors, text='Qtd')
            fig_cmp.update_traces(
                texttemplate='<b>%{text:,.0f}</b>', textposition='outside',
                textfont=dict(size=8, color='#CDD9E5'), marker_line_width=0,
            )
            L4 = layout_base(height=370)
            L4['bargap'] = 0.22; L4['bargroupgap'] = 0.08
            L4['legend'] = dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)',
                                font=dict(color='#8B949E', size=10))
            L4['margin'] = dict(t=50,b=50,l=8,r=8)
            fig_cmp.update_layout(**L4)
            fig_cmp.update_xaxes(tickangle=-30, **ax())
            fig_cmp.update_yaxes(**ax())
            chart(fig_cmp)

# ═══════════════════════ TAB 2: RANKING ═════════════════════
with tab2:
    r1, r2 = st.columns(2)

    with r1:
        sec("Ranking — Quantidade de Vendas", "🏆", '#388BFD')
        df_q = pd.DataFrame({'Funcionario': list(func_qtd.keys()),
                              'Qtd': list(func_qtd.values())}).sort_values('Qtd')
        mx = df_q['Qtd'].max() if not df_q.empty else 1
        fig3 = go.Figure(go.Bar(
            x=df_q['Qtd'], y=df_q['Funcionario'], orientation='h',
            marker=dict(
                color=[f'rgba(56,139,253,{0.35+0.65*(v/mx)})' for v in df_q['Qtd']],
                line=dict(color='rgba(56,139,253,0.8)', width=0.8),
            ),
            text=df_q['Qtd'],
            texttemplate='<b>%{text:,.0f}</b>',
            textposition='outside',
            textfont=dict(color='#8B949E', size=9),
            hovertemplate='<b>%{y}</b><br>Qtd: <b>%{x:,.0f}</b><extra></extra>',
        ))
        L5 = layout_base(height=380)
        L5['margin'] = dict(t=40,b=10,l=8,r=90)
        fig3.update_layout(**L5)
        fig3.update_xaxes(**ax())
        fig3.update_yaxes(**{k:v for k,v in ax().items() if 'grid' not in k}, showgrid=False)
        chart(fig3)

    with r2:
        sec("Ranking — Valor de Vendas R$", "💰", '#3FB950')
        df_v = pd.DataFrame({'Funcionario': list(func_val.keys()),
                              'Valor': list(func_val.values())}).sort_values('Valor')
        mx2 = df_v['Valor'].max() if not df_v.empty else 1
        fig4 = go.Figure(go.Bar(
            x=df_v['Valor'], y=df_v['Funcionario'], orientation='h',
            marker=dict(
                color=[f'rgba(63,185,80,{0.35+0.65*(v/mx2)})' for v in df_v['Valor']],
                line=dict(color='rgba(63,185,80,0.8)', width=0.8),
            ),
            text=df_v['Valor'],
            texttemplate='R$ <b>%{text:,.0f}</b>',
            textposition='outside',
            textfont=dict(color='#8B949E', size=9),
            hovertemplate='<b>%{y}</b><br>R$ <b>%{x:,.0f}</b><extra></extra>',
        ))
        L6 = layout_base(height=380)
        L6['margin'] = dict(t=40,b=10,l=8,r=120)
        fig4.update_layout(**L6)
        fig4.update_xaxes(**ax(), tickformat=',.0f')
        fig4.update_yaxes(**{k:v for k,v in ax().items() if 'grid' not in k}, showgrid=False)
        chart(fig4)

    # Distribuicao Setores — layout completo
    sec("Distribuicao Setores", "🗺", '#BC8CFF',
        f"{len([s for s in setores_sel if setor_vals_f.get(s,0)>0])} setores ativos")

    tree_rows = []
    for func in funcs_sel:
        for setor in setores_sel:
            v = sum(setor_data.get(func,{}).get(setor,[0]*n)[i] for i in idx_f
                    if setor in setor_data.get(func,{}))
            if v > 0:
                tree_rows.append({'Funcionario': func, 'Setor': setor, 'Valor': v})

    if tree_rows:
        df_tree = pd.DataFrame(tree_rows)

        # totais por setor (todos funcionarios)
        setor_tot = df_tree.groupby('Setor')['Valor'].sum().sort_values(ascending=False)
        grand = setor_tot.sum()

        # -- col esquerda: Treemap hierarquico --
        tc1, tc2 = st.columns([3, 2])

        with tc1:
            # adicionar linha raiz "Total"
            df_tm = df_tree.copy()
            df_tm['Total'] = 'Vendas'
            fig_tree = px.treemap(
                df_tm,
                path=['Total', 'Funcionario', 'Setor'],
                values='Valor',
                color='Valor',
                color_continuous_scale=[
                    [0.0,  '#0A0E1A'],
                    [0.15, '#0C1E3B'],
                    [0.4,  '#0E3060'],
                    [0.65, '#1A6FC4'],
                    [0.85, '#388BFD'],
                    [1.0,  '#79C0FF'],
                ],
                custom_data=['Funcionario', 'Setor', 'Valor'],
            )
            fig_tree.update_traces(
                texttemplate=(
                    '<b>%{label}</b><br>'
                    'R$ %{value:,.0f}<br>'
                    '%{percentRoot:.1%}'
                ),
                textfont=dict(size=11, family='Inter', color='#E6EDF3'),
                insidetextfont=dict(size=10),
                hovertemplate=(
                    '<b>%{label}</b><br>'
                    'Valor: <b>R$ %{value:,.0f}</b><br>'
                    '% do total: <b>%{percentRoot:.1%}</b>'
                    '<extra></extra>'
                ),
                marker=dict(
                    line=dict(color='#080C14', width=2.5),
                    cornerradius=6,
                ),
                root_color='#080C14',
            )
            Lt = layout_base(height=460, show_unified=False)
            Lt['margin'] = dict(t=10, b=10, l=6, r=6)
            Lt['coloraxis_colorbar'] = dict(
                tickfont=dict(color='#6E7681', size=8),
                title=dict(text='R$', font=dict(color='#6E7681', size=9)),
                thickness=10, len=0.7,
                outlinecolor='#1E2736', outlinewidth=1,
            )
            fig_tree.update_layout(**Lt)
            chart(fig_tree)

        # -- col direita: barras horizontais por setor + sunburst --
        with tc2:
            # barras ranking setores
            top_s  = setor_tot.head(12)
            mx_s   = top_s.max() if not top_s.empty else 1

            fig_sb = go.Figure()
            for i, (setor, val) in enumerate(top_s.items()):
                ratio  = val / mx_s
                alpha  = 0.30 + 0.70 * ratio
                color  = COLORS[i % len(COLORS)]
                r_int  = int(color[1:3], 16)
                g_int  = int(color[3:5], 16)
                b_int  = int(color[5:7], 16)
                fig_sb.add_trace(go.Bar(
                    x=[val], y=[setor],
                    orientation='h',
                    name=setor,
                    showlegend=False,
                    marker=dict(
                        color=f'rgba({r_int},{g_int},{b_int},{alpha:.2f})',
                        line=dict(color=f'rgba({r_int},{g_int},{b_int},0.9)', width=1),
                        cornerradius=4,
                    ),
                    text=[val],
                    texttemplate='R$ <b>%{text:,.0f}</b>',
                    textposition='outside',
                    textfont=dict(color='#8B949E', size=8),
                    hovertemplate=(
                        f'<b>{setor}</b><br>'
                        'Valor: <b>R$ %{x:,.0f}</b><br>'
                        f'Participacao: <b>{val/grand*100:.1f}%</b>'
                        '<extra></extra>'
                    ),
                ))

            Lb = layout_base(height=460, show_unified=False)
            Lb['margin']    = dict(t=30, b=10, l=8, r=110)
            Lb['title']     = dict(text='Ranking por Setor (R$)',
                                   font=dict(size=12, color='#CDD9E5'), x=0.02)
            Lb['bargap']    = 0.28
            Lb['barmode']   = 'stack'
            fig_sb.update_layout(**Lb)
            fig_sb.update_xaxes(tickformat=',.0f', **ax())
            fig_sb.update_yaxes(
                **{k:v for k,v in ax().items() if 'grid' not in k and k != 'tickfont'},
                showgrid=False, autorange='reversed',
                tickfont=dict(color='#CDD9E5', size=9),
            )
            chart(fig_sb)

        # -- linha inferior: sunburst + barras empilhadas por funcionario --
        bc1, bc2 = st.columns([2, 3])

        with bc1:
            # Sunburst setor > funcionario
            setor_color_map = {s: COLORS[i % len(COLORS)] for i, s in enumerate(setor_tot.index)}
            leaf_ids     = [r['Setor']+'||'+r['Funcionario'] for r in tree_rows]
            branch_ids   = list(setor_tot.index)
            leaf_labels  = [r['Funcionario'] for r in tree_rows]
            branch_labels= [f"<b>{s}</b>" for s in setor_tot.index]
            leaf_parents = [r['Setor'] for r in tree_rows]
            branch_parents = ['']*len(setor_tot)
            leaf_values  = [r['Valor'] for r in tree_rows]
            branch_values= list(setor_tot.values)
            leaf_colors  = [setor_color_map.get(r['Setor'], COLORS[0]) for r in tree_rows]
            branch_colors= [setor_color_map.get(s, COLORS[0]) for s in setor_tot.index]

            fig_sun = go.Figure(go.Sunburst(
                ids    = leaf_ids    + branch_ids,
                labels = leaf_labels + branch_labels,
                parents= leaf_parents+ branch_parents,
                values = leaf_values + branch_values,
                branchvalues='total',
                marker=dict(
                    colors=leaf_colors + branch_colors,
                    line=dict(color='#080C14', width=1.5),
                ),
                textfont=dict(size=10, color='#E6EDF3'),
                hovertemplate='<b>%{label}</b><br>R$ %{value:,.0f}<br>%{percentParent:.1%} do setor<extra></extra>',
                insidetextorientation='radial',
                rotation=20,
            ))
            Lsun = layout_base(height=380, show_unified=False)
            Lsun['margin'] = dict(t=30, b=10, l=8, r=8)
            Lsun['title']  = dict(text='Sunburst: Setor › Funcionario',
                                  font=dict(size=12, color='#CDD9E5'), x=0.02)
            fig_sun.update_layout(**Lsun)
            chart(fig_sun)

        with bc2:
            # Barras empilhadas: funcionario x setor
            funcs_ordered = sorted(
                funcs_sel,
                key=lambda f: sum(
                    setor_data.get(f,{}).get(s,[0]*n)[i]
                    for s in setores_sel for i in idx_f
                    if s in setor_data.get(f,{})
                ),
                reverse=True,
            )
            fig_stk = go.Figure()
            setores_ordered = list(setor_tot.index)
            for i, setor in enumerate(setores_ordered):
                color = COLORS[i % len(COLORS)]
                r_int = int(color[1:3], 16)
                g_int = int(color[3:5], 16)
                b_int = int(color[5:7], 16)
                vals_stk = []
                for func in funcs_ordered:
                    v = sum(setor_data.get(func,{}).get(setor,[0]*n)[j]
                            for j in idx_f if setor in setor_data.get(func,{}))
                    vals_stk.append(v)
                fig_stk.add_trace(go.Bar(
                    name=setor,
                    x=funcs_ordered,
                    y=vals_stk,
                    marker=dict(
                        color=f'rgba({r_int},{g_int},{b_int},0.82)',
                        line=dict(color='#080C14', width=1),
                    ),
                    hovertemplate=(
                        f'<b>{setor}</b><br>'
                        '%{x}<br>'
                        'R$ <b>%{y:,.0f}</b>'
                        '<extra></extra>'
                    ),
                    text=vals_stk,
                    texttemplate='%{text:,.0f}',
                    textposition='inside',
                    insidetextanchor='middle',
                    textfont=dict(size=8, color='rgba(255,255,255,0.7)'),
                ))
            Lstk = layout_base(height=380)
            Lstk['barmode'] = 'stack'
            Lstk['bargap']  = 0.22
            Lstk['title']   = dict(text='Composicao por Funcionario e Setor (R$)',
                                   font=dict(size=12, color='#CDD9E5'), x=0.02)
            Lstk['legend']  = dict(
                orientation='h', y=-0.25, bgcolor='rgba(0,0,0,0)',
                font=dict(color='#8B949E', size=8), itemwidth=40,
            )
            Lstk['margin'] = dict(t=50, b=80, l=8, r=8)
            fig_stk.update_layout(**Lstk)
            fig_stk.update_xaxes(tickangle=-30,
                                  **{k:v for k,v in ax().items() if k != 'tickfont'},
                                  tickfont=dict(color='#CDD9E5', size=9))
            fig_stk.update_yaxes(**ax(), tickformat=',.0f')
            chart(fig_stk)

# ═══════════════════════ TAB 3: ANALISE ═════════════════════
with tab3:
    sec("Heatmap — Quantidade por Funcionario e Mes", "🔥", '#F78166',
        "intensidade = volume")
    funcs_hm = [f for f in funcs_sel if sum(qtd_data.get(f,[0]*n)[i] for i in idx_f) > 0]
    if funcs_hm and idx_f:
        matrix = [[qtd_data.get(f,[0]*n)[i] for i in idx_f] for f in funcs_hm]
        import numpy as np
        mat_arr = np.array(matrix, dtype=float)

        fig5 = go.Figure(go.Heatmap(
            z=mat_arr, x=ml_f, y=funcs_hm,
            colorscale=[
                [0,    '#080C14'],
                [0.15, '#0C1E3B'],
                [0.4,  '#0C2D6B'],
                [0.65, '#1A6FC4'],
                [0.85, '#388BFD'],
                [1,    '#A8D8FF'],
            ],
            text=[[f'{int(v)}' if v > 0 else '' for v in row] for row in mat_arr],
            texttemplate='<b>%{text}</b>',
            textfont=dict(size=9.5),
            hovertemplate='<b>%{y}</b> · %{x}<br>Qtd: <b>%{z:.0f}</b><extra></extra>',
            showscale=True,
            colorbar=dict(
                tickfont=dict(color='#6E7681', size=8),
                outlinecolor='#1E2736', outlinewidth=1,
                bgcolor='rgba(0,0,0,0)',
                title=dict(text='Qtd', font=dict(color='#6E7681', size=9), side='right'),
                thickness=12,
            ),
            xgap=2, ygap=2,
        ))
        Lh = layout_base(height=max(280, len(funcs_hm)*46))
        Lh['margin'] = dict(t=20,b=55,l=8,r=20)
        fig5.update_layout(**Lh)
        fig5.update_xaxes(tickangle=-40, **ax(), side='bottom')
        fig5.update_yaxes(**{k:v for k,v in ax().items() if 'grid' not in k}, showgrid=False)
        chart(fig5)

    # Scatter valor x qtd por funcionario
    sec("Eficiencia — Valor vs Quantidade", "⚡", '#FFA657',
        "tamanho = ticket medio")
    scatter_rows = []
    for func in funcs_sel:
        q = func_qtd.get(func, 0)
        v = func_val.get(func, 0)
        t = v / q if q else 0
        if q > 0:
            scatter_rows.append({'Funcionario': func, 'Qtd': q, 'Valor': v, 'Ticket': t})
    if scatter_rows:
        df_sc = pd.DataFrame(scatter_rows)
        fig_sc = px.scatter(
            df_sc, x='Qtd', y='Valor', text='Funcionario',
            size='Ticket', size_max=50,
            color='Ticket',
            color_continuous_scale=[[0,'#1A6FC4'],[0.5,'#388BFD'],[1,'#A8D8FF']],
            hover_data={'Qtd': ':,.0f', 'Valor': ':,.0f', 'Ticket': ':,.0f'},
        )
        fig_sc.update_traces(
            textposition='top center',
            textfont=dict(size=9, color='#8B949E'),
            marker=dict(line=dict(color='#080C14', width=1.5)),
        )
        Ls = layout_base(height=360, show_unified=False)
        Ls['coloraxis_colorbar'] = dict(
            title=dict(text='Ticket R$', font=dict(color='#6E7681', size=9)),
            tickfont=dict(color='#6E7681', size=8), thickness=12,
        )
        Ls['xaxis']['title'] = dict(text='Quantidade', font=dict(color='#6E7681'))
        Ls['yaxis']['title'] = dict(text='Valor R$', font=dict(color='#6E7681'))
        fig_sc.update_layout(**Ls)
        chart(fig_sc)

# ═══════════════════════ TAB 4: DADOS ═══════════════════════
with tab4:
    sec("Dados Detalhados por Funcionario e Setor", "📋", '#388BFD')
    rows_tab = []
    for func in funcs_sel:
        for setor in setores_sel:
            if setor not in setor_data.get(func, {}): continue
            v = sum(setor_data[func][setor][i] for i in idx_f)
            q = sum(qtd_data.get(func,[0]*n)[i] for i in idx_f)
            if v > 0:
                ultima = None
                for i in reversed(idx_f):
                    if setor_data[func][setor][i] > 0:
                        ultima = dates[i]
                        break
                rows_tab.append({
                    'Funcionario': func, 'Setor': setor,
                    'Qtd Vendas': int(q),
                    'Valor (R$)': round(v, 2),
                    'Ticket Medio': round(v/q, 2) if q else 0,
                    '% da Receita': round(v/total_val*100, 1) if total_val else 0,
                    'Ultima Entrada': ultima.date() if ultima else None,
                })
    if rows_tab:
        df_tab = pd.DataFrame(rows_tab).sort_values(
            ['Valor (R$)'], ascending=False)
        st.dataframe(
            df_tab,
            hide_index=True,
            height=440,
            column_config={
                'Funcionario':   st.column_config.TextColumn('Funcionario',    width=130),
                'Setor':         st.column_config.TextColumn('Setor',          width=200),
                'Qtd Vendas':    st.column_config.NumberColumn('Qtd',          format="%d",      width=90),
                'Valor (R$)':    st.column_config.NumberColumn('Valor',        format="R$ %.2f", width=140),
                'Ticket Medio':  st.column_config.NumberColumn('Ticket',       format="R$ %.2f", width=130),
                '% da Receita':  st.column_config.ProgressColumn('% Receita',  format="%.1f%%",  min_value=0, max_value=100, width=130),
                'Ultima Entrada': st.column_config.DateColumn('Ultima Entrada', format="DD/MM/YYYY", width=130),
            }
        )
        c_dl1, c_dl2, _ = st.columns([1, 1, 4])
        csv = df_tab.to_csv(index=False).encode('utf-8-sig')
        c_dl1.download_button("⬇ Baixar CSV", csv, "vendas.csv", "text/csv", use_container_width=True)

# ───────────────────────── FOOTER ───────────────────────────
st.markdown("""
<div class="footer">
  DASHBOARD DE VENDAS &nbsp;·&nbsp; v3.0 &nbsp;·&nbsp; Fonte: vendas.xlsx &nbsp;·&nbsp; 2026
</div>
""", unsafe_allow_html=True)
