from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app 
from models import Task
from schemas import TaskCreate

client = TestClient(app)

class TestTaskRouter:
    def test_create_task(self, db_session: Session):
        """Test creating a task via API"""
        task_data = {
            "title": "New API Task",
            "description": "Task created through API",
            "status": "pending"
        }
        
        response = client.post("/tasks/", json=task_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        assert "id" in data

    def test_get_all_tasks(self, db_session: Session):
        """Test getting all tasks"""
        # First create some tasks
        task_data_list = [
            {"title": "Task 1", "description": "First task", "status": "pending"},
            {"title": "Task 2", "description": "Second task", "status": "in-progress"}
        ]
        
        for task_data in task_data_list:
            client.post("/tasks/", json=task_data)
        
        response = client.get("/tasks/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        assert isinstance(data, list)

    def test_get_task_by_id(self, db_session: Session):
        """Test getting a specific task by ID"""
        task_data = {
            "title": "Get Task Test",
            "description": "Testing get by ID",
            "status": "pending"
        }
        create_response = client.post("/tasks/", json=task_data)
        task_id = create_response.json()["id"]
        
        response = client.get(f"/tasks/{task_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == task_data["title"]

    def test_update_task(self, db_session: Session):
        """Test updating a task"""
        task_data = {
            "title": "Update Task Test",
            "description": "Testing update",
            "status": "pending"
        }
        create_response = client.post("/tasks/", json=task_data)
        task_id = create_response.json()["id"]
        
        update_data = {
            "status": "in-progress",
            "description": "Updated description"
        }
        
        response = client.patch(f"/tasks/{task_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == update_data["status"]
        assert data["description"] == update_data["description"]
        assert data["title"] == task_data["title"]

    def test_delete_task(self, db_session: Session):
        """Test deleting a task"""
        # Create a task first
        task_data = {
            "title": "Delete Task Test",
            "description": "Testing delete",
            "status": "pending"
        }
        create_response = client.post("/tasks/", json=task_data)
        task_id = create_response.json()["id"]
        
        # Delete the task
        delete_response = client.delete(f"/tasks/{task_id}")
        assert delete_response.status_code == 204
        
        # Verify task is deleted
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_get_tasks_by_status(self, db_session: Session):
        """Test filtering tasks by status"""
        # Create tasks with different statuses
        tasks_data = [
            {"title": "Pending Task", "description": "Test", "status": "pending"},
            {"title": "In Progress Task", "description": "Test", "status": "in-progress"},
            {"title": "Completed Task", "description": "Test", "status": "completed"}
        ]
        
        for task_data in tasks_data:
            client.post("/tasks/", json=task_data)
        
        response = client.get("/tasks/?status=pending")
        
        assert response.status_code == 200
        data = response.json()
        assert all(task["status"] == "pending" for task in data)

    def test_invalid_status_update(self, db_session: Session):
        """Test updating task with invalid status"""
       
        task_data = {
            "title": "Invalid Status Test",
            "description": "Testing invalid status",
            "status": "pending"
        }
        create_response = client.post("/tasks/", json=task_data)
        task_id = create_response.json()["id"]
        
        update_data = {
            "status": "invalid_status"
        }
        
        response = client.patch(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == 422

    def test_create_task_invalid_data(self, db_session: Session):
        """Test creating task with invalid data"""
        invalid_task_data = {
            "title": "",  # Empty title should be invalid
            "status": "pending"
        }
        
        response = client.post("/tasks/", json=invalid_task_data)
        assert response.status_code == 422 