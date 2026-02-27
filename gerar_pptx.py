import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json, os

# ── DADOS ──────────────────────────────────────────────────────────────────────
path_in = 'Bd_dadosprojecao.xlsx'
df = pd.read_excel(path_in, sheet_name='Planilha1', parse_dates=['DATA'])
df = df.dropna(subset=['DATA'])
df['MES'] = df['DATA'].dt.to_period('M')

jan_real    = df[df['MES'] == pd.Period('2026-01', 'M')]['FATURADO'].sum()
fev_parcial = df[df['MES'] == pd.Period('2026-02', 'M')]['FATURADO'].sum()
dias_fev_fat = df[(df['MES'] == pd.Period('2026-02', 'M')) & (df['FATURADO'] > 0)]['DATA'].nunique()
media_dia_fev = fev_parcial / dias_fev_fat
media_dia_jan = jan_real / 31
media_diaria  = (media_dia_jan + media_dia_fev) / 2

meses_pt = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
meses_full = ['Janeiro','Fevereiro','Marco','Abril','Maio','Junho',
              'Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
dias_mes = [31,28,31,30,31,30,31,31,30,31,30,31]
fator    = [1.05,0.95,1.00,0.98,1.02,0.97,0.96,1.00,1.03,1.05,1.08,1.10]

rows = []
for m in range(1, 13):
    if m == 1:
        real=jan_real; proj=jan_real; status='Realizado'
    elif m == 2:
        real=fev_parcial; proj=media_dia_fev*28; status='Parcial'
    else:
        real=None; proj=media_diaria*dias_mes[m-1]*fator[m-1]; status='Projetado'
    rows.append({'Mes': meses_pt[m-1], 'MesFull': meses_full[m-1], 'M': m,
                 'Real': real, 'Proj': proj, 'Status': status})

proj_df    = pd.DataFrame(rows)
total_proj = proj_df['Proj'].sum()
total_real = proj_df['Real'].sum()
media_m    = proj_df['Proj'].mean()
trim_vals  = [proj_df['Proj'][:3].sum(), proj_df['Proj'][3:6].sum(),
              proj_df['Proj'][6:9].sum(), proj_df['Proj'][9:12].sum()]
trim_labels = ['T1\nJan-Mar', 'T2\nAbr-Jun', 'T3\nJul-Set', 'T4\nOut-Dez']

# paleta Midnight Executive
C1 = '#1E2761'   # navy escuro
C2 = '#3A5BA0'   # azul medio
C3 = '#CADCFC'   # ice azul
C4 = '#F0C030'   # ouro/acento
C5 = '#FFFFFF'   # branco
C6 = '#E8EDF8'   # fundo slide

cores_status = {'Realizado': '#2E86AB', 'Parcial': '#F6AE2D', 'Projetado': C3}
cores_bar    = [cores_status[s] for s in proj_df['Status']]

def save_fig(fig, name):
    fig.savefig(name, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    return name

# ── GRAFICO 1: barras mensais ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 5))
fig.patch.set_facecolor(C6)
ax.set_facecolor(C6)
bars = ax.bar(proj_df['Mes'], proj_df['Proj']/1000, color=cores_bar,
              edgecolor=C5, linewidth=0.5, width=0.7)
ax.axhline(media_m/1000, color='#E63946', linestyle='--', linewidth=1.5,
           label=f'Media mensal: R${media_m/1000:.0f}k')
ax.set_ylabel('R$ Mil', fontsize=11, color=C1)
ax.tick_params(axis='x', labelsize=11, colors=C1)
ax.tick_params(axis='y', colors=C1)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'R${x:.0f}k'))
for bar, val in zip(bars, proj_df['Proj']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+4,
            f'R${val/1000:.0f}k', ha='center', va='bottom', fontsize=9, fontweight='bold', color=C1)
patches = [mpatches.Patch(color=cores_status[k], label=k) for k in cores_status]
patches.append(plt.Line2D([0],[0], color='#E63946', linestyle='--', label=f'Media: R${media_m/1000:.0f}k'))
ax.legend(handles=patches, fontsize=9, loc='upper left', framealpha=0.6)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(C3); ax.spines['bottom'].set_color(C3)
fig.tight_layout()
save_fig(fig, 'pptx_g1_barras.png')

# ── GRAFICO 2: acumulado ───────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 5))
fig.patch.set_facecolor(C6)
ax.set_facecolor(C6)
acum = proj_df['Proj'].cumsum().values
ax.fill_between(range(12), acum/1000, alpha=0.18, color=C2)
ax.plot(range(12), acum/1000, marker='o', color=C4, linewidth=2.5,
        markersize=8, markerfacecolor=C4, markeredgecolor=C1, markeredgewidth=1.5)
ax.set_xticks(range(12)); ax.set_xticklabels(proj_df['Mes'], fontsize=11, color=C1)
ax.tick_params(axis='y', colors=C1)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'R${x:.0f}k'))
ax.set_ylabel('R$ Mil', fontsize=11, color=C1)
for x, y in zip(range(12), acum/1000):
    ax.annotate(f'R${y:.0f}k', (x, y), textcoords='offset points', xytext=(0, 9),
                ha='center', fontsize=8, color=C1, fontweight='bold')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(C3); ax.spines['bottom'].set_color(C3)
fig.tight_layout()
save_fig(fig, 'pptx_g2_acumulado.png')

# ── GRAFICO 3: trimestral ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5.5))
fig.patch.set_facecolor(C6)
ax.set_facecolor(C6)
cores_trim = [C1, C2, C3, C4]
bars2 = ax.bar(trim_labels, [v/1000 for v in trim_vals], color=cores_trim,
               edgecolor=C5, linewidth=0.6, width=0.55)
ax.set_ylabel('R$ Mil', fontsize=11, color=C1)
ax.tick_params(colors=C1, labelsize=11)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'R${x:.0f}k'))
for bar, val in zip(bars2, trim_vals):
    pct = val / total_proj * 100
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+8,
            f'R${val/1000:.0f}k\n({pct:.1f}%)', ha='center', va='bottom',
            fontsize=9.5, fontweight='bold', color=C1)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'pptx_g3_trimestral.png')

# ── GRAFICO 4: diario ─────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 4.5))
fig.patch.set_facecolor(C6)
ax.set_facecolor(C6)
df_real = df[(df['DATA'] <= pd.Timestamp('2026-02-16')) & (df['FATURADO'] > 0)].copy().reset_index(drop=True)
ax.bar(range(len(df_real)), df_real['FATURADO'].values/1000, color=C2, width=0.85, alpha=0.85)
mm7 = df_real['FATURADO'].rolling(7).mean().values
ax.plot(range(len(df_real)), mm7/1000, color=C4, linewidth=2, label='Media movel 7 dias')
ax.set_ylabel('R$ Mil', fontsize=11, color=C1)
ax.tick_params(colors=C1); ax.set_xticks([])
ax.legend(fontsize=10, framealpha=0.6)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
fig.tight_layout()
save_fig(fig, 'pptx_g4_diario.png')

print('Graficos gerados.')

# ── SPEC JSON PARA O DECK ──────────────────────────────────────────────────────
W, H = 13.333, 7.5

def title_bar(text, sub=None, bg=C1, fg=C5, y=0.28, h=1.1):
    elems = [
        {'type':'shape','shape':'rectangle','x':0,'y':0,'w':W,'h':H,'fill':C6,'line':C6},
        {'type':'shape','shape':'rectangle','x':0,'y':0,'w':0.12,'h':H,'fill':C4,'line':C4},
        {'type':'shape','shape':'rectangle','x':0,'y':y,'w':W,'h':h,'fill':bg,'line':bg},
        {'type':'text','text':text,'x':0.35,'y':y+0.08,'w':W-0.5,'h':h-0.15,
         'font_size':28,'color':fg,'bold':True,'align':'left'},
    ]
    if sub:
        elems.append({'type':'text','text':sub,'x':0.35,'y':y+h-0.02,'w':W-0.5,'h':0.4,
                      'font_size':13,'color':C2,'bold':False,'align':'left'})
    return elems

def kpi_box(x, y, w, h, label, value, bg=C1, fg=C5, vfg=C4):
    return [
        {'type':'shape','shape':'rounded_rectangle','x':x,'y':y,'w':w,'h':h,'fill':bg,'line':bg},
        {'type':'text','text':label,'x':x+0.1,'y':y+0.1,'w':w-0.2,'h':0.5,
         'font_size':11,'color':fg,'bold':False,'align':'center'},
        {'type':'text','text':value,'x':x+0.1,'y':y+0.52,'w':w-0.2,'h':h-0.65,
         'font_size':20,'color':vfg,'bold':True,'align':'center'},
    ]

slides = []

# ── SLIDE 1: CAPA ──────────────────────────────────────────────────────────────
slides.append({'background': C1, 'elements': [
    {'type':'shape','shape':'rectangle','x':0,'y':0,'w':0.18,'h':H,'fill':C4,'line':C4},
    {'type':'shape','shape':'rectangle','x':0,'y':5.8,'w':W,'h':1.7,'fill':C2,'line':C2},
    {'type':'text','text':'RELATORIO DE PROJECAO','x':0.4,'y':1.4,'w':W-0.6,'h':1.1,
     'font_size':42,'color':C5,'bold':True,'align':'left'},
    {'type':'text','text':'FATURAMENTO 2026','x':0.4,'y':2.5,'w':W-0.6,'h':0.9,
     'font_size':38,'color':C4,'bold':True,'align':'left'},
    {'type':'text','text':'Analise de desempenho e projecao anual com base nos dados realizados de Jan-Fev/2026',
     'x':0.4,'y':3.55,'w':11,'h':0.7,'font_size':15,'color':C3,'bold':False,'align':'left'},
    {'type':'text','text':'Elaborado em 19/02/2026','x':0.4,'y':6.0,'w':8,'h':0.45,
     'font_size':12,'color':C5,'bold':False,'align':'left'},
]})

# ── SLIDE 2: KPIs ──────────────────────────────────────────────────────────────
kpi_elems = [
    {'type':'shape','shape':'rectangle','x':0,'y':0,'w':W,'h':H,'fill':C6,'line':C6},
    {'type':'shape','shape':'rectangle','x':0,'y':0,'w':0.12,'h':H,'fill':C4,'line':C4},
    {'type':'shape','shape':'rectangle','x':0,'y':0.28,'w':W,'h':1.05,'fill':C1,'line':C1},
    {'type':'text','text':'INDICADORES CHAVE','x':0.35,'y':0.35,'w':W-0.5,'h':0.88,
     'font_size':28,'color':C5,'bold':True,'align':'left'},
]
kpis_data = [
    (0.35, 1.65, 2.9, 1.7, 'Total Realizado\n(Jan-Fev)', f'R$ {total_real/1000:.0f}k'),
    (3.45, 1.65, 2.9, 1.7, 'Projecao\nAnual 2026', f'R$ {total_proj/1000:.0f}k'),
    (6.55, 1.65, 2.9, 1.7, 'Media Mensal\nProjetada', f'R$ {media_m/1000:.0f}k'),
    (9.65, 1.65, 2.9, 1.7, 'Meses\nProjetados', '10 meses'),
]
for kd in kpis_data:
    kpi_elems += kpi_box(*kd)

kpi_elems += [
    {'type':'shape','shape':'rectangle','x':0.35,'y':3.6,'w':12.6,'h':0.06,'fill':C3,'line':C3},
    {'type':'text','text':'Crescimento projetado nos ultimos 4 meses do ano com media diaria de '
     f'R$ {media_diaria:,.0f} | Dados reais ate 16/02/2026',
     'x':0.35,'y':3.8,'w':12.3,'h':0.55,'font_size':12,'color':C2,'bold':False,'align':'left'},
]
slides.append({'background': C6, 'elements': kpi_elems})

# ── SLIDE 3: projecao mensal ───────────────────────────────────────────────────
s3 = title_bar('PROJECAO MENSAL DE FATURAMENTO',
               'Combinacao de dados realizados (Jan-Fev) e projecao com fator sazonal (Mar-Dez)')
s3 += [{'type':'image','path':'pptx_g1_barras.png','x':0.35,'y':1.5,'w':12.6,'h':5.6}]
slides.append({'background': C6, 'elements': s3})

# ── SLIDE 4: acumulado ────────────────────────────────────────────────────────
s4 = title_bar('FATURAMENTO ACUMULADO 2026',
               f'Projecao de encerramento do ano: R$ {total_proj/1000:.0f}k')
s4 += [{'type':'image','path':'pptx_g2_acumulado.png','x':0.35,'y':1.5,'w':12.6,'h':5.6}]
slides.append({'background': C6, 'elements': s4})

# ── SLIDE 5: trimestral ───────────────────────────────────────────────────────
s5 = title_bar('DISTRIBUICAO TRIMESTRAL', 'Participacao de cada trimestre na projecao anual')
s5 += [{'type':'image','path':'pptx_g3_trimestral.png','x':2.5,'y':1.5,'w':8.3,'h':5.7}]
trim_x = [0.35, 3.55, 6.75, 9.95]
trim_pct = [v/total_proj*100 for v in trim_vals]
trim_nomes = ['T1\nJan-Mar','T2\nAbr-Jun','T3\nJul-Set','T4\nOut-Dez']
for i,(tx,tv,tp,tn) in enumerate(zip(trim_x, trim_vals, trim_pct, trim_nomes)):
    pass  # grafico ja mostra os valores
slides.append({'background': C6, 'elements': s5})

# ── SLIDE 6: historico diario ─────────────────────────────────────────────────
s6 = title_bar('HISTORICO DE FATURAMENTO DIARIO',
               'Dados realizados de Janeiro a 16 de Fevereiro de 2026')
s6 += [{'type':'image','path':'pptx_g4_diario.png','x':0.35,'y':1.45,'w':12.6,'h':5.65}]
slides.append({'background': C6, 'elements': s6})

# ── SLIDE 7: tabela resumo ─────────────────────────────────────────────────────
s7 = title_bar('TABELA DE PROJECAO MENSAL DETALHADA')
col_x = [0.3, 2.1, 4.4, 6.9, 9.4, 11.5]
col_w = [1.7, 2.2, 2.4, 2.4, 2.0, 1.6]
hdrs  = ['Mes', 'Status', 'Real (R$)', 'Projecao (R$)', 'Acumulado (R$)', 'vs Media']
for cx, cw, hdr in zip(col_x, col_w, hdrs):
    s7.append({'type':'shape','shape':'rectangle','x':cx,'y':1.52,'w':cw,'h':0.42,'fill':C1,'line':C1})
    s7.append({'type':'text','text':hdr,'x':cx+0.05,'y':1.55,'w':cw-0.1,'h':0.36,
               'font_size':10,'color':C5,'bold':True,'align':'center'})

acum3 = 0
for i, row in proj_df.iterrows():
    ry = 2.02 + i * 0.38
    acum3 += row['Proj']
    vs = (row['Proj']/media_m - 1)*100
    real_s = f'R$ {row["Real"]/1000:.0f}k' if row['Real'] is not None and not np.isnan(row['Real']) else '-'
    vals = [row['MesFull'], row['Status'],
            real_s, f'R$ {row["Proj"]/1000:.0f}k',
            f'R$ {acum3/1000:.0f}k', f'{vs:+.1f}%']
    bg_row = C6 if i % 2 == 0 else '#DDE4F0'
    for cx, cw, val in zip(col_x, col_w, vals):
        s7.append({'type':'shape','shape':'rectangle','x':cx,'y':ry,'w':cw,'h':0.36,'fill':bg_row,'line':C3})
        s7.append({'type':'text','text':str(val),'x':cx+0.05,'y':ry+0.03,'w':cw-0.1,'h':0.30,
                   'font_size':9,'color':C1,'bold':False,'align':'center'})

# total
ry_tot = 2.02 + 12 * 0.38
tot_vals = ['TOTAL ANUAL', '', '', f'R$ {total_proj/1000:.0f}k', f'R$ {total_proj/1000:.0f}k', '']
for cx, cw, val in zip(col_x, col_w, tot_vals):
    s7.append({'type':'shape','shape':'rectangle','x':cx,'y':ry_tot,'w':cw,'h':0.38,'fill':C1,'line':C1})
    s7.append({'type':'text','text':str(val),'x':cx+0.05,'y':ry_tot+0.04,'w':cw-0.1,'h':0.30,
               'font_size':10,'color':C4,'bold':True,'align':'center'})

slides.append({'background': C6, 'elements': s7})

# ── SLIDE 8: metodologia ──────────────────────────────────────────────────────
s8 = title_bar('METODOLOGIA E PREMISSAS')
met_items = [
    ('Dados Reais', f'Janeiro 2026: R$ {jan_real:,.2f}  |  Fevereiro 2026 (parcial ate 16/02): R$ {fev_parcial:,.2f}'),
    ('Media Diaria Base', f'R$ {media_diaria:,.2f}/dia  (media de Jan e Fev)'),
    ('Projecao Mensal', 'Media diaria base x Dias do mes x Fator sazonal do mes'),
    ('Fatores Sazonais', 'Mar/Abr/Jun/Jul: -1 a -4%  |  Mai/Set/Out: +2 a +5%  |  Nov/Dez: +8 a +10%'),
    ('Revisao', 'Recomendado atualizar mensalmente conforme novos dados sao realizados'),
]
for i, (titulo, detalhe) in enumerate(met_items):
    ry = 1.65 + i * 0.98
    s8 += [
        {'type':'shape','shape':'rounded_rectangle','x':0.35,'y':ry,'w':12.6,'h':0.82,'fill':C1,'line':C1},
        {'type':'text','text':titulo,'x':0.55,'y':ry+0.06,'w':3.2,'h':0.35,
         'font_size':12,'color':C4,'bold':True,'align':'left'},
        {'type':'text','text':detalhe,'x':3.8,'y':ry+0.06,'w':8.9,'h':0.7,
         'font_size':11,'color':C3,'bold':False,'align':'left'},
    ]
slides.append({'background': C6, 'elements': s8})

# ── SLIDE 9: ENCERRAMENTO ─────────────────────────────────────────────────────
slides.append({'background': C1, 'elements': [
    {'type':'shape','shape':'rectangle','x':0,'y':0,'w':0.18,'h':H,'fill':C4,'line':C4},
    {'type':'shape','shape':'rectangle','x':0,'y':3.2,'w':W,'h':1.2,'fill':C2,'line':C2},
    {'type':'text','text':'Projecao Total 2026','x':0.4,'y':1.5,'w':W-0.6,'h':0.9,
     'font_size':22,'color':C3,'bold':False,'align':'left'},
    {'type':'text','text':f'R$ {total_proj:,.2f}','x':0.4,'y':2.2,'w':W-0.6,'h':1.1,
     'font_size':52,'color':C4,'bold':True,'align':'left'},
    {'type':'text','text':f'Media Mensal: R$ {media_m:,.2f}   |   Media Diaria: R$ {media_diaria:,.2f}',
     'x':0.4,'y':3.35,'w':W-0.6,'h':0.7,'font_size':15,'color':C5,'bold':False,'align':'left'},
    {'type':'text','text':'Os valores projetados sao estimativas baseadas no historico de Jan-Fev/2026 com ajuste sazonal.',
     'x':0.4,'y':5.0,'w':W-0.6,'h':0.6,'font_size':12,'color':C3,'bold':False,'align':'left'},
    {'type':'text','text':'Relatorio gerado em 19/02/2026','x':0.4,'y':6.7,'w':8,'h':0.4,
     'font_size':11,'color':C3,'bold':False,'align':'left'},
]})

# ── LIMPAR # DAS CORES E SALVAR SPEC ─────────────────────────────────────────
import re

def strip_hash(obj):
    if isinstance(obj, dict):
        return {k: strip_hash(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [strip_hash(v) for v in obj]
    if isinstance(obj, str) and re.match(r'^#[0-9A-Fa-f]{6}$', obj):
        return obj[1:]
    return obj

spec = strip_hash({'width': W, 'height': H, 'slides': slides})
with open('pptx_spec.json', 'w', encoding='utf-8') as f:
    json.dump(spec, f, ensure_ascii=False, indent=2)
print('Spec salvo: pptx_spec.json')
