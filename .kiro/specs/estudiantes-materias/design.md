# Design — Estudiantes y Materias Asignadas

## Visión general

Backend en **Flask** con **PostgreSQL** vía **SQLAlchemy**, organizado en capas: `models` (entidades), `repository` (acceso a datos), `schemas` (serialización/validación con Marshmallow) y `routes` (API REST). Sigue el mismo patrón que el módulo `auth/` existente en el proyecto.

## Arquitectura

```
Cliente HTTP
    │
    ▼
routes.py        (Blueprint, valida entrada con schemas, maneja HTTP)
    │
    ▼
repository.py     (funciones CRUD puras contra la BD, sin lógica HTTP)
    │
    ▼
models.py         (entidades SQLAlchemy: Student, Subject, tabla intermedia)
    │
    ▼
PostgreSQL
```

## Modelo de datos

### `students`
| Campo   | Tipo         | Notas                    |
|---------|--------------|---------------------------|
| id      | INTEGER PK   | autoincremental            |
| nombre  | VARCHAR(120) | requerido                  |
| codigo  | VARCHAR(20)  | único, requerido           |
| curso   | VARCHAR(60)  | opcional                   |
| email   | VARCHAR(120) | opcional                   |

### `subjects`
| Campo    | Tipo         | Notas             |
|----------|--------------|--------------------|
| id       | INTEGER PK   | autoincremental     |
| nombre   | VARCHAR(120) | requerido           |
| codigo   | VARCHAR(20)  | único, requerido    |
| creditos | INTEGER      | opcional             |

### `student_subjects` (tabla intermedia, muchos a muchos)
| Campo         | Tipo       | Notas                                   |
|---------------|------------|------------------------------------------|
| student_id    | INTEGER FK | referencia a `students.id`, ON DELETE CASCADE |
| subject_id    | INTEGER FK | referencia a `subjects.id`, ON DELETE CASCADE |
| assigned_at   | TIMESTAMP  | default `now()`                          |

Clave primaria compuesta `(student_id, subject_id)` para impedir asignaciones duplicadas a nivel de base de datos.

## API REST

| Método | Ruta                                         | Descripción                          |
|--------|-----------------------------------------------|---------------------------------------|
| GET    | `/api/estudiantes`                           | Listar estudiantes                    |
| POST   | `/api/estudiantes`                           | Crear estudiante                      |
| GET    | `/api/estudiantes/<id>`                      | Obtener estudiante                    |
| PUT    | `/api/estudiantes/<id>`                      | Editar estudiante                     |
| DELETE | `/api/estudiantes/<id>`                      | Eliminar estudiante                   |
| GET    | `/api/materias`                              | Listar materias (con conteo inscritos)|
| POST   | `/api/materias`                              | Crear materia                         |
| PUT    | `/api/materias/<id>`                         | Editar materia                        |
| DELETE | `/api/materias/<id>`                         | Eliminar materia                      |
| GET    | `/api/estudiantes/<id>/materias`             | Listar materias asignadas             |
| POST   | `/api/estudiantes/<id>/materias`             | Asignar materia (body: `subject_id`)  |
| DELETE | `/api/estudiantes/<id>/materias/<subject_id>`| Quitar materia asignada               |

## Decisiones técnicas

- **Repository pattern**: separa consultas SQL/ORM de la lógica HTTP, igual que `auth/repository.py`, para facilitar pruebas unitarias sin levantar Flask.
- **Marshmallow schemas**: validan el payload de entrada y controlan qué campos se serializan en la respuesta.
- **Cascada en la BD**: la integridad referencial (borrar estudiante → borra sus asignaciones) se garantiza a nivel de PostgreSQL, no solo en la aplicación.
- **Flask-Migrate**: gestiona el versionado del esquema de la base de datos.
- **Configuración por entorno**: la cadena de conexión sale de `DATABASE_URL` (variable de entorno), nunca hardcodeada.

## Manejo de errores

Las rutas devuelven JSON consistente:
```json
{ "error": "mensaje descriptivo" }
```
con los códigos HTTP: `404` (no encontrado), `409` (conflicto/duplicado), `400` (validación fallida).
