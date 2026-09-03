from pathlib import Path
p=Path('app.py')
s=p.read_text(encoding='utf-8')

# Sidebar: robust professional buttons, separated report area lower down, and native collapse control kept clickable.
old_css="section[data-testid=\"stSidebar\"]{{background:var(--bg);border-right:1px solid var(--border)}}section[data-testid=\"stSidebar\"]>div{{padding-top:.25rem!important}}"
new_css="section[data-testid=\"stSidebar\"]{{background:var(--bg);border-right:1px solid var(--border)}}section[data-testid=\"stSidebar\"]>div{{padding-top:.25rem!important}}section[data-testid=\"stSidebar\"] button[aria-label*='Collapse'],section[data-testid=\"stSidebar\"] button[aria-label*='Expand'],header button[aria-label*='Collapse'],header button[aria-label*='Expand']{{position:relative!important;z-index:99999!important;pointer-events:auto!important}}.logo-area{{pointer-events:none!important;position:relative;z-index:0}}"
if old_css not in s: raise SystemExit('css anchor not found')
s=s.replace(old_css,new_css,1)

old_buttons="section[data-testid=\"stSidebar\"] .stButton{{margin-bottom:{cfg.get('menu_gap',8)}px}}section[data-testid=\"stSidebar\"] .stButton>button{{width:100%;min-height:{cfg['item_h']}px;border:0;background:transparent;color:var(--muted);text-align:{cfg['sidebar_align']};justify-content:{'flex-start' if cfg['sidebar_align']=='left' else 'center' if cfg['sidebar_align']=='center' else 'flex-end'};font-size:{cfg['sidebar_font']}px;font-weight:800;border-radius:9px}}section[data-testid=\"stSidebar\"] .stButton>button:hover{{background:var(--p2);color:var(--text)}}section[data-testid=\"stSidebar\"] .stButton>button[kind=\"primary\"]{{background:var(--p);color:#11130F}}section[data-testid=\"stSidebar\"] .stButton>button::first-letter{{color:{cfg['icon_color']}}}"
new_buttons="section[data-testid=\"stSidebar\"] .stButton{{margin-bottom:{cfg.get('menu_gap',8)}px}}section[data-testid=\"stSidebar\"] .stButton>button{{width:100%;min-height:{cfg['item_h']}px;border:1px solid var(--border);background:var(--panel);color:var(--text);text-align:{cfg['sidebar_align']};justify-content:{'flex-start' if cfg['sidebar_align']=='left' else 'center' if cfg['sidebar_align']=='center' else 'flex-end'};font-size:{cfg['sidebar_font']}px;font-weight:800;border-radius:9px;padding:0 14px;box-shadow:0 1px 3px rgba(0,0,0,.18)}}section[data-testid=\"stSidebar\"] .stButton>button:hover{{background:var(--p2);color:var(--text);border-color:var(--p)}}section[data-testid=\"stSidebar\"] .stButton>button[kind=\"primary\"]{{background:var(--p);color:#11130F;border-color:var(--p);box-shadow:0 2px 7px rgba(0,0,0,.22)}}section[data-testid=\"stSidebar\"] .stButton>button::first-letter{{color:{cfg['icon_color']}}}"
if old_buttons not in s: raise SystemExit('button css anchor not found')
s=s.replace(old_buttons,new_buttons,1)

# Make all Streamlit Vega charts use the configured primary yellow.
chart_css="[data-testid=\"stVegaLiteChart\"] svg rect[fill]{{fill:var(--p)!important}}[data-testid=\"stVegaLiteChart\"] svg path[fill]{{fill:var(--p)!important}}[data-testid=\"stVegaLiteChart\"] svg rect[stroke]{{stroke:var(--p)!important}}"
needle="[data-testid=\"stDataFrame\"]{{border:1px solid var(--border);border-radius:10px;overflow:hidden}}"
if needle not in s: raise SystemExit('chart css anchor not found')
s=s.replace(needle,needle+chart_css,1)

# Replace separated report block: no caption/text, lower position.
s=s.replace("st.markdown('<div class=\"sidebar-report-spacer\"></div>',unsafe_allow_html=True)\nst.markdown('<div class=\"sidebar-report-caption\">CONTROLE DE INCONSISTÊNCIAS</div>',unsafe_allow_html=True)\noff=cfg.get('report_top',0)","st.markdown('<div class=\"sidebar-report-spacer\"></div>',unsafe_allow_html=True)\noff=cfg.get('report_top',0)",1)

s=s.replace("section[data-testid=\"stSidebar\"] .sidebar-report-spacer{{height:clamp(70px,24vh,230px)}}section[data-testid=\"stSidebar\"] .sidebar-report-caption{{color:var(--muted);font-size:10px;font-weight:800;letter-spacing:.6px;margin:0 7px 5px;border-top:1px solid var(--border);padding-top:10px}}","section[data-testid=\"stSidebar\"] .sidebar-report-spacer{{height:clamp(140px,34vh,320px)}}section[data-testid=\"stSidebar\"] .sidebar-report-area{{margin:0 7px}}",1)

p.write_text(s,encoding='utf-8')
print('UI v4 patch complete')
