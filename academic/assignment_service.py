"""Lógica de negocio para la asignación de materias a estudiantes."""

from academic import repository as repo
from academic.models import Student, Subject


def list_student_subjects(student_id: int) -> list[Subject]:
    return repo.list_student_subjects(student_id)


def assign_subject(student_id: int, subject_id: int) -> Student:
    """Asigna una materia a un estudiante.

    Es idempotente: si la materia ya estaba asignada, no crea duplicados
    (la comprobación real de duplicados vive en repository.assign_subject).
    """
    return repo.assign_subject(student_id, subject_id)


def unassign_subject(student_id: int, subject_id: int) -> Student:
    return repo.unassign_subject(student_id, subject_id)
