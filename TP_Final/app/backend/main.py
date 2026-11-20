"""
API del TP Final Integrador.

Sirve el modelo entrenado en notebook/entrenamiento.ipynb:
- GET  /health   → comprueba que el servidor está vivo.
- POST /predecir → recibe los hábitos de uso del celular y devuelve
                   si hay adicción alta y con qué probabilidad.
Además sirve la página del frontend en "/", así front y back quedan
en el mismo dominio (no hace falta CORS).

Correr en local (parada en la carpeta app/):
    uvicorn backend.main:app --reload
"""
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, model_validator

# Rutas 
CARPETA_APP = Path(__file__).resolve().parent.parent
RUTA_MODELO = CARPETA_APP / "modelo" / "modelo.joblib"
CARPETA_FRONTEND = CARPETA_APP / "frontend"

# El modelo se carga una sola vez, cuando arranca el servidor,
# y queda en memoria para todas las predicciones.
modelo = joblib.load(RUTA_MODELO)

# Columnas con las que se entrenó el modelo
COLUMNAS = [
    "Daily_Usage_Hours",
    "Sleep_Hours",
    "Time_on_Social_Media",
    "Time_on_Gaming",
    "Phone_Checks_Per_Day",
    "Apps_Used_Daily",
]

app = FastAPI(
    title="API · Adicción al celular en adolescentes",
    description="Clasifica si un/a adolescente tiene nivel de adicción alto "
                "a partir de seis hábitos en el uso del celular. "
                "Modelo: regresión logística (scikit-learn). Datos sintéticos de Kaggle.",
    version="1.0.0",
)


class Entrada(BaseModel):
    """Datos que manda el formulario. Si falta un campo o el tipo/rango es incorrecto: 422."""
    horas_uso_diario: float = Field(ge=0, le=24, description="Horas de uso del celular por día")
    horas_sueno: float = Field(ge=0, le=24, description="Horas de sueño")
    horas_redes: float = Field(ge=0, le=24, description="Horas en redes sociales por día")
    horas_juegos: float = Field(ge=0, le=24, description="Horas en juegos por día")
    chequeos_por_dia: int = Field(ge=0, le=1000, description="Veces que mira el celular por día")
    apps_por_dia: int = Field(ge=0, le=200, description="Cantidad de apps distintas que usa por día")

    @model_validator(mode="after")
    def horas_coherentes(self):
        if self.horas_uso_diario + self.horas_sueno > 24:
            raise ValueError("Las horas de uso y de sueño suman más de 24")
        if self.horas_redes + self.horas_juegos > self.horas_uso_diario:
            raise ValueError("Redes + juegos no puede superar el uso diario total")
        return self

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "horas_uso_diario": 5.5,
                "horas_sueno": 6.5,
                "horas_redes": 2.5,
                "horas_juegos": 1.5,
                "chequeos_por_dia": 90,
                "apps_por_dia": 13,
            }]
        }
    }


class Salida(BaseModel):
    adiccion_alta: bool
    probabilidad: float


@app.get("/health")
def health():
    return {"estado": "ok"}


@app.post("/predecir", response_model=Salida)
def predecir(entrada: Entrada):
    # Del JSON (nombres en castellano) a una fila con las columnas del entrenamiento
    fila = pd.DataFrame([[
        entrada.horas_uso_diario,
        entrada.horas_sueno,
        entrada.horas_redes,
        entrada.horas_juegos,
        entrada.chequeos_por_dia,
        entrada.apps_por_dia,
    ]], columns=COLUMNAS)

    try:
        clase = int(modelo.predict(fila)[0])
        probabilidad = float(modelo.predict_proba(fila)[0, 1])
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error al predecir: {error}")

    return {"adiccion_alta": clase == 1, "probabilidad": round(probabilidad, 3)}


# El frontend se monta al final: así /health, /predecir y /docs tienen prioridad
app.mount("/", StaticFiles(directory=CARPETA_FRONTEND, html=True), name="frontend")
