![Dashboard completo](docs/screenshots/01-visao-geral.png)

# Analytics Engineer — Mercado de Trabalho Brasileiro (CAGED)

Projeto end-to-end seguindo as práticas reais de um **Analytics Engineer**: pipeline Python, transformações em camadas com **dbt**, warehouse local com **DuckDB** e dashboard final em **Streamlit**.

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Ingestão | Python + pandas |
| Warehouse | DuckDB |
| Transformação (Analytics Engineering) | **dbt-duckdb** (staging → intermediate → marts) |
| Qualidade de dados | dbt tests (schema + custom asserts) |
| Visualização | Streamlit + Plotly |

## Como rodar localmente

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. (Opcional) Rodar apenas o dbt para validar as transformações
cd transform
dbt run  --profiles-dir . --project-dir .
dbt test --profiles-dir . --project-dir .

# 3. Rodar o dashboard completo (pipeline + dbt rodam automaticamente)
streamlit run dashboard/app.py
```

## Estrutura do projeto

```
projeto-analytics-engineer/
├── data/
│   ├── raw/                           # parquet bruto (gerado automaticamente)
│   └── processed/                     # parquet limpo + banco DuckDB
├── pipeline/                          # ingestão e limpeza (Python)
│   ├── ingest.py
│   └── clean.py
├── transform/                         # projeto dbt
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
│   │   ├── staging/                   # stg_*  → views (padronização da fonte)
│   │   ├── intermediate/              # int_*  → tables (regras de negócio)
│   │   └── marts/                     # mart_* → tables (entregas para o BI)
│   └── tests/                         # testes customizados (assert_*.sql)
├── dashboard/
│   └── app.py                         # Streamlit lê apenas dos marts
├── queries/
│   └── metricas.sql                   # queries SQL de referência
├── CLAUDE.md                          # contexto permanente para o Claude Code
├── PLANO.md                           # progresso e próximos passos
└── requirements.txt
```

## O que o dashboard mostra

- **KPIs**: admissões, desligamentos, saldo, salário médio
- **Evolução mensal**: saldo por mês + acumulado anual
- **Mapa do Brasil**: saldo por estado (choropleth)
- **Ranking de estados**: top 10 por saldo
- **Análise setorial**: comparativo total e evolução temporal por setor
- **Filtros interativos**: ano, região e setor

## Screenshots

| Tela | Preview |
|------|---------|
| KPIs + evolução mensal | ![KPIs](docs/screenshots/02-kpis.png) |
| Mapa do Brasil + Top 10 estados | ![Mapa](docs/screenshots/03-estados.png) |
| Análise setorial | ![Setores](docs/screenshots/04-setores.png) |

## Marts entregues pelo dbt

| Tabela | Descrição |
|--------|-----------|
| `mart_visao_geral` | Saldo mensal nacional + acumulado + variação % |
| `mart_estados` | Totais por UF com ranking e classificação |
| `mart_setores` | Evolução por setor e mês |

## Qualidade dos dados

Os models possuem testes dbt automatizados:
- `not_null` e `unique` em chaves de negócio (configurados em `schema.yml`)
- `accepted_values` para colunas categóricas
- Testes customizados em `transform/tests/` (ex: saldo coerente, salário positivo)

Rodar todos os testes:
```bash
cd transform && dbt test --profiles-dir . --project-dir .
```

## Deploy no Streamlit Cloud (grátis)

O projeto está pronto para deploy no [share.streamlit.io](https://share.streamlit.io). Configurações já incluídas no repo:

- `.python-version` fixa Python 3.11
- `.streamlit/config.toml` define o tema visual
- `data/processed/.gitkeep` garante que o diretório do DuckDB exista no container
- `requirements.txt` traz todas as dependências (Streamlit, DuckDB, dbt-core, dbt-duckdb, pandas, plotly)

**Passo a passo:**

1. Acesse [share.streamlit.io](https://share.streamlit.io) e faça login com a conta do GitHub
2. Clique em **New app** → selecione o repositório `projeto-analytics-engineer`
3. Configure:
   - **Branch**: `main`
   - **Main file path**: `dashboard/app.py`
4. Em **Advanced settings**, confirme **Python version: 3.11**
5. Clique em **Deploy** (o primeiro build leva 3–8 min)

No primeiro acesso, o app roda o pipeline completo (ingest → clean → `dbt run`) e materializa os marts dentro do container — você verá o spinner "Rodando pipeline dbt pela primeira vez...". Depois disso, o cache do Streamlit segura os DataFrames.

## Conceitos de Analytics Engineering aplicados

- **Camadas dbt**: separação clara entre staging (limpeza), intermediate (negócio) e marts (entrega)
- **Materializações estratégicas**: views em staging (sempre fresco) e tables em marts (performance)
- **Lineage rastreável**: uso de `{{ ref() }}` permite o dbt mapear dependências entre models
- **Testes como código**: validação automatizada da qualidade dos dados em cada execução
- **Documentação versionada**: `schema.yml` documenta cada coluna no mesmo lugar do código

## 🔄 Sincronização GitHub Automática

Este projeto está configurado para fazer **push automático** a cada commit para o GitHub. Não é necessário fazer `git push` manual.

### Setup inicial (uma vez)

```bash
# 1. Executar script de setup
.\setup-github.ps1

# 2. Criar repositório no GitHub (https://github.com/new)
#    - Nome: projeto-analytics-engineer
#    - Escolha: Public (portfólio) ou Private

# 3. Conectar ao remoto (copie os comandos da tela do GitHub)
git remote add origin https://github.com/SEU_USUARIO/NOME_REPO.git
git branch -M main
git push -u origin main
```

### Usar no dia a dia

```bash
git add .
git commit -m "feat: descreve a mudança"
# ✅ Push automático para GitHub acontece automaticamente
```

**Prefixos de commit recomendados:**
- `feat:` — nova funcionalidade
- `fix:` — correção de bug
- `refactor:` — refatoração (sem mudança funcional)
- `docs:` — documentação
- `test:` — testes
- `chore:` — manutenção, dependências

Exemplo:
```bash
git commit -m "feat: adiciona tabela de variação salarial por setor"
git commit -m "refactor: reorganiza modelos dbt para melhor modularidade"
```

O Git hook em `.git/hooks/post-commit` cuida do resto automaticamente!

---

Projeto desenvolvido como portfólio de Analytics Engineer.
