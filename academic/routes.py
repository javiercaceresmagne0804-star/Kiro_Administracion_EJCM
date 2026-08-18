"""API REST: estudiantes, materias y asignaciones.

Las rutas validan la entrada con los schemas de Marshmallow, delegan la
lógica de negocio a la capa de servicios (student_service, subject_service,
assignment_service), y traducen las excepciones del dominio a respuestas
HTTP con el código adecuado. El repository no se llama directamente desde
aquí, igual que en el módulo auth de referencia.
"""

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from academic import repository as repo
from academic import student_service, subject_service, assignment_service
from academic.schemas import (
    assign_subject_schema,
    student_schema,
    students_schema,
    student_update_schema,
    subject_schema,
    subjects_with_count_schema,
    subject_update_schema,
)

academic_bp = Blueprint("academic", __name__, url_prefix="/api")


def _validation_error_response(err: ValidationError):
    return jsonify(error="Datos inválidos", detalles=err.messages), 400


# --------------------------------------------------------------------------
# Estudiantes
# --------------------------------------------------------------------------

@academic_bp.get("/estudiantes")
def get_students():
    search = request.args.get("q")
    students = student_service.list_students(search=search)
    return jsonify(students_schema.dump(students))


@academic_bp.post("/estudiantes")
def post_student():
    try:
        data = student_schema.load(request.get_json(force=True))
    except ValidationError as err:
        return _validation_error_response(err)

    try:
        student = student_service.create_student(**data)
    except repo.DuplicateCodeError as err:
        return jsonify(error=str(err)), 409

    return jsonify(student_schema.dump(student)), 201


@academic_bp.get("/estudiantes/<int:student_id>")
def get_student(student_id: int):
    try:
        student = student_service.get_student(student_id)
    except repo.NotFoundError as err:
        return jsonify(error=str(err)), 404
    return jsonify(student_schema.dump(student))


@academic_bp.put("/estudiantes/<int:student_id>")
def put_student(student_id: int):
    try:
        data = student_update_schema.load(request.get_json(force=True))
    except ValidationError as err:
        return _validation_error_response(err)

    try:
        student = student_service.update_student(student_id, **data)
    except repo.NotFoundError as err:
        return jsonify(error=str(err)), 404
    except repo.DuplicateCodeError as err:
        return jsonify(error=str(err)), 409

    return jsonify(student_schema.dump(student))


@academic_bp.delete("/estudiantes/<int:student_id>")
def delete_student(student_id: int):
    try:
        student_service.delete_student(student_id)
    except repo.NotFoundError as err:
        return jsonify(error=str(err)), 404
    return "", 204


# --------------------------------------------------------------------------
# Materias
# --------------------------------------------------------------------------

@academic_bp.get("/materias")
def get_subjects():
    subjects = subject_service.list_subjects()
    return jsonify(subjects_with_count_schema.dump(subjects))


@academic_bp.post("/materias")
def post_subject():
    try:
        data = subject_schema.load(request.get_json(force=True))
    except ValidationError as err:
        return _validation_error_response(err)

    try:
        subject = subject_service.create_subject(**data)
    except repo.DuplicateCodeError as err:
        return jsonify(error=str(err)), 409
    except ValueError as err:
        return jsonify(error=str(err)), 400

    return jsonify(subject_schema.dump(subject)), 201


@academic_bp.put("/materias/<int:subject_id>")
def put_subject(subject_id: int):
    try:
        data = subject_update_schema.load(request.get_json(force=True))
    except ValidationError as err:
        return _validation_error_response(err)

    try:
        subject = subject_service.update_subject(subject_id, **data)
    except repo.NotFoundError as err:
        return jsonify(error=str(err)), 404
    except repo.DuplicateCodeError as err:
        return jsonify(error=str(err)), 409
    except ValueError as err:
        return jsonify(error=str(err)), 400

    return jsonify(subject_schema.dump(subject))


@academic_bp.delete("/materias/<int:subject_id>")
def delete_subject(subject_id: int):
    try:
        subject_service.delete_subject(subject_id)
    except repo.NotFoundError as err:
        return jsonify(error=str(err)), 404
    return "", 204


# --------------------------------------------------------------------------
# Asignaciones
# --------------------------------------------------------------------------

@academic_bp.get("/estudiantes/<int:student_id>/materias")
def get_student_subjects(student_id: int):
    try:
        subjects = assignment_service.list_student_subjects(student_id)
    except repo.NotFoundError as err:
        return jsonify(error=str(err)), 404
    return jsonify(subject_schema.dump(subjects, many=True))


@academic_bp.post("/estudiantes/<int:student_id>/materias")
def post_student_subject(student_id: int):
    try:
        data = assign_subject_schema.load(request.get_json(force=True))
    except ValidationError as err:
        return _validation_error_response(err)

    try:
        student = assignment_service.assign_subject(student_id, data["subject_id"])
    except repo.NotFoundError as err:
        return jsonify(error=str(err)), 404

    return jsonify(student_schema.dump(student)), 201


@academic_bp.delete("/estudiantes/<int:student_id>/materias/<int:subject_id>")
def delete_student_subject(student_id: int, subject_id: int):
    try:
        assignment_service.unassign_subject(student_id, subject_id)
    except repo.NotFoundError as err:
        return jsonify(error=str(err)), 404
    return "", 204
