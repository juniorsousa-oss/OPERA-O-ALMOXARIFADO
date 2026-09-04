from pathlib import Path
p=Path('app.py')
s=p.read_text(encoding='utf-8')
s=s.replace('.login-wrap{min-height:0!important;display:flex;align-items:flex-start;justify-content:center;padding-top:12px;margin-bottom:0}', '.login-wrap{min-height:0!important;display:flex;align-items:flex-start;justify-content:center;padding-top:12px;margin-bottom:24px}')
s=s.replace('[class*="st-key-login_form"]{margin-top:10px!important}', '[class*="st-key-login_form"]{margin-top:0!important}')
p.write_text(s,encoding='utf-8')
print('login gap adjusted')
