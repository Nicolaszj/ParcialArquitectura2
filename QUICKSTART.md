# Quick Start Guide - Task Management API

## Inicio Rápido con Docker (En mi pc genera problemas, pero sería el ideal)

### Opción 1: Un solo comando

```bash
docker build -t task-api . && docker run -p 8000:8000 task-api
```

### Opción 2: Paso a paso

1. **Build de la imagen:**

   ```bash
   docker build -t task-api .
   ```

2. **Ejecutar el contenedor:**

   ```bash
   docker run -p 8000:8000 --name task-api task-api
   ```

3. **Verificar que funciona:**

   ```bash
   curl http://localhost:8000/health
   ```

4. **Acceder a la documentación:**
   - Abrir navegador en: http://localhost:8000/docs

## Probar la API

### Crear una tarea

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Mi primera tarea", "status": "pending"}'
```

### Ver todas las tareas

```bash
curl http://localhost:8000/tasks
```

### Actualizar una tarea (reemplaza {id} con el ID real)

```bash
curl -X PUT http://localhost:8000/tasks/{id} \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

## Documentación Interactiva

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Detener la aplicación

```bash
docker stop task-api
docker rm task-api
```

## Ejecutar sin Docker (Desarrollo local)

1. **Crear entorno virtual:**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar:**
   ```bash
   python -m uvicorn app.adapters.http.fastapi_app:app --reload
   ```

## Verificación Rápida

Endpoints para probar:

1. Health: `GET http://localhost:8000/health`
2. Crear tarea: `POST http://localhost:8000/tasks`
3. Listar tareas: `GET http://localhost:8000/tasks`
4. Ver tarea: `GET http://localhost:8000/tasks/{id}`
5. Actualizar: `PUT http://localhost:8000/tasks/{id}`
6. Eliminar: `DELETE http://localhost:8000/tasks/{id}`

## Patrones y Principios Implementados

- **Repository Pattern** - Abstracción de persistencia
- **Factory Pattern** - Creación centralizada de entidades
- **Dependency Injection** - Desacoplamiento de componentes
- **SOLID Principles** - Código mantenible y extensible
- **Clean Architecture** - Separación en capas

## Más Información

Ver `README.md` para documentación completa de arquitectura y diseño.
