"""
Application Service - Task Service
Implements SRP: Single responsibility for coordinating task use cases
Implements OCP: Open for extension through the repository abstraction
"""
from typing import List, Optional
from app.domain.task import Task, TaskFactory
from app.application.ports.task_repository import TaskRepository


class TaskService:
    """
    Application service for task management use cases
    Coordinates between domain and persistence layers
    """
    
    def __init__(self, repository: TaskRepository):
        """
        Initialize the service with a repository
        
        Args:
            repository: Task repository implementation (DIP)
        """
        self._repository = repository
    
    def create_task(self, title: str, status: str) -> Task:
        """
        Create a new task
        
        Args:
            title: Task title
            status: Task status ('pending' or 'done')
        
        Returns:
            Task: The created task
        
        Raises:
            ValueError: If validation fails
        """
        # Use factory to create valid task
        task = TaskFactory.create(title=title, status=status)
        
        # Save to repository
        return self._repository.save(task)
    
    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks
        
        Returns:
            List[Task]: List of all tasks
        """
        return self._repository.find_all()
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by its ID
        
        Args:
            task_id: The task ID
        
        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        return self._repository.find_by_id(task_id)
    
    def update_task(self, task_id: str, title: Optional[str] = None, status: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task
        
        Args:
            task_id: The task ID to update
            title: New title (optional)
            status: New status (optional)
        
        Returns:
            Optional[Task]: The updated task if found, None otherwise
        
        Raises:
            ValueError: If validation fails
        """
        # Find existing task
        existing_task = self._repository.find_by_id(task_id)
        if not existing_task:
            return None
        
        # Prepare updated values
        new_title = title if title is not None else existing_task.title
        new_status = status if status is not None else existing_task.status.value
        
        # Create updated task using factory
        updated_task = TaskFactory.create(
            title=new_title,
            status=new_status,
            task_id=task_id
        )
        
        # Update in repository
        return self._repository.update(updated_task)
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by its ID
        
        Args:
            task_id: The task ID to delete
        
        Returns:
            bool: True if deleted, False if not found
        """
        return self._repository.delete(task_id)
    
    def get_tasks_by_status(self, status: str) -> List[Task]:
        """
        Retrieve tasks filtered by status
        Demonstrates OCP: extending functionality without modifying existing code
        
        Args:
            status: Status to filter by
        
        Returns:
            List[Task]: Filtered list of tasks
        """
        all_tasks = self._repository.find_all()
        return [task for task in all_tasks if task.status.value == status.lower()]
