---
name: plantuml-odt
description: Renders PlantUML (.puml) diagrams to PNG and builds an ODT document with embedded images and explanatory text. Use when converting C4/architecture diagrams into images, or generating an .odt (LibreOffice/Word-compatible) document from diagrams plus prose.
---

# PlantUML → PNG + ODT

Renderiza diagramas `.puml` em PNG e monta um documento ODT com as imagens
embutidas e texto explicativo.

## Processo (2 passos)

1. **Renderizar** — converte todos os `.puml` (recursivo) em PNG.
2. **Montar ODT** — empacota as imagens + texto num `.odt`.

```bash
# 1. renderizar diagramas de um diretório
python3 scripts/render_plantuml.py <dir_puml> <dir_saida_png>

# 2. gerar o documento a partir de um JSON de conteúdo
python3 scripts/build_odt.py <conteudo.json> <saida.odt>
```

## Renderizar PlantUML → PNG

O script usa o servidor público **plantuml.com** (não requer Java/Docker local).
Regras críticas (já incorporadas ao script):

- **Alfabeto de encoding é o oficial do PlantUML** (`0-9A-Za-z-_`), NÃO o base64
  padrão. O base64 padrão gera URL inválida e o servidor responde com uma imagem
  PNG de erro "Bad URL".
- **Rejeitar a imagem de erro**: ela tem largura fixa `789px`. O script valida o
  tamanho e faz retry se receber 789px.
- Usar `User-Agent` (ex.: `curl/8.0`) — sem ele o plantuml.com responde 403.
- Respeitar rate limit: retry com backoff em 403/429.

## Gerar o ODT

O ODT é um ZIP com `mimetype`, `content.xml`, `styles.xml`, `meta.xml`,
`META-INF/manifest.xml` e as imagens em `Pictures/`.

Regras críticas:

- `mimetype` deve ser o **primeiro** arquivo do ZIP, **sem compressão** (STORED).
- Nomes de imagem **achatados** em `Pictures/` (subdiretórios quebram em alguns
  leitores). O script troca `/` por `_`.
- Cada `<draw:image>` referencia `Pictures/<nome>` e precisa de entrada
  correspondente no `manifest.xml` e no ZIP.
- Limitar largura (16cm) **e** altura (21cm) para caber em A4; imagens retrato
  são escaladas pela altura.
- XML ODF 1.2 bem-formado; estilos mínimos (Title, Subtitle, Heading 1-3, body,
  caption, list).

## Formato do JSON de conteúdo

```json
{
  "title": "Título do documento",
  "subtitle": "Subtítulo/descrição",
  "blocks": [
    {"type": "h1", "text": "1. Seção"},
    {"type": "p",  "text": "Parágrafo."},
    {"type": "bullets", "items": ["item 1", "item 2"]},
    {"type": "img", "file": "c4-context.png", "caption": "Figura 1 — Contexto."}
  ]
}
```

`file` é relativo ao diretório de imagens passado ao script.

## Pitfalls comuns (quando o PNG sai errado)

| Sintoma | Causa | Correção |
|---|---|---|
| "Bad URL" / imagem de erro 789px | alfabeto base64 errado | usar `0-9A-Za-z-_` |
| 400 "Internal Server Error" no Kroki | `!include` remoto, `→`/`—`, descrições longas + `Rel` | usar `!include <C4/...>` stdlib local e evitar `→`/`—` |
| 403 no plantuml.com | sem User-Agent / rate limit | header `curl/8.0` + backoff |
| imagem não aparece no ODT | subdiretório em `Pictures/` | achar nomes (`/` → `_`) |

Detalhes técnicos em [references/plantuml-encoding.md](references/plantuml-encoding.md).
