from datetime import datetime

from db import db


student_subjects = db.Table(
    "student_subjects",
    db.Column(
        "student_id",
        db.Integer,
        db.ForeignKey("students.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "subject_id",
        db.Integer,
        db.ForeignKey("subjects.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column("assigned_at", db.DateTime, default=datetime.utcnow, nullable=False),
)


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False, index=True)
    curso = db.Column(db.String(60), nullable=True)
    email = db.Column(db.String(120), nullable=True)

    materias = db.relationship(
        "Subject",
        secondary=student_subjects,
        back_populates="estudiantes",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Student {self.codigo} {self.nombre}>"


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False, index=True)
    creditos = db.Column(db.Integer, nullable=True)

    estudiantes = db.relationship(
        "Student",
        secondary=student_subjects,
        back_populates="materias",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Subject {self.codigo} {self.nombre}>"
