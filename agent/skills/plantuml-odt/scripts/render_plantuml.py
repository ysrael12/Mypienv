#!/usr/bin/env python3
"""Renderiza todos os .puml de um diretório (recursivo) em PNG via plantuml.com.

Uso: render_plantuml.py <dir_puml> [dir_saida_png]
  - dir_puml: diretório contendo os arquivos .puml (varre recursivamente)
  - dir_saida_png: diretório de saída (default: <dir_puml>/images)
"""
import sys, zlib, pathlib, urllib.request, urllib.error, time, struct

# Alfabeto oficial do PlantUML (NÃO é o base64 padrão).
# O base64 padrão gera URL inválida -> imagem de erro "Bad URL" (789px).
B64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

def encode(data: bytes) -> str:
    comp = zlib.compress(data, 9)[2:-4]  # remove header zlib (2) e adler32 (4)
    out = []
    n = len(comp)
    i = 0
    while i < n:
        b1 = comp[i]
        b2 = comp[i+1] if i+1 < n else 0
        b3 = comp[i+2] if i+2 < n else 0
        out.append(B64[b1 >> 2])
        out.append(B64[((b1 & 0x3) << 4) | (b2 >> 4)])
        out.append(B64[((b2 & 0xF) << 2) | (b3 >> 6)])
        out.append(B64[b3 & 0x3F])
        i += 3
    return "".join(out)

def render(puml: pathlib.Path, png: pathlib.Path) -> bool:
    url = "https://www.plantuml.com/plantuml/png/" + encode(puml.read_bytes())
    for attempt in range(4):
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8.0"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data, status = r.read(), r.status
        except urllib.error.HTTPError as e:
            data, status = e.read(), e.code
        except Exception as e:
            print(f"FAIL {puml.name}: {e}")
            return False
        if status == 200 and data[:4] == b"\x89PNG":
            w, h = struct.unpack(">II", data[16:24])
            if w == 789:  # imagem de erro "Bad URL"
                print(f"  retry {puml.name}: imagem de erro (789px)")
                time.sleep(3 * (attempt + 1))
                continue
            png.parent.mkdir(parents=True, exist_ok=True)
            png.write_bytes(data)
            return True
        if status in (403, 429):
            time.sleep(4 * (attempt + 1))
            continue
        print(f"FAIL {puml.name}: status {status} ({data[:80]!r})")
        return False
    print(f"FAIL {puml.name}: excedeu retries")
    return False

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = pathlib.Path(sys.argv[1]).resolve()
    out = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else src / "images"
    files = sorted(src.rglob("*.puml"))
    if not files:
        print(f"nenhum .puml em {src}")
        sys.exit(1)
    ok = fail = 0
    for f in files:
        rel = f.relative_to(src)
        png = out / rel.with_suffix(".png")
        if render(f, png):
            print(f"OK   {rel}")
            ok += 1
        else:
            fail += 1
        time.sleep(1.0)  # evita rate limit
    print(f"\n{ok} ok, {fail} fail")

if __name__ == "__main__":
    main()
