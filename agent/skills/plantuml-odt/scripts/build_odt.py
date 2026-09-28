#!/usr/bin/env python3
"""Monta um documento ODT a partir de um JSON de conteúdo + imagens PNG.

Uso: build_odt.py <conteudo.json> <saida.odt> [dir_imagens]
  - conteudo.json: estrutura do documento (ver SKILL.md)
  - saida.odt: caminho do arquivo a gerar
  - dir_imagens: diretório base dos arquivos "file" (default: dir do JSON)
"""
import sys, json, pathlib, struct, zipfile

NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
    "fo": "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
    "xlink": "http://www.w3.org/1999/xlink",
    "dc": "http://purl.org/dc/elements/1.1/",
    "meta": "urn:oasis:names:tc:opendocument:xmlns:meta:1.0",
    "svg": "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
}

MAX_W_CM = 16.0
MAX_H_CM = 21.0

def png_size(path: pathlib.Path):
    w, h = struct.unpack(">II", path.read_bytes()[16:24])
    return w, h

def esc(t: str) -> str:
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def h1(t): return f'<text:h text:style-name="Heading_20_1" text:outline-level="1">{esc(t)}</text:h>'
def h2(t): return f'<text:h text:style-name="Heading_20_2" text:outline-level="2">{esc(t)}</text:h>'
def h3(t): return f'<text:h text:style-name="Heading_20_3" text:outline-level="3">{esc(t)}</text:h>'
def p(t): return f'<text:p text:style-name="Text_20_body">{esc(t)}</text:p>'
def bullets(items):
    out = ['<text:list text:style-name="L1">']
    for it in items:
        out.append(f'<text:list-item><text:p text:style-name="P_20_1">{esc(it)}</text:p></text:list-item>')
    out.append('</text:list>')
    return "".join(out)

def img_block(rel, caption, img_dir, idx):
    f = (img_dir / rel)
    w, h = png_size(f)
    flat = rel.replace("/", "_")
    w_cm, h_cm = MAX_W_CM, MAX_W_CM * h / w
    if h_cm > MAX_H_CM:
        h_cm, w_cm = MAX_H_CM, MAX_H_CM * w / h
    return (flat, f,
        f'<text:p text:style-name="P_20_Caption" style:keep-together="always">'
        f'<draw:frame draw:style-name="fr1" draw:name="img_{idx}" text:anchor-type="as-char" '
        f'svg:width="{w_cm:.2f}cm" svg:height="{h_cm:.2f}cm">'
        f'<draw:image xlink:href="Pictures/{flat}" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>'
        f'</draw:frame></text:p>'
        f'<text:p text:style-name="P_20_Caption"><text:span text:style-name="T3">{esc(caption)}</text:span></text:p>')

def build_body(blocks, img_dir):
    body, pics = [], {}  # flat_name -> source path
    idx = 0
    for b in blocks:
        t = b.get("type")
        if t == "h1": body.append(h1(b["text"]))
        elif t == "h2": body.append(h2(b["text"]))
        elif t == "h3": body.append(h3(b["text"]))
        elif t == "p": body.append(p(b["text"]))
        elif t == "bullets": body.append(bullets(b["items"]))
        elif t == "img":
            flat, src, xml = img_block(b["file"], b.get("caption", ""), img_dir, idx)
            pics[flat] = src
            body.append(xml)
            idx += 1
        else:
            raise ValueError(f"bloco desconhecido: {t!r}")
    return "\n".join(body), pics

STYLES = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles xmlns:office="{NS['office']}" xmlns:style="{NS['style']}"
 xmlns:fo="{NS['fo']}" xmlns:text="{NS['text']}" xmlns:svg="{NS['svg']}"
 xmlns:table="{NS['table']}" office:version="1.2">
 <office:styles>
  <style:default-style style:family="paragraph"><style:paragraph-properties style:font-name="Liberation Sans"/></style:default-style>
  <style:style style:name="Standard" style:family="paragraph" style:class="text"/>
  <style:style style:name="Text_20_body" style:family="paragraph" style:parent-style-name="Standard">
   <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0.212cm" fo:line-height="115%"/>
  </style:style>
  <style:style style:name="Title" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="Text_20_body">
   <style:paragraph-properties fo:margin-bottom="0.423cm"/>
   <style:text-properties fo:font-size="26pt" fo:font-weight="bold" fo:color="#1f2937"/>
  </style:style>
  <style:style style:name="Subtitle" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="Text_20_body">
   <style:paragraph-properties fo:margin-bottom="0.423cm"/>
   <style:text-properties fo:font-size="12pt" fo:font-style="italic" fo:color="#4b5563"/>
  </style:style>
  <style:style style:name="Heading_20_1" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="Text_20_body">
   <style:paragraph-properties fo:margin-top="0.635cm" fo:margin-bottom="0.212cm" fo:keep-with-next="always"/>
   <style:text-properties fo:font-size="20pt" fo:font-weight="bold" fo:color="#0ea5e9"/>
  </style:style>
  <style:style style:name="Heading_20_2" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="Text_20_body">
   <style:paragraph-properties fo:margin-top="0.423cm" fo:margin-bottom="0.212cm" fo:keep-with-next="always"/>
   <style:text-properties fo:font-size="15pt" fo:font-weight="bold" fo:color="#0284c7"/>
  </style:style>
  <style:style style:name="Heading_20_3" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="Text_20_body">
   <style:paragraph-properties fo:margin-top="0.353cm" fo:margin-bottom="0.212cm" fo:keep-with-next="always"/>
   <style:text-properties fo:font-size="13pt" fo:font-weight="bold" fo:color="#075985"/>
  </style:style>
  <style:style style:name="P_20_1" style:family="paragraph" style:parent-style-name="Text_20_body">
   <style:paragraph-properties fo:margin-left="1.0cm" fo:margin-top="0cm" fo:margin-bottom="0.106cm"/>
  </style:style>
  <style:style style:name="P_20_Caption" style:family="paragraph" style:parent-style-name="Standard">
   <style:paragraph-properties fo:margin-top="0.106cm" fo:margin-bottom="0.318cm" fo:text-align="center"/>
  </style:style>
  <style:style style:name="T3" style:family="text">
   <style:text-properties fo:font-size="9pt" fo:font-style="italic" fo:color="#6b7280"/>
  </style:style>
  <text:list-style style:name="L1">
   <text:list-level-style-bullet text:level="1" text:bullet-char="•">
    <style:list-level-properties text:min-label-width="0.5cm" text:space-before="0cm"/>
    <style:text-properties fo:font-family="OpenSymbol"/>
   </text:list-level-style-bullet>
  </text:list-style>
  <style:style style:name="fr1" style:family="graphic" style:parent-style-name="Graphics">
   <style:graphic-properties fo:max-width="16cm" style:run-through="foreground"/>
  </style:style>
 </office:styles>
</office:document-styles>'''

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    cfg_path = pathlib.Path(sys.argv[1]).resolve()
    out_path = pathlib.Path(sys.argv[2]).resolve()
    img_dir = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else cfg_path.parent

    cfg = json.loads(cfg_path.read_text())
    body, pics = build_body(cfg["blocks"], img_dir)

    content_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content xmlns:office="{NS['office']}" xmlns:style="{NS['style']}"
 xmlns:text="{NS['text']}" xmlns:table="{NS['table']}" xmlns:draw="{NS['draw']}"
 xmlns:fo="{NS['fo']}" xmlns:xlink="{NS['xlink']}" xmlns:dc="{NS['dc']}"
 xmlns:meta="{NS['meta']}" xmlns:svg="{NS['svg']}" office:version="1.2">
 <office:automatic-styles>
  <style:style style:name="fr1" style:family="graphic" style:parent-style-name="Graphics">
   <style:graphic-properties fo:max-width="16cm" style:run-through="foreground"/>
  </style:style>
 </office:automatic-styles>
 <office:body><office:text>
<text:h text:style-name="Title" text:outline-level="1">{esc(cfg.get("title", ""))}</text:h>
<text:p text:style-name="Subtitle">{esc(cfg.get("subtitle", ""))}</text:p>
{body}
 </office:text></office:body>
</office:document-content>'''

    meta_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta xmlns:office="{NS['office']}" xmlns:dc="{NS['dc']}"
 xmlns:meta="{NS['meta']}" office:version="1.2">
 <office:meta>
  <dc:title>{esc(cfg.get("title", ""))}</dc:title>
  <dc:creator>{esc(cfg.get("creator", ""))}</dc:creator>
  <dc:language>{esc(cfg.get("language", "pt-BR"))}</dc:language>
  <meta:generator>plantuml-odt skill</meta:generator>
 </office:meta>
</office:document-meta>'''

    manifest_entries = [
        ' <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text" manifest:full-path="/"/>',
        ' <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>',
        ' <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>',
        ' <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="meta.xml"/>',
    ]
    for flat in pics:
        manifest_entries.append(f' <manifest:file-entry manifest:media-type="image/png" manifest:full-path="Pictures/{flat}"/>')

    manifest_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
{chr(10).join(manifest_entries)}
</manifest:manifest>'''

    with zipfile.ZipFile(out_path, "w") as z:
        # mimetype primeiro, SEM compressão
        z.writestr(zipfile.ZipInfo("mimetype"), "application/vnd.oasis.opendocument.text",
                   compress_type=zipfile.ZIP_STORED)
        z.writestr("content.xml", content_xml)
        z.writestr("styles.xml", STYLES)
        z.writestr("meta.xml", meta_xml)
        z.writestr("META-INF/manifest.xml", manifest_xml)
        for flat, src in pics.items():
            z.write(src, f"Pictures/{flat}")

    print(f"Gerado: {out_path} ({len(pics)} imagens)")

if __name__ == "__main__":
    main()
