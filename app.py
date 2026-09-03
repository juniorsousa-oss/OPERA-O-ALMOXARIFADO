
import io
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Inventário Rotativo | Operacional",
    page_icon="📦",
    layout="wide",
)

# -----------------------------
# Helpers
# -----------------------------
def normalize_code(series):
    return (
        series.astype("string")
        .fillna("")
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .str.zfill(8)
    )

def normalize_address(series):
    return (
        series.astype("string")
        .fillna("")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.upper()
    )

def read_excel_file(uploaded_file, sheet_name=0):
    uploaded_file.seek(0)
    return pd.read_excel(uploaded_file, sheet_name=sheet_name, header=1, dtype=str)

def numeric_series(series):
    return pd.to_numeric(
        series.astype("string").str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
        errors="coerce"
    ).fillna(0)

def format_brl(value):
    try:
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"

def build_database(cad_df, end_df, eligible_addresses):
    # CADASTROS: B=Código, C=Descrição, H=Último Preço
    cad = cad_df.iloc[:, [1, 2, 7]].copy()
    cad.columns = ["codigo", "descricao", "ultimo_preco"]
    cad["codigo"] = normalize_code(cad["codigo"])
    cad["descricao"] = cad["descricao"].astype("string").fillna("").str.strip()
    cad["ultimo_preco"] = numeric_series(cad["ultimo_preco"])
    cad = cad.drop_duplicates("codigo", keep="last")

    # ENDEREÇO: A=Código, D=Endereço, H=Quantidade
    end = end_df.iloc[:, [0, 3, 7]].copy()
    end.columns = ["codigo", "endereco", "quantidade"]
    end["codigo"] = normalize_code(end["codigo"])
    end["endereco"] = normalize_address(end["endereco"])
    end["quantidade"] = numeric_series(end["quantidade"])

    # Ignorar lote: produto + endereço = uma posição consolidada
    end = (
        end.groupby(["codigo", "endereco"], as_index=False)["quantidade"]
        .sum()
    )

    eligible = {normalize_address(pd.Series(eligible_addresses)).iloc[i] for i in range(len(eligible_addresses))}
    end["saldo_apto"] = end["endereco"].isin(eligible)

    apto = end[end["saldo_apto"]].copy()

    saldo_prod = (
        apto.groupby("codigo", as_index=False)["quantidade"]
        .sum()
        .rename(columns={"quantidade": "saldo_apto"})
    )

    db = cad.merge(saldo_prod, on="codigo", how="left")
    db["saldo_apto"] = db["saldo_apto"].fillna(0)
    db["valor_total"] = db["saldo_apto"] * db["ultimo_preco"]

    # Classificações apenas para produtos com saldo apto > 0
    active = db["saldo_apto"] > 0
    db["classificacao_r_un"] = pd.NA
    db["classificacao_r_total"] = pd.NA
    db.loc[active, "classificacao_r_un"] = (
        db.loc[active, "ultimo_preco"]
        .rank(method="first", ascending=False)
        .astype(int)
    )
    db.loc[active, "classificacao_r_total"] = (
        db.loc[active, "valor_total"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    db = db.sort_values(["classificacao_r_total", "codigo"], na_position="last")
    return db, end

# -----------------------------
# Session state
# -----------------------------
defaults = {
    "cad_df": None,
    "end_df": None,
    "db_df": None,
    "positions_df": None,
    "eligible_addresses": [],
    "cad_name": "",
    "end_name": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------
# Header
# -----------------------------
st.title("📦 Sistema Operacional — Inventário Rotativo")
st.caption("Versão inicial • Base de dados e parametrização do estoque")

# -----------------------------
# Navigation
# -----------------------------
tab_dash, tab_inv, tab_db, tab_reg = st.tabs([
    "📊 Dashboard",
    "📋 Inventário Rotativo",
    "🗄️ Banco de Dados",
    "📑 Registro",
])

# -----------------------------
# Dashboard
# -----------------------------
with tab_dash:
    st.subheader("Dashboard")
    db = st.session_state.db_df

    if db is None:
        st.info("Importe os dois relatórios na aba **Banco de Dados** para ativar os indicadores.")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Itens com saldo", "0")
        c2.metric("Itens contados", "0")
        c3.metric("Itens divergentes", "0")
        c4.metric("Acuracidade", "—")
    else:
        itens_saldo = int((db["saldo_apto"] > 0).sum())
        # Contagens entram nas próximas etapas; por enquanto ficam zeradas.
        itens_contados = 0
        itens_divergentes = 0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Itens diferentes com saldo", f"{itens_saldo:,}".replace(",", "."))
        c2.metric("Itens contabilizados", str(itens_contados))
        c3.metric("Itens divergentes", str(itens_divergentes))
        c4.metric("Divergentes / contados", "—")

        c5, c6 = st.columns(2)
        c5.metric("Divergentes / itens com saldo", "0,00%")
        c6.metric("Valor total do saldo apto", format_brl(db["valor_total"].sum()))

        st.divider()
        st.info("Os indicadores de contagem e divergência serão conectados ao módulo de Inventário Rotativo na próxima etapa.")

# -----------------------------
# Inventory
# -----------------------------
with tab_inv:
    st.subheader("Inventário Rotativo")
    st.button("＋ Novo Inventário", type="primary", disabled=st.session_state.db_df is None)

    if st.session_state.db_df is None:
        st.info("Primeiro importe e processe a base na aba **Banco de Dados**.")
    else:
        st.info("A estrutura desta tela será implementada na próxima etapa, usando a base consolidada desta versão.")
        st.write("A seleção futura respeitará: ciclo de contagem, classificação R$ UN., classificação R$ TOTAL, duplicidade de produto e expansão por endereço.")

# -----------------------------
# Database
# -----------------------------
with tab_db:
    st.subheader("Banco de Dados")
    st.write("Importe os dois relatórios oficiais. Nesta versão, o cruzamento é feito pelo **código do produto**.")

    col1, col2 = st.columns(2)

    with col1:
        cad_file = st.file_uploader(
            "1. Relatório CADASTROS",
            type=["xlsx", "xlsm", "xltx"],
            key="cad_upload",
            help="Usa B=Código, C=Descrição e H=Último Preço."
        )
        if cad_file:
            try:
                st.session_state.cad_df = read_excel_file(cad_file)
                st.session_state.cad_name = cad_file.name
                st.success(f"Carregado: {cad_file.name}")
                st.caption(f"{len(st.session_state.cad_df):,} linhas".replace(",", "."))
            except Exception as e:
                st.error(f"Não foi possível ler o cadastro: {e}")

    with col2:
        end_file = st.file_uploader(
            "2. Relatório ENDEREÇO",
            type=["xlsx", "xlsm", "xltx"],
            key="end_upload",
            help="Usa A=Código, D=Endereço e H=Quantidade. Lote é ignorado."
        )
        if end_file:
            try:
                st.session_state.end_df = read_excel_file(end_file)
                st.session_state.end_name = end_file.name
                st.success(f"Carregado: {end_file.name}")
                st.caption(f"{len(st.session_state.end_df):,} linhas".replace(",", "."))
            except Exception as e:
                st.error(f"Não foi possível ler o relatório de endereço: {e}")

    if st.session_state.cad_df is not None and st.session_state.end_df is not None:
        st.divider()
        st.subheader("3. Endereços aptos para contabilizar saldo")

        raw_addresses = normalize_address(st.session_state.end_df.iloc[:, 3])
        addresses = sorted([x for x in raw_addresses.unique() if x])

        if not st.session_state.eligible_addresses:
            st.session_state.eligible_addresses = addresses.copy()

        selected = st.multiselect(
            "Selecione os endereços que DEVEM entrar no saldo inventariável:",
            options=addresses,
            default=[x for x in st.session_state.eligible_addresses if x in addresses],
            help="Endereços não selecionados continuam no relatório, mas não entram no saldo apto nem nas classificações."
        )
        st.session_state.eligible_addresses = selected

        a, b = st.columns(2)
        a.metric("Endereços encontrados", len(addresses))
        b.metric("Endereços aptos", len(selected))

        if st.button("⚙️ Processar e atualizar banco", type="primary"):
            try:
                db, positions = build_database(
                    st.session_state.cad_df,
                    st.session_state.end_df,
                    st.session_state.eligible_addresses,
                )
                st.session_state.db_df = db
                st.session_state.positions_df = positions
                st.success("Banco consolidado atualizado com sucesso.")
            except Exception as e:
                st.error(f"Erro no processamento: {e}")

    if st.session_state.db_df is not None:
        st.divider()
        st.subheader("4. Banco consolidado")

        db_view = st.session_state.db_df.copy()
        db_view["ultimo_preco"] = db_view["ultimo_preco"].map(format_brl)
        db_view["valor_total"] = db_view["valor_total"].map(format_brl)
        db_view.columns = [
            "Código", "Descrição", "Último Preço", "Saldo Apto",
            "Valor Total", "Classificação R$ UN.", "Classificação R$ TOTAL"
        ]

        st.dataframe(
            db_view,
            use_container_width=True,
            hide_index=True,
            height=500,
        )

        csv = st.session_state.db_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇️ Exportar banco consolidado (CSV)",
            data=csv,
            file_name=f"banco_consolidado_{datetime.now():%Y%m%d_%H%M%S}.csv",
            mime="text/csv",
        )

        st.caption("Regra atual: produto + endereço são consolidados; lote não participa do cálculo.")

# -----------------------------
# Register
# -----------------------------
with tab_reg:
    st.subheader("Registro")
    st.info("O registro histórico será alimentado automaticamente após o fechamento dos inventários. A estrutura detalhada será construída junto com o fluxo de contagem.")

    columns = [
        "Documento", "Data", "Responsável", "Código", "Descrição",
        "Endereço", "Qtd. Sistema", "1ª Contagem", "2ª Contagem",
        "3ª Contagem", "Contagem Final", "Divergência",
        "Valor do Furo", "Nº de Contagens", "Comentário"
    ]
    st.dataframe(pd.DataFrame(columns=columns), use_container_width=True, hide_index=True)
