"""Pruebas de la capa de negocio subject_service."""

import pytest

from academic import subject_service


def test_create_subject_normaliza_codigo(app):
    subject = subject_service.create_subject(nombre="  Química  ", codigo=" qui-100 ")
    assert subject.nombre == "Química"
    assert subject.codigo == "QUI-100"


def test_create_subject_creditos_negativos_falla(app):
    with pytest.raises(ValueError):
        subject_service.create_subject(nombre="Química", codigo="QUI-100", creditos=-2)


def test_update_subject_creditos_negativos_falla(app, sample_subject):
    with pytest.raises(ValueError):
        subject_service.update_subject(sample_subject.id, creditos=-1)
