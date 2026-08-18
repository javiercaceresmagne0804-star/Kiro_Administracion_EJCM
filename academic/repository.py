"""Capa de acceso a datos.

Contiene únicamente operaciones contra la base de datos (SQLAlchemy),
sin conocer nada de HTTP/Flask. Esto permite probarla de forma aislada
y reutilizarla desde otros contextos (CLI, tareas en background, etc).
"""

from typing import Optional

from sqlalchemy.exc import IntegrityError

from db import db
from academic.models import Student, Subject


class DuplicateCodeError(Exception):
    """Se lanza cuando ya existe un estudiante/materia con ese código."""


class NotFoundError(Exception):
    """Se lanza cuando no se encuentra el recurso solicitado."""


# --------------------------------------------------------------------------
# Estudiantes
# --------------------------------------------------------------------------

def list_students(search: Optional[str] = None) -> list[Student]:
    query = Student.query
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(Student.nombre.ilike(like), Student.codigo.ilike(like))
        )
    return query.order_by(Student.nombre.asc()).all()


def get_student(student_id: int) -> Student:
    student = Student.query.get(student_id)
    if student is None:
        raise NotFoundError(f"Estudiante {student_id} no encontrado")
    return student


def create_student(nombre: str, codigo: str, curso: str = None, email: str = None) -> Student:
    student = Student(nombre=nombre, codigo=codigo, curso=curso, email=email)
    db.session.add(student)
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise DuplicateCodeError(f"Ya existe un estudiante con código {codigo}") from exc
    return student


def update_student(student_id: int, **fields) -> Student:
    student = get_student(student_id)
    for key, value in fields.items():
        if value is not None and hasattr(student, key):
            setattr(student, key, value)
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise DuplicateCodeError("El código ya está en uso por otro estudiante") from exc
    return student


def delete_student(student_id: int) -> None:
    student = get_student(student_id)
    db.session.delete(student)  # cascada elimina sus asignaciones
    db.session.commit()


# --------------------------------------------------------------------------
# Materias
# --------------------------------------------------------------------------

def list_subjects() -> list[Subject]:
    return Subject.query.order_by(Subject.nombre.asc()).all()


def get_subject(subject_id: int) -> Subject:
    subject = Subject.query.get(subject_id)
    if subject is None:
        raise NotFoundError(f"Materia {subject_id} no encontrada")
    return subject


def create_subject(nombre: str, codigo: str, creditos: int = None) -> Subject:
    subject = Subject(nombre=nombre, codigo=codigo, creditos=creditos)
    db.session.add(subject)
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise DuplicateCodeError(f"Ya existe una materia con código {codigo}") from exc
    return subject


def update_subject(subject_id: int, **fields) -> Subject:
    subject = get_subject(subject_id)
    for key, value in fields.items():
        if value is not None and hasattr(subject, key):
            setattr(subject, key, value)
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise DuplicateCodeError("El código ya está en uso por otra materia") from exc
    return subject


def delete_subject(subject_id: int) -> None:
    subject = get_subject(subject_id)
    db.session.delete(subject)  # cascada la quita de todos los estudiantes
    db.session.commit()


# --------------------------------------------------------------------------
# Asignaciones (estudiante <-> materia)
# --------------------------------------------------------------------------

def list_student_subjects(student_id: int) -> list[Subject]:
    student = get_student(student_id)
    return student.materias


def assign_subject(student_id: int, subject_id: int) -> Student:
    student = get_student(student_id)
    subject = get_subject(subject_id)
    if subject not in student.materias:
        student.materias.append(subject)
        db.session.commit()
    return student


def unassign_subject(student_id: int, subject_id: int) -> Student:
    student = get_student(student_id)
    subject = get_subject(subject_id)
    if subject in student.materias:
        student.materias.remove(subject)
        db.session.commit()
    return student
