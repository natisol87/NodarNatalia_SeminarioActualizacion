# Clase 5 · Publicar la app (deploy)

Actividad de la Clase 5: dejar la app funcionando en un servidor de verdad, para que cualquiera pueda usarla aunque mi compu esté apagada, y comprobar que el procedimiento no depende de la herramienta de interfaz. Por eso hay dos versiones publicadas.

## Links

- **Gradio en Render:** https://nodarnatalia-seminarioactualizacion.onrender.com/
- **Streamlit en Streamlit Community Cloud:** https://nodarnataliaseminarioactualizacion-fktrpatjypghnbghj6zzy5.streamlit.app/

> En el plan gratuito, Render apaga la app después de 15 minutos sin visitas. La primera vez que se abre después de eso tarda alrededor de un minuto en cargar: hay que esperar, no está rota.

## Dónde está el código

| Versión | Código | Dependencias |
|---|---|---|
| Gradio (Render) | `app.py` en la **raíz** del repositorio | `requirements.txt` en la raíz |
| Streamlit | `Clase_5/app_streamlit/app.py` | `Clase_5/app_streamlit/requirements.txt` |

La app de Gradio está en la raíz porque Render toma el código desde ahí.

---

## Versión Gradio, en Render

**Qué hace:** escribís un nombre y elegís una intensidad con un control deslizante; devuelve `Hello, <nombre>!` con tantos signos de exclamación como la intensidad.

### Correrla en tu compu

Desde una terminal en la **raíz** del repositorio:

```bash
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Abrí `http://localhost:7860` en el navegador.

### Publicarla en Render

1. Crear una cuenta en https://render.com y conectarla con GitHub.
2. **New → Web Service** y elegir este repositorio.
3. Completar:

   | Campo | Valor |
   |---|---|
   | Root Directory | (vacío: la raíz del repo) |
   | Runtime | Python 3 |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `python app.py` |
   | Instance Type | Free |

4. **Deploy.** Cuando termina, Render muestra la URL pública.

Para que funcione en Render, la app tiene que escuchar en `0.0.0.0` (no solo en la compu propia) y en el puerto que le asigna Render a través de la variable `PORT`. Por eso `app.py` termina así:

```python
demo.launch(server_name="0.0.0.0",
            server_port=int(os.environ.get("PORT", 7860)))
```

En la compu no existe `PORT`, así que usa el 7860.

---

## Versión Streamlit, en Streamlit Community Cloud

**Qué hace:** pide un nombre y un color, y al tocar **Saludar** muestra `Hola, <nombre>. Tu color elegido es <color>.`

### Correrla en tu compu

Desde una terminal en la carpeta `Clase_5/app_streamlit`:

```bash
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
python -m streamlit run app.py
```

Se abre sola en `http://localhost:8501`.

### Publicarla en Streamlit Community Cloud

1. Entrar a https://share.streamlit.io con la cuenta de GitHub.
2. **Create app → Deploy a public app from GitHub.**
3. Completar: el repositorio, la rama `main` y el archivo `Clase_5/app_streamlit/app.py`.
4. **Deploy.** Streamlit instala el `requirements.txt` que está al lado del `app.py`.

---

## Qué resultó distinto entre las dos

| | Render (Gradio) | Streamlit Community Cloud |
|---|---|---|
| Para qué sirve | Cualquier app web de Python | Solo apps de Streamlit |
| Cómo arranca la app | Hay que darle el comando (`python app.py`) | Solo se elige el archivo `.py` |
| Puerto y dirección | La app tiene que leer `PORT` y escuchar en `0.0.0.0`: hubo que cambiar el código | Lo maneja la plataforma: el código no cambia |
| Dónde busca el código | En la carpeta que se indica en *Root Directory* | En la ruta exacta del archivo, aunque esté en una subcarpeta |
| Cuando nadie la usa | Se duerme a los 15 minutos y tarda alrededor de un minuto en volver | También se duerme si no tiene visitas por un tiempo, y hay que despertarla |
