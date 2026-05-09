/*
  Teste customizado dbt: assert_saldo_coerente
  ─────────────────────────────────────────────
  Garante que saldo = admissões - desligamentos em todos os registros.
  O teste FALHA se retornar qualquer linha (rows > 0 = problema).
*/

select
    ano_mes,
    total_admissoes,
    total_desligamentos,
    saldo_mensal,
    (total_admissoes - total_desligamentos) as saldo_esperado

from {{ ref('mart_visao_geral') }}

where saldo_mensal != (total_admissoes - total_desligamentos)
