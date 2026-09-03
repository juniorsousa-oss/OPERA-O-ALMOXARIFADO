from pathlib import Path
p=Path('app.py');s=p.read_text(encoding='utf-8')
# Keep native Streamlit collapse control functional: apply custom width only while expanded.
s=s.replace("section[data-testid=\"stSidebar\"]{{background:var(--bg);border-right:1px solid var(--border);width:{cfg['sidebar_width']}px!important}}section[data-testid=\"stSidebar\"]>div{{padding-top:.25rem!important}}", "section[data-testid=\"stSidebar\"]{{background:var(--bg);border-right:1px solid var(--border)}}section[data-testid=\"stSidebar\"][aria-expanded=\"true\"]{{width:{cfg['sidebar_width']}px!important}}section[data-testid=\"stSidebar\"]>div{{padding-top:.25rem!important}}")
# Make every menu item, including the long Reportar item, obey the same alignment and add configurable inter-button spacing.
old="section[data-testid=\"stSidebar\"] .stButton>button{{width:100%;min-height:{cfg['item_h']}px;border:0;background:transparent;color:var(--muted);text-align:{cfg['sidebar_align']};font-size:{cfg['sidebar_font']}px;font-weight:800;border-radius:9px}}"
new="section[data-testid=\"stSidebar\"] .stButton{{margin-bottom:{cfg.get('menu_gap',8)}px}}section[data-testid=\"stSidebar\"] .stButton>button{{width:100%;min-height:{cfg['item_h']}px;border:0;background:transparent;color:var(--muted);text-align:{cfg['sidebar_align']};justify-content:{'flex-start' if cfg['sidebar_align']=='left' else 'center' if cfg['sidebar_align']=='center' else 'flex-end'};font-size:{cfg['sidebar_font']}px;font-weight:800;border-radius:9px}}"
s=s.replace(old,new)
# Persisted configs need a default for the new spacing control.
s=s.replace("'sidebar_width':250,", "'sidebar_width':250,'menu_gap':8,")
s=s.replace("'sidebar_width':250,\n}", "'sidebar_width':250,\n    'menu_gap':8,\n}")
# Add the new setting to the existing sidebar controls and make Report position independently configurable.
old2="cfg['gap']=st.slider('Espaço antes do MENU',0,60,cfg['gap']);cfg['sidebar_align']="
new2="cfg['gap']=st.slider('Espaço antes do MENU',0,60,cfg['gap']);cfg['menu_gap']=st.slider('Espaçamento entre botões do menu',0,40,cfg.get('menu_gap',8));cfg['sidebar_align']="
s=s.replace(old2,new2)
old3="a,b=st.columns(2);cfg['db_top']=a.slider('Banco — posição',-30,50,cfg['db_top']);cfg['reg_top']=b.slider('Registro — posição',-30,50,cfg['reg_top']);cfg['settings_top']=st.slider('Configurações — posição',-30,50,cfg['settings_top'])"
new3="a,b=st.columns(2);cfg['db_top']=a.slider('Banco — posição',-30,50,cfg['db_top']);cfg['reg_top']=b.slider('Registro — posição',-30,50,cfg['reg_top']);a,b=st.columns(2);cfg['report_top']=a.slider('Reportar Inconsistências — posição',-30,50,cfg.get('report_top',0));cfg['settings_top']=b.slider('Configurações — posição',-30,50,cfg['settings_top'])"
s=s.replace(old3,new3)
p.write_text(s,encoding='utf-8')
print('patched', 'aria' in s, "menu_gap" in s, "report_top" in s)
