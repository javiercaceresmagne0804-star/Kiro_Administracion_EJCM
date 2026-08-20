from marshmallow import Schema, fields, validate


class SubjectSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    codigo = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    creditos = fields.Int(required=False, allow_none=True)


class SubjectWithCountSchema(SubjectSchema):
    estudiantes_inscritos = fields.Method("get_enrolled_count")

    def get_enrolled_count(self, subject):
        return len(subject.estudiantes)


class StudentSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    codigo = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    curso = fields.Str(required=False, allow_none=True, validate=validate.Length(max=60))
    email = fields.Email(required=False, allow_none=True)
    materias = fields.Nested(SubjectSchema, many=True, dump_only=True)


class StudentUpdateSchema(Schema):
    """Igual que StudentSchema pero con todos los campos opcionales (PUT parcial)."""

    nombre = fields.Str(required=False, validate=validate.Length(min=1, max=120))
    codigo = fields.Str(required=False, validate=validate.Length(min=1, max=20))
    curso = fields.Str(required=False, allow_none=True, validate=validate.Length(max=60))
    email = fields.Email(required=False, allow_none=True)


class SubjectUpdateSchema(Schema):
    nombre = fields.Str(required=False, validate=validate.Length(min=1, max=120))
    codigo = fields.Str(required=False, validate=validate.Length(min=1, max=20))
    creditos = fields.Int(required=False, allow_none=True)


class AssignSubjectSchema(Schema):
    subject_id = fields.Int(required=True)


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
student_update_schema = StudentUpdateSchema()

subject_schema = SubjectSchema()
subjects_with_count_schema = SubjectWithCountSchema(many=True)
subject_update_schema = SubjectUpdateSchema()

assign_subject_schema = AssignSubjectSchema()
