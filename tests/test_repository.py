"""Pruebas unitarias de la capa repository (sin pasar por HTTP)."""

import pytest

from academic import repository as repo


def test_create_and_get_student(app):
    student = repo.create_student(nombre="Ana Rojas", codigo="EST-010")
    fetched = repo.get_student(student.id)
    assert fetched.codigo == "EST-010"


def test_create_student_codigo_duplicado(app, sample_student):
    with pytest.raises(repo.DuplicateCodeError):
        repo.create_student(nombre="Otro", codigo=sample_student.codigo)


def test_get_student_inexistente(app):
    with pytest.raises(repo.NotFoundError):
        repo.get_student(9999)


def test_delete_student_elimina_asignaciones(app, sample_student, sample_subject):
    repo.assign_subject(sample_student.id, sample_subject.id)
    repo.delete_student(sample_student.id)

    with pytest.raises(repo.NotFoundError):
        repo.get_student(sample_student.id)
    # La materia sigue existiendo en el catálogo
    assert repo.get_subject(sample_subject.id) is not None


def test_delete_subject_la_quita_de_estudiantes(app, sample_student, sample_subject):
    repo.assign_subject(sample_student.id, sample_subject.id)
    repo.delete_subject(sample_subject.id)

    student = repo.get_student(sample_student.id)
    assert student.materias == []


def test_assign_subject_es_idempotente(app, sample_student, sample_subject):
    repo.assign_subject(sample_student.id, sample_subject.id)
    repo.assign_subject(sample_student.id, sample_subject.id)

    student = repo.get_student(sample_student.id)
    assert len(student.materias) == 1


def test_unassign_subject(app, sample_student, sample_subject):
    repo.assign_subject(sample_student.id, sample_subject.id)
    repo.unassign_subject(sample_student.id, sample_subject.id)

    student = repo.get_student(sample_student.id)
    assert sample_subject not in student.materias
