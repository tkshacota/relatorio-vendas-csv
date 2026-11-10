# Relatorio de vendas em CSV

Projeto pessoal em Python para transformar um arquivo CSV de vendas em um resumo por produto e separar linhas com dados invalidos.

O exemplo usa dados sinteticos. O programa le o arquivo de entrada sem altera-lo e grava os relatorios em novos arquivos.

Este projeto foi preparado com apoio de IA como material inicial de portfólio. Revise e compreenda o código antes de adaptá-lo ou apresentá-lo.

## Recursos

- Confere colunas obrigatorias, datas, quantidades e valores.
- Soma unidades e receita por produto usando `Decimal`.
- Gera um CSV de resumo e outro com as linhas rejeitadas e os motivos.
- Usa somente a biblioteca padrao do Python.

## Como executar

Requer Python 3.10 ou superior.

```bash
python src/relatorio_vendas.py examples/vendas.csv --saida saida/resumo.csv
```

O programa cria a pasta de saida se necessario. O arquivo de erros recebe o sufixo `_erros.csv`.

## Formato de entrada

O CSV deve usar virgula como separador e estas colunas:

```text
data,produto,quantidade,valor_unitario
2026-01-10,Caderno,3,12.50
2026-01-10,Caneta,5,2.00
```

Datas devem estar no formato `AAAA-MM-DD`; quantidades devem ser inteiros positivos e valores devem usar ponto decimal.

## Estrutura

```text
examples/vendas.csv       # dados sinteticos
src/relatorio_vendas.py   # leitura, validacao e agregacao
```

## Limites

Este e um projeto de estudo e demonstracao. Ele nao substitui conciliacao contabil, ERP ou validacao fiscal.
