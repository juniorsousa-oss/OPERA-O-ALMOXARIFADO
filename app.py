import base64
import io
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Gestão Almoxarifado | Inventário Rotativo",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CONFIGURAÇÃO VISUAL E TEXTUAL
# ============================================================
DEFAULT_CONFIG = {
    "theme_mode": "Dark",
    "font_family": "Arial",
    "font_size": 16,
    "title_size": 31,
    "sidebar_width": 250,
    "primary_color": "#FFD63B",
    "primary_hover": "#F7C928",
    "background_dark": "#080B0A",
    "panel_dark": "#101614",
    "panel_dark_2": "#141A17",
    "border_dark": "#2B3732",
    "text_dark": "#F4F5F2",
    "muted_dark": "#A9B1AC",
    "background_clean": "#F5F6F4",
    "panel_clean": "#FFFFFF",
    "panel_clean_2": "#F0F2EF",
    "border_clean": "#D8DDD9",
    "text_clean": "#161A18",
    "muted_clean": "#626B66",
    "app_title": "GESTÃO ALMOXARIFADO",
    "app_subtitle": "01 · ACURÁCIA DE ESTOQUE  |  Inventário Rotativo",
    "sidebar_subtitle": "SISTEMA OPERACIONAL DE ESTOQUE",
    "footer_text": "Sistema Operacional • Almoxarifado",
    "menu_label": "MENU",
    "dashboard_label": "DASHBOARD",
    "inventory_label": "INVENTÁRIO ROTATIVO",
    "database_label": "BANCO DE DADOS",
    "register_label": "REGISTRO",
    "settings_label": "CONFIGURAÇÕES",
    "dashboard_title": "Dashboard",
    "inventory_title": "Inventário Rotativo",
    "database_title": "Banco de Dados",
    "register_title": "Registro",
    "settings_title": "Configurações",
    "dashboard_subtitle": "Visão geral dos indicadores do estoque.",
    "inventory_subtitle": "Controle e execução dos inventários rotativos.",
    "database_subtitle": "Importação, tratamento e classificação da base de estoque.",
    "register_subtitle": "Histórico dos inventários e das contagens realizadas.",
    "new_inventory_text": "＋ Novo Inventário",
    "process_database_text": "⚙️ Processar e atualizar banco",
    "export_database_text": "⬇️ Exportar banco consolidado (CSV)",
    "upload_cadastro_label": "1. Relatório CADASTROS",
    "upload_endereco_label": "2. Relatório ENDEREÇO",
    "address_title": "3. Endereços aptos para contabilizar saldo",
    "database_consolidated_title": "4. Banco consolidado",
    "show_footer": True,
}


def init_config():
    if "ui_config" not in st.session_state:
        st.session_state.ui_config = DEFAULT_CONFIG.copy()
    if "logo_bytes" not in st.session_state:
        st.session_state.logo_bytes = None
    if "logo_name" not in st.session_state:
        st.session_state.logo_name = ""


init_config()
config = st.session_state.ui_config

# ============================================================
# HELPERS VISUAIS
# ============================================================
def logo_data_uri():
    if not st.session_state.logo_bytes:
        return None
    mime = "image/png"
    name = st.session_state.logo_name.lower()
    if name.endswith(".jpg") or name.endswith(".jpeg"):
        mime = "image/jpeg"
    elif name.endswith(".webp"):
        mime = "image/webp"
    elif name.endswith(".svg"):
        mime = "image/svg+xml"
    encoded = base64.b64encode(st.session_state.logo_bytes).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def inject_css():
    dark = config["theme_mode"] == "Dark"
    if dark:
        bg = config["background_dark"]
        panel = config["panel_dark"]
        panel2 = config["panel_dark_2"]
        border = config["border_dark"]
        text = config["text_dark"]
        muted = config["muted_dark"]
        sidebar_bg = bg
        input_bg = panel
    else:
        bg = config["background_clean"]
        panel = config["panel_clean"]
        panel2 = config["panel_clean_2"]
        border = config["border_clean"]
        text = config["text_clean"]
        muted = config["muted_clean"]
        sidebar_bg = config["panel_clean"]
        input_bg = config["panel_clean"]

    primary = config["primary_color"]
    hover = config["primary_hover"]
    font = config["font_family"]
    font_size = config["font_size"]
    title_size = config["title_size"]
    sidebar_width = config["sidebar_width"]

    st.markdown(
        f"""
<style>
:root {{
    --app-primary: {primary};
    --app-primary-hover: {hover};
    --app-bg: {bg};
    --app-panel: {panel};
    --app-panel-2: {panel2};
    --app-border: {border};
    --app-text: {text};
    --app-muted: {muted};
    --app-font: {font};
    --app-font-size: {font_size}px;
}}

html, body, [class*="css"], .stApp {{
    font-family: var(--app-font), Arial, sans-serif !important;
    font-size: var(--app-font-size);
}}

.stApp {{
    background: var(--app-bg);
    color: var(--app-text);
}}

[data-testid="stHeader"] {{ background: var(--app-bg); }}
[data-testid="stToolbar"] {{ visibility: hidden; }}

section[data-testid="stSidebar"] {{
    background: {sidebar_bg};
    border-right: 1px solid var(--app-border);
    width: {sidebar_width}px !important;
}}
section[data-testid="stSidebar"] > div {{ padding-top: 1rem; }}

.logo-area {{
    min-height: 82px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding: 6px 8px 12px 8px;
    margin-bottom: 8px;
}}
.logo-area img {{
    max-width: 205px;
    max-height: 70px;
    object-fit: contain;
    object-position: left center;
}}
.logo-placeholder {{
    color: var(--app-muted);
    font-size: 12px;
    line-height: 1.4;
    padding: 10px 8px;
    border: 1px dashed var(--app-border);
    border-radius: 8px;
    width: 100%;
}}

.sidebar-sub {{
    color: var(--app-muted);
    font-size: 11px;
    margin: 0 7px 22px 7px;
    line-height: 1.35;
}}

.main-title {{
    font-size: {title_size}px;
    line-height: 1.1;
    font-weight: 800;
    margin: 5px 0 2px 0;
    color: var(--app-text);
}}
.main-subtitle {{
    color: var(--app-muted);
    font-size: 14px;
    margin-bottom: 22px;
}}
.section-label {{
    color: var(--app-primary);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .7px;
    margin: 10px 0 8px 7px;
}}

section[data-testid="stSidebar"] .stButton > button {{
    width: 100%;
    border: 0;
    background: transparent;
    color: var(--app-muted);
    text-align: left;
    font-weight: 800;
    border-radius: 9px;
    min-height: 42px;
    font-size: 12px;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
    background: var(--app-panel-2);
    color: var(--app-text);
}}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
    background: var(--app-primary);
    color: #11130F;
}}

[data-testid="stMetric"] {{
    background: var(--app-panel);
    border: 1px solid var(--app-border);
    border-radius: 14px;
    padding: 17px 19px;
    min-height: 105px;
}}
[data-testid="stMetricLabel"] p {{
    color: var(--app-muted) !important;
    font-size: 11px !important;
    font-weight: 800 !important;
    letter-spacing: .5px;
    text-transform: uppercase;
}}
[data-testid="stMetricValue"] {{ color: var(--app-text); }}

div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: var(--app-panel);
    border-color: var(--app-border) !important;
    border-radius: 14px;
}}

.stButton > button, .stDownloadButton > button {{
    border-radius: 8px;
    font-weight: 800;
    border: 1px solid var(--app-border);
    background: var(--app-panel-2);
    color: var(--app-text);
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
    border-color: var(--app-primary);
    color: var(--app-primary);
}}
.stButton > button[kind="primary"] {{
    background: var(--app-primary);
    color: #10120F;
    border-color: var(--app-primary);
}}
.stButton > button[kind="primary"]:hover {{
    background: var(--app-primary-hover);
    color: #10120F;
}}

.stTextInput input, .stNumberInput input,
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div,
.stTextArea textarea {{
    background: {input_bg} !important;
    color: var(--app-text) !important;
    border-color: var(--app-border) !important;
}}
label, .stMarkdown p, .stCaption, .stRadio label, .stCheckbox label {{
    color: var(--app-text) !important;
}}

[data-testid="stDataFrame"] {{
    border: 1px solid var(--app-border);
    border-radius: 10px;
    overflow: hidden;
}}

button[data-baseweb="tab"] {{ color: var(--app-muted) !important; font-weight: 700; }}
button[data-baseweb="tab"][aria-selected="true"] {{ color: var(--app-primary) !important; }}
[role="tablist"] {{ border-bottom: 1px solid var(--app-border); }}
hr {{ border-color: var(--app-border) !important; }}

div[data-testid="stAlert"] {{ border-radius: 10px; }}

.settings-card {{
    background: var(--app-panel);
    border: 1px solid var(--app-border);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
}}
.settings-card h4 {{ margin-top: 0; color: var(--app-text); }}
.small-note {{ color: var(--app-muted); font-size: 12px; }}

.footer-note {{
    position: fixed;
    bottom: 12px;
    left: 18px;
    color: var(--app-muted);
    opacity: .65;
    font-size: 10px;
    line-height: 1.35;
}}
</style>
""",
        unsafe_allow_html=True,
    )


inject_css()

# ============================================================
# HELPERS DE DADOS
# ============================================================
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
        errors="coerce",
    ).fillna(0)


def format_brl(value):
    try:
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


def build_database(cad_df, end_df, eligible_addresses):
    cad = cad_df.iloc[:, [1, 2, 7]].copy()
    cad.columns = ["codigo", "descricao", "ultimo_preco"]
    cad["codigo"] = normalize_code(cad["codigo"])
    cad["descricao"] = cad["descricao"].astype("string").fillna("").str.strip()
    cad["ultimo_preco"] = numeric_series(cad["ultimo_preco"])
    cad = cad.drop_duplicates("codigo", keep="last")

    end = end_df.iloc[:, [0, 3, 7]].copy()
    end.columns = ["codigo", "endereco", "quantidade"]
    end["codigo"] = normalize_code(end["codigo"])
    end["endereco"] = normalize_address(end["endereco"])
    end["quantidade"] = numeric_series(end["quantidade"])
    end = end.groupby(["codigo", "endereco"], as_index=False)["quantidade"].sum()

    eligible = set(normalize_address(pd.Series(eligible_addresses)).tolist())
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

    active = db["saldo_apto"] > 0
    db["classificacao_r_un"] = pd.NA
    db["classificacao_r_total"] = pd.NA
    db.loc[active, "classificacao_r_un"] = db.loc[active, "ultimo_preco"].rank(method="first", ascending=False).astype(int)
    db.loc[active, "classificacao_r_total"] = db.loc[active, "valor_total"].rank(method="first", ascending=False).astype(int)
    db = db.sort_values(["classificacao_r_total", "codigo"], na_position="last")
    return db, end


# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    "cad_df": None,
    "end_df": None,
    "db_df": None,
    "positions_df": None,
    "eligible_addresses": [],
    "cad_name": "",
    "end_name": "",
    "active_section": "Dashboard",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# SIDEBAR / NAVEGAÇÃO
# ============================================================
active = st.session_state.active_section
logo_uri = logo_data_uri()

with st.sidebar:
    if logo_uri:
        st.markdown(f'<div class="logo-area"><img src="{logo_uri}" alt="Logo"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="logo-area"><div class="logo-placeholder">LOGO DA EMPRESA<br>Configure sua imagem em Configurações.</div></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sidebar-sub">{config["sidebar_subtitle"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{config["menu_label"]}</div>', unsafe_allow_html=True)

    nav_items = [
        ("Dashboard", f"▦  {config['dashboard_label']}"),
        ("Inventário Rotativo", f"✎  {config['inventory_label']}"),
        ("Banco de Dados", f"▣  {config['database_label']}"),
        ("Registro", f"◷  {config['register_label']}"),
        ("Configurações", f"⚙  {config['settings_label']}"),
    ]
    for key, label in nav_items:
        st.button(
            label,
            key=f"nav_{key}",
            type="primary" if active == key else "secondary",
            on_click=lambda k=key: st.session_state.update(active_section=k),
        )

    if config["show_footer"]:
        st.markdown(f'<div class="footer-note">{config["footer_text"]}</div>', unsafe_allow_html=True)

# ============================================================
# CABEÇALHO PRINCIPAL
# ============================================================
st.markdown(f'<div class="main-title">{config["app_title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="main-subtitle">{config["app_subtitle"]}</div>', unsafe_allow_html=True)

# ============================================================
# DASHBOARD
# ============================================================
if active == "Dashboard":
    st.subheader(config["dashboard_title"])
    if config["dashboard_subtitle"]:
        st.caption(config["dashboard_subtitle"])

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

# ============================================================
# INVENTÁRIO
# ============================================================
if active == "Inventário Rotativo":
    st.subheader(config["inventory_title"])
    if config["inventory_subtitle"]:
        st.caption(config["inventory_subtitle"])
    st.button(config["new_inventory_text"], type="primary", disabled=st.session_state.db_df is None)

    if st.session_state.db_df is None:
        st.info("Primeiro importe e processe a base na aba **Banco de Dados**.")
    else:
        st.info("A estrutura desta tela será implementada na próxima etapa, usando a base consolidada desta versão.")
        st.write("A seleção futura respeitará: ciclo de contagem, classificação R$ UN., classificação R$ TOTAL, duplicidade de produto e expansão por endereço.")

# ============================================================
# BANCO DE DADOS
# ============================================================
if active == "Banco de Dados":
    st.subheader(config["database_title"])
    if config["database_subtitle"]:
        st.caption(config["database_subtitle"])
    st.write("Importe os dois relatórios oficiais. Nesta versão, o cruzamento é feito pelo **código do produto**.")

    col1, col2 = st.columns(2)
    with col1:
        cad_file = st.file_uploader(
            config["upload_cadastro_label"],
            type=["xlsx", "xlsm", "xltx"],
            key="cad_upload",
            help="Usa B=Código, C=Descrição e H=Último Preço.",
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
            config["upload_endereco_label"],
            type=["xlsx", "xlsm", "xltx"],
            key="end_upload",
            help="Usa A=Código, D=Endereço e H=Quantidade. Lote é ignorado.",
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
        st.subheader(config["address_title"])
        raw_addresses = normalize_address(st.session_state.end_df.iloc[:, 3])
        addresses = sorted([x for x in raw_addresses.unique() if x])
        if not st.session_state.eligible_addresses:
            st.session_state.eligible_addresses = addresses.copy()

        selected = st.multiselect(
            "Selecione os endereços que DEVEM entrar no saldo inventariável:",
            options=addresses,
            default=[x for x in st.session_state.eligible_addresses if x in addresses],
            help="Endereços não selecionados continuam no relatório, mas não entram no saldo apto nem nas classificações.",
        )
        st.session_state.eligible_addresses = selected
        a, b = st.columns(2)
        a.metric("Endereços encontrados", len(addresses))
        b.metric("Endereços aptos", len(selected))

        if st.button(config["process_database_text"], type="primary"):
            try:
                db, positions = build_database(st.session_state.cad_df, st.session_state.end_df, st.session_state.eligible_addresses)
                st.session_state.db_df = db
                st.session_state.positions_df = positions
                st.success("Banco consolidado atualizado com sucesso.")
            except Exception as e:
                st.error(f"Erro no processamento: {e}")

    if st.session_state.db_df is not None:
        st.divider()
        st.subheader(config["database_consolidated_title"])
        db_view = st.session_state.db_df.copy()
        db_view["ultimo_preco"] = db_view["ultimo_preco"].map(format_brl)
        db_view["valor_total"] = db_view["valor_total"].map(format_brl)
        db_view.columns = ["Código", "Descrição", "Último Preço", "Saldo Apto", "Valor Total", "Classificação R$ UN.", "Classificação R$ TOTAL"]
        st.dataframe(db_view, use_container_width=True, hide_index=True, height=500)
        csv = st.session_state.db_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            config["export_database_text"],
            data=csv,
            file_name=f"banco_consolidado_{datetime.now():%Y%m%d_%H%M%S}.csv",
            mime="text/csv",
        )
        st.caption("Regra atual: produto + endereço são consolidados; lote não participa do cálculo.")

# ============================================================
# REGISTRO
# ============================================================
if active == "Registro":
    st.subheader(config["register_title"])
    if config["register_subtitle"]:
        st.caption(config["register_subtitle"])
    st.info("O registro histórico será alimentado automaticamente após o fechamento dos inventários. A estrutura detalhada será construída junto com o fluxo de contagem.")
    columns = [
        "Documento", "Data", "Responsável", "Código", "Descrição", "Endereço", "Qtd. Sistema", "1ª Contagem", "2ª Contagem", "3ª Contagem", "Contagem Final", "Divergência", "Valor do Furo", "Nº de Contagens", "Comentário"
    ]
    st.dataframe(pd.DataFrame(columns=columns), use_container_width=True, hide_index=True)

# ============================================================
# CONFIGURAÇÕES
# ============================================================
if active == "Configurações":
    st.subheader(config["settings_title"])
    st.caption("Aqui você controla a identidade visual e os principais textos do sistema. As alterações valem para a sessão atual.")

    with st.expander("01 · TEMA E CONTRASTE", expanded=True):
        theme = st.radio("Modo de tela", ["Dark", "Clean"], index=0 if config["theme_mode"] == "Dark" else 1, horizontal=True)
        if theme != config["theme_mode"]:
            config["theme_mode"] = theme
            st.rerun()
        st.write("Dark: fundo escuro e textos claros. Clean: fundo claro e textos escuros.")

    with st.expander("02 · TIPOGRAFIA", expanded=True):
        f1, f2 = st.columns(2)
        font = f1.selectbox("Tipo de letra", ["Arial", "Inter", "Roboto", "Poppins", "Montserrat", "Georgia", "Verdana", "Trebuchet MS"], index=["Arial", "Inter", "Roboto", "Poppins", "Montserrat", "Georgia", "Verdana", "Trebuchet MS"].index(config["font_family"]))
        font_size = f2.slider("Tamanho geral", min_value=12, max_value=22, value=int(config["font_size"]), step=1)
        title_size = st.slider("Tamanho do título principal", min_value=22, max_value=48, value=int(config["title_size"]), step=1)
        config["font_family"] = font
        config["font_size"] = font_size
        config["title_size"] = title_size

    with st.expander("03 · CORES", expanded=True):
        c1, c2 = st.columns(2)
        config["primary_color"] = c1.color_picker("Cor principal / destaque", config["primary_color"])
        config["primary_hover"] = c2.color_picker("Cor principal ao passar o mouse", config["primary_hover"])
        if config["theme_mode"] == "Dark":
            c1, c2 = st.columns(2)
            config["background_dark"] = c1.color_picker("Fundo", config["background_dark"])
            config["panel_dark"] = c2.color_picker("Cards / painéis", config["panel_dark"])
            c1, c2 = st.columns(2)
            config["panel_dark_2"] = c1.color_picker("Painéis secundários", config["panel_dark_2"])
            config["border_dark"] = c2.color_picker("Bordas", config["border_dark"])
            c1, c2 = st.columns(2)
            config["text_dark"] = c1.color_picker("Texto principal", config["text_dark"])
            config["muted_dark"] = c2.color_picker("Texto secundário", config["muted_dark"])
        else:
            c1, c2 = st.columns(2)
            config["background_clean"] = c1.color_picker("Fundo", config["background_clean"])
            config["panel_clean"] = c2.color_picker("Cards / painéis", config["panel_clean"])
            c1, c2 = st.columns(2)
            config["panel_clean_2"] = c1.color_picker("Painéis secundários", config["panel_clean_2"])
            config["border_clean"] = c2.color_picker("Bordas", config["border_clean"])
            c1, c2 = st.columns(2)
            config["text_clean"] = c1.color_picker("Texto principal", config["text_clean"])
            config["muted_clean"] = c2.color_picker("Texto secundário", config["muted_clean"])
        st.caption("As cores de texto e fundo são separadas por modo para manter o contraste correto.")

    with st.expander("04 · LOGO / IDENTIDADE", expanded=True):
        st.write("A logo abaixo substitui totalmente a escrita fixa que existia na lateral.")
        logo_file = st.file_uploader("Enviar logo da empresa", type=["png", "jpg", "jpeg", "webp", "svg"], key="company_logo")
        if logo_file:
            st.session_state.logo_bytes = logo_file.getvalue()
            st.session_state.logo_name = logo_file.name
            st.success(f"Logo carregada: {logo_file.name}")
        if st.session_state.logo_bytes:
            st.image(st.session_state.logo_bytes, caption="Pré-visualização da logo", width=240)
            if st.button("Remover logo"):
                st.session_state.logo_bytes = None
                st.session_state.logo_name = ""
                st.rerun()

    with st.expander("05 · MENU", expanded=True):
        c1, c2 = st.columns(2)
        config["menu_label"] = c1.text_input("Título do menu", config["menu_label"])
        config["sidebar_subtitle"] = c2.text_input("Subtítulo da lateral", config["sidebar_subtitle"])
        c1, c2 = st.columns(2)
        config["dashboard_label"] = c1.text_input("Dashboard", config["dashboard_label"])
        config["inventory_label"] = c2.text_input("Inventário", config["inventory_label"])
        c1, c2 = st.columns(2)
        config["database_label"] = c1.text_input("Banco de Dados", config["database_label"])
        config["register_label"] = c2.text_input("Registro", config["register_label"])
        config["settings_label"] = st.text_input("Configurações", config["settings_label"])

    with st.expander("06 · TEXTOS DAS PÁGINAS", expanded=True):
        fields = [
            ("app_title", "Título principal"),
            ("app_subtitle", "Subtítulo principal"),
            ("footer_text", "Rodapé"),
            ("dashboard_title", "Título do Dashboard"),
            ("dashboard_subtitle", "Subtítulo do Dashboard"),
            ("inventory_title", "Título do Inventário"),
            ("inventory_subtitle", "Subtítulo do Inventário"),
            ("database_title", "Título do Banco de Dados"),
            ("database_subtitle", "Subtítulo do Banco de Dados"),
            ("register_title", "Título do Registro"),
            ("register_subtitle", "Subtítulo do Registro"),
            ("address_title", "Título da configuração de endereços"),
            ("database_consolidated_title", "Título do banco consolidado"),
        ]
        for i in range(0, len(fields), 2):
            cols = st.columns(2)
            for col, (key, label) in zip(cols, fields[i:i+2]):
                config[key] = col.text_input(label, config[key], key=f"cfg_{key}")

    with st.expander("07 · BOTÕES E AÇÕES", expanded=True):
        config["new_inventory_text"] = st.text_input("Botão Novo Inventário", config["new_inventory_text"])
        config["process_database_text"] = st.text_input("Botão Processar Banco", config["process_database_text"])
        config["export_database_text"] = st.text_input("Botão Exportar Banco", config["export_database_text"])

    with st.expander("08 · DIMENSIONAMENTO", expanded=False):
        config["sidebar_width"] = st.slider("Largura do menu lateral", 220, 360, int(config["sidebar_width"]), 5)
        config["show_footer"] = st.checkbox("Exibir rodapé no menu", value=bool(config["show_footer"]))

    st.divider()
    c1, c2 = st.columns(2)
    if c1.button("Aplicar alterações visuais", type="primary", use_container_width=True):
        st.rerun()
    if c2.button("Restaurar configuração padrão", use_container_width=True):
        st.session_state.ui_config = DEFAULT_CONFIG.copy()
        st.session_state.logo_bytes = None
        st.session_state.logo_name = ""
        st.rerun()

    st.info("Observação: nesta versão as configurações ficam na sessão atual do aplicativo. Na etapa de banco de dados/Supabase, podemos transformar essas configurações em permanentes para todos os usuários.")
