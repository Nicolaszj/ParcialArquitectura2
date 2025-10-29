"""
Persistence Adapter - In-Memory Task Repository
Implements the TaskRepository interface (DIP)
"""
from typing import List, Optional, Dict
from app.application.ports.task_repository import TaskRepository
from app.domain.task import Task


class MemoryTaskRepository(TaskRepository):
    """
    In-memory implementation of TaskRepository
    Uses a dictionary to store tasks by ID
    Thread-safe for single-threaded applications
    """
    
    def __init__(self):
        """Initialize the repository with an empty storage"""
        self._tasks: Dict[str, Task] = {}
    
    def save(self, task: Task) -> Task:
        """
        Save a task to memory
        
        Args:
            task: Task to save
        
        Returns:
            Task: The saved task
        """
        self._tasks[task.id] = task
        return task
    
    def find_all(self) -> List[Task]:
        """
        Retrieve all tasks
        
        Returns:
            List[Task]: List of all tasks
        """
        return list(self._tasks.values())
    
    def find_by_id(self, task_id: str) -> Optional[Task]:
        """
        Find a task by its ID
        
        Args:
            task_id: The task ID to search for
        
        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        return self._tasks.get(task_id)
    
    def update(self, task: Task) -> Optional[Task]:
        """
        Update an existing task
        
        Args:
            task: Task with updated data
        
        Returns:
            Optional[Task]: The updated task if found, None otherwise
        """
        if task.id not in self._tasks:
            return None
        
        self._tasks[task.id] = task
        return task
    
    def delete(self, task_id: str) -> bool:
        """
        Delete a task by its ID
        
        Args:
            task_id: The task ID to delete
        
        Returns:
            bool: True if deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def clear(self) -> None:
        """
        Clear all tasks (useful for testing)
        """
        self._tasks.clear()
