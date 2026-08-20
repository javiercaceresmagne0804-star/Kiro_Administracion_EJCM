from academic import repository as repo
from academic.models import Student, Subject


def list_student_subjects(student_id: int) -> list[Subject]:
    return repo.list_student_subjects(student_id)


def assign_subject(student_id: int, subject_id: int) -> Student:

    return repo.assign_subject(student_id, subject_id)


def unassign_subject(student_id: int, subject_id: int) -> Student:
    return repo.unassign_subject(student_id, subject_id)
