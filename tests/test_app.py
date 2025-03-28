from fastapi.testclient import TestClient
import app  # Importing app.py directly since it's in the root folder

client = TestClient(app.app)  # Refer to the 'app' instance inside app.py

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Combined App!"}
