from pathlib import Path
p=Path('app.py')
s=p.read_text(encoding='utf-8')
old="SUPABASE_KEY = st.secrets.get('SUPABASE_PUBLISHABLE_KEY', st.secrets.get('SUPABASE_ANON_KEY', ''))"
new="SUPABASE_KEY = st.secrets.get('SUPABASE_PUBLISHABLE_KEY', 'sb_publishable_ZTqIgmA9Ez6AVQsoXa0P8Q_6CYHDFye')"
assert old in s
p.write_text(s.replace(old,new,1),encoding='utf-8')
print('ok')
