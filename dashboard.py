import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

EXCEL_PATH = r"D:\Users\Claudio\OneDrive\Nova pasta\Nova pasta\bd_dados\bd dados.xlsx"

st.set_page_config(page_title="Relatório Financeiro", layout="wide", page_icon="📊")

@st.cache_data
def load_data():
    df_raw = pd.read_excel(EXCEL_PATH, sheet_name="Planilha1")
    date_cols = [c for c in df_raw.columns if hasattr(c, "year") and 2021 <= c.year <= 2026]
    df = df_raw[["Conta", "SubConta"] + date_cols].copy()
    df["Conta"] = df["Conta"].astype(str).str.strip()
    df["SubConta"] = df["SubConta"].astype(str).str.strip()
    df_long = df.melt(id_vars=["Conta", "SubConta"], value_vars=date_cols, var_name="Data", value_name="Valor")
    df_long["Data"] = pd.to_datetime(df_long["Data"])
    df_long["Ano"] = df_long["Data"].dt.year
    df_long["Mes"] = df_long["Data"].dt.month
    df_long["AnoMes"] = df_long["Data"].dt.to_period("M").astype(str)
    df_long["Valor"] = pd.to_numeric(df_long["Valor"], errors="coerce").fillna(0)
    return df_long

df = load_data()

contas_totais = ["Total Entradas", "Total Saídas", "TOTAL"]
contas_venda = ["VENDA DE MERCADORIAS", "Total Vendas"]

st.markdown(
    """
    <style>
    .metric-card {background:#1e1e2f;border-radius:12px;padding:20px 24px;margin-bottom:8px;}
    .metric-label {color:#aab2c8;font-size:13px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;}
    .metric-value {color:#f0f4ff;font-size:28px;font-weight:700;margin-top:4px;}
    .metric-delta-pos {color:#4ade80;font-size:13px;}
    .metric-delta-neg {color:#f87171;font-size:13px;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Relatório Financeiro")
st.caption("Fonte: bd dados.xlsx")

MESES_NOMES = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}

with st.sidebar:
    st.header("Filtros")
    anos_disponiveis = sorted(df["Ano"].unique())
    anos = st.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)
    meses_disponiveis = sorted(df["Mes"].unique())
    meses_opcoes = [MESES_NOMES[m] for m in meses_disponiveis]
    meses_sel_nomes = st.multiselect("Mês", meses_opcoes, default=meses_opcoes)
    meses_sel = [k for k, v in MESES_NOMES.items() if v in meses_sel_nomes]
    contas_disponiveis = sorted(df["Conta"].unique())
    contas_sel = st.multiselect("Conta", contas_disponiveis, default=contas_disponiveis)

df_f = df[df["Ano"].isin(anos) & df["Mes"].isin(meses_sel) & df["Conta"].isin(contas_sel)]

def get_total(conta_list):
    v = df_f[df_f["Conta"].isin(conta_list)]["Valor"].sum()
    return v

total_entradas = get_total(["Total Entradas"])
total_saidas = get_total(["Total Saídas"])
resultado = total_entradas - total_saidas

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Entradas", f"R$ {total_entradas:,.2f}")
with col2:
    st.metric("Total Saídas", f"R$ {total_saidas:,.2f}")
with col3:
    delta_color = "normal" if resultado >= 0 else "inverse"
    st.metric("Resultado (Entradas - Saídas)", f"R$ {resultado:,.2f}", delta=f"R$ {resultado:,.2f}", delta_color=delta_color)

st.divider()

VENDEDORES = ["ANDERSON", "ANDREIA", "CLAUDIO", "CLAUDEMIR", "CRISTIANE", "JHOICE", "LUCIMARA", "LUIZ FERNANDO", "SEBASTIAO"]

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Evolução Mensal", "Por Conta", "Detalhamento", "Vendedores", "Dados Brutos"])

with tab1:
    st.subheader("Entradas vs Saídas por Mês")
    df_es = df_f[df_f["Conta"].isin(["Total Entradas", "Total Saídas"])]
    df_es_grp = df_es.groupby(["AnoMes", "Conta"])["Valor"].sum().reset_index()
    if not df_es_grp.empty:
        fig = px.line(
            df_es_grp.sort_values("AnoMes"),
            x="AnoMes", y="Valor", color="Conta",
            markers=True,
            labels={"AnoMes": "Mês", "Valor": "R$", "Conta": ""},
            color_discrete_map={"Total Entradas": "#4ade80", "Total Saídas": "#f87171"},
        )
        fig.update_layout(xaxis_tickangle=-45, hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhum dado de Total Entradas / Total Saídas no filtro selecionado.")

    st.subheader("Resultado Líquido por Mês")
    df_ent = df_f[df_f["Conta"] == "Total Entradas"].groupby("AnoMes")["Valor"].sum()
    df_sai = df_f[df_f["Conta"] == "Total Saídas"].groupby("AnoMes")["Valor"].sum()
    df_res = (df_ent - df_sai).reset_index()
    df_res.columns = ["AnoMes", "Resultado"]
    df_res = df_res.sort_values("AnoMes")
    if not df_res.empty:
        fig2 = px.bar(
            df_res, x="AnoMes", y="Resultado",
            color="Resultado",
            color_continuous_scale=["#f87171", "#facc15", "#4ade80"],
            labels={"AnoMes": "Mês", "Resultado": "R$"},
        )
        fig2.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Total por Conta")
    df_conta = df_f.groupby("Conta")["Valor"].sum().reset_index().sort_values("Valor", ascending=False)
    df_conta = df_conta[df_conta["Valor"] != 0]
    if not df_conta.empty:
        fig3 = px.bar(
            df_conta, x="Conta", y="Valor",
            labels={"Conta": "", "Valor": "R$"},
            color="Valor",
            color_continuous_scale=["#f87171", "#facc15", "#4ade80"],
        )
        fig3.update_layout(xaxis_tickangle=-40, coloraxis_showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Composição por Conta")
    df_pos = df_conta[df_conta["Valor"] > 0]
    if not df_pos.empty:
        fig4 = px.pie(df_pos, names="Conta", values="Valor", hole=0.4)
        fig4.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig4, use_container_width=True)

with tab3:
    st.subheader("Detalhamento por SubConta")
    conta_detalhe = st.selectbox("Selecione a Conta", sorted(df_f["Conta"].unique()))
    df_sub = df_f[df_f["Conta"] == conta_detalhe]
    df_sub_grp = df_sub.groupby(["AnoMes", "SubConta"])["Valor"].sum().reset_index()
    df_sub_grp = df_sub_grp[df_sub_grp["Valor"] != 0].sort_values("AnoMes")
    if not df_sub_grp.empty:
        fig5 = px.line(
            df_sub_grp, x="AnoMes", y="Valor", color="SubConta",
            markers=True,
            labels={"AnoMes": "Mês", "Valor": "R$", "SubConta": ""},
        )
        fig5.update_layout(xaxis_tickangle=-45, hovermode="x unified")
        st.plotly_chart(fig5, use_container_width=True)

        st.subheader("Total por SubConta")
        df_sub_total = df_sub.groupby("SubConta")["Valor"].sum().reset_index().sort_values("Valor", ascending=False)
        df_sub_total = df_sub_total[df_sub_total["Valor"] != 0]
        fig6 = px.bar(df_sub_total, x="SubConta", y="Valor", labels={"SubConta": "", "Valor": "R$"})
        fig6.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig6, use_container_width=True)
    else:
        st.info("Nenhum valor diferente de zero para esta conta no período selecionado.")

with tab4:
    st.subheader("Vendas por Vendedor")

    vendedor_sel = st.selectbox("Selecione o Vendedor", VENDEDORES, index=VENDEDORES.index("LUIZ FERNANDO"))

    df_vend_base = df[df["Ano"].isin(anos) & df["Mes"].isin(meses_sel) & (df["Conta"] == vendedor_sel)]
    df_vend = df_vend_base[~df_vend_base["SubConta"].isin(["Qtd. vendas por funcionário", "0"])].copy()
    df_vend = df_vend[df_vend["Valor"] != 0]

    total_vend = df_vend["Valor"].sum()
    total_qtd = df_vend_base[df_vend_base["SubConta"] == "Qtd. vendas por funcionário"]["Valor"].sum()

    kc1, kc2 = st.columns(2)
    with kc1:
        st.metric("Total Vendido (R$)", f"R$ {total_vend:,.2f}")
    with kc2:
        st.metric("Qtd. Vendas", f"{int(total_qtd):,}")

    st.markdown("---")

    st.subheader("Comparativo entre Vendedores")
    rows = []
    for v in VENDEDORES:
        df_v = df[df["Ano"].isin(anos) & df["Mes"].isin(meses_sel) & (df["Conta"] == v)]
        df_v = df_v[~df_v["SubConta"].isin(["Qtd. vendas por funcionário", "0"])]
        total = df_v[df_v["Valor"] != 0]["Valor"].sum()
        qtd = df[df["Ano"].isin(anos) & df["Mes"].isin(meses_sel) & (df["Conta"] == v) & (df["SubConta"] == "Qtd. vendas por funcionário")]["Valor"].sum()
        rows.append({"Vendedor": v, "Total (R$)": total, "Qtd. Vendas": int(qtd)})
    df_comp = pd.DataFrame(rows).sort_values("Total (R$)", ascending=False)
    df_comp = df_comp[df_comp["Total (R$)"] > 0]
    if not df_comp.empty:
        fig_comp = px.bar(
            df_comp, x="Vendedor", y="Total (R$)",
            color="Total (R$)",
            color_continuous_scale=["#60a5fa", "#818cf8", "#a78bfa"],
            text="Total (R$)",
        )
        fig_comp.update_traces(texttemplate="R$ %{text:,.0f}", textposition="outside")
        fig_comp.update_layout(coloraxis_showscale=False, uniformtext_minsize=8)
        st.plotly_chart(fig_comp, use_container_width=True)

    st.subheader("Comparativo de Vendedores por Mês")
    rows_mes = []
    for v in VENDEDORES:
        df_v = df[df["Ano"].isin(anos) & df["Mes"].isin(meses_sel) & (df["Conta"] == v)]
        df_v = df_v[~df_v["SubConta"].isin(["Qtd. vendas por funcionário", "0"])]
        df_v = df_v[df_v["Valor"] != 0]
        df_v_grp = df_v.groupby("AnoMes")["Valor"].sum().reset_index()
        df_v_grp["Vendedor"] = v
        rows_mes.append(df_v_grp)
    df_comp_mes = pd.concat(rows_mes, ignore_index=True) if rows_mes else pd.DataFrame()
    df_comp_mes = df_comp_mes[df_comp_mes["Valor"] > 0].sort_values("AnoMes")

    tipo_grafico = st.radio("Tipo de visualização", ["Linha", "Barra Agrupada", "Barra Empilhada"], horizontal=True)

    if not df_comp_mes.empty:
        if tipo_grafico == "Linha":
            fig_mes = px.line(
                df_comp_mes, x="AnoMes", y="Valor", color="Vendedor",
                markers=True,
                labels={"AnoMes": "Mês", "Valor": "R$", "Vendedor": ""},
            )
            fig_mes.update_layout(xaxis_tickangle=-45, hovermode="x unified")
        elif tipo_grafico == "Barra Agrupada":
            fig_mes = px.bar(
                df_comp_mes, x="AnoMes", y="Valor", color="Vendedor",
                barmode="group",
                labels={"AnoMes": "Mês", "Valor": "R$", "Vendedor": ""},
            )
            fig_mes.update_layout(xaxis_tickangle=-45, hovermode="x unified")
        else:
            fig_mes = px.bar(
                df_comp_mes, x="AnoMes", y="Valor", color="Vendedor",
                barmode="stack",
                labels={"AnoMes": "Mês", "Valor": "R$", "Vendedor": ""},
            )
            fig_mes.update_layout(xaxis_tickangle=-45, hovermode="x unified")
        st.plotly_chart(fig_mes, use_container_width=True)

        st.subheader("Ranking Mensal por Vendedor")
        df_pivot = df_comp_mes.pivot_table(index="AnoMes", columns="Vendedor", values="Valor", aggfunc="sum").fillna(0)
        df_pivot.columns.name = None
        df_pivot = df_pivot.reset_index().rename(columns={"AnoMes": "Mês"})
        st.dataframe(
            df_pivot.style.format({c: "R$ {:,.2f}" for c in df_pivot.columns if c != "Mês"}),
            use_container_width=True,
            height=400,
        )

    st.markdown("---")
    st.subheader(f"Detalhes — {vendedor_sel}")

    st.markdown("##### Evolução Mensal")
    df_vend_mes = df_vend.groupby("AnoMes")["Valor"].sum().reset_index().sort_values("AnoMes")
    if not df_vend_mes.empty:
        fig_v1 = px.bar(
            df_vend_mes, x="AnoMes", y="Valor",
            labels={"AnoMes": "Mês", "Valor": "R$"},
            color="Valor",
            color_continuous_scale=["#60a5fa", "#818cf8", "#a78bfa"],
        )
        fig_v1.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)
        st.plotly_chart(fig_v1, use_container_width=True)

    st.markdown("##### Vendas por Categoria de Produto")
    df_vend_cat = df_vend.groupby("SubConta")["Valor"].sum().reset_index().sort_values("Valor", ascending=False)
    df_vend_cat["SubConta"] = df_vend_cat["SubConta"].str.strip().str.replace(r"\s*\*+", "", regex=True).str.strip()
    df_vend_cat = df_vend_cat[df_vend_cat["Valor"] > 0]
    if not df_vend_cat.empty:
        col_a, col_b = st.columns(2)
        with col_a:
            fig_v2 = px.bar(
                df_vend_cat, x="Valor", y="SubConta", orientation="h",
                labels={"SubConta": "", "Valor": "R$"},
                color="Valor",
                color_continuous_scale=["#60a5fa", "#a78bfa"],
            )
            fig_v2.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
            st.plotly_chart(fig_v2, use_container_width=True)
        with col_b:
            fig_v3 = px.pie(df_vend_cat, names="SubConta", values="Valor", hole=0.4)
            fig_v3.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig_v3, use_container_width=True)

    st.markdown("##### Evolução por Categoria ao Longo do Tempo")
    df_vend_ev = df_vend.groupby(["AnoMes", "SubConta"])["Valor"].sum().reset_index()
    df_vend_ev["SubConta"] = df_vend_ev["SubConta"].str.strip().str.replace(r"\s*\*+", "", regex=True).str.strip()
    df_vend_ev = df_vend_ev[df_vend_ev["Valor"] > 0].sort_values("AnoMes")
    if not df_vend_ev.empty:
        fig_v4 = px.line(
            df_vend_ev, x="AnoMes", y="Valor", color="SubConta",
            markers=True,
            labels={"AnoMes": "Mês", "Valor": "R$", "SubConta": "Categoria"},
        )
        fig_v4.update_layout(xaxis_tickangle=-45, hovermode="x unified")
        st.plotly_chart(fig_v4, use_container_width=True)

    if df_vend.empty:
        st.info("Nenhum dado para este vendedor no período selecionado.")

with tab5:
    st.subheader("Dados Brutos")
    df_show = df_f[df_f["Valor"] != 0][["Conta", "SubConta", "AnoMes", "Valor"]].sort_values(["Conta", "AnoMes"])
    st.dataframe(df_show, use_container_width=True, height=500)
    csv = df_show.to_csv(index=False).encode("utf-8")
    st.download_button("Baixar CSV", csv, "dados_financeiros.csv", "text/csv")
