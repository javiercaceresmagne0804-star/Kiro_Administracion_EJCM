from academic import repository as repo
from academic.models import Student
from academic.password_hasher import hash_password
from academic.student_service import normalize_codigo


class RegistrationError(Exception):
    


def register_student(
    nombre: str,
    codigo: str,
    email: str,
    password: str,
    curso: str = None,
) -> Student:
    
    if not nombre or not nombre.strip():
        raise RegistrationError("El nombre es obligatorio")
    if not codigo or not codigo.strip():
        raise RegistrationError("El código es obligatorio")
    if not email or not email.strip():
        raise RegistrationError("El email es obligatorio")
    if not password or not password.strip():
        raise RegistrationError("La contraseña es obligatoria")

    # Normalización
    nombre_norm = nombre.strip()
    codigo_norm = normalize_codigo(codigo)
    email_norm = email.strip().lower()
    curso_norm = curso.strip() if curso else None
    password_hash = hash_password(password)

    # Creación en base de datos
    try:
        student = repo.create_student(
            nombre=nombre_norm,
            codigo=codigo_norm,
            curso=curso_norm,
            email=email_norm,
        )
    except repo.DuplicateCodeError as exc:
        raise RegistrationError(str(exc)) from exc

    return student
kjk
