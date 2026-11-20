# Lector de texto en imágenes · TP Integrador

**Seminario de Actualización**
2.º cuatrimestre 2026
Tecnicatura Superior en Ciencia de Datos e IA · IFTS N.º 18

**Alumna:** Natalia Nodar 
**Docente:** Cynthia M. Villagra 

App web que **lee el texto de una imagen**, tanto impreso como escrito a mano (apuntes, tickets, folletos, documentos), y lo devuelve listo para copiar. Usa el modelo ya entrenado [`lightonai/LightOnOCR-2-1B`](https://huggingface.co/lightonai/LightOnOCR-2-1B) de Hugging Face.

App publicada: https://nodarnatalia-seminarioactualizacion-1.onrender.com/?__theme=light

---

## Contenido de la carpeta

| Archivo / carpeta | Qué es |
|---|---|
| `app.py` | La app (Gradio). Recibe la imagen, la manda al modelo con `InferenceClient` y muestra el texto. |
| `requirements.txt` | Dependencias de la app (las que instala Render). |
| `TP_Nodar_Natalia.ipynb` | Notebook de pruebas: comparación de dos modelos, `pipeline` vs. `InferenceClient`, tiempos y valor de retorno. |
| `imagenes/` | Las 8 fotos de prueba que usan la notebook y los ejemplos de la app. |
| `resultados/` | Tablas de resultados que genera la notebook (CSV). |
| `.env.example` | Modelo del archivo `.env` donde va el token (sin el token real). |
| `.gitignore` | Archivos que no se suben al repo (`.env`, documentos de Word, temporales). |

---

## Cómo funciona

```
Navegador ──(imagen)──► Servidor de la app (Render, corre app.py)
                              │
                              │  InferenceClient + token (HF_TOKEN)
                              ▼
                       Hugging Face → proveedor Featherless AI
                       (ahí están los pesos y se hace la inferencia)
                              │
Navegador ◄──(texto)──────────┘
```

- **El código** vive en GitHub y se ejecuta en Render.
- **Los pesos del modelo** (~2 GB) quedan en los servidores del proveedor; la app no los descarga. Por eso no necesita `torch` ni `transformers`, y entra en el plan gratuito de Render.
- **El token** de Hugging Face nunca está en el código: en mi compu se lee del archivo `.env`, y en Render se carga como variable de entorno.

---

## Requisitos previos

1. **Python 3.11 o superior.**
2. **Una cuenta de Hugging Face y un token** con permiso para usar Inference Providers:
   - Entrar a https://huggingface.co/settings/tokens → **Create new token** → tipo **Fine-grained**.
   - Tildar **"Make calls to Inference Providers"** y copiar el token (empieza con `hf_`).
   - En https://huggingface.co/settings/inference-providers, tener activado **Featherless AI**.
   - La cuenta necesita **créditos** para Inference Providers. Sin créditos, la app devuelve el error `402 Payment Required`.

---

## Correr la app en tu compu

Desde una terminal, parada en esta carpeta (`TP_Integrador`):

```bash
# 1. Crear y activar un entorno virtual
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# 2. Instalar las dependencias
pip install -r requirements.txt

# 3. Crear el archivo .env con tu token
#    Copiá .env.example como .env y reemplazá el valor por tu token real:
#    HF_TOKEN=hf_xxxxxxxxxxxxxxxx

# 4. Arrancar la app
python app.py
```

En la terminal aparece `Running on local URL: http://0.0.0.0:7860`. Abrí **http://localhost:7860** en el navegador (o el número de puerto que indique la terminal). Para cortar la app: `Ctrl+C`.

> Si el puerto 7860 está ocupado por otra app de Gradio, la app usa automáticamente el siguiente libre (7861, 7862…).

---

## Correr la notebook

La notebook corre los modelos **en tu compu** con `pipeline`, así que necesita más dependencias que la app (`torch`, `transformers`, etc.). La primera celda las instala.

1. Abrir `TP_Nodar_Natalia.ipynb` en VS Code o Jupyter, con el mismo entorno virtual.
2. Tener el `.env` con el token (solo lo usan las celdas de `InferenceClient`; la parte de `pipeline` funciona sin token).
3. `Run All`.

Tené en cuenta:
- La primera vez se descargan los pesos de los modelos: ~2 GB (LightOnOCR) y ~9 GB (Qwen3-VL).
- Sin placa de video, cada imagen tarda alrededor de 1 a 2 minutos. Si la compu no tiene RAM suficiente para Qwen (~10 GB libres), en la celda de configuración se puede poner `FORMA_MODELO_B = "api"` para correrlo en los servidores de Hugging Face.
- La notebook ya está guardada con todos los resultados, así que no hace falta correrla para verlos.

---

## Publicar en Render

1. **New → Web Service** y conectar este repositorio.
2. Configuración:

   | Campo | Valor |
   |---|---|
   | Root Directory | `TP_Integrador` |
   | Runtime | Python 3 |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `python app.py` |
   | Instance Type | Free |

3. En **Environment**, agregar la variable `HF_TOKEN` con el token.
4. **Deploy.** Render define la variable `PORT` y la app escucha en ese puerto, en `0.0.0.0`.

> En el plan gratuito, Render apaga el servicio tras 15 minutos sin visitas y tarda alrededor de un minuto en volver a arrancar. Para que esté siempre disponible, un servicio externo (cron-job.org) visita la URL cada 10 minutos.

---

## Limitaciones

- Funciona mejor con **texto impreso** y **letra prolija**. Con letra cursiva, fotos borrosas o muy inclinadas comete más errores.
- Si la imagen no se puede leer, el modelo **puede inventar texto** que parece real. Hay que revisar siempre el resultado.
- La imagen se envía a los servidores de Hugging Face y del proveedor para procesarla: no conviene subir documentos con datos sensibles.
- Cada imagen consume créditos de la cuenta de Hugging Face. Si se terminan los créditos o el token se revoca, la app deja de responder.
