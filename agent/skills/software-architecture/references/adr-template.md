# ADR — template e convenções

Fonte: padrão MADR simplificado (<https://adr.github.io/madr/>).

## Nome e numeração

- `ADR-NNNN-titulo-curto.md`, sequencial por repo (0001, 0002, …).
- Título curto em kebab-case, no idioma do projeto (aqui PT-BR).

## Campos obrigatórios

```markdown
# ADR-NNNN: Título curto

- **Status:** proposta | aceita | deprecada
- **Data:** YYYY-MM-DD
- **Escopo:** serviço(s)/módulo(s)
- **Spec:** link(s) para spec/docs
```

## Seções

1. **Contexto** — problema, forças em jogo, restrições.
2. **Decisão** — o que foi decidido, como funciona, configuração mínima se houver.
3. **Consequências** — positivas e negativas; mitigação de riscos.
4. **Alternativas consideradas** — cada uma com motivo de rejeição.

## Regras

- Uma ADR = uma decisão arquitetural (não uma lista).
- Registre o **porquê**, não a implementação detalhada.
- Se uma decisão for substituída, marque `deprecada` + `superseded by ADR-YYYY`.
- Nunca apague ADRs antigas: o histórico de decisões é o valor.
- Aponte para a spec/issue que motivou a decisão quando existir.
