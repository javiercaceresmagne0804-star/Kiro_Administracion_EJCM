"""Lógica de negocio para estudiantes.

Actúa como intermediario entre las rutas (HTTP) y el repository (datos).
Aquí viven las reglas que no son puramente de acceso a datos ni de
transporte HTTP: normalización de campos, validaciones cruzadas, etc.
"""

from academic import repository as repo
from academic.models import Student


def normalize_codigo(codigo: str) -> str:
    """Los códigos de estudiante se guardan siempre en mayúsculas y sin espacios."""
    return codigo.strip().upper()


def list_students(search: str = None) -> list[Student]:
    return repo.list_students(search=search)


def get_student(student_id: int) -> Student:
    return repo.get_student(student_id)


def create_student(nombre: str, codigo: str, curso: str = None, email: str = None) -> Student:
    return repo.create_student(
        nombre=nombre.strip(),
        codigo=normalize_codigo(codigo),
        curso=curso.strip() if curso else curso,
        email=email.strip().lower() if email else email,
    )


def update_student(student_id: int, **fields) -> Student:
    if fields.get("codigo"):
        fields["codigo"] = normalize_codigo(fields["codigo"])
    if fields.get("email"):
        fields["email"] = fields["email"].strip().lower()
    if fields.get("nombre"):
        fields["nombre"] = fields["nombre"].strip()
    return repo.update_student(student_id, **fields)


def delete_student(student_id: int) -> None:
    repo.delete_student(student_id)
