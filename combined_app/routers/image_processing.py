from fastapi import APIRouter, UploadFile, BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from PIL import Image
import asyncio
import io
import os
from fastapi import APIRouter, UploadFile, HTTPException
from PIL import Image
import io
from fastapi.responses import StreamingResponse
from ddtrace import tracer

# Store progress per client (in-memory for simplicity)
upload_progress = {}

app = FastAPI(title="Image Uploader, risizer with Progress")
router = APIRouter(prefix="/api", tags=["Image Upload"])

async def resize_image(file: UploadFile, width: int, height: int):
    try:
        # Open the uploaded image
        image = Image.open(io.BytesIO(await file.read()))
        
        # Convert RGBA to RGB if necessary
        if image.mode == "RGBA":
            image = image.convert("RGB")
        
        # Resize the image
        resized_image = image.resize((width, height))
        
        # Save the resized image to a buffer
        output = io.BytesIO()
        resized_image.save(output, format="JPEG")
        output.seek(0)
        
        return StreamingResponse(output, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {e}")



@router.post("/upload")
async def upload_image(file: UploadFile, client_id: str, width: int, height: int):
    with tracer.trace("upload_image") as span:
        if not file.content_type.startswith("image/"):
            span.set_tag("error", "Invalid file type")
            raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")
        
        file_data = await file.read()
        resized_image = await process_upload(file_data, client_id, width, height)
        span.set_tag("client_id", client_id)
        return StreamingResponse(resized_image, media_type="image/jpeg")



async def process_upload(file_data: bytes, client_id: str, width: int, height: int) -> io.BytesIO:
    """
    Simulates image processing, updates progress, and resizes the image.
    """
    try:
        total_steps = 10  # Simulated steps
        for step in range(1, total_steps + 1):
            await asyncio.sleep(0.5)  # Simulate delay for processing
            upload_progress[client_id] = (step / total_steps) * 100  # Update progress

        # Save the image
        image = Image.open(io.BytesIO(file_data))
        output_dir = "uploaded_images"
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
        file_path = f"{output_dir}/{client_id}_uploaded_image.png"
        image.save(file_path)  # Save with a client-specific name

        upload_progress[client_id] = 100  # Ensure progress reaches 100%
        print(f"Image upload and processing completed for client_id: {client_id}")

        # Resize the image
        image = image.convert("RGB") if image.mode == "RGBA" else image
        resized_image = image.resize((width, height))

        # Save resized image to memory buffer
        output = io.BytesIO()
        resized_image.save(output, format="JPEG")
        output.seek(0)

        return output
    except Exception as e:
        upload_progress[client_id] = -1  # Indicate failure
        print(f"Image upload failed for client_id: {client_id}. Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")


@router.get("/progress/{client_id}")
async def progress(client_id: str):
    """
    SSE endpoint to send progress updates for a specific client.
    """
    async def event_stream():
        while True:
            progress = upload_progress.get(client_id, 0)
            yield f"data: {progress}\n\n"
            await asyncio.sleep(0.5)  # Adjust frequency as needed
            if progress == 100 or progress == -1:
                break

    return StreamingResponse(event_stream(), media_type="text/event-stream")



from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import httpx

async def video_streamer(url: str):
    # Stream video from the source URL
    async with httpx.AsyncClient() as client:
        response = await client.get(url, stream=True)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching video")
        async for chunk in response.aiter_bytes(chunk_size=1024 * 1024):
            yield chunk

@router.get("/stream-video")
async def stream_video(request: Request, url: str):
    # Check if the URL parameter is provided
    if not url:
        raise HTTPException(status_code=400, detail="Video URL is required")

    # Stream the video
    return StreamingResponse(video_streamer(url), media_type="video/mp4")
