-- Queries analíticas reutilizáveis — execute no DuckDB CLI ou via Python

-- Saldo acumulado por ano
SELECT
    ano,
    SUM(saldo_total) AS saldo_anual
FROM agg_mensal
GROUP BY ano
ORDER BY ano;

-- Top 5 setores que mais empregaram
SELECT setor, total_admissoes, saldo_total
FROM agg_setores
ORDER BY total_admissoes DESC
LIMIT 5;

-- Meses com maior saldo positivo
SELECT ano_mes, saldo_total
FROM agg_mensal
ORDER BY saldo_total DESC
LIMIT 10;

-- Variação percentual mês a mês
SELECT
    ano_mes,
    saldo_total,
    LAG(saldo_total) OVER (ORDER BY ano_mes) AS saldo_mes_anterior,
    ROUND(
        (saldo_total - LAG(saldo_total) OVER (ORDER BY ano_mes))
        / NULLIF(ABS(LAG(saldo_total) OVER (ORDER BY ano_mes)), 0) * 100,
        2
    ) AS variacao_pct
FROM agg_mensal;

-- Estados com saldo negativo
SELECT estado, regiao, saldo_total
FROM agg_estados
WHERE saldo_total < 0
ORDER BY saldo_total;
