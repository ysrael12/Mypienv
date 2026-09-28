---
name: software-architecture
description: Modelagem de arquitetura de software em C4 (Contexto, Container, Componente, Código) com diagramas PlantUML e decisões registradas em ADRs (Architecture Decision Records). Use when modeling system architecture, creating C4 diagrams, writing ADRs, documenting containers/components of a system, or doing architecture/system design reviews.
---

# Software Architecture (C4 + ADRs)

Modela a arquitetura de um sistema em níveis C4 e registra decisões em ADRs.

## Níveis C4

1. **Contexto** — o sistema no ambiente, atores e sistemas externos.
2. **Container** — serviços/containers e bancos de dados.
3. **Componente** — módulos internos de cada serviço.
4. **Código** — classes/funções (gerar sob demanda).

Use o stdlib C4-PlantUML. Convenções:

- Prefixo de arquivo indica o nível: `c4-context.puml`, `c4-container.puml`, `component.puml`, `dynamic-*.puml` (fluxo de uma funcionalidade).
- Incluir `LAYOUT_WITH_LEGEND()` e `title`.
- Um diagrama de componente por módulo, num diretório `modules/<modulo>/`.
- Diagramas dinâmicos (sequence) para fluxos de negócio importantes.
- `System_Ext`/`ContainerDb` para externos/banco; `Rel` com direção e protocolo.

## Template PlantUML (componente)

```plantuml
@startuml nome-component
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

LAYOUT_WITH_LEGEND()
title <servico> — Components

Container_Boundary(svc, "<servico>") {
  Component(a, "modulo/a", "Tecnologia", "responsabilidade")
  Component(b, "modulo/b", "Tecnologia", "responsabilidade")
}
ContainerDb(db, "<db>", "PostgreSQL", "o que guarda")
System_Ext(ext, "<externo>", "o que faz")

Rel(a, b, "chama", "")
Rel(a, db, "SQL", "")
Rel(svc, ext, "HTTPS", "")
@enduml
```

## Template ADR

Um arquivo Markdown por decisão, em `adr/ADR-NNNN-titulo-curto.md`:

```markdown
# ADR-NNNN: Título curto

- **Status:** proposta | aceita | deprecada | superseded by ADR-YYYY
- **Data:** YYYY-MM-DD
- **Escopo:** serviço(s)/módulo(s)
- **Spec:** link(s) para spec/docs

## Contexto
Problema e forças em jogo.

## Decisão
O que foi decidido e como funciona.

## Consequências
Positivas e negativas (custo, risco, mitigação).

## Alternativas consideradas
- Alternativa X (rejeitado: motivo)
```

## Estrutura de saída

```
docs/<versao>/architecture/
  README.md                # índice + convenções
  c4-context.puml
  c4-container.puml
  modules/<modulo>/
    component.puml
    dynamic-<fluxo>.puml
  adr/
    ADR-NNNN-<titulo>.md
```

## Regras

- Baseie os diagramas no **código real** (diretórios, rotas, serviços), não só na spec.
- Quando houver spec v2/versão nova, modele o **alvo** (target state), marcando o legado.
- ADR descreve a decisão e o porquê, não a implementação detalhada.
- Consulte o guia completo: [C4 model](references/c4-reference.md) e [ADR template](references/adr-template.md).
