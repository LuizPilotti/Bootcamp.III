# Especificação Técnica — Gerenciador de Tarefas (SDD)

## 1. Contexto e Problema
Equipes de desenvolvimento necessitam de ferramentas simples, rastreáveis e padronizadas para registro e acompanhamento de tarefas[cite: 3]. O objetivo desta API é implementar a gestão do ciclo de vida dessas tarefas seguindo a abordagem Spec-Driven Development (SDD)[cite: 6, 8], assegurando contratos rígidos de entrada/saída e validação por testes automatizados antes da implementação[cite: 3, 6, 8].

## 2. Requisitos Funcionais

- **RF01 — Criar Tarefa:** Permitir criação de tarefa informando `title` (obrigatório, não vazio) e `description` (opcional)[cite: 3]. A tarefa inicia com status `completed = false`[cite: 3].
- **RF02 — Listar Tarefas:** Retornar todas as tarefas ativas cadastradas no repositório[cite: 3].
- **RF03 — Consultar Tarefa por ID:** Retornar a entidade completa com base no identificador inteiro único (`task_id`)[cite: 3].
- **RF04 — Concluir Tarefa:** Atualizar o campo `completed` de uma tarefa existente para `true` de forma idempotente[cite: 3, 4].
- **RF05 — Endpoint de Saúde:** Retornar integridade e disponibilidade operacional do serviço no caminho `/health`[cite: 3, 4].
- **RF06 — Validação de Entradas:** Rejeitar requisições sem título, com string vazia ou contendo apenas espaços em branco, além de identificadores de rota que não sejam números inteiros[cite: 3, 4].

## 3. Requisitos Não Funcionais

- **RNF01 — Comunicação:** Toda comunicação trafega via JSON sobre o protocolo HTTP REST[cite: 3].
- **RNF02 — Reprodutibilidade de Ambiente:** O ambiente de execução e teste é padronizado via scripts automatizados (`run_tests.bat` e `run_tests.sh`) isolados em `.venv`, sem obrigatoriedade de virtualização pesada[cite: 4, 8].
- **RNF03 — Test Harness:** Suíte de testes automatizados com `pytest` cobrindo cenários felizes e casos de borda (edge cases)[cite: 3, 8, 13].
- **RNF04 — Arquitetura Modular:** Componentes desacoplados com persistência em memória e rotina utilitária de reset de estado para isolamento dos testes[cite: 8].

## 4. Modelo de Dados

### Entidade `Task`
- `id`: Inteiro, sequencial e primário[cite: 3].
- `title`: String, obrigatório (mínimo de 1 caractere real)[cite: 3, 4].
- `description`: String, opcional (padrão `""`)[cite: 3].
- `completed`: Booleano, status de finalização (padrão `false`)[cite: 3].

## 5. Contratos de Entrada/Saída

### POST /tasks
- **Finalidade:** Cadastrar uma nova tarefa no sistema[cite: 3].
- **Status HTTP de Sucesso:** `201 Created`[cite: 3]
- **Request Body (JSON):**
  - `title`: "Estudar SDD"
  - `description`: "Fazer os testes"
- **Response Body (JSON):**
  - `id`: 1
  - `title`: "Estudar SDD"
  - `description`: "Fazer os testes"
  - `completed`: false
- **Erros Mapeados:**
  - `422 Unprocessable Entity`: Quando o campo `title` for omitido, enviado como string vazia `""` ou contendo apenas espaços em branco `"   "`[cite: 3, 4].

### GET /tasks
- **Finalidade:** Listar todas as tarefas cadastradas[cite: 3].
- **Status HTTP de Sucesso:** `200 OK`[cite: 3]
- **Response Body (JSON):**
  - Lista contendo objetos de tarefas com os campos `id`, `title`, `description` e `completed`[cite: 3].
  - Retorna lista vazia `[]` caso não existam tarefas registradas.

### GET /tasks/{task_id}
- **Finalidade:** Consultar uma tarefa existente por ID[cite: 3].
- **Status HTTP de Sucesso:** `200 OK`[cite: 3]
- **Response Body (JSON):**
  - Objeto da tarefa correspondente ao ID informado (`id`, `title`, `description`, `completed`)[cite: 3].
- **Erros Mapeados:**
  - `404 Not Found`: Quando o identificador numérico não existir no repositório[cite: 3].
  - `422 Unprocessable Entity`: Quando o parâmetro `task_id` for alfanumérico ou não conversível para inteiro.

### PATCH /tasks/{task_id}/complete
- **Finalidade:** Marcar o estado da tarefa como concluída[cite: 3].
- **Status HTTP de Sucesso:** `200 OK`
- **Response Body (JSON):**
  - Objeto da tarefa com `completed: true`.
- **Erros Mapeados:**
  - `404 Not Found`: Quando o identificador não for encontrado no sistema[cite: 3].

### GET /health
- **Finalidade:** Verificação rápida de integridade da API[cite: 3, 4].
- **Status HTTP de Sucesso:** `200 OK`
- **Response Body (JSON):**
  - `status`: "ok"

## 6. Regras de Negócio
1. **Obrigatoriedade de Conteúdo Real:** Toda tarefa deve conter título válido, sendo proibidos títulos preenchidos apenas com caracteres de espaçamento[cite: 3, 4].
2. **Estado Inicial:** Novas tarefas iniciam invariavelmente com `completed = false`[cite: 3].
3. **Idempotência de Conclusão:** Concluir uma tarefa já marcada como `completed = true` é uma operação idempotente que mantém o registro concluído e responde HTTP 200[cite: 4].
4. **Isolamento e Persistência:** Os dados são mantidos em memória durante o ciclo de execução da aplicação, suportando redefinição via rotina interna para testes unitários[cite: 8].

## 7. Critérios de Aceitação
- Criar tarefa com payload válido retorna HTTP 201 e dados persistidos[cite: 3].
- Tentar criar tarefa sem título ou com espaços vazios retorna HTTP 422[cite: 3, 4].
- Listar tarefas retorna array com status HTTP 200 (incluindo repositório vazio)[cite: 3].
- Consultar ID inexistente retorna HTTP 404 acompanhado de mensagem explicativa[cite: 3].
- Concluir tarefa existente altera o booleano `completed` para `true` com status HTTP 200[cite: 3].
- Requisições para rotas com IDs em formato incorreto retornam HTTP 422.
- O endpoint `/health` responde `{"status": "ok"}` com status HTTP 200[cite: 3].