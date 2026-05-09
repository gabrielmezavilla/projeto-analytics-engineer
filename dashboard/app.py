"""
Dashboard de Analytics do Mercado de Trabalho Brasileiro (CAGED)

Arquitetura Analytics Engineer:
  ingest.py → clean.py → dbt (staging → intermediate → marts) → este dashboard

Execute com:
  streamlit run dashboard/app.py
"""

import subprocess
import sys
from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "data" / "processed" / "analytics.duckdb"
TRANSFORM_DIR = ROOT / "transform"

st.set_page_config(
    page_title="Analytics CAGED Brasil",
    page_icon="📊",
    layout="wide",
)


# ── Pipeline e dbt ───────────────────────────────────────────────────────────

@st.cache_data
def rodar_pipeline():
    """Roda ingestão + limpeza + dbt run na primeira execução."""
    sys.path.insert(0, str(ROOT / "pipeline"))
    from ingest import carregar_dados
    from clean import processar

    df_raw = carregar_dados()
    processar(df_raw)

    # Roda dbt run (cria os marts no DuckDB)
    resultado = subprocess.run(
        ["dbt", "run", "--profiles-dir", ".", "--project-dir", "."],
        cwd=TRANSFORM_DIR,
        capture_output=True,
        text=True,
    )
    if resultado.returncode != 0:
        st.error(f"Erro no dbt run:\n{resultado.stderr}")
        st.stop()


@st.cache_data
def carregar(schema: str, tabela: str) -> pd.DataFrame:
    con = duckdb.connect(str(DB_PATH), read_only=True)
    return con.execute(f"SELECT * FROM {schema}.{tabela}").fetchdf()


# Garante pipeline completo antes de renderizar
if not DB_PATH.exists():
    with st.spinner("Rodando pipeline dbt pela primeira vez..."):
        rodar_pipeline()

# Carrega os marts (entregáveis do Analytics Engineer)
visao_geral = carregar("marts", "mart_visao_geral")
estados      = carregar("marts", "mart_estados")
setores      = carregar("marts", "mart_setores")


# ── Sidebar — Filtros ────────────────────────────────────────────────────────

with st.sidebar:
    st.title("Filtros")

    anos_disp = sorted(visao_geral["ano"].unique())
    anos_sel = st.multiselect("Ano", anos_disp, default=anos_disp)

    regioes_disp = sorted(estados["regiao"].unique())
    regioes_sel = st.multiselect("Região", regioes_disp, default=regioes_disp)

    setores_disp = sorted(setores["setor"].unique())
    setores_sel = st.multiselect("Setor", setores_disp, default=setores_disp)

    st.divider()
    if st.button("🔄 Reprocessar dados"):
        st.cache_data.clear()
        rodar_pipeline()
        st.rerun()

    st.caption("Fonte: CAGED/MTE | Dados sintéticos para fins didáticos")


# Filtragem
vg_f  = visao_geral[visao_geral["ano"].isin(anos_sel)]
est_f = estados[estados["regiao"].isin(regioes_sel)]
set_f = setores[setores["ano"].isin(anos_sel) & setores["setor"].isin(setores_sel)]


# ── Header ───────────────────────────────────────────────────────────────────

st.title("📊 Analytics do Mercado de Trabalho Brasileiro")
st.markdown(
    "Dashboard alimentado por pipeline **dbt + DuckDB** "
    "sobre dados do **CAGED** (Cadastro Geral de Empregados e Desempregados)"
)
st.divider()


# ── KPIs ─────────────────────────────────────────────────────────────────────

col1, col2, col3, col4 = st.columns(4)

total_adm  = int(vg_f["total_admissoes"].sum())
total_des  = int(vg_f["total_desligamentos"].sum())
saldo      = int(vg_f["saldo_mensal"].sum())
salario    = vg_f["salario_medio"].mean()

col1.metric("Admissões",       f"{total_adm:,}".replace(",", "."))
col2.metric("Desligamentos",   f"{total_des:,}".replace(",", "."))
col3.metric("Saldo de Empregos", f"{saldo:,}".replace(",", "."), delta=f"{saldo:+,}".replace(",", "."))
col4.metric("Salário Médio",   f"R$ {salario:,.0f}".replace(",", "."))

st.divider()


# ── Evolução temporal ─────────────────────────────────────────────────────────

col_esq, col_dir = st.columns(2)

with col_esq:
    st.subheader("Saldo Mensal de Empregos")
    fig = px.bar(
        vg_f, x="ano_mes", y="saldo_mensal",
        color="saldo_mensal",
        color_continuous_scale=["#d73027", "#fee08b", "#1a9850"],
        labels={"ano_mes": "Mês", "saldo_mensal": "Saldo"},
    )
    fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with col_dir:
    st.subheader("Saldo Acumulado no Ano")
    fig2 = px.line(
        vg_f, x="ano_mes", y="saldo_acumulado_ano", color="ano",
        markers=True,
        labels={"ano_mes": "Mês", "saldo_acumulado_ano": "Saldo Acumulado", "ano": "Ano"},
    )
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)


# ── Análise por Estado ────────────────────────────────────────────────────────

st.subheader("Saldo por Estado")
col_mapa, col_rank = st.columns([2, 1])

with col_mapa:
    fig_mapa = px.choropleth(
        est_f,
        geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
        locations="uf",
        featureidkey="properties.sigla",
        color="saldo_total",
        color_continuous_scale=["#d73027", "#fee08b", "#1a9850"],
        hover_data=["regiao", "ranking_saldo", "classificacao_saldo"],
        labels={"saldo_total": "Saldo", "uf": "UF"},
        scope="south america",
    )
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_mapa, use_container_width=True)

with col_rank:
    top10 = est_f.nsmallest(10, "ranking_saldo")[["uf", "saldo_total", "classificacao_saldo"]]
    fig_rank = px.bar(
        top10, x="saldo_total", y="uf", orientation="h",
        color="classificacao_saldo",
        color_discrete_map={"Positivo": "#1a9850", "Negativo": "#d73027", "Neutro": "#fee08b"},
        labels={"saldo_total": "Saldo", "uf": "UF", "classificacao_saldo": ""},
        title="Top 10 Estados",
    )
    fig_rank.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_rank, use_container_width=True)


# ── Análise por Setor ─────────────────────────────────────────────────────────

st.subheader("Análise por Setor")
col_s1, col_s2 = st.columns(2)

# Totais por setor no período filtrado
setor_total = (
    set_f.groupby("setor")[["total_admissoes", "total_desligamentos", "saldo_total"]]
    .sum()
    .reset_index()
    .sort_values("saldo_total")
)

with col_s1:
    fig_setor = px.bar(
        setor_total, x="saldo_total", y="setor", orientation="h",
        color="saldo_total",
        color_continuous_scale=["#d73027", "#fee08b", "#1a9850"],
        labels={"saldo_total": "Saldo", "setor": "Setor"},
        title="Saldo Total por Setor",
    )
    fig_setor.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_setor, use_container_width=True)

with col_s2:
    fig_linha = px.line(
        set_f, x="ano_mes", y="saldo_total", color="setor",
        labels={"ano_mes": "Mês", "saldo_total": "Saldo", "setor": "Setor"},
        title="Evolução do Saldo por Setor",
    )
    fig_linha.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_linha, use_container_width=True)


# ── Tabela detalhada ──────────────────────────────────────────────────────────

with st.expander("Ver mart_visao_geral (dados completos)"):
    st.dataframe(
        vg_f.rename(columns={
            "ano_mes": "Mês", "ano": "Ano", "mes": "Mês Nº",
            "total_admissoes": "Admissões", "total_desligamentos": "Desligamentos",
            "saldo_mensal": "Saldo", "saldo_acumulado_ano": "Saldo Acum.",
            "variacao_pct_mes_anterior": "Var. % Mês ant.",
            "salario_medio": "Salário Médio",
        }),
        use_container_width=True,
        hide_index=True,
    )
