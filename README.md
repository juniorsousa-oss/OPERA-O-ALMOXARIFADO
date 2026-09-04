# Sistema Operacional — Inventário Rotativo V5

- Base: ESTOQUE ANALÍTICO + ENDEREÇO.
- ESTOQUE ANALÍTICO: A Código, D Descrição, H Quantidade/Saldo, K Valor em Estoque.
- Valor unitário = K ÷ H.
- R$ UN = ranking por valor unitário.
- R$ TOTAL = ranking pelo valor K do relatório analítico.
- Valor Total Apto = Saldo Apto × Valor Unitário.
- ENDEREÇO: A Código, D Endereço, H Quantidade; lotes somados por produto/endereço.
- Endereços com pesquisa e checkboxes, sem tags vermelhas.
- Dark/Clean, fontes, cores, logo, posições e textos configuráveis.
- Sidebar: controle nativo de recolher/abrir não é reposicionado.
- Inventário: primeira contagem, recontagem individual, RECONTAR TODOS, auditoria individual/todos e novas rodadas sem limite.
- Histórico completo das contagens por posição.
- Configurações, banco consolidado, inventários e ciclos são gravados em SQLite local para não depender apenas do session_state.

## Persistência em nuvem

A base principal de estoque utiliza Firestore para persistência em nuvem. O SQLite permanece apenas como fallback local para dados legados enquanto a migração das demais estruturas é realizada.

<!-- deploy sync 2026-09-04 -->
