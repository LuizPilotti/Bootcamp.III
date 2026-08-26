# ADR-001 — Arquitetura da API

## Status
Aceito

## Contexto
O projeto precisa de uma estrutura pequena, testável e reproduzível para demonstrar o fluxo SDD.

## Decisão
Foi adotada uma API REST em Python com FastAPI, testes em pytest e execução padronizada via Docker.

## Consequências
- API simples de executar.
- Testes automatizados podem ser executados sem banco externo.
- O armazenamento atual é em memória, adequado ao protótipo acadêmico.
- Uma futura versão pode substituir o repositório em memória por um banco persistente sem alterar os contratos HTTP.
