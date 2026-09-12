# Diretrizes de Orquestração para Agentes de IA (AGENTS.md)

Este documento define o protocolo operacional para ferramentas e agentes de geração/auxílio de código (Antigravity, Cursor, Claude Code, Codex CLI) atuando neste repositório.

## 🎯 Paradigma Operacional: Spec-Driven Development (SDD)

O fluxo de trabalho de qualquer agente neste projeto segue rigorosamente o ciclo iterativo de 5 etapas:

```
[1. Especificação] ➔ [2. Decomposição] ➔ [3. Test Harness] ➔ [4. Implementação] ➔ [5. Validação & Review]
```

### Regras Mandatórias para Agentes

1. **Fonte Única da Verdade:** O arquivo `docs/especificacao.md` é a referência canônica. O agente não deve inferir regras não documentadas. Se um caso de borda for identificado, ele deve ser documentado em `docs/feedback.md` antes ou durante a implementação.
2. **Governança de Branches:**
   - O agente **NUNCA** deve realizar commits diretos na branch `main`.
   - As alterações devem ocorrer em branches no formato `feature/<nome-da-tarefa>` ou `develop`.
3. **Não-Regressão:** O agente não pode remover nem alterar testes existentes para forçar uma implementação a passar.
4. **Preservação do Design Mínimo:** Não adicione dependências pesadas ou frameworks desnecessários sem que haja uma ADR justificando a decisão em `docs/adr/`.
5. **Verificação Automatizada:** Antes de dar como concluída uma tarefa, execute o comando de teste (`pytest -v` ou `run_tests.bat`/`run_tests.sh`) e verifique a taxa de sucesso de 100%.

## 🛠️ Comandos de Execução Rápida para o Agente

| Ação | Comando |
| :--- | :--- |
| **Executar Test Harness** | `pytest -v` |
| **Executar com Cobertura** | `pytest --verbose` |
| **Iniciar API Localmente** | `uvicorn src.main:app --reload --port 8000` |
| **Validar Health Check** | `curl -f http://localhost:8000/health` |
| **Executar via Docker** | `docker compose up --build` |
