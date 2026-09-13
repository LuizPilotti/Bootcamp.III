import time

from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel, Field, field_validator

from src.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Gerenciador de Tarefas", version="1.0.0")

logger.info("Aplicação Gerenciador de Tarefas inicializada.")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware que registra cada requisição HTTP recebida."""
    start = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start) * 1000
    logger.info(
        "%s %s → %s (%.1fms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""

    @field_validator("title")
    @classmethod
    def validate_not_whitespace(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("O título não pode ser vazio ou conter apenas espaços.")
        return trimmed


class Task(TaskCreate):
    id: int
    completed: bool = False


tasks: dict[int, Task] = {}
next_id = 1


def reset_database():
    """Restaura o estado do banco em memória para o harness de testes."""
    global next_id
    tasks.clear()
    next_id = 1


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    global next_id
    task = Task(id=next_id, title=payload.title, description=payload.description)
    tasks[next_id] = task
    next_id += 1
    return task


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return list(tasks.values())


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return task


@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    task.completed = True
    return task