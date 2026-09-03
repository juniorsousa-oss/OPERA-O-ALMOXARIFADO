# Sistema Operacional — Inventário Rotativo

Versão de teste com identidade visual Setta configurável, banco de dados corrigido para números decimais e primeiro fluxo funcional do Inventário Rotativo.

## Correção crítica dos números
A leitura agora preserva formatos como:
- `613,48` → 613,48
- `613.48` → 613,48
- `110,135` → 110,135
- `1.234,56` → 1.234,56

Isso evita transformar 613,48 em 61.348 ou 110,135 em 110.135.

## Inventário Rotativo
- Novo inventário com documento `DDMMAAAA-NNN`.
- Seleção de N produtos distintos.
- Metade priorizada por R$ UN. e metade por R$ TOTAL, eliminando duplicidades.
- Rotação por ciclo: produtos menos contados têm prioridade.
- Expansão por produto × endereço apto.
- Contagem cega ou não cega.
- Comentário opcional; vazio é salvo como `SC`.
- Fechamento da 1ª contagem → análise do gestor.
- 2ª contagem seletiva.
- Se 2ª = 1ª: erro de inventário.
- Se 2ª = sistema: sistema confirmado.
- Se as três quantidades forem diferentes: gestor pode fechar com 1ª/2ª ou solicitar auditoria.
- Auditoria como 3ª contagem.
- Registro dos inventários fechados.

## Identidade visual
- Dark / Clean com contraste automático.
- Logo configurável.
- Fonte, tamanhos, cores, alinhamentos e textos editáveis.
- Sidebar sem forçar display/posição, permitindo o controle nativo do Streamlit funcionar corretamente.

## Limitação desta fase
Os dados ficam em `session_state`, portanto ainda não são permanentes entre sessões/usuários. A próxima etapa pode migrar inventários, configurações e registro para Supabase/PostgreSQL.
