# Ciencia de Datos con Python - Semana 1

## Propósito
Preparar el ambiente de trabajo y comprender el valor de los datos para apoyar decisiones.

## Estructura
- api: API de emprendimiento con FastAPI
- data/raw: datos originales (no se modifican)
- data/processed: datos procesados
- notebooks: ejercicios y análisis
- outputs: reportes y archivos exportados
- docs: documentación
- scripts: código reutilizable

## Cómo reproducir

### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/verificar_ambiente.py
```
Si PowerShell bloquea la activación, ejecuta antes:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

### Linux / WSL / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/verificar_ambiente.py
```

### Abrir el notebook
```
jupyter notebook notebooks/semana_01_contexto_ambiente.ipynb
```
O abre la carpeta en VS Code y selecciona el kernel `.venv`.

## Datos de práctica (sintéticos)
```
python scripts/generar_datos_ejemplo.py
```
Crea `data/raw/seguimiento_academico.csv` con datos ficticios (sin personas reales).

## API de Emprendimiento SENA (FastAPI)

API con datos simulados en JSON y dos tablas relacionadas:
`emprendedores` (1) → `proyectos` (N), unidas por `emprendedor_id`.

### Ejecutar
Con el entorno virtual activo y las dependencias instaladas:
```
python -m uvicorn api.main:app --reload
```
- API: http://127.0.0.1:8000
- Documentación interactiva (Swagger): http://127.0.0.1:8000/docs

### Endpoints (GET)
| Ruta | Descripción |
|---|---|
| `/emprendedores` | Lista de emprendedores (`?regional=Antioquia`) |
| `/emprendedores/{id}` | Un emprendedor por id |
| `/emprendedores/{id}/proyectos` | Un emprendedor con todos sus proyectos |
| `/proyectos` | Lista de proyectos (`?estado=...&sector=...`) |
| `/proyectos/{id}` | Un proyecto por id, con los datos de su emprendedor |

Ejemplos: `/emprendedores/1`, `/proyectos/103`, `/emprendedores/2/proyectos`.
Si el id no existe, responde 404 con un mensaje.

## Buenas prácticas
1. No modificar directamente los datos originales.
2. Documentar cada decisión relevante.
3. Proteger datos personales.
4. Usar rutas relativas.
5. Mantener el notebook ordenado y comentado.