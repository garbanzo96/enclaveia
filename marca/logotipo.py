# Contornea "Enclave IA" en Public Sans (instancia wght=650) y arma los SVG del logotipo.
# Uso: python3 marca/logotipo.py <public-sans variable .woff2 o .ttf> sitio/assets/marca
# Requiere: pip install fonttools brotli uharfbuzz
import sys, json, io
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import uharfbuzz as hb
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from isotipo import build

src, outdir = sys.argv[1], sys.argv[2]
font = TTFont(src)
inst = instantiateVariableFont(font, {"wght": 650})
buf_io = io.BytesIO(); inst.flavor = None; inst.save(buf_io); data = buf_io.getvalue()
upm = inst["head"].unitsPerEm
cap = inst["OS/2"].sCapHeight
gs = inst.getGlyphSet()

def shape(text, tracking_em):
    face = hb.Face(data); f = hb.Font(face)
    b = hb.Buffer(); b.add_str(text); b.guess_segment_properties()
    hb.shape(f, b, {"kern": True, "liga": False})
    x = 0; parts = []
    for info, pos in zip(b.glyph_infos, b.glyph_positions):
        name = inst.getGlyphName(info.codepoint)
        parts.append((name, x + pos.x_offset))
        x += pos.x_advance + tracking_em * upm
    return parts, x - tracking_em * upm

def path_for(parts, scale, dx, baseline):
    pen = SVGPathPen(gs)
    for name, x in parts:
        tp = TransformPen(pen, (scale, 0, 0, -scale, dx + x*scale, baseline))
        gs[name].draw(tp)
    return pen.getCommands()

# Escala: altura de versal del texto = 26 unidades; isotipo en caja de 48 con base en y=41
iso = build(R=17, t=7, cx=24, cy=22, base=41, alpha_deg=17, gap=2.4, protr=3.4)
cap_target = 26.0
scale = cap_target / cap
parts, width = shape("Enclave IA", -0.012)
baseline = iso["base"]
x_text = iso["xmax"] + 12.5   # separación símbolo-texto ~ media altura de versal
text_d = path_for(parts, scale, x_text, baseline)
x_end = x_text + width*scale
x0, y0 = iso["xmin"], iso["ytop"]
W = x_end - x0; H = baseline - y0
ink, blue = "#14171F", "#1F3FA6"

def svg(d_text, ink_col, key_col, with_text=True, pad=0):
    vb = f"{x0-pad:.2f} {y0-pad:.2f} {(W if with_text else iso['xmax']-x0)+2*pad:.2f} {H+2*pad:.2f}"
    t = f'<path fill="{ink_col}" d="{d_text}"/>' if with_text else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Enclave IA">'
            f'<path fill="{ink_col}" d="{iso["left"]}"/><path fill="{ink_col}" d="{iso["right"]}"/>'
            f'<path fill="{key_col}" d="{iso["key"]}"/>{t}</svg>')

files = {
  "enclave-ia-logo.svg": svg(text_d, ink, blue),
  "enclave-ia-logo-negativo.svg": svg(text_d, "#FFFFFF", "#8FA6FF"),
  "enclave-ia-logo-una-tinta.svg": svg(text_d, ink, ink),
  "enclave-ia-isotipo.svg": svg(text_d, ink, blue, with_text=False),
  "enclave-ia-isotipo-negativo.svg": svg(text_d, "#FFFFFF", "#8FA6FF", with_text=False),
}
for n, c in files.items():
    open(f"{outdir}/{n}", "w").write(c + "\n")
# Datos para usar en línea (CSS currentColor)
json.dump({"left": iso["left"], "right": iso["right"], "key": iso["key"], "text": text_d,
           "viewbox_full": f"{x0:.2f} {y0:.2f} {W:.2f} {H:.2f}", "viewbox_iso": f"{x0:.2f} {y0:.2f} {iso['xmax']-x0:.2f} {H:.2f}",
           "ratio": W/H, "cap_units": cap_target, "H": H}, open(f"{outdir}/logo-data.json", "w"))
print("W/H", round(W/H, 3), "H", round(H, 2), "cap", cap, "upm", upm)
