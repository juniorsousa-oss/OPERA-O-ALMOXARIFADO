from pathlib import Path
p=Path('app.py')
s=p.read_text(encoding='utf-8')
old="""                st.session_state.auth_user=data.get('user',{})
                st.session_state.auth_access_token=data.get('access_token','')
                st.session_state.auth_refresh_token=data.get('refresh_token','')
"""
new="""                # Firebase REST returns idToken/localId directly; there is no nested 'user' object.
                st.session_state.auth_user={'email': data.get('email', email), 'localId': data.get('localId','')}
                st.session_state.auth_access_token=data.get('idToken','')
                st.session_state.auth_refresh_token=data.get('refreshToken','')
"""
if old not in s:
    raise SystemExit('Target login block not found')
p.write_text(s.replace(old,new,1),encoding='utf-8')
