# Especificação Técnica — Gerenciador de Tarefas

## 1. Problema

Usuários precisam registrar tarefas, consultar as tarefas cadastradas e marcar uma tarefa como concluída de forma simples e padronizada.

## 2. Requisitos funcionais

### RF01 — Criar tarefa
O sistema deve permitir criar uma tarefa informando título e descrição.

### RF02 — Listar tarefas
O sistema deve retornar todas as tarefas cadastradas.

### RF03 — Consultar tarefa
O sistema deve permitir consultar uma tarefa pelo identificador.

### RF04 — Concluir tarefa
O sistema deve permitir alterar o estado de uma tarefa para concluída.

### RF05 — Validar entrada
O título deve ser obrigatório e não pode ser vazio.

## 3. Requisitos não funcionais

- A API deve responder usando JSON.
- O projeto deve possuir testes automatizados.
- O ambiente deve ser reproduzível por Docker.
- A aplicação deve disponibilizar um endpoint de saúde.
- O código deve ser organizado em unidades pequenas e testáveis.

## 4. Modelo de dados

Uma tarefa possui:
- `id`: identificador inteiro.
- `title`: título.
- `description`: descrição.
- `completed`: indicador booleano de conclusão.

## 5. Contratos de entrada/saída

### POST /tasks

Entrada:

```json
{
  "title": "Estudar SDD",
  "description": "Revisar a especificação do projeto"
}
```

Saída esperada:

```json
{
  "id": 1,
  "title": "Estudar SDD",
  "description": "Revisar a especificação do projeto",
  "completed": false
}
```

### GET /tasks

Retorna uma lista de tarefas.

### GET /tasks/{task_id}

Retorna uma tarefa ou HTTP 404 caso ela não exista.

### PATCH /tasks/{task_id}/complete

Marca a tarefa como concluída.

## 6. Regras de negócio

1. Toda tarefa deve possuir título.
2. Uma tarefa nova começa com `completed = false`.
3. Somente tarefas existentes podem ser concluídas.
4. Um identificador inexistente deve produzir HTTP 404.

## 7. Critérios de aceitação

- Criar tarefa válida retorna HTTP 201.
- Criar tarefa sem título retorna erro de validação.
- Listar tarefas retorna HTTP 200.
- Consultar tarefa inexistente retorna HTTP 404.
- Concluir tarefa existente altera `completed` para `true`.
- `/health` retorna status operacional.
