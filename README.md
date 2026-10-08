# Enclave IA · sitio web

**[Abrir la página en el navegador](https://garbanzo96.github.io/enclaveia/)** · [versión en inglés](https://garbanzo96.github.io/enclaveia/en/)

Sitio de [enclaveia.cl](https://enclaveia.cl). Enclave IA es una marca de Synesis Lab SpA.

Es un sitio estático: HTML, CSS y un archivo de JavaScript opcional. No tiene dependencias ni paso de compilación, y funciona aunque el JavaScript esté desactivado.

## Ver la página

- **GitHub Pages:** [garbanzo96.github.io/enclaveia](https://garbanzo96.github.io/enclaveia/). Cada push a `main` se publica solo en uno o dos minutos (`.github/workflows/pages.yml`). Requiere que en *Settings → Pages → Source* esté elegido **GitHub Actions**.
- **En su computador:** `cd sitio && python3 -m http.server 8000` y abrir [http://localhost:8000](http://localhost:8000).

Las rutas internas son relativas, así que el sitio funciona igual en enclaveia.cl, en una subcarpeta de GitHub Pages o en local.

## Estructura

| Carpeta o archivo | Qué contiene |
| --- | --- |
| `sitio/` | Todo lo que se publica. Es el directorio de salida en Cloudflare Pages |
| `sitio/index.html` | Página en español (versión principal) |
| `sitio/en/index.html` | Página en inglés |
| `sitio/privacidad.html`, `sitio/en/privacy.html` | Política de privacidad |
| `sitio/marca/` | Guía de marca en enclaveia.cl/marca (no se indexa) |
| `sitio/assets/site.css` | Todos los estilos: colores, tipografía y retícula |
| `sitio/assets/site.js` | El ejemplo interactivo y el botón de copiar correo |
| `sitio/assets/fonts/` | Newsreader y Public Sans en WOFF2, con sus licencias OFL |
| `sitio/assets/marca/` | Logotipo e isotipo en SVG (color, negativo y una tinta) |
| `sitio/_headers` | Cabeceras de seguridad para Cloudflare Pages |
| `marca/` | Generadores del isotipo y del logotipo en Python |

## Publicar en Cloudflare Pages

1. En Cloudflare, ir a **Workers & Pages → Create → Pages → Connect to Git** y elegir este repositorio.
2. Configurar: *Framework preset* **None**, *Build command* vacío y *Build output directory* `sitio`.
3. Desplegar y revisar la dirección `*.pages.dev` que entrega Cloudflare.
4. En **Custom domains**, agregar `enclaveia.cl` y `www.enclaveia.cl`. En NIC Chile, apuntar el dominio a los servidores de nombres que indique Cloudflare.
5. Redirigir `www.enclaveia.cl` a `enclaveia.cl`.

Los enlaces internos apuntan a archivos `.html`; Cloudflare Pages los redirige a la dirección sin extensión.

## Antes de publicar

- [ ] Revisar la política de privacidad con un abogado.
- [ ] Confirmar que `hola@enclaveia.cl` recibe correos.
- [ ] Reemplazar el ejemplo de la portada por una salida real del prototipo.
- [ ] Buscar «Enclave» en INAPI, en las clases 9, 35, 41 y 42.
- [ ] No activar Bot Fight Mode ni Web Analytics de Cloudflare. Si se activan, Cloudflare puede instalar una cookie técnica (`__cf_bm`) y hay que corregir la frase «no usa cookies» del pie y de la política de privacidad.

## Cómo editar

- Los textos están en `sitio/index.html` y `sitio/en/index.html`. Cuando se cambia uno hay que cambiar el otro.
- Al modificar contenido, se actualiza la fecha de «Última revisión» del pie en ambas páginas y la fecha de `sitio/sitemap.xml`.
- El logotipo va incrustado en el HTML como SVG para que cambie de color en modo oscuro. Su trazado no se edita a mano: se regenera (ver abajo).
- La política de seguridad (`_headers`) no admite estilos ni scripts en línea. Los estilos van en `site.css` y el código en `site.js`.
- La marca se escribe siempre «Enclave IA», también en inglés. Nunca «Enclave AI», que es el nombre de otra empresa del rubro.

## Decisiones de diseño

- **Un solo acento.** El azul tinta (#1F3FA6) solo aparece en la dovela, los enlaces y la acción principal.
- **Dos familias tipográficas.** Newsreader para titulares y Public Sans para texto.
- **Retícula de 12 columnas.** El espaciado usa múltiplos de 8 px.
- **Contraste AA.** El texto más claro marca 5,2:1 sobre el fondo.
- **Nada de terceros.** No hay cookies, analítica ni solicitudes a otros dominios: las fuentes se alojan en el propio sitio.
- **Peso total:** cerca de 450 KB, de los cuales 110 KB son fuentes.
- **Afirmaciones con fuente.** Las cifras llevan su fuente en notas al pie.

La guía de marca completa está en `sitio/marca/index.html`.

## Regenerar el logotipo

```bash
pip install fonttools brotli uharfbuzz
npm pack @fontsource-variable/public-sans && tar -xzf fontsource-variable-public-sans-*.tgz
python3 marca/logotipo.py package/files/public-sans-latin-wght-normal.woff2 sitio/assets/marca
rm sitio/assets/marca/logo-data.json  # datos intermedios para incrustar el logotipo en el HTML
```

`marca/isotipo.py` contiene la geometría del símbolo: un arco de radio exterior 17 y radio interior 10, y una dovela de 17° por lado, con juntas de 2,4 unidades, que sobresale 3,4 unidades. El texto es Public Sans con peso 650 convertido a curvas.

## Licencias

Newsreader y Public Sans se distribuyen con la SIL Open Font License 1.1; las licencias están en `sitio/assets/fonts/`. Los textos, el logotipo y el código son © 2026 Synesis Lab SpA.
