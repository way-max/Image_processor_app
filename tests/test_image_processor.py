from PIL import Image
import io
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_upload_image_success():
    # Step 1: Generate a sample red image in memory
    image = Image.new("RGB", (100, 100), color="red")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    # Step 2: Send the image to the specified API endpoint
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post(
            "/image_processing/api/upload",
            files={"file": ("test.jpg", buffer, "image/jpeg")},
            params={"client_id": "345", "width": 400, "height": 400},
        )

    # Step 3: Validate the response
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "success"
    assert "image_url" in json_response  # Ensure the resized image URL is returned
