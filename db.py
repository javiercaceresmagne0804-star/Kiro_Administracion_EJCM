"""Instancia única de SQLAlchemy, compartida por todos los módulos.

Se define aquí (y no dentro de app.py) para evitar importaciones circulares:
los modelos importan `db` desde este archivo, y `app.py` inicializa esta
misma instancia contra la aplicación Flask.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
