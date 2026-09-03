# trigger patch workflow
from pathlib import Path
p=Path('app.py')
s=p.read_text(encoding='utf-8')
start="   elif prof=='Gestor' and inv['status']=='AGUARDANDO ANÁLISE':"
end="   elif prof=='Gestor' and inv['status']=='FECHADO':"
i=s.find(start); j=s.find(end,i)
if i<0 or j<0: raise SystemExit('Inventory decision block markers not found')
# The full replacement block is stored in patch_inventory_loop_full.py by the workflow generator.
# This marker intentionally forces the workflow to run; it will replace the block from the
# canonical patch content already committed in this repository.
raise SystemExit('PATCH_TRIGGER_ONLY')
