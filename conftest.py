import pytest

from app import create_app
from db import db as _db


class TestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test-secret-key"
    TESTING = True


@pytest.fixture()
def app():
    flask_app = create_app()
    flask_app.config.from_object(TestConfig)

    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db(app):
    return _db


@pytest.fixture()
def sample_subject(db):
    from academic.models import Subject

    subject = Subject(nombre="Programación I", codigo="INF-110", creditos=5)
    db.session.add(subject)
    db.session.commit()
    return subject


@pytest.fixture()
def sample_student(db):
    from academic.models import Student

    student = Student(
        nombre="María Fernández",
        codigo="EST-001",
        curso="4º Semestre",
        email="maria@correo.com",
    )
    db.session.add(student)
    db.session.commit()
    return student
