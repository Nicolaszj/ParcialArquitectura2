"""
Domain layer - Task Entity
Implements SRP: Single responsibility for task business logic
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import uuid


class TaskStatus(Enum):
    """Valid task statuses"""
    PENDING = "pending"
    DONE = "done"


@dataclass
class Task:
    """
    Task entity - represents a task in the domain
    Immutable after creation to maintain consistency
    """
    id: str
    title: str
    status: TaskStatus
    
    def __post_init__(self):
        """Validate task after initialization"""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        
        if not isinstance(self.status, TaskStatus):
            raise ValueError(f"Invalid status. Must be one of: {[s.value for s in TaskStatus]}")
    
    def to_dict(self) -> dict:
        """Convert task to dictionary representation"""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status.value
        }
    
    def mark_as_done(self) -> 'Task':
        """Create a new task with status done (immutability)"""
        return Task(
            id=self.id,
            title=self.title,
            status=TaskStatus.DONE
        )
    
    def update_title(self, new_title: str) -> 'Task':
        """Create a new task with updated title (immutability)"""
        return Task(
            id=self.id,
            title=new_title,
            status=self.status
        )


class TaskFactory:
    """
    Factory pattern - Encapsulates task creation logic
    Implements SRP: Single responsibility for creating valid tasks
    """
    
    @staticmethod
    def create(title: str, status: str, task_id: Optional[str] = None) -> Task:
        """
        Create a new task with validation
        
        Args:
            title: Task title (required, non-empty)
            status: Task status (must be 'pending' or 'done')
            task_id: Optional task ID (generates UUID if not provided)
        
        Returns:
            Task: A valid task instance
        
        Raises:
            ValueError: If validation fails
        """
        # Validate and convert status
        try:
            task_status = TaskStatus(status.lower())
        except ValueError:
            raise ValueError(f"Invalid status '{status}'. Must be 'pending' or 'done'")
        
        # Generate ID if not provided
        if task_id is None:
            task_id = str(uuid.uuid4())
        
        # Create and return task (validation happens in __post_init__)
        return Task(
            id=task_id,
            title=title.strip(),
            status=task_status
        )
    
    @staticmethod
    def from_dict(data: dict) -> Task:
        """
        Create a task from dictionary data
        
        Args:
            data: Dictionary with task data
        
        Returns:
            Task: A valid task instance
        """
        return TaskFactory.create(
            title=data.get("title", ""),
            status=data.get("status", "pending"),
            task_id=data.get("id")
        )
