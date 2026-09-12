#!/bin/sh
set -e

echo "==> [1/3] Verificando e criando ambiente virtual (.venv)..."
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

echo "==> [2/3] Ativando ambiente e instalando dependencias..."
. .venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "==> [3/3] Executando Harness de Testes..."
pytest -v