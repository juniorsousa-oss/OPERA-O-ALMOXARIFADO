from pathlib import Path
import re

p = Path('app.py')
s = p.read_text(encoding='utf-8')
start = s.index('# Authentication: Supabase Auth')
end = s.index('def render_login():', start)
new = '''# Authentication: Firebase Authentication (email + password). Session remains server-side in Streamlit.
FIREBASE_API_KEY = st.secrets.get('FIREBASE_API_KEY', 'AIzaSyDkS32UBjttYW1bWFho60EUnP4DXRYnKps')
FIREBASE_AUTH_URL = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword'
if 'auth_user' not in st.session_state: st.session_state.auth_user=None

def auth_login(email, password):
    if not FIREBASE_API_KEY:
        return None, 'A autenticação ainda não foi configurada no aplicativo.'
    try:
        body=json.dumps({'email':email.strip().lower(),'password':password,'returnSecureToken':True}).encode('utf-8')
        req=Request(FIREBASE_AUTH_URL+'?key='+FIREBASE_API_KEY,data=body,headers={'Content-Type':'application/json'},method='POST')
        with urlopen(req,timeout=15) as resp: data=json.loads(resp.read().decode('utf-8'))
        return data, None
    except HTTPError as e:
        try:
            raw=e.read().decode('utf-8')
            info=json.loads(raw)
            code=(info.get('error') or {}).get('message','')
            messages={
                'INVALID_LOGIN_CREDENTIALS':'E-mail ou senha inválidos.',
                'INVALID_PASSWORD':'E-mail ou senha inválidos.',
                'EMAIL_NOT_FOUND':'E-mail ou senha inválidos.',
                'USER_DISABLED':'Este usuário está desativado.',
                'TOO_MANY_ATTEMPTS_TRY_LATER':'Muitas tentativas. Tente novamente mais tarde.'
            }
            msg=messages.get(code,'Não foi possível realizar o login.')
        except Exception:
            msg='Não foi possível realizar o login.'
        return None, msg
    except (URLError, TimeoutError):
        return None, 'Não foi possível conectar ao serviço de autenticação.'
    except Exception:
        return None, 'Não foi possível realizar o login.'

def auth_logout():
    st.session_state.auth_user=None
    st.session_state.pop('auth_access_token',None)
    st.session_state.pop('auth_refresh_token',None)
    st.rerun()

'''
p.write_text(s[:start] + new + s[end:], encoding='utf-8')
