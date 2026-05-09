# Plano do Projeto — Analytics CAGED Brasil

## Objetivo
Construir um projeto end-to-end que replique o trabalho real de um **Analytics Engineer**, do zero ao deploy, para portfólio.

---

## O que faz um Analytics Engineer?

| Responsabilidade | Como aparece aqui |
|-----------------|-------------------|
| Modelar dados com SQL | Models dbt (staging → intermediate → marts) |
| Garantir qualidade dos dados | Testes dbt (schema.yml + testes customizados) |
| Documentar a camada analítica | schema.yml, CLAUDE.md, README |
| Entregar marts para o BI | mart_* consumidos pelo Streamlit |
| Versionar com Git | GitHub com commits por camada |

---

## Stack

| Tecnologia | Por que usar |
|-----------|-------------|
| Python + pandas | Ingestão e limpeza da fonte bruta |
| DuckDB | Warehouse local, sem instalar servidor |
| **dbt-duckdb** | Transformações SQL em camadas — **coração do AE** |
| Streamlit + Plotly | Dashboard interativo publicável grátis |
| Git + GitHub | Portfólio versionado |

---

## Fluxo de dados

```
Fonte bruta (parquet)
       │
       ▼
  pipeline/ingest.py   → data/raw/caged_dados.parquet
  pipeline/clean.py    → data/processed/caged_limpo.parquet
       │
       ▼
  dbt staging          → stg_caged (view) — padronização
       │
       ▼
  dbt intermediate     → int_caged_mensal / _geo / _setor (tables)
       │
       ▼
  dbt marts            → mart_visao_geral / _estados / _setores (tables)
       │
       ▼
  dashboard/app.py     → Streamlit lê apenas dos marts
```

---

## Fases do projeto

### Fase 1 — Ingestão e Limpeza (FEITO)
- [x] `pipeline/ingest.py` — carrega e faz cache em parquet
- [x] `pipeline/clean.py` — trata tipos, nulos, cria colunas derivadas

### Fase 2 — Modelagem dbt (FEITO)
- [x] `transform/dbt_project.yml` + `profiles.yml` — configuração do projeto
- [x] `staging/stg_caged.sql` — padronização da fonte (view)
- [x] `intermediate/int_caged_mensal.sql` — saldo + acumulado + variação %
- [x] `intermediate/int_caged_geo.sql` — totais por estado com ranking
- [x] `intermediate/int_caged_setor.sql` — evolução setorial por mês
- [x] `marts/mart_visao_geral.sql` — entregável principal do dashboard
- [x] `marts/mart_estados.sql` — entregável para mapa e ranking
- [x] `marts/mart_setores.sql` — entregável para gráficos setoriais
- [x] Testes dbt (schema.yml + testes customizados assert_*)

### Fase 3 — Dashboard (FEITO)
- [x] `dashboard/app.py` — lê apenas dos marts, com filtros, KPIs e gráficos

### Fase 4 — Deploy e Portfólio (PRÓXIMOS PASSOS)
- [ ] Criar repositório no GitHub e fazer `git push`
- [ ] Publicar dashboard no [share.streamlit.io](https://share.streamlit.io) (grátis)
- [ ] Adicionar screenshots no README.md
- [ ] Publicar no LinkedIn com descrição do stack

---

## Como rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar dbt isoladamente (para testar as transformações)
cd transform
dbt run --profiles-dir . --project-dir .
dbt test --profiles-dir . --project-dir .

# Rodar o dashboard completo
streamlit run dashboard/app.py
```

---

## Próximas melhorias para enriquecer o portfólio

1. **Dados reais do CAGED** — substituir sintéticos pelo FTP oficial do MTE
2. **`dbt source`** — documentar a fonte com freshness check
3. **`dbt docs generate`** — gerar catálogo de dados navegável
4. **Comparativo com IPCA** — cruzar saldo de empregos com inflação
5. **GitHub Actions** — rodar `dbt run` automaticamente todo mês
