"""Configuración de la aplicación.

Las credenciales de PostgreSQL nunca se hardcodean: siempre se leen de
variables de entorno (ver .env.example en la raíz del proyecto).
"""

import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/estudiantes_materias_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    JSON_SORT_KEYS = False
