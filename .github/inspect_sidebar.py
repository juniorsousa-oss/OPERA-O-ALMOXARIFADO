from pathlib import Path
s=Path('app.py').read_text(encoding='utf-8')
for key in ['with st.sidebar:', 'REPORTAR INCONSISTÊNCIAS', 'sidebar_width']:
 print('\n###',key)
 i=s.find(key)
 print('INDEX',i)
 if i>=0: print(s[max(0,i-1800):i+5000])
