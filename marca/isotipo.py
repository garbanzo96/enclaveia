# Genera el isotipo de Enclave IA: arco de medio punto con dovela clave.
# Retícula de 48 unidades. Todas las medidas salen de R (radio exterior).
import math, sys, json

def build(R=17.0, t=8.0, cx=24.0, cy=21.0, base=43.0, alpha_deg=16.0, gap=2.4, protr=3.2):
    r = R - t
    a = math.radians(alpha_deg)
    # Dovela: cuña radial entre 90-alpha y 90+alpha, de r a R+protr, con tapa horizontal.
    # Ángulos medidos desde el eje vertical (0 = arriba), x = cx + rho*sin, y = cy - rho*cos
    def P(rho, ang):
        return (cx + rho*math.sin(ang), cy - rho*math.cos(ang))
    # tapa horizontal: punto donde la línea radial a +-alpha alcanza y_top
    ytop = cy - (R + protr)*math.cos(a)
    rho_top = (cy - ytop)/math.cos(a)
    kL_in, kR_in = P(r, -a), P(r, a)
    kL_top, kR_top = P(rho_top, -a), P(rho_top, a)
    key = [kL_in, kL_top, kR_top, kR_in]
    # Media dovela derecha: borde de junta paralelo al borde de la clave, desplazado 'gap'.
    # Línea radial a ángulo a desplazada perpendicularmente hacia afuera (hacia +x).
    nx, ny = math.cos(a), math.sin(a)  # normal a la línea radial (dirección de giro)
    def joint_point(rho):
        x, y = P(rho, a)
        # solo desplazamos; luego intersectamos con el círculo de radio rho' (aprox. resolviendo)
        return (x + gap*nx, y + gap*ny)
    def on_circle(rad):
        # punto de la línea desplazada que cae sobre el círculo de radio rad
        # línea: p(s) = c + s*u + gap*n, u = dirección radial
        ux, uy = math.sin(a), -math.cos(a)
        ox, oy = gap*nx, gap*ny
        # |o + s u| = rad -> s^2 + 2 s (o.u) + |o|^2 - rad^2 = 0
        b = ox*ux + oy*uy
        c = ox*ox + oy*oy - rad*rad
        s = -b + math.sqrt(b*b - c)
        return (cx + ox + s*ux, cy + oy + s*uy)
    jo = on_circle(R)
    ji = on_circle(r)
    ang_o = math.atan2(jo[0]-cx, -(jo[1]-cy))
    ang_i = math.atan2(ji[0]-cx, -(ji[1]-cy))
    # mitad derecha: junta (ji -> jo), arco exterior hasta 90° (horizontal), jamba exterior baja a base,
    # base hasta jamba interior, sube hasta cy, arco interior de vuelta a ji
    f = lambda v: f"{v:.3f}"
    right = (f"M{f(ji[0])} {f(ji[1])}L{f(jo[0])} {f(jo[1])}"
             f"A{f(R)} {f(R)} 0 0 1 {f(cx+R)} {f(cy)}"
             f"L{f(cx+R)} {f(base)}L{f(cx+r)} {f(base)}L{f(cx+r)} {f(cy)}"
             f"A{f(r)} {f(r)} 0 0 0 {f(ji[0])} {f(ji[1])}Z")
    left = (f"M{f(2*cx-ji[0])} {f(ji[1])}L{f(2*cx-jo[0])} {f(jo[1])}"
            f"A{f(R)} {f(R)} 0 0 0 {f(cx-R)} {f(cy)}"
            f"L{f(cx-R)} {f(base)}L{f(cx-r)} {f(base)}L{f(cx-r)} {f(cy)}"
            f"A{f(r)} {f(r)} 0 0 1 {f(2*cx-ji[0])} {f(ji[1])}Z")
    keyd = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in key) + "Z"
    return {"left": left, "right": right, "key": keyd, "ytop": ytop, "base": base,
            "xmin": cx-R, "xmax": cx+R}

if __name__ == "__main__":
    params = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    print(json.dumps(build(**params)))
