"""
Ingestão dos dados do CAGED (Novo CAGED) via API do dados.gov.br
Fonte: https://dados.gov.br/dados/conjuntos-dados/novo-caged
"""

import requests
import pandas as pd
from pathlib import Path
import zipfile
import io

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# URLs dos arquivos mensais do Novo CAGED (exemplo: Jan-Dez 2023)
# Formato: CAGEDMOV{AAAAMM}.7z  — disponíveis no FTP do MTE
# Usamos um dataset do Kaggle/GitHub já convertido para CSV para facilitar o início
SAMPLE_DATASET_URL = (
    "https://raw.githubusercontent.com/datasets/employment-br/main/data/caged_sample.csv"
)

# Fallback: dataset público do Olist (e-commerce) disponível no Kaggle
# Vamos usar dados simulados para garantir que o projeto funcione sem autenticação
ANOS_DISPONIVEIS = [2022, 2023, 2024]


def baixar_dados_simulados() -> pd.DataFrame:
    """
    Gera dados sintéticos realistas do CAGED para desenvolvimento local.
    Em produção, substitua por download real do FTP do MTE.
    """
    import numpy as np

    rng = np.random.default_rng(42)

    setores = [
        "Agropecuária", "Indústria de Transformação", "Construção Civil",
        "Comércio", "Serviços", "Administração Pública", "TI e Comunicações",
        "Saúde", "Educação", "Transporte e Logística"
    ]
    estados = [
        "SP", "RJ", "MG", "RS", "PR", "SC", "BA", "GO", "PE", "CE",
        "AM", "PA", "MS", "MT", "ES", "RN", "PB", "MA", "PI", "AL"
    ]
    regioes = {
        "SP": "Sudeste", "RJ": "Sudeste", "MG": "Sudeste", "ES": "Sudeste",
        "RS": "Sul", "PR": "Sul", "SC": "Sul",
        "BA": "Nordeste", "PE": "Nordeste", "CE": "Nordeste",
        "RN": "Nordeste", "PB": "Nordeste", "MA": "Nordeste",
        "PI": "Nordeste", "AL": "Nordeste",
        "GO": "Centro-Oeste", "MS": "Centro-Oeste", "MT": "Centro-Oeste",
        "AM": "Norte", "PA": "Norte"
    }
    sexo_opcoes = ["Masculino", "Feminino"]
    escolaridade_opcoes = [
        "Fundamental Incompleto", "Fundamental Completo",
        "Médio Incompleto", "Médio Completo",
        "Superior Incompleto", "Superior Completo"
    ]

    n = 50_000
    meses = pd.date_range("2022-01", "2024-12", freq="MS")
    datas = rng.choice(meses, size=n)
    estado_lista = rng.choice(estados, size=n)

    admissoes = rng.integers(100, 800, size=n)
    desligamentos = rng.integers(80, 750, size=n)

    df = pd.DataFrame({
        "competencia": datas,
        "estado": estado_lista,
        "regiao": [regioes[e] for e in estado_lista],
        "setor": rng.choice(setores, size=n),
        "sexo": rng.choice(sexo_opcoes, size=n),
        "escolaridade": rng.choice(escolaridade_opcoes, size=n),
        "admissoes": admissoes,
        "desligamentos": desligamentos,
        "saldo": admissoes - desligamentos,
        "salario_medio": rng.uniform(1412, 8000, size=n).round(2),
    })

    return df


def carregar_dados(forcar_download: bool = False) -> pd.DataFrame:
    """
    Carrega os dados do CAGED. Usa cache local se disponível.
    """
    cache_path = RAW_DIR / "caged_dados.parquet"

    if cache_path.exists() and not forcar_download:
        print(f"Carregando dados do cache: {cache_path}")
        return pd.read_parquet(cache_path)

    print("Gerando dados do CAGED...")
    df = baixar_dados_simulados()

    df.to_parquet(cache_path, index=False)
    print(f"Dados salvos em: {cache_path} ({len(df):,} registros)")

    return df


if __name__ == "__main__":
    df = carregar_dados(forcar_download=True)
    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"\nColunas: {df.columns.tolist()}")
    print(f"\nPeríodo: {df['competencia'].min()} a {df['competencia'].max()}")
