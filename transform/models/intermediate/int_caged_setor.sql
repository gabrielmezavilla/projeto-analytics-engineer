/*
  Intermediate: int_caged_setor
  ───────────────────────────────
  Agrega dados por setor econômico e mês.
  Permite análise de evolução setorial ao longo do tempo.
*/

with base as (

    select * from {{ ref('stg_caged') }}

),

por_setor_mes as (

    select
        ano_mes,
        ano,
        setor,
        sum(qtd_admissoes)     as total_admissoes,
        sum(qtd_desligamentos) as total_desligamentos,
        sum(saldo_empregos)    as saldo_total,
        avg(vl_salario_medio)  as salario_medio

    from base
    group by ano_mes, ano, setor

),

por_setor_total as (

    select
        setor,
        sum(qtd_admissoes)     as total_admissoes,
        sum(qtd_desligamentos) as total_desligamentos,
        sum(saldo_empregos)    as saldo_total,
        avg(vl_salario_medio)  as salario_medio,
        rank() over (order by sum(saldo_empregos) desc) as ranking_saldo

    from base
    group by setor

)

-- Exporta a visão por mês (usada nos gráficos de linha do dashboard)
select
    m.ano_mes,
    m.ano,
    m.setor,
    m.total_admissoes,
    m.total_desligamentos,
    m.saldo_total,
    m.salario_medio,
    t.ranking_saldo

from por_setor_mes m
left join por_setor_total t using (setor)
order by m.ano_mes, m.setor
