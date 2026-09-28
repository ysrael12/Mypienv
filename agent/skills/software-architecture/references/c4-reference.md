# C4 model — referência rápida

Fonte: <https://c4model.com> e stdlib <https://github.com/plantuml-stdlib/C4-PlantUML>.

## Elementos

| Nível | Função | Elemento PlantUML |
|---|---|---|
| 1 | Sistema no ambiente | `Person`, `System`, `System_Ext` |
| 2 | Containers | `Container`, `ContainerDb`, `System_Ext` |
| 3 | Componentes | `Component`, `Container_Boundary`, `ContainerDb` |
| 4 | Código | `Component` (classes/funções) |

## Relacionamentos

```plantuml
Rel(from, to, "descrição", "protocolo/tecnologia")
```

- Direção importa: quem inicia a interação.
- Sempre anotar protocolo quando relevante (HTTPS, SQL, gRPC, SMTP).

## Estilo

- `LAYOUT_WITH_LEGEND()` — legenda de cores por tipo.
- `title` curto com o nome do sistema + nível.
- `note right of X` para invariantes/regras (ex.: "não é checkpointer").
- Boundaries agrupam containers de um mesmo sistema/serviço.
- Externos com `_Ext`; bancos com `Db`.

## Tipos de diagrama

- **Componente** — módulos internos de um serviço.
- **Dinâmico** (sequence) — um fluxo de negócio atravessando componentes, com `alt`/`else` para ramificações.
- **Deployment** — nós e containers físicos (opcional, por spec).
