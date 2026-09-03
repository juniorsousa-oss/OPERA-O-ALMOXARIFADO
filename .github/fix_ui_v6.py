from pathlib import Path
p=Path('app.py')
s=p.read_text(encoding='utf-8')
# 1) Dashboard chart colors: yellow bars, dark/transparent background, white gridlines.
s=s.replace("color=alt.Color('Status:N',scale=alt.Scale(domain=['Sem divergência','Com divergência'],range=['#FFD63B','#D95C5C']),legend=None),\n    tooltip=", "color=alt.value('#FFD63B'),\n    tooltip=", 1)
s=s.replace("color=alt.Color('Status:N',scale=alt.Scale(domain=['Contabilizadas','Divergentes'],range=['#FFD63B','#D95C5C']),legend=alt.Legend(title=None,orient='bottom')),\n     tooltip=", "color=alt.value('#FFD63B'),\n     tooltip=", 1)
s=s.replace("y=alt.Y('Quantidade:Q',axis=alt.Axis(title=None,grid=True)),", "y=alt.Y('Quantidade:Q',axis=alt.Axis(title=None,grid=True,gridColor='#FFFFFF',gridOpacity=0.28,tickColor='#FFFFFF',labelColor='#FFFFFF')),", 1)
s=s.replace("y=alt.Y('Quantidade:Q',axis=alt.Axis(title=None,grid=True)),", "y=alt.Y('Quantidade:Q',axis=alt.Axis(title=None,grid=True,gridColor='#FFFFFF',gridOpacity=0.28,tickColor='#FFFFFF',labelColor='#FFFFFF')),", 1)
s=s.replace(").properties(height=260)\n   st.altair_chart(chart1", ").properties(height=260,background='transparent')\n   st.altair_chart(chart1", 1)
s=s.replace(").properties(height=260)\n    st.altair_chart(chart2", ").properties(height=260,background='transparent')\n    st.altair_chart(chart2", 1)
# Remove old generic Vega CSS that forced every chart mark to yellow and could override chart styling.
s=s.replace("[data-testid=\"stVegaLiteChart\"] svg rect[fill]{{fill:var(--p)!important}}[data-testid=\"stVegaLiteChart\"] svg path[fill]{{fill:var(--p)!important}}[data-testid=\"stVegaLiteChart\"] svg rect[stroke]{{stroke:var(--p)!important}}", "")
# 2) Reduce main menu gaps further.
s=s.replace("'sidebar_width':250,'menu_gap':8", "'sidebar_width':250,'menu_gap':2", 1)
s=s.replace("'sidebar_width':250,'menu_gap':8,", "'sidebar_width':250,'menu_gap':2,", 1)
s=s.replace("margin-bottom:{cfg.get('menu_gap',4)}px", "margin-bottom:{cfg.get('menu_gap',2)}px", 1)
# 3) Keep report button separated, pin it near bottom without creating a scroll area, and remove spacer/title.
s=s.replace("section[data-testid=\"stSidebar\"]>div{{padding-top:.25rem!important}}", "section[data-testid=\"stSidebar\"]>div{{padding-top:.25rem!important;position:relative!important}}", 1)
s=s.replace("section[data-testid=\"stSidebar\"] .sidebar-report-spacer{{height:clamp(60px,10vh,90px)}}section[data-testid=\"stSidebar\"] .sidebar-report-area{{margin:0 7px}}", "section[data-testid=\"stSidebar\"] .sidebar-report-spacer{{display:none!important}}section[data-testid=\"stSidebar\"] .sidebar-report-area{{position:absolute;left:10px;right:10px;bottom:18px;margin:0;z-index:20}}section[data-testid=\"stSidebar\"] .sidebar-report-area .stButton{{margin-bottom:0!important}}", 1)
old=" st.markdown('<div class=\"sidebar-report-spacer\"></div>',unsafe_allow_html=True)\n off=cfg.get('report_top',0)\n st.markdown(f'<div style=\"height:0;margin-top:{off}px\"></div>',unsafe_allow_html=True)\n if st.button(f'⚠  {config[\"report_label\"]}',key='nav_Reportar Inconsistências',type='primary' if st.session_state.section=='Reportar Inconsistências' else 'secondary'):\n  st.session_state.section='Reportar Inconsistências';st.rerun()"
new=" st.markdown('<div class=\"sidebar-report-area\">',unsafe_allow_html=True)\n if st.button(f'⚠  {config[\"report_label\"]}',key='nav_Reportar Inconsistências',type='primary' if st.session_state.section=='Reportar Inconsistências' else 'secondary'):\n  st.session_state.section='Reportar Inconsistências';st.rerun()\n st.markdown('</div>',unsafe_allow_html=True)"
if old not in s:
    raise SystemExit('report block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('UI v6 patch complete')
