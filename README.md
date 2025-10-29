# Task Management API - Examen de Arquitectura de Software

**Estudiante:** Nicolás
**Fecha:** 2025-10-29  
**Tecnologías:** Python 3.11, FastAPI, Docker

## Descripción

API REST para gestión de tareas que demuestra la aplicación de patrones de diseño y principios SOLID. La aplicación está construida con una arquitectura limpia en capas, siguiendo las mejores prácticas de desarrollo de software.

## Arquitectura y Diseño

### Estructura del Proyecto

```
ParcialArquitectura2/
│
├── app/
│   ├── domain/                    # Capa de Dominio
│   │   ├── __init__.py
│   │   └── task.py               # Entidad Task + TaskFactory
│   │
│   ├── application/              # Capa de Aplicación
│   │   ├── ports/               # Interfaces (abstracciones)
│   │   │   ├── __init__.py
│   │   │   └── task_repository.py
│   │   └── services/            # Casos de uso
│   │       ├── __init__.py
│   │       └── task_service.py
│   │
│   └── adapters/                # Capa de Adaptadores
│       ├── http/                # Adaptador HTTP (FastAPI)
│       │   ├── __init__.py
│       │   └── fastapi_app.py
│       └── persistence/         # Adaptador de persistencia
│           ├── __init__.py
│           └── memory_task_repository.py
│
├── Dockerfile
├── requirements.txt
└── README.md
```

### Patrones de Diseño Implementados

#### 1. **Repository Pattern**

- **Ubicación:** `app/application/ports/task_repository.py` (interfaz) y `app/adapters/persistence/memory_task_repository.py` (implementación)
- **Propósito:** Abstrae el acceso a datos, permitiendo cambiar fácilmente la implementación de persistencia (ej: de memoria a base de datos) sin afectar la lógica de negocio
- **Beneficio:** Desacoplamiento entre la lógica de negocio y el almacenamiento de datos

#### 2. **Factory Pattern**

- **Ubicación:** `app/domain/task.py` (`TaskFactory`)
- **Propósito:** Centraliza la lógica de creación de objetos `Task` con validaciones
- **Beneficio:** Garantiza que todas las tareas creadas sean válidas y consistentes

#### 3. **Dependency Injection**

- **Ubicación:** `app/application/services/task_service.py` (constructor recibe `TaskRepository`)
- **Propósito:** El servicio depende de abstracciones, no de implementaciones concretas
- **Beneficio:** Mayor testabilidad y flexibilidad

### Principios SOLID Aplicados

#### **S - Single Responsibility Principle (SRP)**

- **`Task`**: Representa únicamente una tarea del dominio
- **`TaskFactory`**: Responsable solo de crear tareas válidas
- **`TaskService`**: Coordina únicamente los casos de uso de tareas
- **`TaskRepository`**: Gestiona solo la persistencia de tareas
- **DTOs en FastAPI**: Separan las preocupaciones de HTTP del dominio

#### **O - Open/Closed Principle (OCP)**

- El sistema está abierto a extensión (nuevos repositorios, nuevos casos de uso) pero cerrado a modificación
- Ejemplo: Se puede agregar `get_tasks_by_status()` sin modificar el código existente
- Se puede cambiar de persistencia en memoria a SQLite sin modificar la lógica de negocio

#### **L - Liskov Substitution Principle (LSP)**

- Cualquier implementación de `TaskRepository` puede sustituirse sin afectar el comportamiento
- `MemoryTaskRepository` puede ser reemplazado por `SQLiteTaskRepository` sin cambios en `TaskService`

#### **I - Interface Segregation Principle (ISP)**

- `TaskRepository` define solo los métodos necesarios para la gestión de tareas
- No se fuerza a implementar métodos innecesarios

#### **D - Dependency Inversion Principle (DIP)**

- **Alto nivel:** `TaskService` depende de la abstracción `TaskRepository`
- **Bajo nivel:** `MemoryTaskRepository` implementa `TaskRepository`
- Las capas superiores no dependen de las inferiores, sino de abstracciones

## Funcionalidades

### Endpoints Implementados

#### **Mínimo requerido:**

- `GET /health` - Verificar estado del servicio
- `GET /tasks` - Listar todas las tareas (con filtro opcional por status)
- `POST /tasks` - Crear nueva tarea

#### **Endpoints adicionales (mejoras):**

- `GET /tasks/{id}` - Obtener tarea específica por ID
- `PUT /tasks/{id}` - Actualizar tarea existente
- `DELETE /tasks/{id}` - Eliminar tarea por ID
- `GET /` - Información de la API

### Validaciones

- `title` obligatorio y no vacío
- `status` debe ser `"pending"` o `"done"`
- Respuestas 400 para datos inválidos
- Respuestas 404 para recursos no encontrados
- Validaciones con Pydantic en la capa HTTP

## Docker

### Build de la Imagen

```bash
docker build -t task-api .
```

### Ejecutar el Contenedor

```bash
docker run -d -p 8000:8000 --name task-api task-api
```

O en primer plano para ver logs:

```bash
docker run -p 8000:8000 --name task-api task-api
```

### Detener y Eliminar

```bash
docker stop task-api
docker rm task-api
```

## Uso de la API

### 1. Health Check

```bash
curl http://localhost:8000/health
```

**Respuesta:**

```json
{
  "status": "healthy",
  "message": "Task Management API is running"
}
```

### 2. Crear Tarea

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Completar examen de arquitectura",
    "status": "pending"
  }'
```

**Respuesta:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Completar examen de arquitectura",
  "status": "pending"
}
```

### 3. Listar Tareas

```bash
curl http://localhost:8000/tasks
```

**Respuesta:**

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Completar examen de arquitectura",
    "status": "pending"
  }
]
```

### 4. Filtrar por Status

```bash
curl http://localhost:8000/tasks?status=pending
```

### 5. Obtener Tarea Específica

```bash
curl http://localhost:8000/tasks/{id}
```

### 6. Actualizar Tarea

```bash
curl -X PUT http://localhost:8000/tasks/{id} \
  -H "Content-Type: application/json" \
  -d '{
    "status": "done"
  }'
```

### 7. Eliminar Tarea

```bash
curl -X DELETE http://localhost:8000/tasks/{id}
```

## Documentación Interactiva

FastAPI genera documentación automática:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Ejecución Local (sin Docker)

### 1. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
python -m uvicorn app.adapters.http.fastapi_app:app --reload --port 8000
```

La API estará disponible en: http://localhost:8000

## Decisiones de Diseño

### ¿Por qué esta arquitectura?

1. **Separación por capas:** Facilita mantenimiento y testing
2. **Inversión de dependencias:** Permite cambiar implementaciones sin afectar la lógica central
3. **Factory para validación:** Centraliza reglas de negocio y evita inconsistencias
4. **Repository Pattern:** Abstrae persistencia, permitiendo evolución futura (ej: migrar a SQLite/PostgreSQL)
5. **DTOs en FastAPI:** Separa contratos HTTP del dominio

## Tecnologías

- **Python:** 3.11
- **Framework:** FastAPI 0.115.0
- **Servidor ASGI:** Uvicorn 0.32.0
- **Validación:** Pydantic 2.9.2
- **Containerización:** Docker

## Autor

**Nicolás Zapata Jurado** - Examen de Arquitectura de Software 2025

---

## Notas

- La persistencia es **en memoria**, por lo que los datos se pierden al reiniciar el contenedor
- Todos los endpoints incluyen manejo de errores apropiado
- La API sigue el estándar REST con códigos HTTP correctos
- El código incluye documentación y comentarios explicativos
