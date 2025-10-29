"""
Unit Tests for Task Management API
Demonstrates testing with dependency injection and mocking
"""
import pytest
from app.domain.task import Task, TaskFactory, TaskStatus
from app.application.services.task_service import TaskService
from app.adapters.persistence.memory_task_repository import MemoryTaskRepository


# ===== Domain Tests =====

class TestTaskFactory:
    """Test TaskFactory creation and validation"""
    
    def test_create_valid_task(self):
        """Test creating a valid task"""
        task = TaskFactory.create(title="Test Task", status="pending")
        
        assert task.title == "Test Task"
        assert task.status == TaskStatus.PENDING
        assert task.id is not None
    
    def test_create_task_with_done_status(self):
        """Test creating a task with done status"""
        task = TaskFactory.create(title="Completed Task", status="done")
        
        assert task.status == TaskStatus.DONE
    
    def test_create_task_invalid_status(self):
        """Test that invalid status raises ValueError"""
        with pytest.raises(ValueError, match="Invalid status"):
            TaskFactory.create(title="Test", status="invalid")
    
    def test_create_task_empty_title(self):
        """Test that empty title raises ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            TaskFactory.create(title="", status="pending")
    
    def test_create_task_whitespace_title(self):
        """Test that whitespace-only title raises ValueError"""
        with pytest.raises(ValueError, match="cannot be empty"):
            TaskFactory.create(title="   ", status="pending")
    
    def test_from_dict(self):
        """Test creating task from dictionary"""
        data = {"title": "From Dict", "status": "pending"}
        task = TaskFactory.from_dict(data)
        
        assert task.title == "From Dict"
        assert task.status == TaskStatus.PENDING


class TestTask:
    """Test Task entity behavior"""
    
    def test_task_to_dict(self):
        """Test task serialization to dictionary"""
        task = TaskFactory.create(title="Test", status="pending")
        task_dict = task.to_dict()
        
        assert task_dict["title"] == "Test"
        assert task_dict["status"] == "pending"
        assert "id" in task_dict
    
    def test_mark_as_done_immutability(self):
        """Test that mark_as_done creates a new task (immutability)"""
        task = TaskFactory.create(title="Test", status="pending")
        done_task = task.mark_as_done()
        
        # Original task unchanged
        assert task.status == TaskStatus.PENDING
        # New task is done
        assert done_task.status == TaskStatus.DONE
        # Same ID
        assert task.id == done_task.id


# ===== Repository Tests =====

class TestMemoryTaskRepository:
    """Test in-memory repository implementation"""
    
    def setup_method(self):
        """Setup fresh repository for each test"""
        self.repo = MemoryTaskRepository()
    
    def test_save_and_find_by_id(self):
        """Test saving and retrieving a task"""
        task = TaskFactory.create(title="Test", status="pending")
        saved_task = self.repo.save(task)
        
        found_task = self.repo.find_by_id(saved_task.id)
        assert found_task is not None
        assert found_task.id == saved_task.id
        assert found_task.title == "Test"
    
    def test_find_all(self):
        """Test retrieving all tasks"""
        task1 = TaskFactory.create(title="Task 1", status="pending")
        task2 = TaskFactory.create(title="Task 2", status="done")
        
        self.repo.save(task1)
        self.repo.save(task2)
        
        all_tasks = self.repo.find_all()
        assert len(all_tasks) == 2
    
    def test_update_existing_task(self):
        """Test updating an existing task"""
        task = TaskFactory.create(title="Original", status="pending")
        self.repo.save(task)
        
        updated_task = TaskFactory.create(
            title="Updated", 
            status="done", 
            task_id=task.id
        )
        result = self.repo.update(updated_task)
        
        assert result is not None
        assert result.title == "Updated"
        assert result.status == TaskStatus.DONE
    
    def test_update_nonexistent_task(self):
        """Test updating a task that doesn't exist"""
        task = TaskFactory.create(title="Test", status="pending")
        result = self.repo.update(task)
        
        assert result is None
    
    def test_delete_existing_task(self):
        """Test deleting an existing task"""
        task = TaskFactory.create(title="To Delete", status="pending")
        self.repo.save(task)
        
        deleted = self.repo.delete(task.id)
        assert deleted is True
        
        found = self.repo.find_by_id(task.id)
        assert found is None
    
    def test_delete_nonexistent_task(self):
        """Test deleting a task that doesn't exist"""
        deleted = self.repo.delete("nonexistent-id")
        assert deleted is False


# ===== Service Tests =====

class TestTaskService:
    """Test TaskService use cases"""
    
    def setup_method(self):
        """Setup service with fresh repository for each test"""
        self.repo = MemoryTaskRepository()
        self.service = TaskService(self.repo)
    
    def test_create_task(self):
        """Test creating a task through the service"""
        task = self.service.create_task(title="Service Task", status="pending")
        
        assert task.title == "Service Task"
        assert task.status == TaskStatus.PENDING
        
        # Verify it's in repository
        found = self.repo.find_by_id(task.id)
        assert found is not None
    
    def test_get_all_tasks(self):
        """Test retrieving all tasks"""
        self.service.create_task("Task 1", "pending")
        self.service.create_task("Task 2", "done")
        
        tasks = self.service.get_all_tasks()
        assert len(tasks) == 2
    
    def test_get_task_by_id(self):
        """Test retrieving a specific task"""
        created = self.service.create_task("Test", "pending")
        
        found = self.service.get_task_by_id(created.id)
        assert found is not None
        assert found.id == created.id
    
    def test_update_task_title(self):
        """Test updating task title"""
        task = self.service.create_task("Original", "pending")
        
        updated = self.service.update_task(task.id, title="Updated")
        assert updated is not None
        assert updated.title == "Updated"
        assert updated.status == TaskStatus.PENDING
    
    def test_update_task_status(self):
        """Test updating task status"""
        task = self.service.create_task("Test", "pending")
        
        updated = self.service.update_task(task.id, status="done")
        assert updated is not None
        assert updated.status == TaskStatus.DONE
    
    def test_update_nonexistent_task(self):
        """Test updating a task that doesn't exist"""
        updated = self.service.update_task("nonexistent", title="Test")
        assert updated is None
    
    def test_delete_task(self):
        """Test deleting a task"""
        task = self.service.create_task("To Delete", "pending")
        
        deleted = self.service.delete_task(task.id)
        assert deleted is True
        
        found = self.service.get_task_by_id(task.id)
        assert found is None
    
    def test_get_tasks_by_status(self):
        """Test filtering tasks by status"""
        self.service.create_task("Task 1", "pending")
        self.service.create_task("Task 2", "pending")
        self.service.create_task("Task 3", "done")
        
        pending_tasks = self.service.get_tasks_by_status("pending")
        done_tasks = self.service.get_tasks_by_status("done")
        
        assert len(pending_tasks) == 2
        assert len(done_tasks) == 1


# Run with: pytest tests/test_task_api.py -v
