# Projeto SDD — Gerenciador de Tarefas

Projeto acadêmico estruturado para desenvolvimento orientado por especificação (SDD / Spec-Driven Development).

## Objetivo
Disponibilizar uma API simples para criação, consulta, atualização e conclusão de tarefas.

## Estrutura
- `docs/especificacao.md` — especificação técnica do problema.
- `docs/adr/ADR-001-arquitetura.md` — decisão arquitetural.
- `.cursor/rules/project-rules.md` — regras/contexto para agente de IA.
- `Dockerfile` e `docker-compose.yml` — ambiente padronizado.
- `src/` — aplicação.
- `tests/` — harness de testes.
- `.github/workflows/tests.yml` — pipeline de testes.
- `.github/pull_request_template.md` — padrão de Pull Request.

## Execução com Docker

```bash
docker compose up --build
```

A API ficará disponível em `http://localhost:8000`.

## Testes

Localmente:

```bash
pip install -r requirements.txt
pytest -q
```

Com Docker:

```bash
docker compose run --rm app pytest -q
```

## Endpoints

- `GET /health`
- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}/complete`

## Governança Git

Fluxo sugerido:
- `main` — branch protegida.
- `develop` — integração.
- `feature/*` — desenvolvimento de funcionalidades.

Não são previstos commits diretos em `main`; alterações devem passar por Pull Request e revisão.
