/*
  Mart: mart_estados
  ───────────────────
  Tabela final com métricas por estado — consumida pelo mapa e ranking.
*/

select
    uf,
    regiao,
    total_admissoes,
    total_desligamentos,
    saldo_total,
    round(salario_medio, 2) as salario_medio,
    ranking_saldo,
    ranking_salario,

    -- Classificação textual para facilitar filtros no BI
    case
        when saldo_total > 0 then 'Positivo'
        when saldo_total < 0 then 'Negativo'
        else 'Neutro'
    end as classificacao_saldo

from {{ ref('int_caged_geo') }}

order by ranking_saldo
