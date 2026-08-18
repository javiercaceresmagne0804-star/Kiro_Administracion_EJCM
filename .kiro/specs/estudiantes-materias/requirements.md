# Requirements — Estudiantes y Materias Asignadas

## Introducción

Este documento define los requisitos para un módulo backend que permite administrar un listado de estudiantes, un catálogo de materias, y la asignación de materias a cada estudiante, con persistencia en PostgreSQL.

## Requisito 1 — Gestión de estudiantes

**User Story:** Como administrador académico, quiero registrar, consultar, editar y eliminar estudiantes, para mantener actualizado el listado institucional.

**Acceptance Criteria (EARS)**

1. CUANDO el administrador envía un nombre y un código válidos, EL SISTEMA DEBERÁ crear un nuevo estudiante y devolver su identificador.
2. CUANDO el código de estudiante ya existe, EL SISTEMA DEBERÁ rechazar la creación con un error 409.
3. CUANDO se solicita el listado de estudiantes, EL SISTEMA DEBERÁ devolverlo ordenado por nombre, con paginación opcional.
4. CUANDO se solicita un estudiante por id inexistente, EL SISTEMA DEBERÁ devolver un error 404.
5. CUANDO se elimina un estudiante, EL SISTEMA DEBERÁ eliminar también sus asignaciones de materias (cascada).

## Requisito 2 — Catálogo de materias

**User Story:** Como administrador académico, quiero mantener un catálogo de materias con código y créditos, para poder asignarlas a los estudiantes.

**Acceptance Criteria (EARS)**

1. CUANDO se crea una materia con código duplicado, EL SISTEMA DEBERÁ rechazar la operación con un error 409.
2. CUANDO se elimina una materia, EL SISTEMA DEBERÁ quitarla automáticamente de todos los estudiantes que la tenían asignada.
3. CUANDO se solicita el listado de materias, EL SISTEMA DEBERÁ incluir el número de estudiantes inscritos en cada una.

## Requisito 3 — Asignación de materias a estudiantes

**User Story:** Como administrador académico, quiero asignar y quitar materias de un estudiante, para reflejar su carga académica actual.

**Acceptance Criteria (EARS)**

1. CUANDO se asigna una materia ya asignada al mismo estudiante, EL SISTEMA DEBERÁ ignorar la operación sin crear duplicados.
2. CUANDO se asigna una materia inexistente o a un estudiante inexistente, EL SISTEMA DEBERÁ devolver un error 404.
3. CUANDO se solicita la lista de materias de un estudiante, EL SISTEMA DEBERÁ devolver solo las materias vigentes asignadas a ese estudiante.
4. CUANDO se quita una materia de un estudiante, EL SISTEMA DEBERÁ eliminar únicamente esa asignación, sin afectar al catálogo de materias.

## Requisito 4 — Persistencia

**User Story:** Como equipo de desarrollo, quiero que los datos se almacenen en PostgreSQL a través de un ORM, para garantizar integridad referencial y facilitar migraciones.

**Acceptance Criteria (EARS)**

1. EL SISTEMA DEBERÁ usar PostgreSQL como motor de base de datos en todos los entornos (desarrollo, pruebas, producción).
2. EL SISTEMA DEBERÁ definir la relación estudiante-materia como una tabla intermedia (muchos a muchos) con clave foránea en cascada.
3. EL SISTEMA DEBERÁ exponer variables de entorno para la cadena de conexión, sin credenciales hardcodeadas en el código.
