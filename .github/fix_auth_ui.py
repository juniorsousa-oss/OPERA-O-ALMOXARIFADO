from pathlib import Path

p=Path('app.py')
s=p.read_text(encoding='utf-8')

# 1) Add auth imports/session and login gate before the app UI.
old="import os, io, json, base64, pickle, sqlite3, uuid\nfrom datetime import datetime\nimport pandas as pd\nimport streamlit as st\n"
new="import os, io, json, base64, pickle, sqlite3, uuid\nfrom datetime import datetime\nfrom urllib.request import Request, urlopen\nfrom urllib.error import HTTPError, URLError\nimport pandas as pd\nimport streamlit as st\n"
assert old in s
s=s.replace(old,new,1)

marker="for _k, _v in _cfg_defaults.items():\n    config.setdefault(_k, _v)\n    cfg.setdefault(_k, _v)\n\n\ndef persist_cfg():"
insert="""for _k, _v in _cfg_defaults.items():
    config.setdefault(_k, _v)
    cfg.setdefault(_k, _v)

# Authentication: Supabase Auth (email + password). Session remains server-side in Streamlit.
SUPABASE_URL = 'https://cuixazpxkvniqldmmnth.supabase.co'
SUPABASE_KEY = st.secrets.get('SUPABASE_PUBLISHABLE_KEY', st.secrets.get('SUPABASE_ANON_KEY', ''))
if 'auth_user' not in st.session_state: st.session_state.auth_user=None

def auth_login(email, password):
    if not SUPABASE_KEY:
        return None, 'A autenticação ainda não foi configurada no aplicativo.'
    try:
        body=json.dumps({'email':email.strip().lower(),'password':password}).encode('utf-8')
        req=Request(SUPABASE_URL+'/auth/v1/token?grant_type=password',data=body,headers={'apikey':SUPABASE_KEY,'Content-Type':'application/json'},method='POST')
        with urlopen(req,timeout=15) as resp: data=json.loads(resp.read().decode('utf-8'))
        return data, None
    except HTTPError as e:
        try: msg=json.loads(e.read().decode('utf-8')).get('msg') or json.loads(e.read().decode('utf-8')).get('error_description')
        except Exception: msg='Usuário ou senha inválidos.'
        return None, msg or 'Usuário ou senha inválidos.'
    except (URLError, TimeoutError):
        return None, 'Não foi possível conectar ao serviço de autenticação.'
    except Exception:
        return None, 'Não foi possível realizar o login.'

def auth_logout():
    st.session_state.auth_user=None
    st.session_state.pop('auth_access_token',None)
    st.session_state.pop('auth_refresh_token',None)
    st.rerun()

def render_login():
    st.markdown('''<style>
    [data-testid="stHeader"]{background:transparent!important}
    .login-wrap{min-height:78vh;display:flex;align-items:center;justify-content:center}
    .login-card{width:min(440px,92vw);padding:34px 32px 30px;background:#101614;border:1px solid #2B3732;border-radius:18px;box-shadow:0 14px 45px rgba(0,0,0,.35)}
    .login-brand{text-align:center;font-size:34px;font-weight:900;letter-spacing:-1px;color:#F4F5F2;margin-bottom:4px}
    .login-brand span{color:#FFD63B}.login-sub{text-align:center;color:#A9B1AC;font-size:12px;margin-bottom:26px}
    .login-title{text-align:center;color:#F4F5F2;font-size:18px;font-weight:800;margin-bottom:20px}
    </style>''',unsafe_allow_html=True)
    st.markdown('<div class="login-wrap"><div class="login-card"><div class="login-brand">Se<span>tt</span>a</div><div class="login-sub">SISTEMA OPERACIONAL DE ESTOQUE</div><div class="login-title">ACESSO AO SISTEMA</div>',unsafe_allow_html=True)
    with st.form('login_form'):
        email=st.text_input('E-mail',placeholder='seu e-mail')
        password=st.text_input('Senha',type='password',placeholder='••••••••')
        submitted=st.form_submit_button('ENTRAR',type='primary',use_container_width=True,icon=':material/login:')
    if submitted:
        if not email or not password:
            st.error('Informe o e-mail e a senha.')
        else:
            data,err=auth_login(email,password)
            if err: st.error(err)
            else:
                st.session_state.auth_user=data.get('user',{})
                st.session_state.auth_access_token=data.get('access_token','')
                st.session_state.auth_refresh_token=data.get('refresh_token','')
                st.rerun()
    st.markdown('<div style="text-align:center;color:#A9B1AC;font-size:11px;margin-top:14px">Acesso autorizado somente para usuários cadastrados.</div></div></div>',unsafe_allow_html=True)

if not st.session_state.auth_user:
    render_login()
    st.stop()


def persist_cfg():"""
assert marker in s
s=s.replace(marker,insert,1)

# 2) Replace sidebar CSS with fixed-width icon/button treatment. Keep native collapse untouched.
old_css="section[data-testid=\"stSidebar\"] .stButton{{margin-bottom:{cfg.get('menu_gap',2)}px}}section[data-testid=\"stSidebar\"] .stButton>button{{width:100%;min-height:{cfg['item_h']}px;border:1px solid var(--border);background:var(--panel);color:var(--text);text-align:{cfg['sidebar_align']};justify-content:{'flex-start' if cfg['sidebar_align']=='left' else 'center' if cfg['sidebar_align']=='center' else 'flex-end'};font-size:{cfg['sidebar_font']}px;font-weight:800;border-radius:9px;padding:0 14px;box-shadow:0 1px 3px rgba(0,0,0,.18)}}section[data-testid=\"stSidebar\"] .stButton>button:hover{{background:var(--p2);color:var(--text);border-color:var(--p)}}section[data-testid=\"stSidebar\"] .stButton>button[kind=\"primary\"]{{background:var(--p);color:#11130F;border-color:var(--p);box-shadow:0 2px 7px rgba(0,0,0,.22)}}section[data-testid=\"stSidebar\"] .stButton>button::first-letter{{color:{cfg['icon_color']}}}"
new_css="section[data-testid=\"stSidebar\"] .stButton{{width:100%!important;margin-bottom:{cfg.get('menu_gap',2)}px}}section[data-testid=\"stSidebar\"] .stButton>button{{width:100%!important;min-height:{cfg['item_h']}px;height:{cfg['item_h']}px;border:1px solid var(--border);background:var(--panel);color:var(--text);text-align:left;justify-content:flex-start;font-size:{cfg['sidebar_font']}px;font-weight:800;border-radius:9px;padding:0 14px;box-shadow:0 1px 3px rgba(0,0,0,.18);gap:10px}}section[data-testid=\"stSidebar\"] .stButton>button:hover{{background:var(--p2);color:var(--text);border-color:var(--p)}}section[data-testid=\"stSidebar\"] .stButton>button[kind=\"primary\"]{{background:var(--p);color:#11130F;border-color:var(--p);box-shadow:0 2px 7px rgba(0,0,0,.22)}}section[data-testid=\"stSidebar\"] .stButton>button [data-testid=\"stIconMaterial\"]{{font-size:20px!important;width:22px!important;min-width:22px!important;height:22px!important;line-height:22px!important;color:{cfg['icon_color']}!important;display:inline-flex!important;align-items:center!important;justify-content:center!important}}"
assert old_css in s
s=s.replace(old_css,new_css,1)

# 3) Replace nav labels with native Material Symbols icons.
old_nav="nav=[('Dashboard',f'▦  {config[\"dashboard_label\"]}'),('Inventário Rotativo',f'✎  {config[\"inventory_label\"]}'),('Banco de Dados',f'▣  {config[\"database_label\"]}'),('Registro',f'◷  {config[\"register_label\"]}'),('Configurações',f'⚙  {config[\"settings_label\"]}')]"
new_nav="nav=[('Dashboard',config[\"dashboard_label\"],':material/dashboard:'),('Inventário Rotativo',config[\"inventory_label\"],':material/inventory_2:'),('Banco de Dados',config[\"database_label\"],':material/database:'),('Registro',config[\"register_label\"],':material/history:'),('Configurações',config[\"settings_label\"],':material/settings:')]"
assert old_nav in s
s=s.replace(old_nav,new_nav,1)
old_loop="for k,l in nav:\n  off=tops.get(k,0)\n  st.markdown(f'<div style=\"height:0;margin-top:{off}px\"></div>',unsafe_allow_html=True)\n  if st.button(l,key='nav_'+k,type='primary' if st.session_state.section==k else 'secondary'):st.session_state.section=k;st.rerun()"
new_loop="for k,l,ic in nav:\n  off=tops.get(k,0)\n  st.markdown(f'<div style=\"height:0;margin-top:{off}px\"></div>',unsafe_allow_html=True)\n  if st.button(l,key='nav_'+k,icon=ic,icon_position='left',type='primary' if st.session_state.section==k else 'secondary'):st.session_state.section=k;st.rerun()"
assert old_loop in s
s=s.replace(old_loop,new_loop,1)
old_report="if st.button(f'⚠  {config[\"report_label\"]}',key='nav_Reportar Inconsistências',type='primary' if st.session_state.section=='Reportar Inconsistências' else 'secondary'):"
new_report="if st.button(config[\"report_label\"],key='nav_Reportar Inconsistências',icon=':material/report_problem:',icon_position='left',type='primary' if st.session_state.section=='Reportar Inconsistências' else 'secondary'):"
assert old_report in s
s=s.replace(old_report,new_report,1)

# 4) Add authenticated user/logout area at bottom of sidebar, without disturbing report placement.
old_end=" st.session_state.section='Reportar Inconsistências';st.rerun()\n st.markdown('</div>',unsafe_allow_html=True)\n\nst.markdown(f'<div class=\"main-title\">"
new_end=" st.session_state.section='Reportar Inconsistências';st.rerun()\n st.markdown('</div>',unsafe_allow_html=True)\n st.markdown('<div class=\"sidebar-user-area\">',unsafe_allow_html=True)\n _uemail=str(st.session_state.auth_user.get('email',''))\n st.caption('ACESSO: '+_uemail)\n if st.button('SAIR',key='logout_btn',icon=':material/logout:',use_container_width=True): auth_logout()\n st.markdown('</div>',unsafe_allow_html=True)\n\nst.markdown(f'<div class=\"main-title\">"
assert old_end in s
s=s.replace(old_end,new_end,1)

# 5) Add CSS for user area and slightly stronger sidebar geometry.
needle="section[data-testid=\"stSidebar\"] .sidebar-report-area .stButton{{margin-bottom:0!important}}</style>''',unsafe_allow_html=True)"
replacement="section[data-testid=\"stSidebar\"] .sidebar-report-area .stButton{{margin-bottom:0!important}}section[data-testid=\"stSidebar\"] .sidebar-user-area{{position:absolute;left:10px;right:10px;bottom:78px;padding-top:6px;border-top:1px solid var(--border);z-index:19}}section[data-testid=\"stSidebar\"] .sidebar-user-area .stCaption{{font-size:10px!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}section[data-testid=\"stSidebar\"] .sidebar-user-area .stButton{{margin:0!important}}section[data-testid=\"stSidebar\"] .sidebar-user-area .stButton>button{{min-height:32px;height:32px;font-size:11px!important}}</style>''',unsafe_allow_html=True)"
assert needle in s
s=s.replace(needle,replacement,1)

p.write_text(s,encoding='utf-8')
print('patched')
