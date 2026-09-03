# Sistema Operacional — Inventário Rotativo

Versão com identidade visual configurável e base do módulo de Inventário Rotativo.

## Novidades desta versão

- Tema **Dark** e **Clean** com contraste automático.
- Aba **Configurações**.
- Upload de logo da empresa; a escrita fixa da lateral foi removida.
- Configuração de tipo de letra e tamanhos.
- Configuração de cores de fundo, painéis, bordas e textos para cada tema.
- Configuração dos nomes do menu e dos principais textos das páginas.
- Configuração dos textos dos botões.
- Configuração da largura do menu lateral.
- Restauração da configuração padrão.

> Nesta versão, as configurações ficam na sessão atual do aplicativo. Para persistência definitiva, a próxima etapa pode gravá-las em PostgreSQL/Supabase.

## Banco de Dados

### CADASTROS
- B: Código do produto
- C: Descrição
- H: Último Preço

### ENDEREÇO
- A: Código do produto
- D: Endereço
- H: Quantidade
- Lote ignorado nesta primeira versão

### Regras
1. Código do produto é a chave de relacionamento.
2. Produto + endereço são consolidados em uma posição.
3. Lotes diferentes no mesmo endereço são somados.
4. Endereços são parametrizáveis como aptos/não aptos.
5. Saldo apto considera somente endereços selecionados.
6. Valor total = saldo apto × último preço.
7. Classificação R$ UN. = ranking decrescente pelo último preço.
8. Classificação R$ TOTAL = ranking decrescente pelo valor total.
9. Banco de produtos apresenta uma linha por produto.
