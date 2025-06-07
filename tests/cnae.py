"""test file para ler o cnae do excel do ibge"""

from pathlib import Path

from openpyxl import load_workbook


def read_cnae(file_path: Path) -> dict:
    """Lê o arquivo Excel do IBGE e retorna um dicionário com os dados do CNAE.

    Args:
        file_path (Path): Caminho para o arquivo Excel.

    Returns:
        dict: Dicionário contendo os dados do CNAE.
    """
    wb = load_workbook(file_path)
    ws = wb.active
    cnae_dict = {}

    for row in ws.iter_rows(min_row=2, values_only=True):
        cnae_code, description = row[0], row[1]
        cnae_dict[cnae_code] = description

    return cnae_dict
