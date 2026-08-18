"""Pruebas de integración: ejercitan la API completa vía el test_client de Flask."""

import json


def post_json(client, url, data):
    return client.post(url, data=json.dumps(data), content_type="application/json")


def put_json(client, url, data):
    return client.put(url, data=json.dumps(data), content_type="application/json")


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_crear_y_listar_estudiante(client):
    resp = post_json(client, "/api/estudiantes", {"nombre": "Ana Rojas", "codigo": "EST-030"})
    assert resp.status_code == 201
    student_id = resp.get_json()["id"]

    resp = client.get("/api/estudiantes")
    assert resp.status_code == 200
    codigos = [s["codigo"] for s in resp.get_json()]
    assert "EST-030" in codigos

    resp = client.get(f"/api/estudiantes/{student_id}")
    assert resp.status_code == 200


def test_crear_estudiante_codigo_duplicado(client):
    post_json(client, "/api/estudiantes", {"nombre": "Ana", "codigo": "EST-040"})
    resp = post_json(client, "/api/estudiantes", {"nombre": "Otra Ana", "codigo": "EST-040"})
    assert resp.status_code == 409


def test_estudiante_no_encontrado(client):
    resp = client.get("/api/estudiantes/99999")
    assert resp.status_code == 404


def test_crear_materia_y_asignar_a_estudiante(client):
    student_resp = post_json(client, "/api/estudiantes", {"nombre": "Jorge Q.", "codigo": "EST-050"})
    student_id = student_resp.get_json()["id"]

    subject_resp = post_json(client, "/api/materias", {"nombre": "Física", "codigo": "FIS-200", "creditos": 4})
    subject_id = subject_resp.get_json()["id"]

    assign_resp = post_json(client, f"/api/estudiantes/{student_id}/materias", {"subject_id": subject_id})
    assert assign_resp.status_code == 201

    resp = client.get(f"/api/estudiantes/{student_id}/materias")
    codigos = [m["codigo"] for m in resp.get_json()]
    assert "FIS-200" in codigos


def test_quitar_materia_asignada(client):
    student_resp = post_json(client, "/api/estudiantes", {"nombre": "Luis P.", "codigo": "EST-060"})
    student_id = student_resp.get_json()["id"]
    subject_resp = post_json(client, "/api/materias", {"nombre": "Química", "codigo": "QUI-300"})
    subject_id = subject_resp.get_json()["id"]

    post_json(client, f"/api/estudiantes/{student_id}/materias", {"subject_id": subject_id})
    resp = client.delete(f"/api/estudiantes/{student_id}/materias/{subject_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/estudiantes/{student_id}/materias")
    assert resp.get_json() == []


def test_eliminar_estudiante_borra_asignaciones(client):
    student_resp = post_json(client, "/api/estudiantes", {"nombre": "Carla M.", "codigo": "EST-070"})
    student_id = student_resp.get_json()["id"]

    resp = client.delete(f"/api/estudiantes/{student_id}")
    assert resp.status_code == 204

    resp = client.get(f"/api/estudiantes/{student_id}")
    assert resp.status_code == 404


def test_listar_materias_incluye_conteo_inscritos(client):
    student_resp = post_json(client, "/api/estudiantes", {"nombre": "Diego T.", "codigo": "EST-080"})
    student_id = student_resp.get_json()["id"]
    subject_resp = post_json(client, "/api/materias", {"nombre": "Álgebra", "codigo": "MAT-200"})
    subject_id = subject_resp.get_json()["id"]

    post_json(client, f"/api/estudiantes/{student_id}/materias", {"subject_id": subject_id})

    resp = client.get("/api/materias")
    materia = next(m for m in resp.get_json() if m["codigo"] == "MAT-200")
    assert materia["estudiantes_inscritos"] == 1
