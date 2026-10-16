# Clase 2 · Preparación del entorno de desarrollo

Laboratorio de la Clase 2: dejar listo todo lo necesario para programar el proyecto. Al final hay una app mínima de Gradio que corre dentro de un entorno virtual y está guardada en Git.

## Qué se hizo

1. **Verificar e instalar** Python, VS Code y Git, y configurar Git con mi nombre.
2. **Crear el proyecto:** una carpeta con `app.py` y `README.md`, abierta en VS Code.
3. **Armar el entorno virtual** (`.venv`): una carpeta con un Python propio del proyecto, para que las librerías que instalo acá no se mezclen con las de otros proyectos. Se activó y se seleccionó como intérprete en VS Code.
4. **Registrar las dependencias:** instalé Gradio dentro del entorno y guardé la lista de librerías en `requirements.txt`, para que otra persona pueda instalar exactamente lo mismo.
5. **Inicializar el repositorio:** `git init`, revisar el estado, crear el `.gitignore` y hacer el primer commit.

## Archivos

| Archivo | Qué es | ¿Se sube a GitHub? |
|---|---|---|
| `app.py` | La app de Gradio | Sí |
| `requirements.txt` | Lista de librerías que necesita la app | Sí |
| `.gitignore` | Lista de lo que Git **no** tiene que subir (el entorno virtual, archivos temporales, el `.env`) | Sí |
| `README.md` | Este archivo | Sí |
| `.venv/` | El entorno virtual | **No**: cada persona crea el suyo |

## Qué hace la app

Es el ejemplo básico de Gradio: escribís un nombre, movés un control deslizante y la app devuelve un saludo con tantos signos de exclamación como indique el control. Por ejemplo, `Natalia` con intensidad 3 devuelve `Hello, Natalia!!!`.

## Cómo correrla

Necesitás **Python 3.10 o superior**. Abrí una terminal **dentro de la carpeta `Clase_2`** y seguí estos pasos:

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

La terminal muestra dos direcciones:

- `http://127.0.0.1:7860`: abrila en el navegador para usar la app en tu compu.
- Un link `https://....gradio.live`: es un link público y temporal (lo genera `share=True`) para que otra persona pueda probar la app mientras tu compu la tiene abierta. Dura 72 horas como máximo.

Para cortar la app, volvé a la terminal y apretá `Ctrl + C`.

## Comandos útiles de esta clase

```bash
python --version          # versión de Python
git --version             # versión de Git
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
pip freeze > requirements.txt   # guarda las librerías instaladas en el entorno
git status                # qué cambió y qué falta guardar
git add .
git commit -m "Mensaje que explique el cambio"
```
