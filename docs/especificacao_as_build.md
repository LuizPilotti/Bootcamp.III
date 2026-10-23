# ESPECIFICAÇÃO TÉCNICA DEFINITIVA (SDD AS-BUILT)
**Projeto:** API REST Task Manager & Logger  
**Repositório:** [Bootcamp.III](https://github.com/LuizPilotti/Bootcamp.III)  
**Release:** v1.0.0  
**Data:** 23 de Outubro de 2026  

---

## 1. Visão Geral do Sistema
A aplicação consiste em uma API REST desenvolvida sob a abordagem **Spec-Driven Development (SDD)** para gerenciamento de tarefas e logs estruturados. O sistema prioriza robustez, sanitização de entradas, idempotência em operações de estado e cobertura completa de testes.

## 2. Arquitetura e Tecnologia
- **Linguagem:** Python 3.12+ / 3.14
- **Framework Web:** FastAPI
- **Validação de Schemas:** Pydantic
- **Test Harness:** Pytest com Pytest-Cov (22 testes automatizados | 99% de cobertura)
- **Containerização:** Docker & Docker Compose
- **Integração Contínua:** GitHub Actions (`.github/workflows/tests.yml`)

---

## 3. Contratos de API & Regras de Negócio

### 3.1 Health Check
- `GET /health` -> Retorna HTTP 200 `{"status": "ok"}` para monitoramento do serviço.

### 3.2 Gerenciamento de Tarefas (`/tasks`)
- `POST /tasks` -> Criação de tarefa.
  - **Validação SDD:** Títulos vazios ou compostos exclusivamente por espaços (`whitespace_only`) são sanitizados (`strip()`) e rejeitados com HTTP 422 Unprocessable Entity.
- `GET /tasks` -> Listagem de todas as tarefas cadastradas.
- `GET /tasks/{task_id}` -> Busca por ID.
  - **Sanitização:** IDs inexistentes ou negativos retornam HTTP 404 Not Found de forma graciosa.
- `PUT /tasks/{task_id}/complete` -> Conclusão de tarefa.
  - **Garantia de Idempotência:** Concluir uma tarefa já finalizada mantém o estado de forma consistente sem levantar exceções, retornando HTTP 200.

---

## 4. Módulo de Logging (`src/logger.py`)
- Módulo isolado para geração de logs estruturados em arquivo físico e terminal.
- Garante a não duplicidade de *handlers* e criação automática do diretório de logs (`logs/`).

---

## 5. Homologação do Test Harness
- **Total de Testes:** 22/22 Aprovados (100% Pass)
- **Métricas de Cobertura:**
  - `src/__init__.py`: 100%
  - `src/logger.py`: 96%
  - `src/main.py`: 100%
  - **TOTAL:** 99%