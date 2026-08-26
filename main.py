from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Gerenciador de Tarefas", version="1.0.0")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""


class Task(TaskCreate):
    id: int
    completed: bool = False


tasks: dict[int, Task] = {}
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
