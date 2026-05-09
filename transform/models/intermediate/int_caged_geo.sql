/*
  Intermediate: int_caged_geo
  ─────────────────────────────
  Agrega os dados por UF e região.
  Calcula ranking de estados por saldo — lógica de negócio.
*/

with base as (

    select * from {{ ref('stg_caged') }}

),

por_estado as (

    select
        uf,
        regiao,
        sum(qtd_admissoes)     as total_admissoes,
        sum(qtd_desligamentos) as total_desligamentos,
        sum(saldo_empregos)    as saldo_total,
        avg(vl_salario_medio)  as salario_medio

    from base
    group by uf, regiao

),

com_ranking as (

    select
        *,
        rank() over (order by saldo_total desc) as ranking_saldo,
        rank() over (order by salario_medio desc) as ranking_salario

    from por_estado

)

select * from com_ranking
order by saldo_total desc
