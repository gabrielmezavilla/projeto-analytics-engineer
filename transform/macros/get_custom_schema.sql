{#
    Override do macro padrão `generate_schema_name` do dbt.

    Comportamento padrão do dbt-duckdb:
      Se o model tem `+schema: marts` e o profile tem `schema: main`,
      a tabela final fica em `main_marts.mart_xxx` (concatenado).

    Esse override faz o dbt usar o `+schema` direto, sem prefixar:
      `+schema: marts` → tabela em `marts.mart_xxx`

    Isso casa com como o dashboard consulta os marts:
      `SELECT * FROM marts.mart_visao_geral`
#}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
