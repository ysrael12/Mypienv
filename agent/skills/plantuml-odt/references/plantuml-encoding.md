# Encoding da URL do PlantUML server

O servidor público `https://www.plantuml.com/plantuml/png/<enc>` usa um encoding
próprio, **diferente do base64 padrão**.

## Algoritmo

1. Comprimir o texto com **deflate (zlib), level 9**.
2. Remover os **2 primeiros bytes** (header zlib) e os **4 últimos** (adler32).
3. Re-encodar os bytes em grupos de 6 bits (3 bytes → 4 chars), usando o alfabeto:

```
0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_
```

## O bug do "Bad URL"

Se usar o **base64 padrão** (`A-Za-z0-9+/`) no lugar do alfabeto acima, a URL é
inválida e o servidor responde **HTTP 400** com uma **imagem PNG de erro
"Bad URL"** (largura fixa ~789px).

Como essa imagem é um PNG válido, um checagem ingênua de `magic number` (`\x89PNG`)
passa e aceita a imagem de erro. **Sempre validar a largura** (`w != 789`) ou o
conteúdo do chunk `iTXt` (contém o source do diagrama).

## Headers / rate limit

- Sem `User-Agent`, o plantuml.com responde **403 Forbidden**.
- Rate limit: usar `User-Agent: curl/8.0` e retry com backoff em 403/429, com
  pequeno delay (~1s) entre requisições.

## Referência

- Algoritmo oficial: classe `ZopfliDeflater` / `encodeDiagramm` no repositório
  `plantuml/plantuml-server` (método `encodeDiagramm` em `PlantUmlServlet`).
- O endpoint `/plantuml/svg/<enc>` e `/plantuml/txt/<enc>` usam o mesmo encoding.
