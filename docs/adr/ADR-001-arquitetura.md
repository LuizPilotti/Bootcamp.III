# ADR-001 — Arquitetura da API e Padronização de Ambiente

## Status
Aceito

## Contexto
O projeto precisa de uma estrutura enxuta, testável e reproduzível para demonstrar o fluxo de Spec-Driven Development (SDD). Inicialmente considerou-se a conteinerização estrita via Docker, porém optou-se pela padronização via scripts automatizados equivalentes para evitar dependências pesadas de virtualização local sem abrir mão da reprodutibilidade.

## Decisão
- API REST construída em Python com FastAPI e Pydantic para validação rígida de contratos.
- Armazenamento em memória com rotina utilitária de reset de estado para testes.
- Padronização de ambiente garantida por scripts de automação (`run_tests.bat` e `run_tests.sh`) que instalam dependências fixadas em um ambiente virtual isolado (`.venv`).
- Test Harness automatizado utilizando `pytest` e `TestClient`.

## Consequências
- Execução imediata em qualquer sistema operacional sem overhead de máquinas virtuais ou WSL.
- Ambiente 100% reproduzível via execução em comando único.
- Facilidade na orquestração dos testes tanto localmente quanto no pipeline de CI.