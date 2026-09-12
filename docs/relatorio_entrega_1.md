# Relatório de Submissão — Entrega 1
## Ambiente, Especificação Técnica e Test Harness

---

### 👥 Identificação da Equipe
- **Repositório GitHub:** [https://github.com/LuizPilotti/Bootcamp.III](https://github.com/LuizPilotti/Bootcamp.III)
- **Branch de Desenvolvimento / Entrega:** `feature/entrega-1-sdd-test-harness` (ou PR vinculado à `develop`)
- **Integrantes:**
  1. *[Nome Completo do Integrante 1]* — RA: *[00000000]*
  2. *[Nome Completo do Integrante 2]* — RA: *[00000000]*
  3. *[Nome Completo do Integrante 3]* — RA: *[00000000]*
  4. *[Nome Completo do Integrante 4]* — RA: *[00000000]*

---

### 1. Governança e Estrutura do Projeto
- **Política de Branches:** O repositório segue um modelo estruturado com as branches `main`, `develop` e `feature/*`. A branch `main` é protegida, sendo proibidos commits diretos.
- **Decomposição e Gestão de Tarefas:** Tarefas decompostas a partir dos requisitos funcionais (`RF01` a `RF06`) e não funcionais, utilizando templates padronizados de Issues (`.github/ISSUE_TEMPLATE/task_template.md`).
- **Code Review:** Pull Requests submetidos com checklist de aceitação SDD e aprovação entre pares via `.github/pull_request_template.md`.
- **ADRs (Architecture Decision Records):** Decisões técnicas registradas sinteticamente no `README.md` e detalhadas em `docs/adr/ADR-001-arquitetura.md` (escolha de FastAPI, Pydantic, armazenamento em memória isolado e automação sem dependência pesada de virtualização).

---

### 2. Especificação Técnica (Spec-Driven Development)
- **Documento Canônico:** Localizado em `docs/especificacao.md`, definindo escopo, modelo de dados (`Task`), contratos de entrada/saída HTTP REST, regras de negócio e critérios de aceitação.
- **Decomposição em Unidades:**
  1. *Contratos e DTOs:* `TaskCreate` e `Task` com Pydantic.
  2. *Validação Semântica de Negócio:* `@field_validator` garantindo rejeição de strings vazias ou compostas unicamente por espaços.
  3. *Repositório e Estado:* Dicionário em memória com função de reset (`reset_database`) para isolamento dos testes.
  4. *Controladores HTTP:* Roteamento FastAPI com códigos HTTP padronizados (`200`, `201`, `404`, `422`).
- **Refinamento Iterativo:** Registrado em `docs/feedback.md`, documentando melhorias a partir de feedbacks e testes prévios (inclusão de health check, sanitização de espaços e controle de idempotência).

---

### 3. Ambiente Padronizado e Orquestração de Agentes de IA
- **Agentes Utilizados:** **Antigravity** e **Cursor**, guiados pelas diretrizes de contexto em `AGENTS.md` e `.cursorrules`.
- **Fluxo do Agente:** O agente opera no ciclo `Especificação -> Decomposição -> Testes no Harness -> Implementação Mínima -> Validação`.
- **Padronização de Ambiente:**
  - Script Windows: `run_tests.bat` (cria/ativa `.venv`, instala dependências e dispara os testes em 1 comando).
  - Script Linux/macOS: `run_tests.sh`.
  - Alternativa Conteinerizada: `Dockerfile` e `docker-compose.yml`.

---

### 4. Test Harness & Evidências de Execução
O Test Harness foi construído com `pytest` e `TestClient`, totalizando **15 cenários de teste automatizados** cobrindo fluxos principais e casos de borda:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.4, pytest-8.4.2, pluggy-1.6.0
rootdir: Bootcamp.III
plugins: anyio-4.15.1
collected 15 items

tests/test_tasks.py::test_health PASSED                                  [  6%]
tests/test_tasks.py::test_create_task PASSED                             [ 13%]
tests/test_tasks.py::test_list_tasks PASSED                              [ 20%]
tests/test_tasks.py::test_get_task_success PASSED                        [ 26%]
tests/test_tasks.py::test_complete_task PASSED                           [ 33%]
tests/test_tasks.py::test_list_tasks_empty PASSED                        [ 40%]
tests/test_tasks.py::test_create_task_missing_title_field PASSED         [ 46%]
tests/test_tasks.py::test_title_is_required_empty_string PASSED          [ 53%]
tests/test_tasks.py::test_title_whitespace_only PASSED                   [ 60%]
tests/test_tasks.py::test_get_missing_task PASSED                        [ 66%]
tests/test_tasks.py::test_get_task_invalid_id_type PASSED                [ 73%]
tests/test_tasks.py::test_complete_missing_task PASSED                   [ 80%]
tests/test_tasks.py::test_complete_task_idempotency PASSED               [ 86%]
tests/test_tasks.py::test_create_task_title_with_surrounding_whitespace PASSED [ 93%]
tests/test_tasks.py::test_get_task_negative_id_not_found PASSED          [100%]

======================= 15 passed, 2 warnings in 0.51s ========================
```

> **Instrução para os Alunos:** Para gerar o PDF para submissão no Moodle, preencha os nomes e RAs acima, anexe um print da tela do terminal executando `run_tests.bat` (ou `pytest -v`) e exporte este arquivo como PDF.
