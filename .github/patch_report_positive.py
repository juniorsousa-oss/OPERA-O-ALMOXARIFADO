from pathlib import Path
p=Path('app.py')
s=p.read_text(encoding='utf-8')
s=s.replace("codes=sorted(st.session_state.db.loc[st.session_state.db.saldo_apto>0,'codigo'].astype(str).unique())", "codes=sorted(st.session_state.db['codigo'].astype(str).unique())")
s=s.replace("df=pd.DataFrame(rows);st.dataframe(df,use_container_width=True,hide_index=True);export_df=df.copy();export_df['Valor Divergência']=export_df['Valor Divergência'].map(signed_brl);st.download_button", "df=pd.DataFrame(rows);display_df=df.copy();display_df['Valor Divergência']=display_df['Valor Divergência'].map(signed_brl);st.dataframe(display_df,use_container_width=True,hide_index=True);export_df=display_df.copy();st.download_button")
p.write_text(s,encoding='utf-8')
print('patched')
