from pathlib import Path
p=Path('app.py')
s=p.read_text(encoding='utf-8')
# 1) Remove the width override entirely so Streamlit's native collapse/expand control owns sidebar geometry.
s=s.replace("section[data-testid=\"stSidebar\"]{{background:var(--bg);border-right:1px solid var(--border)}}section[data-testid=\"stSidebar\"][aria-expanded=\"true\"]{{width:{cfg['sidebar_width']}px!important}}section[data-testid=\"stSidebar\"]>div{{padding-top:.25rem!important}}", "section[data-testid=\"stSidebar\"]{{background:var(--bg);border-right:1px solid var(--border)}}section[data-testid=\"stSidebar\"]>div{{padding-top:.25rem!important}}")
# 2) Replace sidebar nav with normal items first, then a separated report item near the bottom, with Configurations kept in the main group.
old=''' nav=[('Dashboard',f'▦  {config["dashboard_label"]}'),('Inventário Rotativo',f'✎  {config["inventory_label"]}'),('Banco de Dados',f'▣  {config["database_label"]}'),('Registro',f'◷  {config["register_label"]}'),('Reportar Inconsistências',f'⚠  {config["report_label"]}'),('Configurações',f'⚙  {config["settings_label"]}')]\n\n tops={'Dashboard':cfg['dash_top'],'Inventário Rotativo':cfg['inv_top'],'Banco de Dados':cfg['db_top'],'Registro':cfg['reg_top'],'Reportar Inconsistências':cfg.get('report_top',0),'Configurações':cfg['settings_top']}\n for k,l in nav:\n  off=tops.get(k,0)\n  st.markdown(f'<div style=\"height:0;margin-top:{off}px\"></div>',unsafe_allow_html=True)\n  if st.button(l,key='nav_'+k,type='primary' if st.session_state.section==k else 'secondary'):st.session_state.section=k;st.rerun()\n'''
new=''' nav=[('Dashboard',f'▦  {config["dashboard_label"]}'),('Inventário Rotativo',f'✎  {config["inventory_label"]}'),('Banco de Dados',f'▣  {config["database_label"]}'),('Registro',f'◷  {config["register_label"]}'),('Configurações',f'⚙  {config["settings_label"]}')]\n tops={'Dashboard':cfg['dash_top'],'Inventário Rotativo':cfg['inv_top'],'Banco de Dados':cfg['db_top'],'Registro':cfg['reg_top'],'Configurações':cfg['settings_top']}\n for k,l in nav:\n  off=tops.get(k,0)\n  st.markdown(f'<div style=\"height:0;margin-top:{off}px\"></div>',unsafe_allow_html=True)\n  if st.button(l,key='nav_'+k,type='primary' if st.session_state.section==k else 'secondary'):st.session_state.section=k;st.rerun()\n # Reportes ficam em uma área visualmente segregada, no rodapé da barra lateral.\n st.markdown('<div class=\"sidebar-report-spacer\"></div>',unsafe_allow_html=True)\n st.markdown(f'<div class=\"sidebar-report-area\"><div class=\"sidebar-report-caption\">CONTROLE DE INCONSISTÊNCIAS</div>',unsafe_allow_html=True)\n off=cfg.get('report_top',0)\n st.markdown(f'<div style=\"height:0;margin-top:{off}px\"></div>',unsafe_allow_html=True)\n if st.button(f'⚠  {config["report_label"]}',key='nav_Reportar Inconsistências',type='primary' if st.session_state.section=='Reportar Inconsistências' else 'secondary'):\n  st.session_state.section='Reportar Inconsistências';st.rerun()\n st.markdown('</div>',unsafe_allow_html=True)\n'''
if old not in s:
 raise SystemExit('sidebar nav block not found')
s=s.replace(old,new)
# 3) Make the new report area and spacer configurable while preserving existing menu-gap setting.
needle='section[data-testid="stSidebar"] .stButton{margin-bottom:{cfg.get(\'menu_gap\',8)}px}'
replacement='section[data-testid="stSidebar"] .stButton{margin-bottom:{cfg.get(\'menu_gap\',8)}px}.sidebar-report-spacer{{height:clamp(28px,18vh,150px)}}.sidebar-report-area{{border-top:1px solid var(--border);padding-top:12px;margin:0 7px}}.sidebar-report-area .stButton{{margin-left:-7px;margin-right:-7px}}.sidebar-report-caption{{color:var(--muted);font-size:10px;font-weight:800;letter-spacing:.6px;margin:0 0 6px}}'
if needle not in s:
 raise SystemExit('css needle not found')
s=s.replace(needle,replacement)
# 4) Keep a compatibility setting for sidebar width, but do not use it to break native collapse.
p.write_text(s,encoding='utf-8')
print('sidebar v2 patched')
