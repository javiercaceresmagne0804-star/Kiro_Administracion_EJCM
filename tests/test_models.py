"""Pruebas unitarias de los modelos SQLAlchemy."""

from academic.models import Student, Subject


def test_crear_estudiante(db):
    student = Student(nombre="Jorge Quispe", codigo="EST-002", curso="2º Semestre")
    db.session.add(student)
    db.session.commit()

    assert student.id is not None
    assert student.materias == []


def test_crear_materia(db):
    subject = Subject(nombre="Historia Universal", codigo="HIS-201", creditos=3)
    db.session.add(subject)
    db.session.commit()

    assert subject.id is not None
    assert subject.estudiantes == []


def test_relacion_muchos_a_muchos(db, sample_student, sample_subject):
    sample_student.materias.append(sample_subject)
    db.session.commit()

    assert sample_subject in sample_student.materias
    assert sample_student in sample_subject.estudiantes


def test_codigo_estudiante_es_unico(db, sample_student):
    duplicado = Student(nombre="Otro Nombre", codigo=sample_student.codigo)
    db.session.add(duplicado)

    import pytest
    from sqlalchemy.exc import IntegrityError

    with pytest.raises(IntegrityError):
        db.session.commit()
