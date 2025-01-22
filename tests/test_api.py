import uuid
from fastapi import status

def test_create_task(test_client):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending"
    }
    response = test_client.post("/tasks/", json=task_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["status"] == task_data["status"]

def test_get_tasks(test_client):
    # Create multiple tasks
    tasks = [
        {"title": f"Task {i}", "description": f"Description {i}", "status": "pending"}
        for i in range(3)
    ]
    for task in tasks:
        test_client.post("/tasks/", json=task)
    
    response = test_client.get("/tasks/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 3
    assert data["total"] == 3
    assert data["page"] == 1

def test_update_task(test_client):
    # Create a task
    task_data = {
        "title": "Original Task",
        "description": "Original Description",
        "status": "pending"
    }
    create_response = test_client.post("/tasks/", json=task_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    task_id = create_response.json()["id"]
    
    # Update the task
    update_data = {
        "title": "Updated Task",
        "status": "in-progress"
    }
    response = test_client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["status"] == update_data["status"]

def test_delete_task(test_client):
    # Create a task
    task_data = {
        "title": "Task to Delete",
        "description": "Will be deleted",
        "status": "pending"
    }
    create_response = test_client.post("/tasks/", json=task_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = test_client.delete(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_health_check(test_client):
    response = test_client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"