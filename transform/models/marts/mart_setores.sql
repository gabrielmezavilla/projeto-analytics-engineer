/*
  Mart: mart_setores
  ───────────────────
  Tabela final com métricas por setor econômico e mês.
  Alimenta os gráficos de evolução setorial no dashboard.
*/

select
    ano_mes,
    ano,
    setor,
    total_admissoes,
    total_desligamentos,
    saldo_total,
    round(salario_medio, 2) as salario_medio,
    ranking_saldo

from {{ ref('int_caged_setor') }}

order by ano_mes, ranking_saldo
