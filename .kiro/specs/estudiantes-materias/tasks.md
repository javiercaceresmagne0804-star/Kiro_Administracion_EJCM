# Tasks — Estudiantes y Materias Asignadas

- [x] 1. Configurar proyecto base
  - [x] 1.1 Crear estructura de carpetas (`academic/`, `instance/`)
  - [x] 1.2 Configurar conexión a PostgreSQL vía `DATABASE_URL`
  - [x] 1.3 Configurar Flask-SQLAlchemy y Flask-Migrate en `db.py` / `extensions.py`

- [x] 2. Modelos de datos (`academic/models.py`)
  - [x] 2.1 Modelo `Student`
  - [x] 2.2 Modelo `Subject`
  - [x] 2.3 Tabla intermedia `student_subjects` con `ON DELETE CASCADE`
  - _Requisitos: 4.2_

- [x] 3. Capa de acceso a datos (`academic/repository.py`)
  - [x] 3.1 CRUD de estudiantes
  - [x] 3.2 CRUD de materias
  - [x] 3.3 Asignar / quitar materia de un estudiante
  - [x] 3.4 Consultar materias asignadas a un estudiante
  - _Requisitos: 1, 2, 3_

- [x] 4. Schemas de validación/serialización (`academic/schemas.py`)
  - [x] 4.1 `StudentSchema`
  - [x] 4.2 `SubjectSchema`
  - _Requisitos: 1.1, 2.1_

- [x] 5. Rutas de la API (`academic/routes.py`)
  - [x] 5.1 Endpoints de estudiantes (listar, crear, obtener, editar, eliminar)
  - [x] 5.2 Endpoints de materias (listar, crear, editar, eliminar)
  - [x] 5.3 Endpoints de asignación (asignar, quitar, listar asignadas)
  - _Requisitos: 1, 2, 3_

- [x] 6. Capa de servicios (`academic/*_service.py`)
  - [x] 6.1 `student_service.py` — normalización de nombre/código/email
  - [x] 6.2 `subject_service.py` — normalización de código, validación de créditos
  - [x] 6.3 `assignment_service.py` — asignar/quitar materias
  - [x] 6.4 Rutas actualizadas para llamar a los servicios en vez del repository directamente
  - _Requisitos: 1, 2, 3_

- [x] 7. Pruebas
  - [x] 7.1 `conftest.py` con fixtures (app, client, db, sample_student, sample_subject) sobre SQLite en memoria
  - [x] 7.2 Pruebas unitarias de modelos (`tests/test_models.py`)
  - [x] 7.3 Pruebas unitarias del repository (`tests/test_repository.py`)
  - [x] 7.4 Pruebas unitarias de schemas (`tests/test_schemas.py`)
  - [x] 7.5 Pruebas unitarias de servicios (`tests/test_student_service.py`, `tests/test_subject_service.py`, `tests/test_assignment_service.py`)
  - [x] 7.6 Pruebas de integración de endpoints (`tests/test_routes_integration.py`)
  - _Requisitos: 1, 2, 3_

- [ ] 8. Migraciones de base de datos (pendiente, requiere PostgreSQL real)
  - [ ] 8.1 Ejecutar `flask db init`
  - [ ] 8.2 Generar migración inicial con `flask db migrate`
  - [ ] 8.3 Aplicar con `flask db upgrade`
  - _Requisitos: 4_
