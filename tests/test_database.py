from sqlalchemy.sql import text
from models import Task
import pytest
def test_database_connection(test_db):
    """Test database connection"""
    try:
        test_db.execute(text("SELECT 1"))
        test_db.commit()
        assert True
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}")

def test_task_crud_operations(test_db):
    """Test Create, Read, Update, Delete operations"""
    # Create
    task = Task(
        title="Test Task",
        description="Test Description",
        status="pending"
    )
    test_db.add(task)
    test_db.commit()
    test_db.refresh(task)
    
    # Read
    saved_task = test_db.query(Task).filter(Task.id == task.id).first()
    assert saved_task is not None
    assert saved_task.title == "Test Task"
    
    # Update
    saved_task.status = "completed"
    test_db.commit()
    test_db.refresh(saved_task)
    assert saved_task.status == "completed"
    
    # Delete
    test_db.delete(saved_task)
    test_db.commit()
    deleted_task = test_db.query(Task).filter(Task.id == task.id).first()
    assert deleted_task is None