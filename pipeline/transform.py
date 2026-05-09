"""
Modelagem analítica com DuckDB (SQL moderno, sem servidor).
Cria tabelas agregadas prontas para o dashboard.
"""

import duckdb
import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
DB_PATH = PROCESSED_DIR / "analytics.duckdb"


def criar_tabelas(df: pd.DataFrame) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(str(DB_PATH))

    # Registra o DataFrame como tabela virtual
    con.register("caged_raw", df)

    # Tabela base normalizada
    con.execute("""
        CREATE OR REPLACE TABLE fato_caged AS
        SELECT *
        FROM caged_raw
    """)

    # Agregação mensal nacional
    con.execute("""
        CREATE OR REPLACE TABLE agg_mensal AS
        SELECT
            ano_mes,
            ano,
            mes,
            SUM(admissoes)    AS total_admissoes,
            SUM(desligamentos) AS total_desligamentos,
            SUM(saldo)        AS saldo_total,
            AVG(salario_medio) AS salario_medio
        FROM fato_caged
        GROUP BY ano_mes, ano, mes
        ORDER BY ano_mes
    """)

    # Saldo acumulado no ano (window function)
    con.execute("""
        CREATE OR REPLACE TABLE agg_acumulado AS
        SELECT
            ano_mes,
            ano,
            saldo_total,
            SUM(saldo_total) OVER (
                PARTITION BY ano
                ORDER BY ano_mes
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS saldo_acumulado_ano
        FROM agg_mensal
        ORDER BY ano_mes
    """)

    # Ranking de estados por saldo
    con.execute("""
        CREATE OR REPLACE TABLE agg_estados AS
        SELECT
            estado,
            regiao,
            SUM(admissoes)     AS total_admissoes,
            SUM(desligamentos) AS total_desligamentos,
            SUM(saldo)         AS saldo_total,
            AVG(salario_medio) AS salario_medio
        FROM fato_caged
        GROUP BY estado, regiao
        ORDER BY saldo_total DESC
    """)

    # Análise por setor
    con.execute("""
        CREATE OR REPLACE TABLE agg_setores AS
        SELECT
            setor,
            SUM(admissoes)     AS total_admissoes,
            SUM(desligamentos) AS total_desligamentos,
            SUM(saldo)         AS saldo_total,
            AVG(salario_medio) AS salario_medio
        FROM fato_caged
        GROUP BY setor
        ORDER BY saldo_total DESC
    """)

    # Análise por setor e período (para filtros no dashboard)
    con.execute("""
        CREATE OR REPLACE TABLE agg_setor_mensal AS
        SELECT
            ano_mes,
            ano,
            setor,
            SUM(saldo) AS saldo_total
        FROM fato_caged
        GROUP BY ano_mes, ano, setor
        ORDER BY ano_mes, setor
    """)

    # Distribuição por escolaridade
    con.execute("""
        CREATE OR REPLACE TABLE agg_escolaridade AS
        SELECT
            escolaridade,
            sexo,
            SUM(admissoes)  AS total_admissoes,
            AVG(salario_medio) AS salario_medio
        FROM fato_caged
        GROUP BY escolaridade, sexo
        ORDER BY total_admissoes DESC
    """)

    print(f"Banco criado em: {DB_PATH}")
    tabelas = con.execute("SHOW TABLES").fetchdf()
    print(f"Tabelas criadas: {tabelas['name'].tolist()}")

    return con


def carregar_tabela(nome: str) -> pd.DataFrame:
    con = duckdb.connect(str(DB_PATH), read_only=True)
    return con.execute(f"SELECT * FROM {nome}").fetchdf()


if __name__ == "__main__":
    from clean import processar
    from ingest import carregar_dados

    df_raw = carregar_dados()
    df_clean = processar(df_raw)
    con = criar_tabelas(df_clean)

    print("\n--- Amostra: agg_mensal ---")
    print(con.execute("SELECT * FROM agg_mensal LIMIT 5").fetchdf())

    print("\n--- Top 5 estados ---")
    print(con.execute("SELECT * FROM agg_estados LIMIT 5").fetchdf())
