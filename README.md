# Mypienv

Este repositório reúne configurações, extensões e skills para uso com agentes de IA em ambientes de desenvolvimento. A estrutura foi organizada para servir como base de prompts, regras e ferramentas reutilizáveis para agentes e integrações de produtividade.

## Visão geral

O workspace contém um diretório principal chamado `agent/`, que centraliza:

- `AGENTS.md`: guia e instruções para agentes
- `mcp.json`: configuração de servidores MCP (Model Context Protocol)
- `settings.json`: ajustes do ambiente/agent
- `extensions/`: extensões e utilitários auxiliares
- `skills/`: pacotes de conhecimento e regras especializadas por área

A ideia é permitir que diferentes agentes e ferramentas tenham acesso a padrões, diretrizes e conhecimentos bem estruturados.

## Estrutura do repositório

```text
Mypienv/
├── README.md
├── .gitignore
├── agent/
│   ├── AGENTS.md
│   ├── mcp.json
│   ├── settings.json
│   ├── extensions/
│   │   └── cbmem.ts
│   └── skills/
│       ├── axum/
│       ├── banner-design/
│       ├── brand/
│       ├── codebase-memory/
│       ├── design/
│       ├── design-pattern-review/
│       ├── design-system/
│       ├── mastering-typescript/
│       ├── next-cache-components-adoption/
│       ├── next-cache-components-optimizer/
│       ├── next-dev-loop/
│       ├── next-partial-prefetching-adoption/
│       ├── next-partial-prefetching-optimizer/
│       ├── python/
│       ├── react-best-practices/
│       ├── rust-skills/
│       ├── shadcn/
│       ├── slides/
│       ├── ui-styling/
│       └── ui-ux-pro-max/
```

## O que está presente em `agent/skills`

A pasta `skills` contém diversos conjuntos de regras e documentação para áreas como:

- backend e APIs com `axum`
- design e branding
- arquitetura de software e padrões
- TypeScript, React e Next.js
- desenvolvimento Python
- Rust
- UI/UX, shadcn e styling
- apresentações e materiais visuais

Esses pacotes funcionam como conhecimento especializado que pode ser usado por agentes para:

- revisar código
- sugerir melhorias estruturais
- aplicar boas práticas por contexto
- facilitar a criação de soluções consistentes e alinhadas ao padrão do projeto

## Como usar

1. Abra este workspace em um ambiente com suporte a agentes de IA.
2. Configure o agente para ler os arquivos em `agent/`.
3. Use os arquivos `AGENTS.md`, `mcp.json` e `settings.json` como base de contexto.
4. Consulte o diretório `skills/` conforme a área em que o agente deve operar.

## Exemplo de uso

Um agente pode ser instruído a:

- revisar código com regras de React
- validar implementações em Rust com `rust-skills`
- orientar desenvolvimento front-end com `shadcn` e `ui-styling`
- usar padrões de design e UX em projetos de interface

## Observações

Este repositório não é uma aplicação de execução direta, e sim um repositório de conhecimento e configuração para agentes de IA. Ele é mais útil quando conectado a ferramentas de desenvolvimento e ao contexto do projeto em que será utilizado.

## Contribuição

Para ampliar o repositório, você pode:

- adicionar novas skills em `agent/skills/`
- ajustar `AGENTS.md` para refletir regras globais
- atualizar `settings.json` e `mcp.json` conforme o ambiente
- incluir extensões úteis em `agent/extensions/`

## Licença

Consulte os arquivos específicos de cada skill ou projeto para verificar as licenças aplicáveis, caso existam dentro de subdiretórios individuais.
