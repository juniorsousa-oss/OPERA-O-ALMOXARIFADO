from pathlib import Path
s=Path('app.py').read_text(encoding='utf-8')
checks=[('expanded width','[aria-expanded=\\"true\\"]' in s),('menu gap','menu_gap' in s),('report position','Reportar Inconsistências — posição' in s),('flex alignment','justify-content:' in s)]
for n,v in checks: print(n, v)
compile(s,'app.py','exec')
print('PYTHON SYNTAX OK')
