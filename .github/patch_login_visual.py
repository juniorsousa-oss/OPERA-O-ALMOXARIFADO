from pathlib import Path

p = Path('app.py')
s = p.read_text(encoding='utf-8')

start = s.index('def render_login():')
end = s.index("\nif not st.session_state.auth_user:", start)

new_func = """def render_login():
    login_logo = logo_uri()
    st.markdown('''<style>
    [data-testid="stHeader"]{background:transparent!important}
    .login-wrap{min-height:0!important;display:flex;align-items:flex-start;justify-content:center;padding-top:12px;margin-bottom:0}
    .login-card{width:min(440px,92vw);padding:18px 24px 14px;background:#101614;border:1px solid #2B3732;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,.28);text-align:center}
    .login-logo{display:flex;align-items:center;justify-content:center;height:66px;margin:0 auto 4px;overflow:hidden}
    .login-logo img{max-width:250px;max-height:62px;width:auto;height:auto;object-fit:contain;display:block}
    .login-brand{text-align:center;font-size:34px;font-weight:900;letter-spacing:-1px;color:#F4F5F2;margin-bottom:4px}
    .login-brand span{color:#FFD63B}
    .login-sub{text-align:center;color:#A9B1AC;font-size:12px;margin-bottom:10px}
    .login-title{text-align:center;color:#F4F5F2;font-size:18px;font-weight:800;margin-bottom:0}
    [class*="st-key-login_form"]{margin-top:10px!important}
    [class*="st-key-login_form"] [data-testid="stForm"]{border:1px solid #2B3732!important;border-radius:14px!important;padding:18px 20px 16px!important;background:transparent!important}
    [class*="st-key-login_form"] [data-testid="stFormSubmitButton"] button{margin-top:4px!important}
    .login-footer{width:min(440px,92vw);text-align:center;color:#A9B1AC;font-size:11px;margin:8px auto 0}
    </style>''',unsafe_allow_html=True)
    logo_html = (f'<div class="login-logo"><img src="{login_logo}"></div>' if login_logo else '<div class="login-brand">Se<span>tt</span>a</div>')
    st.markdown(f'<div class="login-wrap"><div class="login-card">{logo_html}<div class="login-sub">SISTEMA OPERACIONAL DE ESTOQUE</div><div class="login-title">ACESSO AO SISTEMA</div></div></div>',unsafe_allow_html=True)
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
    st.markdown('<div class="login-footer">Acesso autorizado somente para usuários cadastrados.</div>',unsafe_allow_html=True)
"""

s = s[:start] + new_func + s[end:]
p.write_text(s, encoding='utf-8')
print('login visual patch applied')
