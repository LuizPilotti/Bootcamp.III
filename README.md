# Projeto SDD — Gerenciador de Tarefas

Projeto acadêmico estruturado para desenvolvimento orientado por especificação (**Spec-Driven Development — SDD**).

## Objetivo
Disponibilizar uma API REST para criação, consulta, atualização e conclusão de tarefas, com validação de contratos e suíte de testes automatizada.

## Estrutura do Repositório
- `docs/especificacao.md` — Especificação técnica do problema (requisitos, contratos e modelos).
- `docs/feedback.md` — Histórico de refinamentos por feedback do projeto.
- `docs/adr/ADR-001-arquitetura.md` — Registro de decisões arquiteturais técnicas.
- `.cursor/rules/project-rules.md` — Regras e diretrizes de contexto para agentes de IA.
- `run_tests.bat` e `run_tests.sh` — Scripts de padronização e reprodução do ambiente.
- `Dockerfile` e `docker-compose.yml` — Empacotamento alternativo em contêineres.
- `src/` — Código-fonte da aplicação FastAPI.
- `tests/` — Test Harness automatizado (pytest).
- `.github/workflows/tests.yml` — Pipeline de integração contínua (CI).
- `.github/pull_request_template.md` — Padrão institucional de Pull Request.

---

## Padronização de Ambiente e Execução dos Testes

O ambiente foi padronizado através de scripts automatizados que isolam as dependências em `.venv`, garantindo a reprodutibilidade da execução.

### No Windows (sem Docker):
Dê um duplo clique ou execute no terminal:
```cmd
run_tests.bat