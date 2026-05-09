/*
  Mart: mart_visao_geral
  ────────────────────────
  Tabela final consumida pelo dashboard — visão mensal nacional completa.
  Esta é a entrega do Analytics Engineer para o time de BI/produto.
*/

select
    ano_mes,
    ano,
    mes,
    total_admissoes,
    total_desligamentos,
    saldo_mensal,
    saldo_acumulado_ano,
    variacao_pct_mes_anterior,
    round(salario_medio, 2) as salario_medio

from {{ ref('int_caged_mensal') }}

order by ano_mes
