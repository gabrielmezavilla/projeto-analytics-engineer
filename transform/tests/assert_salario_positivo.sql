/*
  Teste customizado dbt: assert_salario_positivo
  ────────────────────────────────────────────────
  Garante que nenhum estado possui salário médio negativo ou zero.
  Um salário <= 0 indica problema na fonte de dados.
*/

select
    uf,
    salario_medio

from {{ ref('mart_estados') }}

where salario_medio <= 0
