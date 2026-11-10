"""Gera resumos por produto a partir de um CSV de vendas."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


CAMPOS_OBRIGATORIOS = {"data", "produto", "quantidade", "valor_unitario"}


def validar_linha(linha: dict[str, str], numero: int) -> tuple[date, str, int, Decimal]:
    """Converte e valida uma linha; inclui o numero da linha em erros."""
    try:
        data_venda = date.fromisoformat(linha["data"].strip())
        produto = linha["produto"].strip()
        quantidade = int(linha["quantidade"].strip())
        valor_unitario = Decimal(linha["valor_unitario"].strip())
    except (AttributeError, KeyError, ValueError, InvalidOperation) as erro:
        raise ValueError(f"linha {numero}: campo ausente ou formato invalido ({erro})") from erro

    if not produto:
        raise ValueError(f"linha {numero}: produto vazio")
    if quantidade <= 0:
        raise ValueError(f"linha {numero}: quantidade deve ser maior que zero")
    if not valor_unitario.is_finite() or valor_unitario < 0:
        raise ValueError(f"linha {numero}: valor_unitario deve ser um numero nao negativo")

    return data_venda, produto, quantidade, valor_unitario


def processar(arquivo_entrada: Path, arquivo_saida: Path) -> tuple[int, int]:
    """Gera resumo e relatorio de erros. Retorna (linhas validas, invalidas)."""
    arquivo_erros = arquivo_saida.with_name(f"{arquivo_saida.stem}_erros.csv")
    caminhos = {arquivo_entrada.resolve(), arquivo_saida.resolve(), arquivo_erros.resolve()}
    if len(caminhos) != 3:
        raise ValueError("arquivos de saida nao podem substituir o arquivo de entrada")

    totais: dict[str, list[int | Decimal]] = defaultdict(lambda: [0, Decimal("0")])
    erros: list[dict[str, str]] = []
    linhas_validas = 0

    with arquivo_entrada.open("r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        campos = set(leitor.fieldnames or [])
        faltantes = CAMPOS_OBRIGATORIOS - campos
        if faltantes:
            nomes = ", ".join(sorted(faltantes))
            raise ValueError(f"colunas obrigatorias ausentes: {nomes}")

        for numero, linha in enumerate(leitor, start=2):
            try:
                _, produto, quantidade, valor_unitario = validar_linha(linha, numero)
            except ValueError as erro:
                erros.append({"linha": str(numero), "motivo": str(erro)})
                continue

            totais[produto][0] += quantidade
            totais[produto][1] += quantidade * valor_unitario
            linhas_validas += 1

    arquivo_saida.parent.mkdir(parents=True, exist_ok=True)
    with arquivo_saida.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["produto", "unidades", "receita"])
        for produto, (unidades, receita) in sorted(totais.items()):
            escritor.writerow([produto, unidades, f"{receita:.2f}"])

    with arquivo_erros.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["linha", "motivo"])
        escritor.writeheader()
        escritor.writerows(erros)

    return linhas_validas, len(erros)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("arquivo", type=Path, help="caminho do CSV de entrada")
    parser.add_argument("--saida", type=Path, default=Path("saida/resumo.csv"))
    argumentos = parser.parse_args()

    if not argumentos.arquivo.is_file():
        parser.error(f"arquivo nao encontrado: {argumentos.arquivo}")

    try:
        linhas_validas, linhas_invalidas = processar(argumentos.arquivo, argumentos.saida)
    except (OSError, csv.Error, ValueError) as erro:
        parser.error(str(erro))

    print(f"Resumo salvo em: {argumentos.saida}")
    print(f"Linhas validas: {linhas_validas}; linhas invalidas: {linhas_invalidas}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
