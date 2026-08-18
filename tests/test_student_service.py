"""Pruebas de la capa de negocio student_service."""

from academic import student_service


def test_create_student_normaliza_codigo_y_email(app):
    student = student_service.create_student(
        nombre="  Ana Rojas  ",
        codigo=" est-020 ",
        email=" ANA@Correo.com ",
    )
    assert student.nombre == "Ana Rojas"
    assert student.codigo == "EST-020"
    assert student.email == "ana@correo.com"


def test_update_student_normaliza_codigo(app, sample_student):
    updated = student_service.update_student(sample_student.id, codigo=" est-999 ")
    assert updated.codigo == "EST-999"
