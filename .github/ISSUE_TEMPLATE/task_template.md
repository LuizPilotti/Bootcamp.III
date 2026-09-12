---
name: Tarefa do Projeto (Sprint)
about: Decomposição de tarefas da sprint no fluxo SDD
title: "[TASK] "
labels: ["sdd", "enhancement"]
assignees: ""
---

## 🎯 Objetivo da Tarefa
Descreva de forma clara e objetiva o que precisa ser realizado nesta tarefa.

## 📋 Requisito(s) Associado(s)
- [ ] RF01 — Criar Tarefa
- [ ] RF02 — Listar Tarefas
- [ ] RF03 — Consultar Tarefa por ID
- [ ] RF04 — Concluir Tarefa
- [ ] RF05 — Endpoint de Saúde
- [ ] RF06 — Validação de Entradas
- [ ] RNF (Descrever qual)

## 🧩 Unidade / Componente Envolvido
- [ ] Contratos e Schemas Pydantic (`TaskCreate`, `Task`)
- [ ] Lógica de Validação e Regras de Negócio
- [ ] Armazenamento / Repositório em memória
- [ ] Controladores HTTP / Endpoints FastAPI
- [ ] Test Harness (`tests/test_tasks.py`)
- [ ] Documentação / ADRs / Governança

## 🛠️ Critérios de Aceitação
- [ ] Teste automatizado correspondente implementado no Harness.
- [ ] Execução com 100% de sucesso sem regressão.
- [ ] Código em conformidade com as diretrizes do `AGENTS.md` e `.cursorrules`.
