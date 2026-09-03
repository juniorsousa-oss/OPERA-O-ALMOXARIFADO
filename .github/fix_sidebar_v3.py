from pathlib import Path
p=Path('app.py')
s=p.read_text(encoding='utf-8')
# Remove custom width override so Streamlit native collapse/expand remains authoritative.
old_width="section[data-testid=\"stSidebar\"]{{background:var(--bg);border-right:1px solid var(--border)}}section[data-testid=\"stSidebar\"][aria-expanded=\"true\"]{{width:{cfg['sidebar_width']}px!important}}section[data-testid=\"stSidebar\"]>div{{padding-top:.25rem!important}}"
new_width="section[data-testid=\"stSidebar\"]{{background:var(--bg);border-right:1px solid var(--border)}}section[data-testid=\"stSidebar\"]>div{{padding-top:.25rem!important}}"
s=s.replace(old_width,new_width)
s=s.replace("section[data-testid=\"stSidebar\"][aria-expanded=\"true\"]{{width:{cfg['sidebar_width']}px!important}}","")
# Move Reportar Inconsistências out of the main nav group and render it after a large flexible spacer.
start=s.find(" nav=[('Dashboard'")
end=s.find("st.markdown(f'<div class=\"main-title\">", start)
if start==-1 or end==-1:
    raise SystemExit('sidebar navigation anchors not found')
new_nav=''' nav=[('Dashboard',f'▦  {config["dashboard_label"]}'),('Inventário Rotativo',f'✎  {config["inventory_label"]}'),('Banco de Dados',f'▣  {config["database_label"]}'),('Registro',f'◷  {config["register_label"]}'),('Configurações',f'⚙  {config["settings_label"]}')]\n tops={'Dashboard':cfg['dash_top'],'Inventário Rotativo':cfg['inv_top'],'Banco de Dados':cfg['db_top'],'Registro':cfg['reg_top'],'Configurações':cfg['settings_top']}\n for k,l in nav:\n  off=tops.get(k,0)\n  st.markdown(f'<div style="height:0;margin-top:{off}px"></div>',unsafe_allow_html=True)\n  if st.button(l,key='nav_'+k,type='primary' if st.session_state.section==k else 'secondary'):st.session_state.section=k;st.rerun()\n st.markdown('<div class="sidebar-report-spacer"></div>',unsafe_allow_html=True)\n st.markdown('<div class="sidebar-report-caption">CONTROLE DE INCONSISTÊNCIAS</div>',unsafe_allow_html=True)\n off=cfg.get('report_top',0)\n st.markdown(f'<div style="height:0;margin-top:{off}px"></div>',unsafe_allow_html=True)\n if st.button(f'⚠  {config["report_label"]}',key='nav_Reportar Inconsistências',type='primary' if st.session_state.section=='Reportar Inconsistências' else 'secondary'):\n  st.session_state.section='Reportar Inconsistências';st.rerun()\n\n'''
s=s[:start]+new_nav+s[end:]
# Dedicated visual separator/spacer. Insert directly before </style> to avoid dependence on the exact button CSS string.
css_add='section[data-testid="stSidebar"] .sidebar-report-spacer{{height:clamp(70px,24vh,230px)}}section[data-testid="stSidebar"] .sidebar-report-caption{{color:var(--muted);font-size:10px;font-weight:800;letter-spacing:.6px;margin:0 7px 5px;border-top:1px solid var(--border);padding-top:10px}}'
if css_add not in s:
    s=s.replace('</style>',css_add+'</style>')
p.write_text(s,encoding='utf-8')
print('patched sidebar v3')
