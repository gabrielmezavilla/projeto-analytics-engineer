/*
  Intermediate: int_caged_mensal
  ────────────────────────────────
  Agrega os dados por mês a nível nacional.
  Aplica window function para saldo acumulado no ano — lógica de negócio pura.
*/

with base as (

    select * from {{ ref('stg_caged') }}

),

agregado_mensal as (

    select
        ano_mes,
        ano,
        mes,
        sum(qtd_admissoes)    as total_admissoes,
        sum(qtd_desligamentos) as total_desligamentos,
        sum(saldo_empregos)   as saldo_mensal,
        avg(vl_salario_medio) as salario_medio

    from base
    group by ano_mes, ano, mes

),

com_acumulado as (

    select
        *,

        -- Saldo acumulado desde o início do ano (window function)
        sum(saldo_mensal) over (
            partition by ano
            order by ano_mes
            rows between unbounded preceding and current row
        ) as saldo_acumulado_ano,

        -- Variação percentual em relação ao mês anterior
        round(
            (saldo_mensal - lag(saldo_mensal) over (order by ano_mes))
            / nullif(abs(lag(saldo_mensal) over (order by ano_mes)), 0) * 100,
        2) as variacao_pct_mes_anterior

    from agregado_mensal
    order by ano_mes

)

select * from com_acumulado
