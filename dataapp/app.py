from pathlib import Path
import streamlit as st
import pandas as pd


# ======================================================
# Configuração da página
# ======================================================

st.set_page_config(
    page_title="Otimização de Ações Promocionais",
    layout="wide"
)

st.title("📊 Otimização de Ações Promocionais")
st.markdown("""
Este Data App apoia a tomada de decisão estratégica,
identificando **onde promoções geram maior retorno em vendas**
por **loja, departamento e tipo de loja**.
""")


# ======================================================
# Caminhos (compatível com Streamlit Cloud)
# ======================================================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


# ======================================================
# Funções auxiliares
# ======================================================

def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Converte colunas MultiIndex em colunas simples"""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join([str(c) for c in col if c not in ["", None]])
            for col in df.columns
        ]
    df.columns = [c.lower() for c in df.columns]
    return df


def find_column(cols, keyword):
    """Encontra coluna pelo significado semântico"""
    matches = [c for c in cols if keyword in c]
    if not matches:
        raise ValueError(f"Coluna com '{keyword}' não encontrada")
    return matches[0]


# ======================================================
# Carregamento dos dados
# ======================================================

@st.cache_data
def load_data():
    # PRIORIDADE LOJA × DEPARTAMENTO
    prioridade = pd.read_parquet(
        DATA_DIR / "store_dept_priority.parquet"
    )

    prioridade = prioridade.rename(columns={
        "Store": "loja",
        "Dept": "departamento",
        "avg_sales": "venda_media",
        "total_sales": "venda_total",
        "avg_markdown": "desconto_medio",
        "priority_score": "score_prioridade"
    })

    # EFICIÊNCIA POR TIPO DE LOJA
    promo_tipo = pd.read_parquet(
        DATA_DIR / "promo_efficiency_by_type.parquet"
    )
    promo_tipo = flatten_columns(promo_tipo)

    col_tipo = find_column(promo_tipo.columns, "type")
    col_eff = find_column(promo_tipo.columns, "promo_efficiency")
    col_lift = find_column(promo_tipo.columns, "lift")

    promo_tipo = promo_tipo.rename(columns={
        col_tipo: "tipo_loja",
        col_eff: "eficiencia_promocional",
        col_lift: "uplift"
    })

    # EFICIÊNCIA POR DEPARTAMENTO
    promo_depto = pd.read_parquet(
        DATA_DIR / "promo_efficiency_by_dept.parquet"
    )
    promo_depto = flatten_columns(promo_depto)

    col_dept = find_column(promo_depto.columns, "dept")
    col_eff_d = find_column(promo_depto.columns, "promo_efficiency")
    col_lift_d = find_column(promo_depto.columns, "lift")

    promo_depto = promo_depto.rename(columns={
        col_dept: "departamento",
        col_eff_d: "eficiencia_promocional",
        col_lift_d: "uplift"
    })

    return prioridade, promo_tipo, promo_depto


# ======================================================
# Execução
# ======================================================

prioridade, promo_tipo, promo_depto = load_data()


# ======================================================
# Filtros laterais
# ======================================================

st.sidebar.header("🔎 Filtros")

with st.sidebar.expander("🏬 Tipo de Loja", expanded=True):
    tipos = sorted(promo_tipo["tipo_loja"].dropna().unique())
    tipo_sel = st.multiselect(
        "Selecione os tipos",
        tipos,
        default=tipos
    )

with st.sidebar.expander("📦 Departamento", expanded=False):
    departamentos = sorted(prioridade["departamento"].unique())
    dept_sel = st.multiselect(
        "Selecione os departamentos",
        departamentos,
        default=departamentos
    )


# ======================================================
# Aplicação dos filtros
# ======================================================

prioridade_f = prioridade[
    prioridade["departamento"].isin(dept_sel)
]

promo_tipo_f = promo_tipo[
    promo_tipo["tipo_loja"].isin(tipo_sel)
]


# ======================================================
# KPIs
# ======================================================

st.subheader("📌 Indicadores Gerais")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Venda Média",
        f"${prioridade_f['venda_media'].mean():,.0f}"
    )

with col2:
    st.metric(
        "Desconto Médio",
        f"${prioridade_f['desconto_medio'].mean():,.0f}"
    )

with col3:
    st.metric(
        "Score Médio de Prioridade",
        f"{prioridade_f['score_prioridade'].mean():.2f}"
    )


# ======================================================
# Ranking Prescritivo
# ======================================================

st.subheader("🏆 Ranking de Prioridade (Loja × Departamento)")

st.dataframe(
    prioridade_f
    .sort_values("score_prioridade", ascending=False)
    .head(20),
    use_container_width=True
)


# ======================================================
# Gráficos
# ======================================================

st.subheader("📈 Eficiência Promocional por Tipo de Loja")

st.bar_chart(
    promo_tipo_f
    .set_index("tipo_loja")[["eficiencia_promocional"]]
)

st.subheader("📊 Departamentos com Maior Retorno Promocional")

top_dept = (
    promo_depto
    .sort_values("eficiencia_promocional", ascending=False)
    .head(15)
)

st.bar_chart(
    top_dept
    .set_index("departamento")[["eficiencia_promocional"]]
)


# ======================================================
# Rodapé
# ======================================================

st.markdown("---")
st.markdown("📁 Case Técnico — Plataforma de Dados para Varejo")
