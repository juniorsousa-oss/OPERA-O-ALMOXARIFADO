import base64
import io
import json
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
# CONFIGURAÇÃO VISUAL / TEXTUAL
# ============================================================
DEFAULT_CONFIG = {
    "theme_mode": "Dark",
    "font_family": "Arial",
    "font_size": 16,
    "title_size": 31,
    "sidebar_width": 250,
    "sidebar_align": "left",
    "sidebar_font_size": 12,
    "sidebar_item_height": 42,
    "sidebar_logo_width": 190,
    "sidebar_logo_height": 70,
    "sidebar_logo_align": "left",
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
    "process_database_text": "⚙ Processar e atualizar banco",
    "export_database_text": "↓ Exportar banco consolidado (CSV)",
    "upload_cadastro_label": "1. Relatório CADASTROS",
    "upload_endereco_label": "2. Relatório ENDEREÇO",
    "address_title": "3. Endereços aptos para contabilizar saldo",
    "database_consolidated_title": "4. Banco consolidado",
    "inventory_default_blind": False,
    "inventory_manager_profile": "Gestor",
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
    if name.endswith((".jpg", ".jpeg")):
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
        bg, panel, panel2, border, text, muted = (
            config["background_dark"], config["panel_dark"], config["panel_dark_2"],
            config["border_dark"], config["text_dark"], config["muted_dark"]
        )
        sidebar_bg = bg
        input_bg = panel
    else:
        bg, panel, panel2, border, text, muted = (
            config["background_clean"], config["panel_clean"], config["panel_clean_2"],
            config["border_clean"], config["text_clean"], config["muted_clean"]
        )
        sidebar_bg = config["panel_clean"]
        input_bg = config["panel_clean"]

    primary = config["primary_color"]
    hover = config["primary_hover"]
    font = config["font_family"]
    font_size = config["font_size"]
    title_size = config["title_size"]
    sidebar_width = config["sidebar_width"]
    sidebar_align = config["sidebar_align"]
    logo_align = config["sidebar_logo_align"]

    st.markdown(
        f"""
<style>
:root {{
    --app-primary: {primary}; --app-primary-hover: {hover}; --app-bg: {bg};
    --app-panel: {panel}; --app-panel-2: {panel2}; --app-border: {border};
    --app-text: {text}; --app-muted: {muted}; --app-font: {font};
    --app-font-size: {font_size}px;
}}
html, body, [class*="css"], .stApp {{ font-family: var(--app-font), Arial, sans-serif !important; font-size: var(--app-font-size); }}
.stApp {{ background: var(--app-bg); color: var(--app-text); }}
[data-testid="stHeader"] {{ background: var(--app-bg); }}

/* IMPORTANTE: não forçar display/posição da sidebar. O Streamlit controla o recolhimento. */
section[data-testid="stSidebar"] {{
    background: {sidebar_bg}; border-right: 1px solid var(--app-border);
    z-index: 9999 !important;
}}
section[data-testid="stSidebar"] > div {{ padding-top: 1rem; }}

/* Botão nativo de abrir/recolher: permanece preso à borda da janela */
[data-testid="stSidebarCollapsedControl"] {{
    position: fixed !important; left: 0.35rem !important; top: 0.75rem !important;
    z-index: 100000 !important; display: flex !important; visibility: visible !important;
}}
[data-testid="stSidebarCollapseButton"] {{ z-index: 100000 !important; }}

.logo-area {{ min-height: 82px; display:flex; align-items:center; justify-content:{logo_align};
    padding: 6px 8px 12px 8px; margin-bottom: 8px; overflow:hidden; }}
.logo-area img {{ width:{config['sidebar_logo_width']}px; height:{config['sidebar_logo_height']}px;
    max-width:100%; object-fit:contain; object-position:center; display:block; }}
.logo-placeholder {{ color:var(--app-muted); font-size:12px; line-height:1.4; padding:10px 8px;
    border:1px dashed var(--app-border); border-radius:8px; width:100%; text-align:center; }}
.sidebar-sub {{ color:var(--app-muted); font-size:11px; margin:0 7px 22px 7px; line-height:1.35;
    text-align:{sidebar_align}; }}
.section-label {{ color:var(--app-primary); font-size:12px; font-weight:800; letter-spacing:.7px;
    margin:10px 7px 8px 7px; text-align:{sidebar_align}; }}
section[data-testid="stSidebar"] .stButton > button {{ width:100%; border:0; background:transparent;
    color:var(--app-muted); text-align:{sidebar_align}; font-weight:800; border-radius:9px;
    min-height:{config['sidebar_item_height']}px; font-size:{config['sidebar_font_size']}px; }}
section[data-testid="stSidebar"] .stButton > button:hover {{ background:var(--app-panel-2); color:var(--app-text); }}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {{ background:var(--app-primary); color:#11130F; }}

.main-title {{ font-size:{title_size}px; line-height:1.1; font-weight:800; margin:5px 0 2px 0; color:var(--app-text); }}
.main-subtitle {{ color:var(--app-muted); font-size:14px; margin-bottom:22px; }}
[data-testid="stMetric"] {{ background:var(--app-panel); border:1px solid var(--app-border); border-radius:14px; padding:17px 19px; min-height:105px; }}
[data-testid="stMetricLabel"] p {{ color:var(--app-muted)!important; font-size:11px!important; font-weight:800!important; letter-spacing:.5px; text-transform:uppercase; }}
[data-testid="stMetricValue"] {{ color:var(--app-text); }}
div[data-testid="stVerticalBlockBorderWrapper"] {{ background:var(--app-panel); border-color:var(--app-border)!important; border-radius:14px; }}
.stButton > button, .stDownloadButton > button {{ border-radius:8px; font-weight:800; border:1px solid var(--app-border); background:var(--app-panel-2); color:var(--app-text); }}
.stButton > button:hover, .stDownloadButton > button:hover {{ border-color:var(--app-primary); color:var(--app-primary); }}
.stButton > button[kind="primary"] {{ background:var(--app-primary); color:#10120F; border-color:var(--app-primary); }}
.stButton > button[kind="primary"]:hover {{ background:var(--app-primary-hover); color:#10120F; }}
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div, .stTextArea textarea {{ background:{input_bg}!important; color:var(--app-text)!important; border-color:var(--app-border)!important; }}
label, .stMarkdown p, .stCaption, .stRadio label, .stCheckbox label {{ color:var(--app-text)!important; }}
[data-testid="stDataFrame"] {{ border:1px solid var(--app-border); border-radius:10px; overflow:hidden; }}
button[data-baseweb="tab"] {{ color:var(--app-muted)!important; font-weight:700; }}
button[data-baseweb="tab"][aria-selected="true"] {{ color:var(--app-primary)!important; }}
[role="tablist"] {{ border-bottom:1px solid var(--app-border); }}
hr {{ border-color:var(--app-border)!important; }}
.settings-card {{ background:var(--app-panel); border:1px solid var(--app-border); border-radius:14px; padding:18px; margin-bottom:12px; }}
.small-note {{ color:var(--app-muted); font-size:12px; }}
.footer-note {{ position:fixed; bottom:12px; left:18px; color:var(--app-muted); opacity:.65; font-size:10px; line-height:1.35; }}
.status-pill {{ display:inline-block; padding:4px 9px; border-radius:20px; border:1px solid var(--app-border); font-size:11px; font-weight:800; }}
</style>
""", unsafe_allow_html=True)


inject_css()

# ============================================================
# DADOS / NÚMEROS
# ============================================================
def normalize_code(series):
    return (series.astype("string").fillna("").str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(8))


def normalize_address(series):
    return (series.astype("string").fillna("").str.strip().str.replace(r"\s+", " ", regex=True).str.upper())


def read_excel_file(uploaded_file, sheet_name=0):
    uploaded_file.seek(0)
    return pd.read_excel(uploaded_file, sheet_name=sheet_name, header=1, dtype=str)


def parse_locale_number(value):
    """Converte números BR/Excel sem apagar a casa decimal.
    Exemplos: 613,48 -> 613.48 | 613.48 -> 613.48 | 1.234,56 -> 1234.56.
    """
    if value is None or pd.isna(value):
        return 0.0
    s = str(value).strip().replace("R$", "").replace(" ", "")
    if not s:
        return 0.0
    neg = s.startswith("-")
    s = s.lstrip("+-")
    if "," in s and "." in s:
        # O último separador é o decimal.
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        # No ERP/relatório brasileiro, vírgula é decimal.
        s = s.replace(",", ".")
    elif "." in s:
        # Quando o Excel entrega a célula numérica como texto, ponto é separador decimal.
        # Não removemos o ponto: quantidades como 110.135 devem continuar 110,135.
        pass
    try:
        out = float(s)
        return -out if neg else out
    except Exception:
        return 0.0


def numeric_series(series):
    return series.apply(parse_locale_number).astype(float)


def format_number(value, decimals=3):
    try:
        return f"{float(value):,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "0"


def format_brl(value):
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
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
    end["apto"] = end["endereco"].isin(eligible)
    apto = end[end["apto"]].copy()
    saldo_prod = apto.groupby("codigo", as_index=False)["quantidade"].sum().rename(columns={"quantidade": "saldo_apto"})

    db = cad.merge(saldo_prod, on="codigo", how="left")
    db["saldo_apto"] = db["saldo_apto"].fillna(0.0)
    db["valor_total"] = db["saldo_apto"] * db["ultimo_preco"]
    active = db["saldo_apto"] > 0
    db["classificacao_r_un"] = pd.NA
    db["classificacao_r_total"] = pd.NA
    db.loc[active, "classificacao_r_un"] = db.loc[active, "ultimo_preco"].rank(method="first", ascending=False).astype(int)
    db.loc[active, "classificacao_r_total"] = db.loc[active, "valor_total"].rank(method="first", ascending=False).astype(int)
    db = db.sort_values(["classificacao_r_total", "codigo"], na_position="last").reset_index(drop=True)
    return db, end


# ============================================================
# INVENTÁRIO ROTATIVO
# ============================================================
def next_document_id():
    today = datetime.now().strftime("%d%m%Y")
    seq = 1
    for inv in st.session_state.inventories.values():
        if inv.get("documento", "").startswith(today + "-"):
            try:
                seq = max(seq, int(inv["documento"].split("-")[-1]) + 1)
            except Exception:
                pass
    return f"{today}-{seq:03d}"


def ensure_inventory_state():
    if "inventories" not in st.session_state:
        st.session_state.inventories = {}
    if "product_count_cycles" not in st.session_state:
        st.session_state.product_count_cycles = {}


def current_cycle(db):
    active_codes = db.loc[db["saldo_apto"] > 0, "codigo"].astype(str).tolist()
    if not active_codes:
        return 1
    counts = [int(st.session_state.product_count_cycles.get(c, 0)) for c in active_codes]
    return min(counts) + 1


def select_rotative_products(db, quantity):
    """Seleciona N produtos distintos, metade por R$ UN e metade por R$ TOTAL.
    Produtos com menor número de ciclos têm prioridade. Em empate, usa os rankings.
    """
    quantity = max(1, int(quantity))
    work = db[db["saldo_apto"] > 0].copy()
    if work.empty:
        return work
    work["cycle_count"] = work["codigo"].astype(str).map(lambda c: int(st.session_state.product_count_cycles.get(c, 0)))
    min_cycle = int(work["cycle_count"].min())
    work = work[work["cycle_count"] == min_cycle].copy()
    if work.empty:
        return work

    unit_rank = work.sort_values(["classificacao_r_un", "codigo"], na_position="last")
    total_rank = work.sort_values(["classificacao_r_total", "codigo"], na_position="last")
    target_unit = quantity // 2
    target_total = quantity - target_unit
    selected = []

    for code in unit_rank["codigo"].tolist():
        if len(selected) >= target_unit:
            break
        if code not in selected:
            selected.append(code)

    for code in total_rank["codigo"].tolist():
        if len([x for x in selected if x in set(unit_rank.head(target_unit)["codigo"])]) >= target_unit and len(selected) >= target_unit + target_total:
            break
        if code not in selected:
            selected.append(code)
        if len(selected) >= target_unit + target_total:
            break

    if len(selected) < quantity:
        combined = pd.concat([unit_rank, total_rank]).drop_duplicates("codigo")
        for code in combined["codigo"].tolist():
            if code not in selected:
                selected.append(code)
            if len(selected) >= quantity:
                break

    return db[db["codigo"].isin(selected)].copy().sort_values("codigo")


def expand_products_to_positions(selected_products, positions_df):
    rows = []
    for _, p in selected_products.iterrows():
        pos = positions_df[(positions_df["codigo"] == p["codigo"]) & (positions_df["apto"])]
        for _, r in pos.iterrows():
            rows.append({
                "codigo": p["codigo"],
                "descricao": p["descricao"],
                "endereco": r["endereco"],
                "qtd_sistema": float(r["quantidade"]),
                "classificacao_r_un": int(p["classificacao_r_un"]),
                "classificacao_r_total": int(p["classificacao_r_total"]),
                "primeira_contagem": None,
                "comentario_1": "SC",
                "segunda_contagem": None,
                "comentario_2": "SC",
                "terceira_contagem": None,
                "comentario_3": "SC",
                "contagem_final": None,
                "comentario_final": "SC",
                "status": "PENDENTE",
                "classificacao_furo": "",
                "valor_furo": 0.0,
                "resultado_final": "",
                "audit_solicitada": False,
            })
    return rows


def create_inventory(quantity, blind_count, responsible="Operador"):
    db = st.session_state.db_df
    positions = st.session_state.positions_df
    selected = select_rotative_products(db, quantity)
    if selected.empty:
        return None, "Não há produtos elegíveis para seleção."
    rows = expand_products_to_positions(selected, positions)
    if not rows:
        return None, "Os produtos selecionados não possuem endereços aptos."
    doc = next_document_id()
    cycle = current_cycle(db)
    inv = {
        "documento": doc,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "responsavel": responsible,
        "quantidade_produtos_solicitada": int(quantity),
        "blind_count": bool(blind_count),
        "ciclo": cycle,
        "status": "EM CONTAGEM",
        "rows": rows,
        "criado_em": datetime.now().isoformat(timespec="seconds"),
    }
    st.session_state.inventories[doc] = inv
    return doc, None


def inventory_summary(inv):
    rows = inv["rows"]
    return {
        "posicoes": len(rows),
        "produtos": len(set(r["codigo"] for r in rows)),
        "pendentes": sum(r["primeira_contagem"] is None for r in rows),
        "divergentes": sum(r["primeira_contagem"] is not None and abs(float(r["primeira_contagem"]) - float(r["qtd_sistema"])) > 1e-9 for r in rows),
    }


def mark_product_cycles(inv):
    counted_codes = set()
    for r in inv["rows"]:
        if r["primeira_contagem"] is not None:
            counted_codes.add(r["codigo"])
    for code in counted_codes:
        st.session_state.product_count_cycles[code] = int(st.session_state.product_count_cycles.get(code, 0)) + 1


def finish_first_count(inv):
    if any(r["primeira_contagem"] is None for r in inv["rows"]):
        return False, "Ainda existem posições sem primeira contagem."
    inv["status"] = "AGUARDANDO ANÁLISE"
    return True, None


def calculate_furo(row, count_value):
    return (float(count_value) - float(row["qtd_sistema"]))


def classify_divergence(row, final_count):
    diff_qty = calculate_furo(row, final_count)
    value = abs(diff_qty) * abs(float(row["valor_unitario"])) if "valor_unitario" in row else 0.0
    row["valor_furo"] = value
    if abs(diff_qty) < 1e-9:
        row["classificacao_furo"] = "SEM DIVERGÊNCIA"
    elif value <= 100:
        row["classificacao_furo"] = "BAIXO"
    elif value <= 1000:
        row["classificacao_furo"] = "MÉDIO"
    else:
        row["classificacao_furo"] = "ALTO"


def all_inventory_rows_dataframe(inv):
    rows = []
    for r in inv["rows"]:
        item = dict(r)
        rows.append(item)
    return pd.DataFrame(rows)


# ============================================================
# SESSION STATE
# ============================================================
def init_state():
    defaults = {
        "cad_df": None, "end_df": None, "db_df": None, "positions_df": None,
        "eligible_addresses": [], "cad_name": "", "end_name": "", "active_section": "Dashboard",
        "inventories": {}, "product_count_cycles": {}, "inventory_profile": "Operador",
        "selected_inventory": None, "new_inventory_open": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()
ensure_inventory_state()

# ============================================================
# SIDEBAR
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
        st.button(label, key=f"nav_{key}", type="primary" if active == key else "secondary",
                  on_click=lambda k=key: st.session_state.update(active_section=k))
    if config["show_footer"]:
        st.markdown(f'<div class="footer-note">{config["footer_text"]}</div>', unsafe_allow_html=True)

# ============================================================
# CABEÇALHO
# ============================================================
st.markdown(f'<div class="main-title">{config["app_title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="main-subtitle">{config["app_subtitle"]}</div>', unsafe_allow_html=True)

# ============================================================
# DASHBOARD
# ============================================================
if active == "Dashboard":
    st.subheader(config["dashboard_title"])
    if config["dashboard_subtitle"]: st.caption(config["dashboard_subtitle"])
    db = st.session_state.db_df
    if db is None:
        st.info("Importe os dois relatórios na aba **Banco de Dados** para ativar os indicadores.")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Itens com saldo", "0"); c2.metric("Itens contados", "0"); c3.metric("Itens divergentes", "0"); c4.metric("Acuracidade", "—")
    else:
        itens_saldo = int((db["saldo_apto"] > 0).sum())
        all_rows = [r for inv in st.session_state.inventories.values() for r in inv["rows"]]
        counted = [r for r in all_rows if r["primeira_contagem"] is not None]
        div = [r for r in counted if abs(float(r["primeira_contagem"]) - float(r["qtd_sistema"])) > 1e-9]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Itens diferentes com saldo", f"{itens_saldo:,}".replace(",", "."))
        c2.metric("Posições contabilizadas", f"{len(counted):,}".replace(",", "."))
        c3.metric("Posições divergentes", f"{len(div):,}".replace(",", "."))
        c4.metric("Divergentes / contados", f"{len(div)/len(counted)*100:.2f}%" if counted else "—")
        c5, c6 = st.columns(2)
        c5.metric("Divergentes / itens com saldo", f"{len(div)/itens_saldo*100:.2f}%" if itens_saldo else "—")
        c6.metric("Valor total do saldo apto", format_brl(db["valor_total"].sum()))

# ============================================================
# INVENTÁRIO ROTATIVO
# ============================================================
if active == "Inventário Rotativo":
    st.subheader(config["inventory_title"])
    if config["inventory_subtitle"]: st.caption(config["inventory_subtitle"])

    if st.session_state.db_df is None:
        st.info("Primeiro importe e processe a base na aba **Banco de Dados**.")
    else:
        p1, p2 = st.columns([1, 1])
        profile = p1.radio("Perfil de teste", ["Operador", "Gestor"], index=0 if st.session_state.inventory_profile == "Operador" else 1, horizontal=True)
        st.session_state.inventory_profile = profile
        if p2.button(config["new_inventory_text"], type="primary", use_container_width=True):
            st.session_state.new_inventory_open = True
            st.rerun()

        if st.session_state.new_inventory_open:
            st.markdown("### Novo Inventário")
            with st.container(border=True):
                c1, c2, c3 = st.columns(3)
                qty = c1.number_input("Quantidade de produtos", min_value=1, max_value=500, value=10, step=1)
                blind = c2.checkbox("Contagem cega", value=bool(config["inventory_default_blind"]))
                c3.metric("Ciclo atual", current_cycle(st.session_state.db_df))
                st.caption("A quantidade é de produtos distintos. Cada produto pode gerar várias posições físicas, uma por endereço apto.")
                b1, b2 = st.columns(2)
                if b1.button("Criar inventário", type="primary", use_container_width=True):
                    doc, err = create_inventory(qty, blind, responsible=profile)
                    if err: st.error(err)
                    else:
                        st.session_state.new_inventory_open = False
                        st.session_state.selected_inventory = doc
                        st.success(f"Inventário {doc} criado.")
                        st.rerun()
                if b2.button("Cancelar", use_container_width=True):
                    st.session_state.new_inventory_open = False
                    st.rerun()

        inventories = list(st.session_state.inventories.values())
        if inventories:
            st.markdown("### Inventários abertos / recentes")
            for inv in sorted(inventories, key=lambda x: x["criado_em"], reverse=True):
                s = inventory_summary(inv)
                with st.container(border=True):
                    a, b, c, d, e = st.columns([2.2, 1.2, 1.2, 1.2, 1.4])
                    a.markdown(f"**{inv['documento']}**  ")
                    a.caption(f"Ciclo {inv['ciclo']} · {inv['data']}")
                    b.write(f"**{inv['status']}**")
                    c.metric("Produtos", s["produtos"])
                    d.metric("Posições", s["posicoes"])
                    e.metric("Pendentes", s["pendentes"])
                    if st.button("Abrir", key=f"open_{inv['documento']}"):
                        st.session_state.selected_inventory = inv["documento"]
                        st.rerun()

        doc = st.session_state.selected_inventory
        if doc and doc in st.session_state.inventories:
            inv = st.session_state.inventories[doc]
            st.divider()
            st.markdown(f"### Inventário {doc}")
            st.write(f"**Status:** {inv['status']} · **Ciclo:** {inv['ciclo']} · **Contagem cega:** {'SIM' if inv['blind_count'] else 'NÃO'}")

            if profile == "Operador" and inv["status"] == "EM CONTAGEM":
                st.markdown("#### 1ª Contagem")
                st.caption("Comentário é opcional. Se ficar vazio, o sistema registra SC.")
                for i, row in enumerate(inv["rows"]):
                    if row["primeira_contagem"] is not None:
                        continue
                    with st.container(border=True):
                        c1, c2, c3 = st.columns([1.1, 2.6, 1.3])
                        c1.markdown(f"**{row['codigo']}**")
                        c2.write(f"{row['descricao']}  \n**Endereço:** {row['endereco']}")
                        if inv["blind_count"]:
                            c3.write("**Qtd. sistema:** OCULTA")
                        else:
                            c3.write(f"**Qtd. sistema:** {format_number(row['qtd_sistema'])}")
                        d1, d2 = st.columns([1, 2])
                        count = d1.number_input("Contagem", min_value=0.0, step=0.001, format="%.3f", key=f"c1_{doc}_{i}")
                        comment = d2.text_input("Comentário (opcional)", key=f"cm1_{doc}_{i}")
                        if st.button("Salvar contagem", key=f"save1_{doc}_{i}", type="primary"):
                            row["primeira_contagem"] = float(count)
                            row["comentario_1"] = comment.strip() if comment.strip() else "SC"
                            st.rerun()
                if all(r["primeira_contagem"] is not None for r in inv["rows"]):
                    if st.button("Fechar Contagem", type="primary"):
                        ok, err = finish_first_count(inv)
                        if ok:
                            mark_product_cycles(inv)
                            st.rerun()
                        else: st.error(err)

            elif profile == "Gestor" and inv["status"] == "AGUARDANDO ANÁLISE":
                st.markdown("#### Análise do gestor — somente divergências")
                divergent_rows = []
                unit_price_map = st.session_state.db_df.set_index("codigo")["ultimo_preco"].to_dict()
                for i, row in enumerate(inv["rows"]):
                    if row["primeira_contagem"] is not None:
                        row["valor_unitario"] = float(unit_price_map.get(row["codigo"], 0))
                        diff = float(row["primeira_contagem"]) - float(row["qtd_sistema"])
                        if abs(diff) > 1e-9:
                            row["valor_furo"] = abs(diff) * row["valor_unitario"]
                            if row["valor_furo"] <= 100: row["classificacao_furo"] = "BAIXO"
                            elif row["valor_furo"] <= 1000: row["classificacao_furo"] = "MÉDIO"
                            else: row["classificacao_furo"] = "ALTO"
                            divergent_rows.append((i, row))
                if not divergent_rows:
                    st.success("Não existem divergências. O gestor pode fechar o inventário.")
                    if st.button("Fechar Inventário", type="primary"):
                        inv["status"] = "FECHADO"
                        st.rerun()
                else:
                    for i, row in divergent_rows:
                        with st.container(border=True):
                            st.markdown(f"**{row['codigo']} — {row['endereco']}**")
                            st.write(row["descricao"])
                            c1, c2, c3, c4 = st.columns(4)
                            c1.metric("Sistema", format_number(row["qtd_sistema"]))
                            c2.metric("1ª contagem", format_number(row["primeira_contagem"]))
                            c3.metric("Diferença", format_number(float(row["primeira_contagem"]) - float(row["qtd_sistema"])))
                            c4.metric("Valor do furo", format_brl(row["valor_furo"]))
                            st.caption(f"Classificação: {row['classificacao_furo']} · Comentário: {row['comentario_1']}")
                            if st.button("Solicitar 2ª contagem", key=f"req2_{doc}_{i}"):
                                row["status"] = "SEGUNDA_CONTAGEM"
                                row["segunda_contagem"] = None
                                inv["status"] = "AGUARDANDO 2ª CONTAGEM"
                                st.rerun()
                    if st.button("Fechar com 1ª contagem", type="primary"):
                        for _, row in divergent_rows:
                            row["contagem_final"] = row["primeira_contagem"]
                            row["resultado_final"] = "FECHADO PELO GESTOR"
                        inv["status"] = "FECHADO"
                        st.rerun()

            elif profile == "Operador" and inv["status"] == "AGUARDANDO 2ª CONTAGEM":
                st.markdown("#### 2ª Contagem")
                for i, row in enumerate(inv["rows"]):
                    if row["status"] != "SEGUNDA_CONTAGEM": continue
                    with st.container(border=True):
                        st.markdown(f"**{row['codigo']} — {row['endereco']}**")
                        st.write(row["descricao"])
                        c1, c2 = st.columns(2)
                        c1.metric("1ª contagem", format_number(row["primeira_contagem"]))
                        c2.metric("Sistema", "OCULTO" if inv["blind_count"] else format_number(row["qtd_sistema"]))
                        count2 = st.number_input("2ª contagem", min_value=0.0, step=0.001, format="%.3f", key=f"c2_{doc}_{i}")
                        comment2 = st.text_input("Comentário (opcional)", key=f"cm2_{doc}_{i}")
                        if st.button("Salvar 2ª contagem", key=f"save2_{doc}_{i}", type="primary"):
                            row["segunda_contagem"] = float(count2)
                            row["comentario_2"] = comment2.strip() if comment2.strip() else "SC"
                            row["status"] = "SEGUNDA_CONTAGEM_FEITA"
                            st.rerun()

                if all(r["status"] != "SEGUNDA_CONTAGEM" for r in inv["rows"]):
                    inv["status"] = "AGUARDANDO ANÁLISE 2"
                    st.rerun()

            elif profile == "Gestor" and inv["status"] == "AGUARDANDO ANÁLISE 2":
                st.markdown("#### Análise da 2ª contagem")
                unit_price_map = st.session_state.db_df.set_index("codigo")["ultimo_preco"].to_dict()
                pending_audit = False
                for i, row in enumerate(inv["rows"]):
                    if row["status"] != "SEGUNDA_CONTAGEM_FEITA": continue
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Sistema", format_number(row["qtd_sistema"]))
                    c2.metric("1ª", format_number(row["primeira_contagem"]))
                    c3.metric("2ª", format_number(row["segunda_contagem"]))
                    c4.metric("Valor 1ª", format_brl(abs(float(row["primeira_contagem"]) - float(row["qtd_sistema"])) * float(unit_price_map.get(row["codigo"], 0))))
                    if abs(float(row["segunda_contagem"]) - float(row["primeira_contagem"])) < 1e-9:
                        st.success(f"{row['codigo']} / {row['endereco']}: 2ª contagem igual à 1ª — erro de inventário cravado.")
                        row["contagem_final"] = row["primeira_contagem"]
                        row["resultado_final"] = "ERRO DE INVENTÁRIO"
                    elif abs(float(row["segunda_contagem"]) - float(row["qtd_sistema"])) < 1e-9:
                        st.success(f"{row['codigo']} / {row['endereco']}: 2ª contagem bate com o sistema.")
                        row["contagem_final"] = row["segunda_contagem"]
                        row["resultado_final"] = "SISTEMA CONFIRMADO"
                    else:
                        pending_audit = True
                        st.warning(f"{row['codigo']} / {row['endereco']}: 1ª, 2ª e sistema são diferentes.")
                        choice = st.selectbox("Decisão do gestor", ["Fechar com 1ª", "Fechar com 2ª", "Solicitar auditoria"], key=f"dec_{doc}_{i}")
                        if choice == "Solicitar auditoria":
                            row["status"] = "AUDITORIA"
                        elif choice == "Fechar com 1ª":
                            row["contagem_final"] = row["primeira_contagem"]; row["resultado_final"] = "FECHADO COM 1ª"
                        else:
                            row["contagem_final"] = row["segunda_contagem"]; row["resultado_final"] = "FECHADO COM 2ª"
                if not pending_audit and all(r["contagem_final"] is not None for r in inv["rows"]):
                    if st.button("Fechar Inventário", type="primary"):
                        inv["status"] = "FECHADO"; st.rerun()
                elif any(r["status"] == "AUDITORIA" for r in inv["rows"]):
                    if st.button("Enviar itens para auditoria"):
                        inv["status"] = "AUDITORIA"; st.rerun()

            elif profile == "Gestor" and inv["status"] == "AUDITORIA":
                st.markdown("#### Auditoria / 3ª contagem")
                for i, row in enumerate(inv["rows"]):
                    if row["status"] != "AUDITORIA": continue
                    with st.container(border=True):
                        st.markdown(f"**{row['codigo']} — {row['endereco']}**")
                        st.write(row["descricao"])
                        c1, c2 = st.columns(2)
                        c1.metric("Sistema", format_number(row["qtd_sistema"]))
                        c2.metric("1ª / 2ª", f"{format_number(row['primeira_contagem'])} / {format_number(row['segunda_contagem'])}")
                        count3 = st.number_input("3ª contagem / auditoria", min_value=0.0, step=0.001, format="%.3f", key=f"c3_{doc}_{i}")
                        comment3 = st.text_input("Comentário da auditoria (opcional)", key=f"cm3_{doc}_{i}")
                        if st.button("Salvar auditoria", key=f"save3_{doc}_{i}", type="primary"):
                            row["terceira_contagem"] = float(count3)
                            row["comentario_3"] = comment3.strip() if comment3.strip() else "SC"
                            row["contagem_final"] = float(count3)
                            row["comentario_final"] = row["comentario_3"]
                            row["resultado_final"] = "AUDITORIA"
                            row["status"] = "AUDITORIA_FEITA"
                            st.rerun()
                if all(r["status"] != "AUDITORIA" for r in inv["rows"]):
                    if st.button("Fechar Inventário após auditoria", type="primary"):
                        inv["status"] = "FECHADO"; st.rerun()

            elif inv["status"] == "FECHADO":
                st.success("Inventário fechado e pronto para registro histórico.")
                df = all_inventory_rows_dataframe(inv)
                if not df.empty:
                    view = df[["codigo","descricao","endereco","qtd_sistema","primeira_contagem","segunda_contagem","terceira_contagem","contagem_final","comentario_final","resultado_final"]].copy()
                    view.columns = ["Código","Descrição","Endereço","Qtd. Sistema","1ª Contagem","2ª Contagem","3ª Contagem","Contagem Final","Comentário","Resultado"]
                    st.dataframe(view, use_container_width=True, hide_index=True)

# ============================================================
# BANCO DE DADOS
# ============================================================
if active == "Banco de Dados":
    st.subheader(config["database_title"])
    if config["database_subtitle"]: st.caption(config["database_subtitle"])
    st.write("Importe os dois relatórios oficiais. O cruzamento é feito pelo **código do produto** e os números respeitam as casas decimais do relatório.")
    col1, col2 = st.columns(2)
    with col1:
        cad_file = st.file_uploader(config["upload_cadastro_label"], type=["xlsx","xlsm","xltx"], key="cad_upload", help="B=Código, C=Descrição e H=Último Preço.")
        if cad_file:
            try:
                st.session_state.cad_df = read_excel_file(cad_file); st.session_state.cad_name = cad_file.name
                st.success(f"Carregado: {cad_file.name}"); st.caption(f"{len(st.session_state.cad_df):,} linhas".replace(",", "."))
            except Exception as e: st.error(f"Não foi possível ler o cadastro: {e}")
    with col2:
        end_file = st.file_uploader(config["upload_endereco_label"], type=["xlsx","xlsm","xltx"], key="end_upload", help="A=Código, D=Endereço e H=Quantidade. Lote ignorado.")
        if end_file:
            try:
                st.session_state.end_df = read_excel_file(end_file); st.session_state.end_name = end_file.name
                st.success(f"Carregado: {end_file.name}"); st.caption(f"{len(st.session_state.end_df):,} linhas".replace(",", "."))
            except Exception as e: st.error(f"Não foi possível ler o endereço: {e}")

    if st.session_state.cad_df is not None and st.session_state.end_df is not None:
        st.divider(); st.subheader(config["address_title"])
        raw_addresses = normalize_address(st.session_state.end_df.iloc[:, 3])
        addresses = sorted([x for x in raw_addresses.unique() if x])
        if not st.session_state.eligible_addresses: st.session_state.eligible_addresses = addresses.copy()
        selected = st.multiselect("Selecione os endereços que DEVEM entrar no saldo inventariável:", options=addresses,
                                  default=[x for x in st.session_state.eligible_addresses if x in addresses],
                                  help="Endereços não selecionados continuam no relatório, mas não entram no saldo apto.")
        st.session_state.eligible_addresses = selected
        a, b = st.columns(2); a.metric("Endereços encontrados", len(addresses)); b.metric("Endereços aptos", len(selected))
        if st.button(config["process_database_text"], type="primary"):
            try:
                db, positions = build_database(st.session_state.cad_df, st.session_state.end_df, st.session_state.eligible_addresses)
                st.session_state.db_df = db; st.session_state.positions_df = positions
                st.session_state.inventories = {}; st.session_state.product_count_cycles = {}
                st.success("Banco consolidado atualizado com sucesso. Valores numéricos preservados.")
            except Exception as e: st.error(f"Erro no processamento: {e}")

    if st.session_state.db_df is not None:
        st.divider(); st.subheader(config["database_consolidated_title"])
        db_view = st.session_state.db_df.copy()
        db_view["ultimo_preco"] = db_view["ultimo_preco"].map(format_brl)
        db_view["saldo_apto"] = db_view["saldo_apto"].map(lambda x: format_number(x, 3))
        db_view["valor_total"] = db_view["valor_total"].map(format_brl)
        db_view.columns = ["Código","Descrição","Último Preço","Saldo Apto","Valor Total","Classificação R$ UN.","Classificação R$ TOTAL"]
        st.dataframe(db_view, use_container_width=True, hide_index=True, height=500)
        csv = st.session_state.db_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(config["export_database_text"], data=csv, file_name=f"banco_consolidado_{datetime.now():%Y%m%d_%H%M%S}.csv", mime="text/csv")
        st.caption("Regra: produto + endereço são consolidados; lotes diferentes no mesmo endereço são somados. Ex.: 613,48 permanece 613,48 e 110,135 permanece 110,135.")

# ============================================================
# REGISTRO
# ============================================================
if active == "Registro":
    st.subheader(config["register_title"])
    if config["register_subtitle"]: st.caption(config["register_subtitle"])
    records = []
    for inv in st.session_state.inventories.values():
        if inv["status"] != "FECHADO": continue
        for r in inv["rows"]:
            records.append({
                "Documento": inv["documento"], "Data": inv["data"], "Responsável": inv["responsavel"],
                "Ciclo": inv["ciclo"], "Código": r["codigo"], "Descrição": r["descricao"], "Endereço": r["endereco"],
                "Qtd. Sistema": r["qtd_sistema"], "1ª Contagem": r["primeira_contagem"], "2ª Contagem": r["segunda_contagem"],
                "3ª Contagem": r["terceira_contagem"], "Contagem Final": r["contagem_final"], "Resultado": r["resultado_final"],
                "Comentário": r["comentario_final"], "Valor Furo": r["valor_furo"],
            })
    if records:
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("Exportar Registro CSV", df.to_csv(index=False).encode("utf-8-sig"), f"registro_inventarios_{datetime.now():%Y%m%d_%H%M%S}.csv", "text/csv")
    else:
        st.info("Nenhum inventário fechado nesta sessão.")

# ============================================================
# CONFIGURAÇÕES
# ============================================================
if active == "Configurações":
    st.subheader(config["settings_title"])
    st.caption("A configuração visual é separada por modo. As alterações ficam na sessão atual até conectarmos o armazenamento permanente.")

    with st.expander("01 · TEMA E CONTRASTE", expanded=True):
        theme = st.radio("Modo de tela", ["Dark", "Clean"], index=0 if config["theme_mode"] == "Dark" else 1, horizontal=True)
        if theme != config["theme_mode"]:
            config["theme_mode"] = theme; st.rerun()
        st.caption("Dark = fundo escuro + textos claros. Clean = fundo claro + textos escuros.")

    with st.expander("02 · TIPOGRAFIA", expanded=True):
        fonts = ["Arial","Inter","Roboto","Poppins","Montserrat","Georgia","Verdana","Trebuchet MS"]
        f1, f2 = st.columns(2)
        config["font_family"] = f1.selectbox("Tipo de letra", fonts, index=fonts.index(config["font_family"]))
        config["font_size"] = f2.slider("Tamanho geral", 12, 22, int(config["font_size"]), 1)
        config["title_size"] = st.slider("Tamanho do título principal", 22, 48, int(config["title_size"]), 1)

    with st.expander("03 · CORES", expanded=True):
        c1, c2 = st.columns(2); config["primary_color"] = c1.color_picker("Cor principal / destaque", config["primary_color"]); config["primary_hover"] = c2.color_picker("Cor ao passar mouse", config["primary_hover"])
        if config["theme_mode"] == "Dark":
            c1, c2 = st.columns(2); config["background_dark"] = c1.color_picker("Fundo Dark", config["background_dark"]); config["panel_dark"] = c2.color_picker("Cards / painéis Dark", config["panel_dark"])
            c1, c2 = st.columns(2); config["panel_dark_2"] = c1.color_picker("Painel secundário Dark", config["panel_dark_2"]); config["border_dark"] = c2.color_picker("Bordas Dark", config["border_dark"])
            c1, c2 = st.columns(2); config["text_dark"] = c1.color_picker("Texto Dark", config["text_dark"]); config["muted_dark"] = c2.color_picker("Texto secundário Dark", config["muted_dark"])
        else:
            c1, c2 = st.columns(2); config["background_clean"] = c1.color_picker("Fundo Clean", config["background_clean"]); config["panel_clean"] = c2.color_picker("Cards / painéis Clean", config["panel_clean"])
            c1, c2 = st.columns(2); config["panel_clean_2"] = c1.color_picker("Painel secundário Clean", config["panel_clean_2"]); config["border_clean"] = c2.color_picker("Bordas Clean", config["border_clean"])
            c1, c2 = st.columns(2); config["text_clean"] = c1.color_picker("Texto Clean", config["text_clean"]); config["muted_clean"] = c2.color_picker("Texto secundário Clean", config["muted_clean"])

    with st.expander("04 · LOGO / IDENTIDADE", expanded=True):
        logo_file = st.file_uploader("Enviar logo da empresa", type=["png","jpg","jpeg","webp","svg"], key="company_logo")
        if logo_file:
            st.session_state.logo_bytes = logo_file.getvalue(); st.session_state.logo_name = logo_file.name
        c1, c2, c3 = st.columns(3)
        config["sidebar_logo_width"] = c1.slider("Largura da logo", 80, 300, int(config["sidebar_logo_width"]), 5)
        config["sidebar_logo_height"] = c2.slider("Altura da logo", 40, 150, int(config["sidebar_logo_height"]), 5)
        config["sidebar_logo_align"] = c3.selectbox("Alinhamento da logo", ["left","center","right"], index=["left","center","right"].index(config["sidebar_logo_align"]))
        if st.session_state.logo_bytes:
            st.image(st.session_state.logo_bytes, caption="Pré-visualização", width=min(config["sidebar_logo_width"], 300))
            if st.button("Remover logo"):
                st.session_state.logo_bytes = None; st.session_state.logo_name = ""; st.rerun()

    with st.expander("05 · MENU LATERAL", expanded=True):
        c1, c2 = st.columns(2)
        config["menu_label"] = c1.text_input("Título do menu", config["menu_label"])
        config["sidebar_subtitle"] = c2.text_input("Subtítulo da lateral", config["sidebar_subtitle"])
        c1, c2 = st.columns(2); config["sidebar_align"] = c1.selectbox("Alinhamento dos tópicos", ["left","center","right"], index=["left","center","right"].index(config["sidebar_align"]))
        config["sidebar_font_size"] = c2.slider("Tamanho da letra dos tópicos", 10, 20, int(config["sidebar_font_size"]), 1)
        config["sidebar_item_height"] = st.slider("Altura dos botões", 30, 60, int(config["sidebar_item_height"]), 1)
        c1, c2 = st.columns(2)
        config["dashboard_label"] = c1.text_input("Dashboard", config["dashboard_label"])
        config["inventory_label"] = c2.text_input("Inventário", config["inventory_label"])
        c1, c2 = st.columns(2)
        config["database_label"] = c1.text_input("Banco de Dados", config["database_label"])
        config["register_label"] = c2.text_input("Registro", config["register_label"])
        config["settings_label"] = st.text_input("Configurações", config["settings_label"])

    with st.expander("06 · TEXTOS DAS PÁGINAS", expanded=False):
        fields = [("app_title","Título principal"),("app_subtitle","Subtítulo principal"),("footer_text","Rodapé"),("dashboard_title","Título do Dashboard"),("dashboard_subtitle","Subtítulo do Dashboard"),("inventory_title","Título do Inventário"),("inventory_subtitle","Subtítulo do Inventário"),("database_title","Título do Banco de Dados"),("database_subtitle","Subtítulo do Banco de Dados"),("register_title","Título do Registro"),("register_subtitle","Subtítulo do Registro"),("address_title","Título da configuração de endereços"),("database_consolidated_title","Título do banco consolidado")]
        for i in range(0, len(fields), 2):
            cols = st.columns(2)
            for col, (key, label) in zip(cols, fields[i:i+2]): config[key] = col.text_input(label, config[key], key=f"cfg_{key}")

    with st.expander("07 · BOTÕES E INVENTÁRIO", expanded=True):
        config["new_inventory_text"] = st.text_input("Botão Novo Inventário", config["new_inventory_text"])
        config["process_database_text"] = st.text_input("Botão Processar Banco", config["process_database_text"])
        config["export_database_text"] = st.text_input("Botão Exportar Banco", config["export_database_text"])
        config["inventory_default_blind"] = st.checkbox("Usar contagem cega por padrão", value=bool(config["inventory_default_blind"]))
        st.caption("A contagem cega pode ser alterada ao criar cada inventário.")

    with st.expander("08 · DIMENSIONAMENTO", expanded=False):
        config["sidebar_width"] = st.slider("Largura do menu lateral", 220, 360, int(config["sidebar_width"]), 5)
        config["show_footer"] = st.checkbox("Exibir rodapé no menu", value=bool(config["show_footer"]))

    st.divider()
    c1, c2 = st.columns(2)
    if c1.button("Aplicar alterações visuais", type="primary", use_container_width=True): st.rerun()
    if c2.button("Restaurar configuração padrão", use_container_width=True):
        st.session_state.ui_config = DEFAULT_CONFIG.copy(); st.session_state.logo_bytes = None; st.session_state.logo_name = ""; st.rerun()
