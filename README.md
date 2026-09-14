# Mypienv

This repository brings together configurations, extensions, and skills for AI agents in software development environments. The structure is organized as a reusable knowledge base for prompts, rules, and productivity-oriented tooling.

## Overview

The workspace contains a main directory called `agent/`, which centralizes:

- `AGENTS.md`: guidance and instructions for agents
- `mcp.json`: configuration for MCP servers (Model Context Protocol)
- `settings.json`: environment and agent configuration
- `extensions/`: helper extensions and utilities
- `skills/`: specialized knowledge packs and best-practice rules by domain

The goal is to give different agents and tools access to consistent standards, guidance, and structured domain knowledge.

## Repository structure

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

## What is included in `agent/skills`

The `skills` folder contains several sets of rules and documentation covering areas such as:

- backend and APIs with `axum`
- design and branding
- software architecture and patterns
- TypeScript, React, and Next.js
- Python development
- Rust
- UI/UX, shadcn, and styling
- presentation and visual content design

These packages act as specialized knowledge that agents can use to:

- review code
- suggest structural improvements
- apply best practices in context
- support the creation of consistent, high-quality solutions

## How to use it

1. Open this workspace in an environment that supports AI agents.
2. Configure the agent to read the files in `agent/`.
3. Use `AGENTS.md`, `mcp.json`, and `settings.json` as the base context.
4. Consult the `skills/` directory based on the area in which the agent should operate.

## Example use cases

An agent can be instructed to:

- review code using React best practices
- validate Rust implementations with `rust-skills`
- guide front-end development using `shadcn` and `ui-styling`
- apply UI/UX standards in interface projects

## Notes

This repository is not a standalone application; it is primarily a knowledge and configuration repository for AI agents. It is most useful when connected to a development environment and the project context where it will be used.

## Contributing

To expand the repository, you can:

- add new skills in `agent/skills/`
- update `AGENTS.md` to reflect global rules
- adjust `settings.json` and `mcp.json` as needed for the environment
- include useful extensions in `agent/extensions/`

## License

Check the specific files or subprojects for licensing details, where applicable.
