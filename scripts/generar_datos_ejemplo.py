"""Genera un CSV SINTÉTICO para el caso de seguimiento académico.

No contiene personas reales: los códigos son ficticios.
"""
from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
rng = np.random.default_rng(42)  # semilla fija = resultados reproducibles

n = 60
df = pd.DataFrame({
    "id_aprendiz": [f"APR{i:03d}" for i in range(1, n + 1)],
    "ficha": rng.choice(["2900001", "2900002", "2900003"], n),
    "asistencia_porcentaje": rng.uniform(55, 100, n).round(1),
    "promedio_actividades": rng.uniform(2.0, 5.0, n).round(1),
    "evidencias_entregadas": rng.integers(0, 11, n),
    "observacion": "",
})

salida = BASE_DIR / "data" / "raw" / "seguimiento_academico.csv"
salida.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(salida, index=False)
print("Archivo creado:", salida)
print(df.head())