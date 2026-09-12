@echo off
echo ========================================================
echo   PADRONIZACAO DE AMBIENTE E EXECUCAO DO TEST HARNESS
echo ========================================================

IF NOT EXIST ".venv" (
    echo [1/3] Criando ambiente virtual isolado (.venv)...
    where py >nul 2>nul
    IF NOT ERRORLEVEL 1 (
        py -m venv .venv
    ) ELSE (
        python -m venv .venv
    )
) ELSE (
    echo [1/3] Ambiente virtual (.venv) ja detectado.
)

echo [2/3] Ativando .venv e sincronizando dependencias...
call .venv\Scripts\activate
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo [3/3] Executando Harness de Testes (pytest)...
echo --------------------------------------------------------
pytest -v
echo --------------------------------------------------------
pause