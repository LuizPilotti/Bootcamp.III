# Regras do Agente — Projeto SDD

## Contexto
Este repositório é um projeto acadêmico baseado em Spec-Driven Development.

## Regras
1. Consultar `docs/especificacao.md` antes de alterar comportamento.
2. Não criar requisitos que não estejam especificados sem registrar a decisão.
3. Manter os contratos HTTP documentados.
4. Criar ou atualizar testes para mudanças de comportamento.
5. Não remover testes existentes para fazer uma implementação passar.
6. Manter funções pequenas e com responsabilidade única.
7. Atualizar documentação quando uma decisão arquitetural mudar.
8. Preferir alterações incrementais e fáceis de revisar.

## Fluxo sugerido
Especificação → decomposição → teste → implementação → execução do harness → revisão.
