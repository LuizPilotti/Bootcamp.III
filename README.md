# 🚀 Projeto SDD — Gerenciador de Tarefas

> **Entrega 1: Ambiente, Especificação Técnica e Test Harness**  
> Projeto estruturado e desenvolvido seguindo a metodologia **Spec-Driven Development (SDD)**, com apoio de agentes inteligentes de IA, governança de repositório e infraestrutura de validação automatizada (Test Harness).

---

## 📌 Visão Geral e Objetivo

O objetivo deste projeto é fornecer uma **API REST modular e resiliente** para o gerenciamento do ciclo de vida de tarefas (criação, listagem, consulta por identificador e conclusão). O desenvolvimento é orientado estritamente por especificação prévia, garantindo que contratos de entrada/saída, regras de validação e casos de borda sejam definidos e cobertos por testes antes e durante a implementação.

---

## 🏛️ Registro Sintético de Decisões Arquiteturais (ADRs)

| ADR | Título | Status | Resumo da Decisão Técnica |
| :--- | :--- | :--- | :--- |
| [**ADR-001**](docs/adr/ADR-001-arquitetura.md) | Arquitetura da API e Padronização de Ambiente | **Aceito** | Adoção de **FastAPI** + **Pydantic v2** para validação estrita de tipos e contratos HTTP REST. Persistência em memória com rotina utilitária de isolamento/reset de estado para testes. Padronização via scripts de execução direta (`run_tests.bat`, `run_tests.sh`) com isolamento em `.venv` e suporte alternativo via contêineres Docker. |

---

## 📂 Estrutura do Repositório

```text
├── .cursor/
│   └── rules/project-rules.md     # Regras de contexto para agentes de IA no Cursor
├── .cursorrules                   # Regras de orquestração na raiz do repositório
├── AGENTS.md                      # Diretrizes globais de orquestração (Antigravity/Cursor/Claude)
├── docs/
│   ├── adr/
│   │   └── ADR-001-arquitetura.md # Arquivo detalhado da ADR-001
│   ├── especificacao.md           # Especificação técnica do problema (RFs, RNFs, Contratos e Unidades)
│   ├── feedback.md                # Registro iterativo de refinamentos por feedback
│   └── relatorio_entrega_1.md     # Relatório formatado para submissão (PDF Moodle)
├── src/
│   ├── __init__.py
│   └── main.py                    # Implementação FastAPI da API e regras de negócio
├── tests/
│   ├── __init__.py
│   └── test_tasks.py              # Test Harness com suíte de testes e casos de borda
├── .github/
│   ├── ISSUE_TEMPLATE/            # Templates para decomposição de tarefas da sprint
│   ├── workflows/tests.yml        # Pipeline automatizado de CI (GitHub Actions)
│   └── pull_request_template.md   # Template institucional para Pull Requests e Code Review
├── Dockerfile                     # Empacotamento da aplicação em contêiner
├── docker-compose.yml             # Orquestração do serviço via Docker
├── requirements.txt               # Dependências pinadas do ecossistema Python
├── run_tests.bat                  # Script de execução automatizada em 1 clique (Windows)
├── run_tests.sh                   # Script de execução automatizada em 1 comando (Linux/macOS)
├── test_execution.log             # Log comprobatório da execução do Test Harness
└── README.md                      # Documentação técnica principal
```

---

## 🌿 Governança do Projeto e Fluxo de Versionamento

Para garantir rastreabilidade, colaboração segura e qualidade contínua de código, o projeto adota o seguinte modelo de governança:

### 1. Estrutura de Branches
- **`main`**: Branch de produção/estável. **Commits diretos são estritamente proibidos**.
- **`develop`**: Branch de integração para consolidação de funcionalidades.
- **`feature/<nome-da-tarefa>`**: Branches dedicadas para implementação de tarefas independentes decompostas na sprint.

### 2. Decomposição de Tarefas e Divisão em Equipe
- As tarefas são planejadas e decompostas no GitHub Projects / Issues com base nos requisitos da especificação (`RF01` a `RF06` e `RNFs`).
- Cada issue descreve o escopo, unidades envolvidas e critérios de aceitação.

### 3. Code Review e Política de Pull Requests
- Toda alteração deve ser submetida via **Pull Request (PR)** preenchendo o template padronizado ([`.github/pull_request_template.md`](.github/pull_request_template.md)).
- O merge exige:
  1. Suíte de testes passando com 100% de sucesso.
  2. Aprovação de ao menos um membro revisor (Code Review entre pares).
  3. Atualização correspondente na documentação (`especificacao.md` ou `feedback.md`), se houver mudança de comportamento.

---

## 🤖 Configuração e Orquestração de Agentes de IA

O projeto foi configurado para atuar no fluxo **Spec-Driven Development (SDD)** com auxílio de agentes inteligentes de engenharia de software (como **Antigravity**, **Cursor** e **Claude Code**).

- **Diretrizes Globais:** Definidas em [`AGENTS.md`](AGENTS.md) e [`.cursorrules`](.cursorrules).
- **Ciclo Operacional do Agente:**
  1. Leitura e interpretação da especificação canônica ([`docs/especificacao.md`](docs/especificacao.md)).
  2. Identificação ou escrita dos testes no Test Harness ([`tests/test_tasks.py`](tests/test_tasks.py)).
  3. Implementação e refatoração de código mínimo necessário.
  4. Execução automatizada dos testes e registro de refinamento em [`docs/feedback.md`](docs/feedback.md).

---

## ⚙️ Guia de Instalação e Execução

### Opção A — Execução Automatizada (Recomendado)

#### No Windows:
Dê um duplo clique no arquivo ou execute no PowerShell/CMD:
```cmd
run_tests.bat
```
*O script detecta/cria o ambiente virtual `.venv`, sincroniza as dependências do `requirements.txt` e executa o Test Harness com `pytest -v`.*

#### No Linux / macOS:
No terminal, execute:
```bash
chmod +x run_tests.sh
./run_tests.sh
```

---

### Opção B — Execução Manual (Python)

1. **Criar e ativar o ambiente virtual:**
   ```bash
   # Windows
   py -m venv .venv
   .venv\Scripts\activate

   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar o Test Harness:**
   ```bash
   pytest -v
   ```

4. **Subir a API localmente:**
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```
   Acesse a documentação interativa Swagger em: `http://localhost:8000/docs`

---

### Opção C — Execução via Docker / Docker Compose

1. **Subir a aplicação em contêiner:**
   ```bash
   docker compose up --build
   ```

2. **Executar os testes no ambiente conteinerizado:**
   ```bash
   docker compose run --rm app pytest -v
   ```

---

## 🧪 Test Harness e Evidências de Execução

O Test Harness cobre todos os fluxos de sucesso (Happy Path) e cenários de borda (Edge Cases) mapeados na especificação técnica.

### Resumo da Suíte de Testes

| Categoria | Cenário | Status |
| :--- | :--- | :---: |
| **Health Check** | Verificação de integridade operacional (`GET /health`) | `PASSED` |
| **Criação** | Criação com payload válido (`POST /tasks`) | `PASSED` |
| **Listagem** | Listar múltiplas tarefas cadastradas (`GET /tasks`) | `PASSED` |
| **Consulta** | Consultar tarefa por ID existente (`GET /tasks/{id}`) | `PASSED` |
| **Conclusão** | Concluir tarefa existente alterando status (`PATCH /tasks/{id}/complete`) | `PASSED` |
| **Borda: Vazio** | Listar tarefas com repositório vazio retornando `[]` | `PASSED` |
| **Borda: Validação** | Rejeição de payload sem campo `title` (`HTTP 422`) | `PASSED` |
| **Borda: Validação** | Rejeição de título como string vazia `""` (`HTTP 422`) | `PASSED` |
| **Borda: Validação** | Rejeição de título composto apenas por espaços (`HTTP 422`) | `PASSED` |
| **Borda: Sanitização**| Trim de espaços externos preservando conteúdo interno | `PASSED` |
| **Borda: Consulta** | Consulta de ID inexistente (`HTTP 404`) | `PASSED` |
| **Borda: Consulta** | Consulta com ID alfanumérico inválido (`HTTP 422`) | `PASSED` |
| **Borda: Consulta** | Consulta com ID numérico negativo (`HTTP 404`) | `PASSED` |
| **Borda: Conclusão** | Concluir tarefa inexistente (`HTTP 404`) | `PASSED` |
| **Borda: Idempotência** | Concluir tarefa repetidas vezes mantendo `completed = true` | `PASSED` |

Para visualizar os logs detalhados, consulte o arquivo [`test_execution.log`](test_execution.log) e o documento de submissão [`docs/relatorio_entrega_1.md`](docs/relatorio_entrega_1.md).