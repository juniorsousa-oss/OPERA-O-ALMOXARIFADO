
# Aplicativo Operacional — Inventário Rotativo

## Objetivo desta versão

Construir a base do módulo de Inventário Rotativo, começando pelo Banco de Dados.

### Relatório CADASTROS
- B: Código do produto
- C: Descrição
- H: Último Preço

### Relatório ENDEREÇO
- A: Código do produto
- D: Endereço
- H: Quantidade
- Lote: ignorado nesta primeira versão

## Regras já implementadas

1. Código do produto é a chave de relacionamento.
2. Produto + endereço é consolidado em uma única posição.
3. Lotes diferentes no mesmo endereço são somados.
4. Endereços são parametrizáveis como aptos/não aptos.
5. Saldo apto considera somente endereços selecionados.
6. Valor total = saldo apto × último preço.
7. Classificação R$ UN. = ranking decrescente pelo último preço.
8. Classificação R$ TOTAL = ranking decrescente pelo valor total.
9. Banco de produtos apresenta uma linha por produto.
10. A estrutura de inventário, contagem, análise, recontagem e auditoria será conectada nas próximas etapas.

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicação futura

O projeto está organizado para posteriormente ser colocado no GitHub e publicado no Streamlit Cloud. O banco persistente poderá ser migrado para PostgreSQL/Supabase quando o fluxo operacional estiver validado.
