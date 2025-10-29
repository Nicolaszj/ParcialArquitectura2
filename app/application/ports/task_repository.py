"""
Application Ports - Repository Interface
Implements DIP (Dependency Inversion Principle):
- High-level modules (services) depend on abstractions (this interface)
- Low-level modules (persistence) implement this abstraction
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.task import Task


class TaskRepository(ABC):
    """
    Abstract repository interface for task persistence
    This allows the application layer to be independent of the persistence implementation
    """
    
    @abstractmethod
    def save(self, task: Task) -> Task:
        """
        Save a task to the repository
        
        Args:
            task: Task to save
        
        Returns:
            Task: The saved task
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[Task]:
        """
        Retrieve all tasks
        
        Returns:
            List[Task]: List of all tasks
        """
        pass
    
    @abstractmethod
    def find_by_id(self, task_id: str) -> Optional[Task]:
        """
        Find a task by its ID
        
        Args:
            task_id: The task ID to search for
        
        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update(self, task: Task) -> Optional[Task]:
        """
        Update an existing task
        
        Args:
            task: Task with updated data
        
        Returns:
            Optional[Task]: The updated task if found, None otherwise
        """
        pass
    
    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """
        Delete a task by its ID
        
        Args:
            task_id: The task ID to delete
        
        Returns:
            bool: True if deleted, False if not found
        """
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """
        Clear all tasks (useful for testing)
        """
        pass
