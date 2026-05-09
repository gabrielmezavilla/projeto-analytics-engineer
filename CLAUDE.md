# CLAUDE.md — Analytics CAGED Brasil

Contexto permanente do projeto. Leia isto antes de qualquer tarefa.

## O que é este projeto

Dashboard de analytics end-to-end do mercado de trabalho brasileiro (CAGED), modelado com as práticas reais de um **Analytics Engineer**. O usuário tem background em SQL, Power BI, DAX e Excel avançado, e está aprendendo Python — então o código deve ser didático, bem comentado e aproveitar SQL sempre que possível.

## Papel: Analytics Engineer

Este projeto segue o fluxo de trabalho real da profissão:

```
Fonte bruta → Ingestão (Python) → dbt (staging → intermediate → marts) → Dashboard (Streamlit)
```

O Analytics Engineer é responsável pelas camadas dbt. O dashboard consome apenas os **marts** — nunca acessa staging ou tabelas brutas diretamente.

## Stack

| Camada | Tecnologia | Onde fica |
|--------|-----------|-----------|
| Ingestão | Python + pandas | `pipeline/ingest.py` + `pipeline/clean.py` |
| Warehouse | DuckDB | `data/processed/analytics.duckdb` |
| Transformação | dbt-duckdb | `transform/` |
| Dashboard | Streamlit + Plotly | `dashboard/app.py` |

## Estrutura dbt (`transform/`)

```
transform/
├── dbt_project.yml
├── profiles.yml
├── models/
│   ├── staging/          # stg_* — limpeza e renomeação da fonte bruta (view)
│   │   ├── stg_caged.sql
│   │   └── schema.yml
│   ├── intermediate/     # int_* — lógica de negócio e agregações (table)
│   │   ├── int_caged_mensal.sql
│   │   ├── int_caged_geo.sql
│   │   └── int_caged_setor.sql
│   └── marts/            # mart_* — entregáveis finais para o BI (table)
│       ├── mart_visao_geral.sql
│       ├── mart_estados.sql
│       ├── mart_setores.sql
│       └── schema.yml
└── tests/                # testes customizados dbt (assert_*)
    ├── assert_saldo_coerente.sql
    └── assert_salario_positivo.sql
```

## Marts disponíveis no DuckDB (schema: `marts`)

| Tabela | Descrição | Usado em |
|--------|-----------|----------|
| `mart_visao_geral` | Saldo mensal nacional + acumulado + variação % | KPIs, gráfico de barras, linha acumulada |
| `mart_estados` | Totais por UF com ranking e classificação | Mapa, ranking top 10 |
| `mart_setores` | Evolução por setor e mês | Gráfico de barras setorial, linhas |

## Regras obrigatórias

### Comunicação com o usuário (PRIORIDADE)

- **Sempre explique o que está fazendo** antes ou durante as ações — não execute em silêncio
- **Linguagem simples e intuitiva** — o usuário está aprendendo Python e Analytics Engineering, evite jargões sem explicar
- **Use analogias do mundo real** quando introduzir conceitos novos (ex: "dbt funciona como uma esteira de fábrica que limpa e organiza os dados em etapas")
- **Explique o "porquê", não só o "o quê"** — sempre justifique a escolha técnica
- **Documente cada avanço** — atualize `PLANO.md` marcando tarefas concluídas e `README.md` quando algo mudar na estrutura
- **Foco em portfólio**: o projeto será publicado, então cada decisão técnica deve poder ser justificada em uma entrevista

### Regras técnicas

- **Nunca escreva transformações no dashboard** — toda lógica de negócio fica nos models dbt
- **Respeite as camadas**: staging não tem regra de negócio; intermediate tem; marts são somente selects finais
- **Use `{{ ref() }}`** para referenciar outros models dbt — nunca hardcode schema/tabela
- **Comente os models em português** — o usuário está aprendendo
- **Testes dbt**: toda coluna de negócio importante deve ter teste `not_null` ou `unique` no schema.yml
- **Caminhos relativos sempre** — use `Path(__file__).parent` no Python
- **Cache Streamlit** — use `@st.cache_data` em todas as funções que leem o DuckDB

## Como rodar o projeto

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Rodar apenas o pipeline dbt (sem o dashboard)
cd transform
dbt run --profiles-dir . --project-dir .
dbt test --profiles-dir . --project-dir .

# 3. Rodar o dashboard completo (pipeline roda automaticamente)
streamlit run dashboard/app.py
```

## Repositório GitHub — Sincronização Automática

Este projeto está versionado no GitHub com **push automático** a cada commit. Sempre que você faz alterações, o repositório remoto é atualizado automaticamente.

### Setup inicial (uma vez)

```bash
# 1. Executar script de setup (Windows PowerShell)
.\setup-github.ps1

# 2. Criar repositório no GitHub (https://github.com/new)
#    - Nome: projeto-analytics-engineer (ou outro de sua preferência)
#    - Escolha: Public (portfólio) ou Private

# 3. Vincular ao remoto (substitua SEU_USUARIO/NOME_REPO)
git remote add origin https://github.com/SEU_USUARIO/NOME_REPO.git
git branch -M main
git push -u origin main
```

### A partir daí

Toda vez que você faz `git commit`, o push automático funciona via Git hook (`.git/hooks/post-commit`). Não precisa fazer `git push` manual.

**Fluxo dia a dia:**
```bash
git add .
git commit -m "feat: descrição da mudança"
# ✅ Push automático acontece aqui
```

### Estrutura de commits (Conventional Commits)

Use prefixos semânticos para manter o histórico limpo:

- `feat:` — nova funcionalidade
- `fix:` — correção de bug
- `refactor:` — refatoração (sem mudança funcional)
- `docs:` — atualização de documentação
- `test:` — testes
- `chore:` — manutenção, dependências, etc

**Exemplo:**
```bash
git commit -m "feat: adiciona nova métrica de variação salarial"
git commit -m "refactor: reorganiza modelos dbt para melhor legibilidade"
git commit -m "docs: atualiza README com instruções de deploy"
```

## Próximos passos planejados

1. Substituir dados sintéticos por dados reais do FTP do MTE
2. Adicionar `dbt source` para documentar a fonte oficial
3. Fazer deploy no Streamlit Cloud
4. Subir para o GitHub com README e screenshots
5. (Opcional) Adicionar `dbt docs generate` para catálogo de dados
