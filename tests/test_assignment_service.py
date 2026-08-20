from academic import assignment_service


def test_assign_and_list(app, sample_student, sample_subject):
    assignment_service.assign_subject(sample_student.id, sample_subject.id)
    materias = assignment_service.list_student_subjects(sample_student.id)
    assert sample_subject in materias


def test_unassign(app, sample_student, sample_subject):
    assignment_service.assign_subject(sample_student.id, sample_subject.id)
    assignment_service.unassign_subject(sample_student.id, sample_subject.id)
    materias = assignment_service.list_student_subjects(sample_student.id)
    assert sample_subject not in materias
