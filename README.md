# Seminario de Actualización · Portfolio de la cursada

**Tecnicatura Superior en Ciencia de Datos e IA · IFTS N.º 18**
**Alumna:** Natalia Nodar · **Docente:** Cynthia M. Villagra · 2.º cuatrimestre 2026

Este repositorio junta las actividades de cada clase del Seminario de Actualización. Cada clase tiene su carpeta, con su propio README que explica qué se hizo y cómo reproducirlo paso a paso.

---

## Resumen de las clases

| Clase | Tema | Qué hay en la carpeta | Ver |
|---|---|---|---|
| 2 | Preparación del entorno de desarrollo | Primera app de Gradio, entorno virtual, `requirements.txt` y `.gitignore` | [Clase_2](Clase_2/) |
| 3 | Git y GitHub: problemas frecuentes | Explicación de tres situaciones: README duplicado, carpeta sin ignorar y ramas `master`/`main` | [Clase_3](Clase_3/) |
| 4 | Interfaces con Gradio | App mínima de Gradio compartida con un link temporal (`share=True`) | [Clase_4](Clase_4/) |
| 5 | Publicar una app (deploy) | La misma idea publicada en dos lugares: Gradio en Render y Streamlit en Streamlit Community Cloud | [Clase_5](Clase_5/) |

### Clase 2 · Preparación del entorno

Se instalaron y verificaron Python, VS Code y Git; se creó un **entorno virtual** (`.venv`) para que las librerías del proyecto no se mezclen con las del resto de la compu; se instaló Gradio, se guardaron las dependencias en `requirements.txt` y se inicializó el repositorio con un `.gitignore` y el primer commit.

### Clase 3 · Problemas frecuentes con Git

Tres situaciones que aparecen al subir un proyecto a GitHub y cómo se resolvieron: un README creado dos veces (en GitHub y en la compu), una carpeta que se subió sin querer porque no estaba en el `.gitignore`, y la diferencia entre la rama `master` (la que crea Git) y `main` (la que usa GitHub).

### Clase 4 · Interfaces con Gradio

Una app web mínima hecha con Gradio: recibe un nombre y devuelve un saludo. Se corre en la compu y se comparte con un link público temporal usando `share=True`.

### Clase 5 · Deploy

La app se publicó en un servidor de verdad, para que funcione aunque la compu esté apagada:

- **Gradio en Render:** https://nodarnatalia-seminarioactualizacion.onrender.com/
- **Streamlit en Streamlit Community Cloud:** https://nodarnataliaseminarioactualizacion-fktrpatjypghnbghj6zzy5.streamlit.app/

