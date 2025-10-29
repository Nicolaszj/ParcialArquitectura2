"""
HTTP Adapter - FastAPI Application
Handles HTTP requests and responses
"""
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

from app.application.services.task_service import TaskService
from app.adapters.persistence.memory_task_repository import MemoryTaskRepository


# ===== DTOs (Data Transfer Objects) =====
# SRP: Separate HTTP concerns from domain logic

class CreateTaskRequest(BaseModel):
    """Request model for creating a task"""
    title: str = Field(..., min_length=1, description="Task title (required, non-empty)")
    status: str = Field(..., description="Task status (pending or done)")
    
    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace"""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()
    
    @field_validator('status')
    @classmethod
    def status_valid(cls, v: str) -> str:
        """Validate status is valid"""
        if v.lower() not in ['pending', 'done']:
            raise ValueError("Status must be 'pending' or 'done'")
        return v.lower()


class UpdateTaskRequest(BaseModel):
    """Request model for updating a task"""
    title: Optional[str] = Field(None, min_length=1, description="New task title (optional)")
    status: Optional[str] = Field(None, description="New task status (optional)")
    
    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty or whitespace if provided"""
        if v is not None and (not v or not v.strip()):
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip() if v else None
    
    @field_validator('status')
    @classmethod
    def status_valid(cls, v: Optional[str]) -> Optional[str]:
        """Validate status is valid if provided"""
        if v is not None and v.lower() not in ['pending', 'done']:
            raise ValueError("Status must be 'pending' or 'done'")
        return v.lower() if v else None


class TaskResponse(BaseModel):
    """Response model for a task"""
    id: str
    title: str
    status: str


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    message: str


# ===== FastAPI Application =====

# Create application instance
app = FastAPI(
    title="Task Management API",
    description="API REST para gestión de tareas - Examen Arquitectura de Software",
    version="1.0.0"
)

# Initialize dependencies (Dependency Injection)
# In a production app, this would use FastAPI's dependency injection
task_repository = MemoryTaskRepository()
task_service = TaskService(task_repository)


# ===== Endpoints =====

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    Verifies the service is running
    """
    return HealthResponse(
        status="healthy",
        message="Task Management API is running"
    )


@app.get("/tasks", response_model=List[TaskResponse], tags=["Tasks"])
async def get_tasks(status: Optional[str] = None):
    """
    Get all tasks or filter by status
    
    Query Parameters:
    - status: Optional filter by status (pending or done)
    
    Returns:
    - List of tasks
    """
    try:
        if status:
            # Validate status parameter
            if status.lower() not in ['pending', 'done']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Status must be 'pending' or 'done'"
                )
            tasks = task_service.get_tasks_by_status(status)
        else:
            tasks = task_service.get_all_tasks()
        
        return [TaskResponse(**task.to_dict()) for task in tasks]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks: {str(e)}"
        )


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(request: CreateTaskRequest):
    """
    Create a new task
    
    Request Body:
    - title: Task title (required, non-empty)
    - status: Task status (pending or done)
    
    Returns:
    - Created task with generated ID
    
    Errors:
    - 400: Invalid input data
    """
    try:
        task = task_service.create_task(
            title=request.title,
            status=request.status
        )
        return TaskResponse(**task.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def get_task(task_id: str):
    """
    Get a specific task by ID
    
    Path Parameters:
    - task_id: Task identifier
    
    Returns:
    - Task details
    
    Errors:
    - 404: Task not found
    """
    task = task_service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id '{task_id}' not found"
        )
    return TaskResponse(**task.to_dict())


@app.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def update_task(task_id: str, request: UpdateTaskRequest):
    """
    Update an existing task
    
    Path Parameters:
    - task_id: Task identifier
    
    Request Body:
    - title: New task title (optional)
    - status: New task status (optional)
    
    Returns:
    - Updated task
    
    Errors:
    - 400: Invalid input data
    - 404: Task not found
    """
    try:
        task = task_service.update_task(
            task_id=task_id,
            title=request.title,
            status=request.status
        )
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id '{task_id}' not found"
            )
        return TaskResponse(**task.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_task(task_id: str):
    """
    Delete a task by ID
    
    Path Parameters:
    - task_id: Task identifier
    
    Returns:
    - 204 No Content on success
    
    Errors:
    - 404: Task not found
    """
    deleted = task_service.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id '{task_id}' not found"
        )
    return None


# ===== Root endpoint =====

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Task Management API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "tasks": "/tasks",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }
