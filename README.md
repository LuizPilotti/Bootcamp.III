# 🚀 Projeto SDD — Gerenciador de Tarefas

> **Entrega 1: Ambiente, Especificação Técnica e Test Harness**
> Projeto estruturado e desenvolvido seguindo a metodologia **Spec-Driven Development (SDD)**, com apoio de agentes inteligentes de IA, governança de repositório e infraestrutura de validação automatizada (Test Harness).

---

## 📌 Visão Geral e Objetivo

O objetivo deste projeto é fornecer uma **API REST modular e resiliente** para o gerenciamento do ciclo de vida de tarefas, contemplando criação, listagem, consulta por identificador e conclusão.

O desenvolvimento é orientado estritamente por especificação prévia, garantindo que contratos de entrada e saída, regras de validação e casos de borda sejam definidos e cobertos por testes antes e durante a implementação.

A aplicação também disponibiliza um endpoint de verificação de integridade, permitindo confirmar rapidamente se o serviço está operacional.

---

## 🌐 Funcionalidades e Endpoints da API

A aplicação disponibiliza uma API REST para criação, consulta, listagem e conclusão de tarefas.

| Método  | Endpoint                    | Descrição                              | Respostas principais                                  |
| :------ | :-------------------------- | :------------------------------------- | :---------------------------------------------------- |
| `GET`   | `/health`                   | Verifica se a API está operacional     | `200 OK`                                              |
| `POST`  | `/tasks`                    | Cria uma nova tarefa                   | `201 Created`, `422 Unprocessable Entity`             |
| `GET`   | `/tasks`                    | Lista todas as tarefas cadastradas     | `200 OK`                                              |
| `GET`   | `/tasks/{task_id}`          | Consulta uma tarefa pelo identificador | `200 OK`, `404 Not Found`, `422 Unprocessable Entity` |
| `PATCH` | `/tasks/{task_id}/complete` | Marca uma tarefa como concluída        | `200 OK`, `404 Not Found`                             |

### Health Check

Requisição:

```http
GET /health
```

Resposta esperada:

```json
{
  "status": "ok"
}
```

---

### Criar uma tarefa

Endpoint:

```http
POST /tasks
```

Exemplo de payload:

```json
{
  "title": "Estudar SDD",
  "description": "Revisar o Test Harness"
}
```

Resposta esperada:

```json
{
  "id": 1,
  "title": "Estudar SDD",
  "description": "Revisar o Test Harness",
  "completed": false
}
```

O identificador da tarefa é gerado automaticamente.

Toda nova tarefa é criada inicialmente com:

```json
{
  "completed": false
}
```

---

### Listar tarefas

Endpoint:

```http
GET /tasks
```

Exemplo de resposta:

```json
[
  {
    "id": 1,
    "title": "Estudar SDD",
    "description": "Revisar o Test Harness",
    "completed": false
  },
  {
    "id": 2,
    "title": "Executar testes",
    "description": "",
    "completed": true
  }
]
```

Caso nenhuma tarefa esteja cadastrada, a API retorna:

```json
[]
```

---

### Consultar tarefa por ID

Endpoint:

```http
GET /tasks/{task_id}
```

Exemplo:

```http
GET /tasks/1
```

Resposta:

```json
{
  "id": 1,
  "title": "Estudar SDD",
  "description": "Revisar o Test Harness",
  "completed": false
}
```

Caso o identificador não exista:

```json
{
  "detail": "Tarefa não encontrada"
}
```

com status:

```text
404 Not Found
```

Identificadores em formatos incompatíveis, como valores alfanuméricos, são rejeitados pelo FastAPI com status `422`.

---

### Concluir tarefa

Endpoint:

```http
PATCH /tasks/{task_id}/complete
```

Exemplo:

```http
PATCH /tasks/1/complete
```

Resposta:

```json
{
  "id": 1,
  "title": "Estudar SDD",
  "description": "Revisar o Test Harness",
  "completed": true
}
```

A operação é **idempotente**.

Isso significa que executar o endpoint novamente para uma tarefa já concluída não gera erro e mantém:

```json
{
  "completed": true
}
```

---

## ✅ Regras de Validação

O modelo de criação de tarefas possui regras de validação para garantir a integridade dos dados recebidos.

### Campo `title`

O campo `title`:

* é obrigatório;
* deve possuir pelo menos um caractere válido;
* não pode ser uma string vazia;
* não pode conter somente espaços em branco;
* tem espaços externos removidos automaticamente antes do armazenamento.

Exemplo:

Entrada:

```json
{
  "title": "   Estudar SDD   "
}
```

Valor armazenado:

```json
{
  "title": "Estudar SDD"
}
```

Os seguintes exemplos são inválidos:

```json
{
  "title": ""
}
```

```json
{
  "title": "     "
}
```

Esses casos retornam:

```text
HTTP 422 Unprocessable Entity
```

### Campo `description`

O campo `description` é opcional.

Quando não informado, seu valor padrão é:

```json
{
  "description": ""
}
```

---

## 💾 Persistência dos Dados

Nesta versão do projeto, as tarefas são armazenadas **em memória**.

O armazenamento atual utiliza uma estrutura interna da aplicação durante sua execução.

Isso significa que os dados existem apenas enquanto o processo da API estiver ativo.

Ao reiniciar:

* a aplicação;
* o processo do Uvicorn;
* ou o contêiner Docker;

os dados cadastrados anteriormente são perdidos.

Não há banco de dados externo configurado nesta versão do projeto.

### Isolamento dos Testes

A aplicação possui a função:

```python
reset_database()
```

Essa rotina é utilizada pelo Test Harness para restaurar o estado do armazenamento em memória antes de cada cenário de teste.

Ela:

* remove todas as tarefas existentes;
* restaura o contador de IDs;
* garante que um teste não interfira no resultado do próximo.

---

## 🧱 Tecnologias Utilizadas

O projeto utiliza atualmente:

* **Python**
* **FastAPI**
* **Pydantic v2**
* **Uvicorn**
* **Pytest**
* **HTTPX**
* **Docker**
* **Docker Compose**
* **Git**
* **GitHub Actions**

O FastAPI é utilizado para construção da API REST e geração automática da documentação.

O Pydantic é responsável pela validação dos modelos de entrada e saída.

O Pytest compõe o Test Harness utilizado para validação automatizada dos requisitos.

---

## 🏛️ Registro Sintético de Decisões Arquiteturais (ADRs)

| ADR                                            | Título                                        | Status     | Resumo da Decisão Técnica                                                                                                                                                                                                                                                                                                                     |
| :--------------------------------------------- | :-------------------------------------------- | :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [**ADR-001**](docs/adr/ADR-001-arquitetura.md) | Arquitetura da API e Padronização de Ambiente | **Aceito** | Adoção de **FastAPI** + **Pydantic v2** para validação estrita de tipos e contratos HTTP REST. Persistência em memória com rotina utilitária de isolamento/reset de estado para testes. Padronização via scripts de execução direta (`run_tests.bat`, `run_tests.sh`) com isolamento em `.venv` e suporte alternativo via contêineres Docker. |

---

## 📂 Estrutura do Repositório

```text
├── .cursor/
│   └── rules/project-rules.md      # Regras de contexto para agentes de IA no Cursor
├── .github/
│   ├── ISSUE_TEMPLATE/             # Templates para decomposição de tarefas da sprint
│   ├── workflows/
│   │   └── tests.yml               # Pipeline automatizado de CI com GitHub Actions
│   └── pull_request_template.md    # Template institucional para Pull Requests
├── docs/
│   ├── adr/
│   │   └── ADR-001-arquitetura.md  # Arquivo detalhado da ADR-001
│   ├── especificacao.md            # Especificação técnica do problema
│   ├── feedback.md                 # Registro iterativo de refinamentos
│   └── relatorio_entrega_1.md      # Relatório formatado para submissão
├── src/
│   ├── __init__.py
│   └── main.py                     # Implementação FastAPI da API
├── tests/
│   ├── __init__.py
│   └── test_tasks.py               # Test Harness e casos de borda
├── .cursorrules                    # Regras de orquestração para agentes no Cursor
├── .gitignore                      # Arquivos, caches e ambientes ignorados pelo Git
├── AGENTS.md                       # Diretrizes globais de orquestração de agentes
├── Dockerfile                      # Empacotamento da aplicação em contêiner
├── docker-compose.yml              # Orquestração do serviço via Docker
├── requirements.txt                # Dependências e faixas de versões Python
├── run_tests.bat                   # Script automatizado para Windows
├── run_tests.sh                    # Script automatizado para Linux/macOS
├── test_execution.log              # Evidência da execução do Test Harness
└── README.md                       # Documentação técnica principal
```

---

## 🌿 Governança do Projeto e Fluxo de Versionamento

Para garantir rastreabilidade, colaboração segura e qualidade contínua de código, o projeto adota um modelo estruturado de governança.

### 1. Estrutura de Branches

#### `main`

Branch de produção e versão estável do projeto.

**Commits diretos são estritamente proibidos.**

#### `develop`

Branch de integração utilizada para consolidação de funcionalidades antes da incorporação à versão estável.

#### `feature/<nome-da-tarefa>`

Branches dedicadas ao desenvolvimento de funcionalidades, correções ou melhorias independentes.

Exemplo:

```text
feature/atualiza-readme
```

---

### 2. Decomposição de Tarefas e Divisão em Equipe

As tarefas são planejadas e decompostas no GitHub Projects e/ou Issues com base nos requisitos definidos na especificação.

Cada issue deve representar uma unidade de trabalho rastreável e possuir:

* escopo;
* requisitos relacionados;
* critérios de aceitação;
* responsável;
* evidências de validação quando aplicável.

---

### 3. Code Review e Política de Pull Requests

Toda alteração deve ser submetida através de **Pull Request (PR)** utilizando o template padronizado:

```text
.github/pull_request_template.md
```

O merge exige:

1. Suíte de testes passando com 100% de sucesso.
2. Aprovação de ao menos um membro revisor.
3. Atualização correspondente da documentação quando houver mudança de comportamento.
4. Ausência de regressões na suíte de testes existente.

---

## 🤖 Configuração e Orquestração de Agentes de IA

O projeto foi configurado para utilizar agentes inteligentes de engenharia de software dentro do fluxo **Spec-Driven Development (SDD)**.

Entre as ferramentas consideradas estão:

* Antigravity;
* Cursor;
* Claude Code;
* Codex CLI.

### Diretrizes Globais

As regras principais estão definidas nos arquivos:

```text
AGENTS.md
.cursorrules
```

Os agentes devem respeitar:

* a especificação como fonte única da verdade;
* a política de branches;
* a preservação dos testes existentes;
* o design mínimo do projeto;
* a validação automatizada antes da conclusão de qualquer alteração.

### Ciclo Operacional do Agente

O fluxo esperado é:

```text
1. Especificação
        ↓
2. Decomposição
        ↓
3. Test Harness
        ↓
4. Implementação
        ↓
5. Validação e Review
```

Durante uma alteração, o agente deve:

1. Ler e interpretar a especificação canônica em `docs/especificacao.md`.
2. Identificar os testes relacionados à funcionalidade.
3. Criar ou ajustar testes quando previsto pela especificação.
4. Implementar somente o código necessário.
5. Executar a suíte automatizada.
6. Registrar refinamentos em `docs/feedback.md`, quando aplicável.

---

## ⚙️ Guia de Instalação e Execução

### Opção A — Execução Automatizada

#### Windows

Execute no PowerShell ou Prompt de Comando:

```cmd
run_tests.bat
```

Também é possível executar o arquivo diretamente através do Explorador de Arquivos.

O script automatiza:

1. verificação/criação do ambiente virtual;
2. instalação das dependências;
3. execução do Test Harness.

---

#### Linux / macOS

Primeiro, conceda permissão de execução:

```bash
chmod +x run_tests.sh
```

Depois:

```bash
./run_tests.sh
```

O script:

1. verifica ou cria o ambiente `.venv`;
2. ativa o ambiente virtual;
3. atualiza o `pip`;
4. instala as dependências;
5. executa `pytest -v`.

---

## 🐍 Opção B — Execução Manual com Python

### 1. Criar o ambiente virtual

#### Windows

```cmd
py -m venv .venv
```

#### Linux/macOS

```bash
python3 -m venv .venv
```

---

### 2. Ativar o ambiente

#### Windows — PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### Windows — CMD

```cmd
.venv\Scripts\activate.bat
```

#### Linux/macOS

```bash
source .venv/bin/activate
```

---

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Executar o Test Harness

```bash
pytest -v
```

---

### 5. Iniciar a API

```bash
uvicorn src.main:app --reload --port 8000
```

A aplicação estará disponível em:

```text
http://localhost:8000
```

---

## 📖 Documentação Interativa

O FastAPI gera automaticamente interfaces para visualização e teste dos endpoints.

### Swagger UI

```text
http://localhost:8000/docs
```

### OpenAPI

```text
http://localhost:8000/openapi.json
```

O Swagger permite executar diretamente pelo navegador as operações da API.

---

## 🧪 Testando Rapidamente a API

Com a aplicação em execução, é possível validar os principais endpoints utilizando `curl`.

### Health Check

```bash
curl http://localhost:8000/health
```

Resposta:

```json
{
  "status": "ok"
}
```

---

### Criar uma tarefa

Linux/macOS:

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Estudar SDD","description":"Revisar o projeto"}'
```

Exemplo de resposta:

```json
{
  "id": 1,
  "title": "Estudar SDD",
  "description": "Revisar o projeto",
  "completed": false
}
```

---

### Listar tarefas

```bash
curl http://localhost:8000/tasks
```

---

### Consultar tarefa

```bash
curl http://localhost:8000/tasks/1
```

---

### Concluir tarefa

```bash
curl -X PATCH http://localhost:8000/tasks/1/complete
```

---

## 🐳 Opção C — Execução via Docker

O projeto também pode ser executado sem configuração direta do ambiente Python local.

### Subir a aplicação

Execute:

```bash
docker compose up --build
```

O Docker Compose constrói a imagem do projeto e inicia a API expondo a porta:

```text
8000
```

Acesse:

```text
http://localhost:8000
```

ou:

```text
http://localhost:8000/docs
```

---

### Executar os testes dentro do contêiner

```bash
docker compose run --rm app pytest -v
```

---

### Encerrar os serviços

```bash
docker compose down
```

---

## 🧪 Test Harness e Evidências de Execução

O Test Harness cobre os fluxos principais da aplicação e os casos de borda definidos para esta entrega.

A execução atual possui:

```text
15 testes
```

com resultado:

```text
15 passed
```

### Resumo da Suíte de Testes

| Categoria               | Cenário                                                      |  Status  |
| :---------------------- | :----------------------------------------------------------- | :------: |
| **Health Check**        | Verificação de integridade operacional (`GET /health`)       | `PASSED` |
| **Criação**             | Criação com payload válido (`POST /tasks`)                   | `PASSED` |
| **Listagem**            | Listagem de múltiplas tarefas (`GET /tasks`)                 | `PASSED` |
| **Consulta**            | Consulta por ID existente (`GET /tasks/{id}`)                | `PASSED` |
| **Conclusão**           | Conclusão de tarefa existente (`PATCH /tasks/{id}/complete`) | `PASSED` |
| **Borda: Vazio**        | Repositório vazio retorna `[]`                               | `PASSED` |
| **Borda: Validação**    | Payload sem `title` retorna `HTTP 422`                       | `PASSED` |
| **Borda: Validação**    | `title` vazio retorna `HTTP 422`                             | `PASSED` |
| **Borda: Validação**    | `title` somente com espaços retorna `HTTP 422`               | `PASSED` |
| **Borda: Sanitização**  | Remove espaços externos do título                            | `PASSED` |
| **Borda: Consulta**     | ID inexistente retorna `HTTP 404`                            | `PASSED` |
| **Borda: Consulta**     | ID alfanumérico retorna `HTTP 422`                           | `PASSED` |
| **Borda: Consulta**     | ID numérico negativo inexistente retorna `HTTP 404`          | `PASSED` |
| **Borda: Conclusão**    | Tarefa inexistente retorna `HTTP 404`                        | `PASSED` |
| **Borda: Idempotência** | Conclusão repetida mantém `completed = true`                 | `PASSED` |

---

## 📋 Execução Atual do Test Harness

Exemplo do resultado esperado:

```text
============================= test session starts =============================

collected 15 items

tests/test_tasks.py::test_health PASSED
tests/test_tasks.py::test_create_task PASSED
tests/test_tasks.py::test_list_tasks PASSED
tests/test_tasks.py::test_get_task_success PASSED
tests/test_tasks.py::test_complete_task PASSED
tests/test_tasks.py::test_list_tasks_empty PASSED
tests/test_tasks.py::test_create_task_missing_title_field PASSED
tests/test_tasks.py::test_title_is_required_empty_string PASSED
tests/test_tasks.py::test_title_whitespace_only PASSED
tests/test_tasks.py::test_get_missing_task PASSED
tests/test_tasks.py::test_get_task_invalid_id_type PASSED
tests/test_tasks.py::test_complete_missing_task PASSED
tests/test_tasks.py::test_complete_task_idempotency PASSED
tests/test_tasks.py::test_create_task_title_with_surrounding_whitespace PASSED
tests/test_tasks.py::test_get_task_negative_id_not_found PASSED

======================== 15 passed ========================
```

Para visualizar a evidência completa da execução, consulte:

```text
test_execution.log
```

---

## 🔄 Fluxo Recomendado de Contribuição

Antes de iniciar uma alteração, atualize sua branch base:

```bash
git switch develop
git pull origin develop
```

Crie uma branch específica:

```bash
git switch -c feature/nome-da-tarefa
```

Exemplo para atualização da documentação:

```bash
git switch -c feature/atualiza-readme
```

Após realizar as alterações, execute:

```bash
pytest -v
```

Verifique os arquivos modificados:

```bash
git status
```

Adicione os arquivos:

```bash
git add .
```

Confira as alterações preparadas para commit:

```bash
git diff --cached
```

Crie o commit:

```bash
git commit -m "docs: atualiza README do projeto"
```

Envie a branch para o GitHub:

```bash
git push -u origin feature/atualiza-readme
```

Depois, abra um Pull Request direcionado para a branch de integração definida pelo projeto.

---

## 📚 Documentação do Projeto

Os principais documentos de referência são:

| Arquivo                           | Finalidade                                                      |
| :-------------------------------- | :-------------------------------------------------------------- |
| `README.md`                       | Documentação principal do projeto                               |
| `docs/especificacao.md`           | Fonte canônica dos requisitos e contratos                       |
| `docs/feedback.md`                | Histórico de refinamentos identificados durante desenvolvimento |
| `docs/adr/ADR-001-arquitetura.md` | Registro das decisões arquiteturais                             |
| `docs/relatorio_entrega_1.md`     | Relatório preparado para a entrega                              |
| `AGENTS.md`                       | Regras para agentes automatizados                               |
| `.cursorrules`                    | Regras adicionais para ferramentas de IA                        |
| `test_execution.log`              | Evidência da execução dos testes                                |

---

## 🎯 Metodologia Spec-Driven Development

O projeto adota **Spec-Driven Development (SDD)** como abordagem central.

Nesse modelo, a implementação deve ser consequência direta da especificação.

O fluxo adotado é:

```text
Especificação
     ↓
Decomposição
     ↓
Test Harness
     ↓
Implementação
     ↓
Validação e Review
```

Essa abordagem busca:

* reduzir ambiguidades;
* aumentar rastreabilidade;
* prevenir regressões.
* facilitar colaboração.
* tornar critérios de aceitação verificáveis;
* estabelecer uma fonte única da verdade para o comportamento do sistema.

---

## ✅ Estado Atual da Entrega

Nesta etapa, o projeto possui:

* API REST funcional desenvolvida com FastAPI;
* criação de tarefas;
* listagem de tarefas;
* consulta individual;
* conclusão de tarefas;
* endpoint de health check;
* validação de entradas;
* sanitização de títulos;
* armazenamento em memória;
* isolamento de estado entre testes;
* Test Harness automatizado;
* 15 cenários de teste;
* execução automatizada em Windows;
* execução automatizada em Linux/macOS;
* suporte a Docker;
* Docker Compose;
* documentação interativa via Swagger;
* governança de branches;
* política de Pull Requests;
* documentação de ADR;
* configuração para agentes de IA;
* evidência de execução dos testes.

---

## 📄 Evidências

Para visualizar os logs detalhados da execução do Test Harness, consulte:

[`test_execution.log`](test_execution.log)

Para consultar o documento formal de submissão:

[`docs/relatorio_entrega_1.md`](docs/relatorio_entrega_1.md)

Para consultar a especificação técnica:

[`docs/especificacao.md`](docs/especificacao.md)

Para consultar o histórico de refinamentos:

[`docs/feedback.md`](docs/feedback.md)

---

## 📝 Observação sobre Persistência

A persistência em memória foi adotada nesta entrega como parte do design mínimo do projeto.

A introdução futura de um banco de dados deverá respeitar o processo de decisão arquitetural adotado pelo repositório e, caso represente uma mudança significativa de arquitetura, deverá ser registrada através de uma nova ADR.

---

## 📌 Resumo

O **Projeto SDD — Gerenciador de Tarefas** demonstra a aplicação prática de Spec-Driven Development em uma API REST, combinando:

* especificação prévia;
* implementação mínima;
* validação automatizada;
* testes de happy path;
* testes de casos de borda;
* governança de código;
* documentação arquitetural;
* execução reproduzível;
* contêineres;
* e apoio de agentes inteligentes no ciclo de desenvolvimento.

O resultado é uma base simples, rastreável e preparada para evolução incremental sem comprometer os requisitos e comportamentos já validados.
