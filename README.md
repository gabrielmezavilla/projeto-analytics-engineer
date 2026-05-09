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

1. Suba o projeto no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte o repositório e aponte para `dashboard/app.py`
4. Clique em Deploy

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
