"""Verifica versiones, librerías y estructura de carpetas del proyecto.

Ejecutar desde cualquier lugar:  python scripts/verificar_ambiente.py
"""
from pathlib import Path
import sys

try:
    import pandas as pd
    import numpy as np
    import faker
except ImportError as error:
    print("Falta instalar una librería:", error)
    print("Active el entorno virtual y ejecute: pip install -r requirements.txt")
    sys.exit(1)

print("Ambiente listo para iniciar Ciencia de Datos con Python")
print("Python:", sys.version.split()[0])
print("Pandas:", pd.__version__)
print("NumPy:", np.__version__)

# Raíz del proyecto = carpeta que contiene /scripts
BASE_DIR = Path(__file__).resolve().parent.parent
carpetas = ["data/raw", "data/processed", "notebooks", "outputs", "docs", "scripts"]

for carpeta in carpetas:
    ruta = BASE_DIR / carpeta
    ruta.mkdir(parents=True, exist_ok=True)
    print("Verificada:", ruta)