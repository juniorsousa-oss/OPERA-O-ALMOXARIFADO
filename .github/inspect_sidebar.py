from pathlib import Path
s=Path('app.py').read_text(encoding='utf-8')
for key in ["# Settings", "elif active=='Configurações'", "item_h"]:
 print('\n###',key)
 i=s.find(key)
 print('INDEX',i)
 if i>=0: print(s[max(0,i-2500):i+10000])
