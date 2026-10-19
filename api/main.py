"""API del Servicio de Emprendimiento SENA (datos simulados).

Dos tablas relacionadas (1 emprendedor -> N proyectos):
  - emprendedores  (data/raw/emprendedores.json)
  - proyectos      (data/raw/proyectos.json)  -> campo emprendedor_id

Ejecutar desde la raíz del proyecto:
    python -m uvicorn api.main:app --reload
Documentación interactiva: http://127.0.0.1:8000/docs
"""
import json
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"


def cargar_json(nombre_archivo: str) -> list:
    """Lee un archivo JSON de data/raw y devuelve su contenido."""
    ruta = DATA_DIR / nombre_archivo
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


# "Tablas" simuladas, cargadas en memoria al iniciar la API
EMPRENDEDORES = cargar_json("emprendedores.json")
PROYECTOS = cargar_json("proyectos.json")


# ---------- Modelos (esquemas de respuesta) ----------
class Emprendedor(BaseModel):
    id: int
    nombre: str
    programa: str
    regional: str
    correo: str
    fecha_registro: str


class Proyecto(BaseModel):
    id: int
    emprendedor_id: int
    nombre_proyecto: str
    sector: str
    modalidad: str
    estado: str
    presupuesto_cop: int
    empleos_proyectados: int


class ProyectoConEmprendedor(Proyecto):
    emprendedor: Emprendedor


class EmprendedorConProyectos(Emprendedor):
    total_proyectos: int
    proyectos: List[Proyecto]


# ---------- Aplicación ----------
app = FastAPI(
    title="API Servicio de Emprendimiento SENA",
    description="Datos simulados: emprendedores y sus proyectos de emprendimiento.",
    version="1.0.0",
)


def buscar_emprendedor(emprendedor_id: int) -> dict:
    for e in EMPRENDEDORES:
        if e["id"] == emprendedor_id:
            return e
    raise HTTPException(status_code=404, detail=f"No existe el emprendedor con id {emprendedor_id}")


@app.get("/")
def inicio():
    return {
        "servicio": "Emprendimiento SENA",
        "documentacion": "/docs",
        "endpoints": [
            "/emprendedores",
            "/emprendedores/{id}",
            "/emprendedores/{id}/proyectos",
            "/proyectos",
            "/proyectos/{id}",
        ],
    }


# ----- Tabla 1: emprendedores -----
@app.get("/emprendedores", response_model=List[Emprendedor])
def listar_emprendedores(regional: Optional[str] = Query(None, description="Filtrar por regional")):
    """Lista todos los emprendedores (opcional: filtrar por regional)."""
    if regional:
        return [e for e in EMPRENDEDORES if e["regional"].lower() == regional.lower()]
    return EMPRENDEDORES


@app.get("/emprendedores/{emprendedor_id}", response_model=Emprendedor)
def obtener_emprendedor(emprendedor_id: int):
    """Consulta UN emprendedor por su id."""
    return buscar_emprendedor(emprendedor_id)


@app.get("/emprendedores/{emprendedor_id}/proyectos", response_model=EmprendedorConProyectos)
def proyectos_del_emprendedor(emprendedor_id: int):
    """Consulta un emprendedor junto con todos sus proyectos (relación 1 a N)."""
    emprendedor = buscar_emprendedor(emprendedor_id)
    sus_proyectos = [p for p in PROYECTOS if p["emprendedor_id"] == emprendedor_id]
    return {**emprendedor, "total_proyectos": len(sus_proyectos), "proyectos": sus_proyectos}


# ----- Tabla 2: proyectos -----
@app.get("/proyectos", response_model=List[Proyecto])
def listar_proyectos(
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    sector: Optional[str] = Query(None, description="Filtrar por sector"),
):
    """Lista todos los proyectos (opcional: filtrar por estado y/o sector)."""
    resultado = PROYECTOS
    if estado:
        resultado = [p for p in resultado if p["estado"].lower() == estado.lower()]
    if sector:
        resultado = [p for p in resultado if p["sector"].lower() == sector.lower()]
    return resultado


@app.get("/proyectos/{proyecto_id}", response_model=ProyectoConEmprendedor)
def obtener_proyecto(proyecto_id: int):
    """Consulta UN proyecto por su id, incluyendo los datos de su emprendedor."""
    for p in PROYECTOS:
        if p["id"] == proyecto_id:
            return {**p, "emprendedor": buscar_emprendedor(p["emprendedor_id"])}
    raise HTTPException(status_code=404, detail=f"No existe el proyecto con id {proyecto_id}")