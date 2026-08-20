import pytest
from marshmallow import ValidationError

from academic.schemas import student_schema, subject_schema


def test_student_schema_valido():
    data = student_schema.load({"nombre": "Ana Rojas", "codigo": "EST-010"})
    assert data["nombre"] == "Ana Rojas"
    assert data["codigo"] == "EST-010"


def test_student_schema_falla_sin_nombre():
    with pytest.raises(ValidationError):
        student_schema.load({"codigo": "EST-010"})


def test_student_schema_email_invalido():
    with pytest.raises(ValidationError):
        student_schema.load({"nombre": "Ana", "codigo": "EST-010", "email": "no-es-email"})


def test_subject_schema_valido():
    data = subject_schema.load({"nombre": "Física", "codigo": "FIS-150", "creditos": 4})
    assert data["creditos"] == 4


def test_subject_schema_falla_sin_codigo():
    with pytest.raises(ValidationError):
        subject_schema.load({"nombre": "Física"})
