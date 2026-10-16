# Clase 4 · App mínima con Gradio

Actividad de la Clase 4: armar una interfaz web con Gradio, correrla en la compu y compartirla con un link público temporal (`share=True`).

## Qué hace la app

Tiene un campo para escribir un nombre y devuelve un saludo: si escribís `Natalia`, responde `Hola, Natalia!`. Si dejás el campo vacío, responde `Hola, mundo!`.

## Cómo está hecha

- **`saludar(nombre)`** es la función propia: recibe el texto, le saca los espacios de más con `.strip()` y devuelve el saludo con `return`.
- **La interfaz** conecta la función con sus componentes de Gradio: un `Textbox` de entrada (`Tu nombre`) y uno de salida (`Saludo`).
- **`launch(share=True)`** arranca la app y además genera un link público temporal.

## Archivos

| Archivo | Qué es |
|---|---|
| `app.py` | La app |
| `requirements.txt` | La librería que necesita: `gradio` |
| `.gitignore` | Lo que no se sube a GitHub (entorno virtual, temporales, `.env`) |

## Cómo correrla

Necesitás **Python 3.10 o superior**. Abrí una terminal **dentro de la carpeta `Clase_4`**:

```bash
# 1. Crear el entorno virtual
python -m venv .venv

# 2. Activarlo
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# 3. Instalar las dependencias
pip install -r requirements.txt

# 4. Correr la app
python app.py
```

En la terminal aparecen dos direcciones:

- `http://127.0.0.1:7860`: la app en tu compu. Abrila en el navegador.
- `https://....gradio.live`: el link público. Cualquiera puede abrirlo **mientras la app siga corriendo en tu compu**; si la cerrás, el link deja de andar. Dura 72 horas como máximo.

Para cortar la app: `Ctrl + C` en la terminal.

> Si el puerto 7860 está ocupado por otra app de Gradio, Gradio usa el siguiente libre (7861, 7862…): fijate en la terminal qué dirección te dio.
