from academic import repository as repo
from academic.models import Subject


def normalize_codigo(codigo: str) -> str:
    """Los códigos de materia se guardan siempre en mayúsculas y sin espacios."""
    return codigo.strip().upper()


def list_subjects() -> list[Subject]:
    return repo.list_subjects()


def get_subject(subject_id: int) -> Subject:
    return repo.get_subject(subject_id)


def create_subject(nombre: str, codigo: str, creditos: int = None) -> Subject:
    if creditos is not None and creditos < 0:
        raise ValueError("Los créditos no pueden ser negativos")
    return repo.create_subject(
        nombre=nombre.strip(),
        codigo=normalize_codigo(codigo),
        creditos=creditos,
    )


def update_subject(subject_id: int, **fields) -> Subject:
    if fields.get("codigo"):
        fields["codigo"] = normalize_codigo(fields["codigo"])
    if fields.get("nombre"):
        fields["nombre"] = fields["nombre"].strip()
    if fields.get("creditos") is not None and fields["creditos"] < 0:
        raise ValueError("Los créditos no pueden ser negativos")
    return repo.update_subject(subject_id, **fields)


def delete_subject(subject_id: int) -> None:
    repo.delete_subject(subject_id)
