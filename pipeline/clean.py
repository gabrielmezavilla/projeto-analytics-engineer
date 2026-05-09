"""
Limpeza e validação dos dados brutos do CAGED com pandas.
"""

import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Garantir tipo correto de data
    df["competencia"] = pd.to_datetime(df["competencia"])

    # Colunas de texto: strip e title case
    colunas_texto = ["estado", "regiao", "setor", "sexo", "escolaridade"]
    for col in colunas_texto:
        df[col] = df[col].astype(str).str.strip()

    # Remover registros com valores negativos impossíveis
    df = df[df["admissoes"] >= 0]
    df = df[df["desligamentos"] >= 0]
    df = df[df["salario_medio"] > 0]

    # Recalcular saldo para garantir consistência
    df["saldo"] = df["admissoes"] - df["desligamentos"]

    # Colunas derivadas úteis para análise
    df["ano"] = df["competencia"].dt.year
    df["mes"] = df["competencia"].dt.month
    df["ano_mes"] = df["competencia"].dt.to_period("M").astype(str)

    # Ordenar por data
    df = df.sort_values("competencia").reset_index(drop=True)

    return df


def validar_dados(df: pd.DataFrame) -> None:
    assert df["competencia"].notna().all(), "Datas nulas encontradas"
    assert df["saldo"].notna().all(), "Saldo com nulos"
    assert (df["admissoes"] >= 0).all(), "Admissões negativas"
    assert (df["desligamentos"] >= 0).all(), "Desligamentos negativos"
    print("Validacao OK: todos os checks passaram.")


def processar(df: pd.DataFrame) -> pd.DataFrame:
    print("Limpando dados...")
    df_limpo = limpar_dados(df)
    validar_dados(df_limpo)

    caminho = PROCESSED_DIR / "caged_limpo.parquet"
    df_limpo.to_parquet(caminho, index=False)
    print(f"Dados limpos salvos em: {caminho} ({len(df_limpo):,} registros)")

    return df_limpo


if __name__ == "__main__":
    from ingest import carregar_dados

    df_raw = carregar_dados()
    df_clean = processar(df_raw)
    print(df_clean.dtypes)
    print(df_clean.head())
