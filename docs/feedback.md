# Histórico de Refinamento por Feedback (SDD)

Este documento registra as iterações e refinamentos realizados na especificação e arquitetura com base em revisões do grupo, testes prévios e feedback do processo de desenvolvimento orientado por especificação (Spec-Driven Development).

---

## Ciclo 1 — Especificação Inicial e Escopo Base
- **Proposta Inicial:** Criação de endpoints CRUD mínimos para gerenciar tarefas (`POST /tasks`, `GET /tasks`, `GET /tasks/{id}`, `PATCH /tasks/{id}/complete`).
- **Feedback da Equipe:** A especificação inicial não deixava explícita a regra para títulos contendo apenas caracteres de espaçamento nem como orquestrar a saúde do serviço em ambientes de CI/CD.
- **Ações Realizadas:**
  - Inclusão do endpoint `GET /health` para simplificar sondagens de liveness em pipelines e contêineres.
  - Definição do comportamento estrito de validação para campos de texto.

---

## Ciclo 2 — Refinamento por Testes Prévios (Casos de Borda)
- **Problema Detectado nos Testes:** Ao submeter payloads como `{"title": "   "}`, a validação padrão de string aceitava a requisição, violando o princípio de integridade de dados.
- **Feedback dos Testes:** É indispensável rejeitar payloads compostos unicamente por espaços vazios e retornar código de status `422 Unprocessable Entity`.
- **Ações Realizadas:**
  - Implementação de um validador semântico (`@field_validator("title")`) com rotina de trimming.
  - Adição de testes de borda dedicados no Test Harness (`test_title_whitespace_only` e `test_title_is_required_empty_string`).
  - Verificação de idempotência no endpoint de conclusão (`PATCH /tasks/{id}/complete`), assegurando que concluir uma tarefa repetidas vezes retorna `200 OK` e preserva `completed = true`.

---

## Ciclo 3 — Refinamento de Governança e Isolamento de Estado
- **Feedback de Arquitetura:** Testes unitários executados em sequência compartilhavam a memória global, causando interferência mútua na contagem de IDs e listagem de tarefas.
- **Ações Realizadas:**
  - Criação da função de isolamento `reset_database()` invocada via fixture `setup_function()` antes de cada teste do pytest.
  - Formalização da arquitetura em ADR-001 (FastAPI + Armazenamento em memória com reset + TestClient).
  - Estruturação do fluxo de branches no Git (`main`, `develop`, `feature/*`), proibindo commits diretos na `main` e padronizando templates de Pull Request e Issues.

---

## Ciclo 4 — Observabilidade Local e Expansão do Test Harness
- **Feedback da Equipe:** A ausência de mecanismo de log dificultava a depuração de requisições e a rastreabilidade de eventos durante desenvolvimento e testes manuais.
- **Problema Detectado:** Alguns cenários de borda válidos (description default, sequencialidade de IDs, preservação de campos ao concluir, Content-Type do health, títulos longos) não possuíam cobertura explícita no Test Harness.
- **Ações Realizadas:**
  - Criação do módulo de logging local (`src/logger.py`) utilizando exclusivamente a biblioteca padrão `logging` do Python, sem dependências externas.
  - Implementação de middleware HTTP no FastAPI para registro automático de cada requisição (método, path, status code, tempo de resposta).
  - Geração automática de arquivos de log diários na pasta `logs/` (adicionada ao `.gitignore`).
  - Adição de 5 novos testes de borda no Test Harness (`tests/test_tasks.py`) e criação de suíte dedicada para o logger (`tests/test_logger.py`).
  - Registro da decisão arquitetural em ADR-002 (`docs/adr/ADR-002-logging.md`).

