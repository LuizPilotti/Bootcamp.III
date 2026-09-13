from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator

# Inicializa a aplicação FastAPI com as informações básicas da API.
app = FastAPI(title="Gerenciador de Tarefas", version="1.0.0")


# Modelo utilizado para validar os dados recebidos na criação de uma tarefa.
class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""

    # Valida o título para impedir valores vazios ou compostos apenas por espaços.
    @field_validator("title")
    @classmethod
    def validate_not_whitespace(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("O título não pode ser vazio ou conter apenas espaços.")
        return trimmed


# Modelo completo da tarefa, incluindo identificador e status de conclusão.
class Task(TaskCreate):
    id: int
    completed: bool = False


# Armazena temporariamente as tarefas em memória durante a execução da aplicação.
tasks: dict[int, Task] = {}

# Mantém o próximo identificador disponível para uma nova tarefa.
next_id = 1


# Restaura os dados em memória para o estado inicial utilizado pelos testes.
def reset_database():
    """Restaura o estado do banco em memória para o harness de testes."""
    global next_id
    tasks.clear()
    next_id = 1


# Endpoint utilizado para verificar se a API está disponível.
@app.get("/health")
def health():
    return {"status": "ok"}


# Cria uma nova tarefa e gera seu identificador automaticamente.
@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    global next_id

    # Monta a tarefa com os dados recebidos e o próximo ID disponível.
    task = Task(id=next_id, title=payload.title, description=payload.description)

    # Salva a tarefa no armazenamento em memória.
    tasks[next_id] = task
    next_id += 1

    return task


# Retorna todas as tarefas atualmente cadastradas.
@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return list(tasks.values())


# Busca uma tarefa específica através do seu identificador.
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = tasks.get(task_id)

    # Retorna erro 404 caso o identificador informado não exista.
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return task


# Marca uma tarefa existente como concluída.
@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    task = tasks.get(task_id)

    # Garante que apenas tarefas existentes possam ser atualizadas.
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    task.completed = True
    return task