"""
TP Integrador · Seminario de Actualización · IFTS N.º 18
App que lee el texto de una imagen (impreso o manuscrito)
"""

import base64
import io
import os
import re
import time

import gradio as gr
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from PIL import Image, ImageOps

# ---------------------------------------------------------------- configuración
load_dotenv(override=True)              # en mi compu lee el .env; en el deploy el token viene de la plataforma

MODELO = "lightonai/LightOnOCR-2-1B"
PROVEEDOR = "featherless-ai"            # el proveedor que sirve este modelo en Hugging Face
MAX_TOKENS = 1024                       # largo máximo de la respuesta
LADO_MAX = 1540                         # tamaño de imagen que recomienda la model card

HF_TOKEN = os.environ.get("HF_TOKEN")
cliente = InferenceClient(provider=PROVEEDOR, token=HF_TOKEN)


# ---------------------------------------------------------------- funciones
def preparar_imagen(imagen):
    """Endereza la foto según el celular, la pasa a RGB y la achica si es muy grande."""
    imagen = ImageOps.exif_transpose(imagen).convert("RGB")
    imagen.thumbnail((LADO_MAX, LADO_MAX))
    return imagen


def imagen_a_base64(imagen):
    """InferenceClient no recibe objetos de Python: la imagen viaja como texto base64."""
    buffer = io.BytesIO()
    imagen.save(buffer, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()


def limpiar(texto):
    """LightOnOCR marca las fotos con ![image](image_1.png); en la app no sirven, las saco."""
    texto = re.sub(r"!\[image\]\([^)]*\)", "", texto)
    return re.sub(r"\n{3,}", "\n\n", texto).strip()


def leer_texto(imagen):
    if imagen is None:
        raise gr.Error("Primero subí una imagen.")
    if not HF_TOKEN:
        raise gr.Error("La app no tiene configurado el token de Hugging Face (variable HF_TOKEN).")

    mensajes = [{
        "role": "user",
        "content": [{"type": "image_url",
                     "image_url": {"url": imagen_a_base64(preparar_imagen(imagen))}}],
    }]

    t0 = time.perf_counter()
    try:
        respuesta = cliente.chat_completion(model=MODELO, messages=mensajes, max_tokens=MAX_TOKENS)
    except Exception as e:
        raise gr.Error(f"No pude procesar la imagen. Detalle: {e}")
    segundos = time.perf_counter() - t0

    texto = limpiar(respuesta.choices[0].message.content or "")
    if not texto:
        texto = "(El modelo no encontró texto en la imagen.)"

    detalle = f"Tiempo: {segundos:.1f} s · modelo `{MODELO}`"
    if respuesta.usage:
        detalle += f" · {respuesta.usage.total_tokens} tokens"
    return texto, texto, detalle


# ---------------------------------------------------------------- interfaz
EJEMPLOS = [os.path.join("imagenes", f) for f in
            ["01_impreso_limpio.jpeg", "05_manuscrito_prolijo.jpg", "06_manuscrito_apurado.jpeg"]]
EJEMPLOS = [[e] for e in EJEMPLOS if os.path.exists(e)]

# Paleta: crema #FFF1E6 · rosa #FDE2E4 · menta #E2ECE9 · celeste #CDDAFD · verde salvia #DBE7E4
TEXTO_OSCURO = "#3B3F51"
TEMA = gr.themes.Soft(font=[gr.themes.GoogleFont("Chakra Petch"), "sans-serif"],
                      radius_size=gr.themes.sizes.radius_none).set(
    body_background_fill="#FFF1E6",
    body_text_color=TEXTO_OSCURO,
    block_background_fill="#FFFFFF",
    block_border_color="#DBE7E4",
    block_label_background_fill="#E2ECE9",
    block_label_text_color=TEXTO_OSCURO,
    block_title_text_color=TEXTO_OSCURO,
    input_background_fill="#FFFFFF",
    border_color_primary="#DBE7E4",
    color_accent="#CDDAFD",
    color_accent_soft="#E2ECE9",
    button_primary_background_fill="#CDDAFD",
    button_primary_background_fill_hover="#BACBFA",
    button_primary_text_color=TEXTO_OSCURO,
    button_secondary_background_fill="#FDE2E4",
    button_secondary_text_color=TEXTO_OSCURO,
)

ALTO_PANEL = 440   # alto de la imagen y del texto, para que las dos columnas sean simétricas
ALTO_BARRA = 46    # alto del botón y de la barra de pestañas, para que queden alineados

CSS = f"""
/* Bordes rectos en todos los botones y módulos */
.gradio-container *, .gradio-container *::before, .gradio-container *::after {{ border-radius: 0 !important; }}
.gradio-container, .gradio-container button, .gradio-container textarea {{ font-family: 'Chakra Petch', sans-serif !important; }}
#encabezado h1 {{ font-family: 'Chakra Petch', sans-serif !important; font-weight: 700 !important;
                 font-size: 2.3rem !important; letter-spacing: 0.5px; }}
.gradio-container {{ max-width: 1150px !important; margin: auto; }}
#encabezado {{ background: #FDE2E4; padding: 22px 28px; text-align: center; }}
#encabezado h1 {{ margin: 0 0 6px 0; color: {TEXTO_OSCURO}; }}
#encabezado p {{ margin: 2px 0; }}

/* Botón y pestañas: misma altura y alineados arriba */
#boton-leer {{ height: {ALTO_BARRA}px !important; min-height: {ALTO_BARRA}px !important;
              max-height: {ALTO_BARRA}px !important; padding: 0 !important; box-shadow: none !important; font-weight: 700; font-size: 1rem; }}
#pestanas .tab-wrapper, #pestanas .tab-container {{ height: {ALTO_BARRA}px !important; min-height: {ALTO_BARRA}px !important;
              padding: 0 !important; border: none !important; box-shadow: none !important; }}
#pestanas .tab-container {{ display: flex; gap: 8px; width: 100%; }}
#pestanas button[role="tab"] {{ flex: 1; height: {ALTO_BARRA}px !important;
              background: #FFFFFF; color: {TEXTO_OSCURO}; font-weight: 700; font-size: 1rem;
              border: 1px solid #DBE7E4 !important; justify-content: center; }}
#pestanas button[role="tab"].selected {{ background: #CDDAFD; }}
#pestanas button[role="tab"].selected::after {{ display: none; }}
#pestanas .tabitem {{ padding: 0 !important; margin: 0 !important; border: none !important; background: transparent !important; }}

/* Imagen y texto: mismo alto */
#entrada, #salida-texto, #salida-md {{ height: {ALTO_PANEL}px !important; min-height: {ALTO_PANEL}px !important;
             max-height: {ALTO_PANEL}px !important; box-sizing: border-box !important; margin: 0 !important; }}
#salida-texto textarea {{ height: {ALTO_PANEL - 60}px !important; max-height: {ALTO_PANEL - 60}px !important; }}
#salida-texto {{ height: {ALTO_PANEL}px !important; }}
#salida-md {{ height: {ALTO_PANEL}px; overflow-y: auto; background: #FFFFFF;
             border: 1px solid #DBE7E4; padding: 12px 16px; }}

#detalle {{ text-align: center; min-height: 1.5em; }}
#ejemplos {{ background: #FFFFFF; padding: 10px 16px; }}
#limitaciones {{ background: #CDDAFD; padding: 14px 22px; font-size: 0.92rem; }}
footer {{ display: none !important; }}
"""

# Tipografía de Google Fonts: Chakra Petch en toda la app
HEAD = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:ital,wght@0,300;0,400;0,500;0,600;0,700;'
    '1,300;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet">'
)

# Fuerza el modo claro aunque el navegador esté en modo oscuro, para que se vea la paleta.
JS_MODO_CLARO = """
() => {
  const url = new URL(window.location.href);
  if (url.searchParams.get('__theme') !== 'light') {
    url.searchParams.set('__theme', 'light');
    window.location.replace(url.href);
  }
}
"""

with gr.Blocks(title="Lector de texto en imágenes") as demo:
    gr.Markdown(
        "# Lector de texto en imágenes\n"
        "Subí una foto o un escaneo de un texto **impreso o escrito a mano** "
        "(apuntes, tickets, folletos, documentos) y la app te devuelve el texto para copiarlo.\n\n"
        "Usa el modelo [LightOnOCR-2-1B](https://huggingface.co/lightonai/LightOnOCR-2-1B) "
        "a través de Hugging Face.",
        elem_id="encabezado",
    )

    with gr.Row(equal_height=True):
        with gr.Column(scale=1, elem_classes="columna"):
            boton = gr.Button("Leer texto", variant="primary", elem_id="boton-leer")
            entrada = gr.Image(type="pil", label="Imagen con texto", elem_id="entrada",
                               sources=["upload", "webcam", "clipboard"], height=ALTO_PANEL)
        with gr.Column(scale=1, elem_classes="columna"):
            with gr.Tabs(elem_id="pestanas"):
                with gr.Tab("Texto"):
                    salida_texto = gr.Textbox(label="Texto leído", buttons=["copy"],
                                              lines=16, max_lines=16, elem_id="salida-texto")
                with gr.Tab("Vista con formato"):
                    salida_md = gr.Markdown(elem_id="salida-md")

    detalle = gr.Markdown(elem_id="detalle")

    if EJEMPLOS:
        with gr.Column(elem_id="ejemplos"):
            gr.Examples(EJEMPLOS, inputs=entrada, label="Probá con un ejemplo")

    gr.Markdown(
        "**Limitaciones:** funciona mejor con texto impreso y letra prolija. Con letra cursiva "
        "o fotos borrosas puede equivocarse, y si la imagen no se puede leer **puede inventar texto**: "
        "revisá siempre el resultado. La imagen se envía a los servidores de Hugging Face para "
        "procesarla, así que no subas documentos con datos sensibles.",
        elem_id="limitaciones",
    )

    boton.click(leer_texto, inputs=entrada, outputs=[salida_texto, salida_md, detalle])


if __name__ == "__main__":
    # En Render la plataforma define la variable PORT y la app tiene que escuchar ahí, en 0.0.0.0.
    # En mi compu no hay PORT: con server_port=None, Gradio prueba desde el 7860 en adelante
    # y usa el primer puerto libre (así no choca con otras apps de Gradio que estén abiertas).
    puerto = os.environ.get("PORT")
    demo.launch(server_name="0.0.0.0", server_port=int(puerto) if puerto else None,
                theme=TEMA, css=CSS, js=JS_MODO_CLARO, head=HEAD)
