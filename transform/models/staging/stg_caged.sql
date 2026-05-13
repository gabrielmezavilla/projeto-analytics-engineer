/*
  Staging: stg_caged
  ───────────────────
  Camada de contato com a fonte bruta.
  Responsabilidade: renomear, tipar e padronizar — SEM regra de negócio.
  Fonte: parquet gerado pelo pipeline/ingest.py + clean.py
*/

with source as (

    select * from read_parquet('../data/processed/caged_limpo.parquet')

),

renamed as (

    select
        -- Identificadores temporais
        competencia::date           as data_competencia,
        ano::integer                as ano,
        mes::integer                as mes,
        ano_mes::varchar            as ano_mes,

        -- Dimensões geográficas
        upper(trim(estado))         as uf,
        upper(substring(trim(regiao), 1, 1)) || lower(substring(trim(regiao), 2)) as regiao,

        -- Dimensões de negócio
        upper(substring(trim(setor), 1, 1)) || lower(substring(trim(setor), 2)) as setor,
        upper(substring(trim(sexo), 1, 1)) || lower(substring(trim(sexo), 2)) as sexo,
        upper(substring(trim(escolaridade), 1, 1)) || lower(substring(trim(escolaridade), 2)) as escolaridade,

        -- Métricas
        admissoes::integer          as qtd_admissoes,
        desligamentos::integer      as qtd_desligamentos,
        saldo::integer              as saldo_empregos,
        salario_medio::double       as vl_salario_medio

    from source

)

select * from renamed
