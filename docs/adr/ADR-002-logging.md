# ADR-002 — Sistema de Logging Local

## Status
Aceito

## Contexto
Durante o desenvolvimento iterativo, a equipe identificou a necessidade de rastreabilidade das requisições HTTP e eventos da aplicação para fins de depuração e auditoria local. Sem um mecanismo de log, erros e comportamentos inesperados são difíceis de diagnosticar, especialmente em testes manuais e demonstrações.

## Decisão
- Implementar um módulo de logging isolado (`src/logger.py`) utilizando **exclusivamente o módulo `logging` nativo do Python**, sem adicionar dependências externas ao `requirements.txt`.
- Os arquivos de log são gerados automaticamente na pasta `logs/` na raiz do projeto, com nomenclatura diária: `app_YYYY-MM-DD.log`.
- O formato padronizado é: `[TIMESTAMP] [LEVEL] [LOGGER] MENSAGEM`.
- Um middleware HTTP registra automaticamente cada requisição recebida (método, path, status code e tempo de resposta).
- A pasta `logs/` é adicionada ao `.gitignore` para não versionar arquivos de log gerados localmente.

## Consequências
- **Zero dependências adicionais:** O módulo `logging` já faz parte da biblioteca padrão do Python.
- **Baixo acoplamento:** O logger é um módulo independente, importado pontualmente — não altera schemas, repositório nem contratos de API.
- **Rastreabilidade local:** Facilita a depuração durante o desenvolvimento sem necessidade de ferramentas externas.
- **Sem impacto nos testes existentes:** Os testes do logger utilizam diretórios temporários (`tmp_path`) e não interferem no Test Harness principal.
