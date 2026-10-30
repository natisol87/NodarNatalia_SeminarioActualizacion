# Clase 10 · El camino del entrenamiento

Seminario de Actualización · Tecnicatura Superior en Ciencia de Datos e IA · IFTS N.º 18 · 2026

## De qué trata

Del dataset al modelo exportado: entrenar una regresión lineal que predice el precio de una casa (m², balcón, ascensor) y ver qué hace `fit` por dentro.

1. **El problema**: estimar a ojo los pesos mirando los datos.
2. **Una vuelta a mano**: predicción, pérdida, gradiente y corrección, con los números a la vista.
3. **scikit-learn**: `LinearRegression` (fórmula de una vez) y `SGDRegressor` (corrigiendo de a poco), y por qué hay que escalar las x con `StandardScaler`.
4. **PyTorch**: el ciclo de entrenamiento escrito a mano, y qué pasa con una tasa de aprendizaje demasiado grande.
5. **Keras**: el mismo ciclo adentro de `fit`.
6. **Evaluación** con datos de test (RMSE y R²).
7. **Qué es un modelo**: transformación + fórmula con sus parámetros (`Pipeline`).
8. **Exportar**: joblib, `state_dict` y `.keras`, y por qué el scaler tiene que viajar con el modelo.

## Contenido de la carpeta

| Archivo | Qué es |
|---|---|
| `Clase_10_Notebook_Camino_Entrenamiento.ipynb` | Notebook ejecutado, con mis predicciones y la Actividad |
| `requirements.txt` | Librerías necesarias para correrlo localmente |

## Actividad: formato `.weights.h5` (Keras)

Exporté el modelo de Keras con `save_weights` y respondí qué guarda el archivo, qué hace falta para cargarlo, si es seguro abrirlo y para qué caso lo usaría. Las respuestas están al final del notebook.

## Cómo correrlo localmente

```bash
pip install -r requirements.txt
```

Keras se usa con PyTorch como backend: el notebook define `KERAS_BACKEND=torch` antes de importar `keras`, así no hace falta instalar TensorFlow.

La carpeta `modelos_exportados/` se genera al ejecutar el notebook y no se sube al repositorio.
