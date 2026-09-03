from pathlib import Path
p=Path('app.py')
s=p.read_text(encoding='utf-8')

# Dashboard charts: replace the current chart block robustly by anchors.
start=s.find("  ch1,ch2=st.columns(2)")
end=s.find("\n# Inventory", start)
if start < 0 or end < 0:
    raise SystemExit('dashboard chart anchors not found')
new="""  ch1,ch2=st.columns(2)\n  with ch1:\n   import altair as alt\n   status_df=pd.DataFrame({'Status':['Sem divergência','Com divergência'],'Quantidade':[max(qtd_cnt-qtd_div,0),qtd_div]})\n   chart1=alt.Chart(status_df).mark_bar(cornerRadiusTopLeft=7,cornerRadiusTopRight=7,size=72).encode(\n    x=alt.X('Status:N',sort=['Sem divergência','Com divergência'],axis=alt.Axis(title=None,labelAngle=0)),\n    y=alt.Y('Quantidade:Q',axis=alt.Axis(title=None,grid=True)),\n    color=alt.Color('Status:N',scale=alt.Scale(domain=['Sem divergência','Com divergência'],range=['#FFD63B','#D95C5C']),legend=None),\n    tooltip=[alt.Tooltip('Status:N',title='Status'),alt.Tooltip('Quantidade:Q',title='Posições')]\n   ).properties(height=260)\n   st.altair_chart(chart1,use_container_width=True)\n  with ch2:\n   inv_rows=[]\n   for x in sorted(st.session_state.inventories.values(),key=lambda z:z.get('criado_em','')):\n    total=sum(1 for r in x['rows'] if r['contagens']);dv=sum(1 for r in x['rows'] if r['contagens'] and abs(diff(r,last(r)))>1e-9)\n    if total:inv_rows.extend([{'Inventário':x['documento'],'Status':'Contabilizadas','Quantidade':total},{'Inventário':x['documento'],'Status':'Divergentes','Quantidade':dv}])\n   if inv_rows:\n    chart=pd.DataFrame(inv_rows)\n    chart2=alt.Chart(chart).mark_bar(cornerRadiusTopLeft=5,cornerRadiusTopRight=5,size=26).encode(\n     x=alt.X('Inventário:N',axis=alt.Axis(title=None,labelAngle=-45)),\n     y=alt.Y('Quantidade:Q',axis=alt.Axis(title=None,grid=True)),\n     xOffset=alt.XOffset('Status:N'),\n     color=alt.Color('Status:N',scale=alt.Scale(domain=['Contabilizadas','Divergentes'],range=['#FFD63B','#D95C5C']),legend=alt.Legend(title=None,orient='bottom')),\n     tooltip=[alt.Tooltip('Inventário:N',title='Inventário'),alt.Tooltip('Status:N',title='Status'),alt.Tooltip('Quantidade:Q',title='Posições')]\n    ).properties(height=260)\n    st.altair_chart(chart2,use_container_width=True)\n   else:\n    st.info('Ainda não existem contagens para gerar o gráfico por inventário.')\n"""
s=s[:start]+new+s[end:]

# Reduce the excessive gaps between main menu buttons.
s=s.replace("section[data-testid=\"stSidebar\"] .stButton{{margin-bottom:{cfg.get('menu_gap',8)}px}}","section[data-testid=\"stSidebar\"] .stButton{{margin-bottom:{cfg.get('menu_gap',4)}px}}",1)
# Move the report button upward enough to avoid sidebar scrolling, without bringing it into the main menu.
s=s.replace("section[data-testid=\"stSidebar\"] .sidebar-report-spacer{{height:clamp(140px,34vh,320px)}}","section[data-testid=\"stSidebar\"] .sidebar-report-spacer{{height:clamp(60px,10vh,90px)}}",1)
# Remove the report section title/caption entirely.
s=s.replace(" st.markdown('<div class=\"sidebar-report-spacer\"></div>',unsafe_allow_html=True)\n st.markdown('<div class=\"sidebar-report-caption\">CONTROLE DE INCONSISTÊNCIAS</div>',unsafe_allow_html=True)\n off=cfg.get('report_top',0)"," st.markdown('<div class=\"sidebar-report-spacer\"></div>',unsafe_allow_html=True)\n off=cfg.get('report_top',0)",1)

p.write_text(s,encoding='utf-8')
print('UI v5 patch complete')
